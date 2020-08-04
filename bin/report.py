import os
import json
import utils
from scipy import stats
import matplotlib.pyplot as plt
from draw_category_similars import DrawCategorySimilars

class Report:
    def __init__(self, config):
        self.config = config
        self.report_dir = os.path.join(self.config['version_dir'], 'reports')
        self.version = self.config['version']
        self.graph = utils.load_graph('similar-labeled-import.pickle', config)
        types = self.graph.get_nodes()
        self.categories = types['Category'].values()
        self.exhibitions = types['Exhibition']
        self.artists = types['Artist'].values()
        self.report = {
            'graph': {},
            'version': self.version,
            'model': {},
            'results': {
                'linregress': {},
                'error_rates' : {},
            }
        }

    def mean(self, s):
        return sum([x for x in s]) / len(s)

    def variance(self, s):
        difference_sq = [(x - self.mean(s))**2 for x in s]
        return sum(difference_sq) / len(s)

    def get_category_error_rates(self):
        error_rates = {
            'all': {
                'scores': []
            },
        }
        for category in self.categories:
            if category.degrees > 1:
                cat_score = self.score_category(category)
                if cat_score == None:
                    continue
                error_rates[category.id] = cat_score
                error_rates['all']['scores'] += cat_score['scores']
        error_rates['all']['mean'] = self.mean(error_rates['all']['scores'])
        error_rates['all']['variance'] = self.variance(error_rates['all']['scores'])
        return error_rates

    def score_category(self, cat):
        all_labeled_nodes = utils.get_labeled_nodes(self.categories)
        # Score is defined as `misses / (hits + misses)`
        scores = []
        for n in cat.edges:
            A = self.graph[n]
            hits = []
            misses = []
            for token, score in A.similar:
                # Hits: token is in cat.edges
                if token in cat.edges:
                    hits.append(score)
                # Misses: token is labeled but not as this category
                if token in all_labeled_nodes and token not in cat.edges:
                    misses.append(score)
            if len(misses) + len(hits) == 0:
                continue
            else:
                score = sum(misses) / (sum(hits) + sum(misses))
                scores.append(score)

        if len(scores) == 0:
            return None

        return {
            # 'cat': cat.id,
            'degrees': cat.degrees,
            'mean': self.mean(scores),
            'variance': self.variance(scores),
            'scores': scores,
        }

    def run(self):
        # Yolo
        try:
            os.mkdir(self.report_dir)
            os.mkdir(f'{self.report_dir}/images')
        except FileExistsError as err:
            print(f'Warning: {err}')

        # Labeled and Unlabeled
        labeled_artists = utils.get_labeled_nodes(self.categories)
        artists_degree_gt_1 = set([a.id for a in self.artists if a.degrees > 2])
        unlabeled_artists = artists_degree_gt_1 ^ labeled_artists

        # Graph name
        self.report['graph']['edges'] = self.graph.count_edges()
        self.report['graph']['nodes'] = self.graph.count_nodes()
        self.report['graph']['density'] = self.graph.density()
        self.report['graph']['exhibitions']  = len(self.exhibitions)
        self.report['graph']['categories']  = len(self.categories)
        self.report['graph']['artists']  = len(self.artists)
        self.report['graph']['unlabeled_artists']  = len(unlabeled_artists)
        self.report['graph']['labeled_artists']  = len(labeled_artists)

        # Open model's report
        # TODO the model provides some useful stats on vocab, etc
        training_notes_path = os.path.join(self.config['version_dir'], 'training-notes.json')
        with open(training_notes_path, 'r') as f:
            model_notes = json.loads(f.read())

        self.report['model']['sg'] = model_notes['sg']
        self.report['model']['workers'] = model_notes['workers']
        self.report['model']['size'] = model_notes['size']
        # self.report['model']['min_count'] = model_notes['min_count']
        self.report['model']['epochs'] = model_notes['epochs']
        self.report['model']['topn'] = self.config['topn']

        # Error rates per category
        self.report['results']['error_rates'] = self.get_category_error_rates()

        # Error Rate Histogram
        plt.title('Error rate distribution')
        plt.hist(self.report['results']['error_rates']['all']['scores'], cumulative=False)
        plt.savefig(os.path.join(self.report_dir, 'images/error-distribution.png'))
        plt.close()

        # Error rate distribution
        corr_scatter = os.path.join(self.report_dir, 'images/scatter-err-per-cat.png')

        filtered_cat_scores = [v for k, v in self.report['results']['error_rates'].items() if v['mean'] < 1 and k != 'all']
        corr_X = [s['mean'] for s in filtered_cat_scores]
        corr_Y = [len(s['scores']) for s in filtered_cat_scores]

        plt.title('Mean Error per Category')
        plt.scatter(corr_X, corr_Y, alpha=0.2)
        plt.savefig(corr_scatter)
        plt.close()

        lg = stats.linregress(corr_X, corr_Y)
        self.report['results']['linregress'] = {k:v for k,v in zip(lg._fields, lg)}

        # Category Graphs
        for k, v in self.report['results']['error_rates'].items():
            if len(v['scores']) > 9 and k != 'all':
                image_name = f"images/{k.replace(' ', '')}.png"
                image_path = os.path.join(self.report_dir, image_name)
                grapher = DrawCategorySimilars(self.graph, k, image_path)
                grapher.run()

        # And, finally!
        with open(os.path.join(self.report_dir, 'report.json'), 'w') as f:
            f.write(json.dumps(self.report))

def run(config):
    report = Report(config)
    report.run()