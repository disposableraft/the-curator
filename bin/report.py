import os
import pickle
import json
import utils
from scipy import stats
import matplotlib.pyplot as plt
import constants as c
from draw_category_similars import DrawCategorySimilars

"""
CONFIGS
"""
report_dir = c.DATA.joinpath('report-02')
title = 'Report 01 for 20200721-skipgram.word2vec'
model_name = '20200721-skipgram.word2vec'
dataset = 'train-01'
"""
/CONFIGS
"""

# Yolo
try:
    os.mkdir(report_dir)
except FileExistsError:
    print(f'Directory exists: {report_dir}')

def get_labeled_nodes(cats):
    labeled = set()
    for c in cats:
        for m in c.edges:
            labeled.add(m)
    return labeled

def mean(s):
    return sum([x for x in s]) / len(s)

def diff_sq(s):
    return [(x - mean(s))**2 for x in s]

def variance(s):
    return sum(diff_sq(s)) / len(s)

def score_category(graph, cat, all_labeled_nodes):
    # Score is misses / (hits + misses)
    scores = []
    for m in cat.edges:
        A = graph[m]
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
            # Return 1 for a full on error
            # score = 1
            continue
        else:
            score = len(misses) / (len(hits) + len(misses))
            scores.append(score)

    if len(scores) == 0:
        return None

    return {
        'cat': cat.id,
        'degrees': cat.degrees,
        'mean': mean(scores),
        'variance': variance(scores),
        'scores': scores,
        'total_hits_misses': len(hits) + len(misses)
    }

def report_error_rates(lines, report_dict):
    errs = report_dict['results']['error_rates']
    for line in lines:
        cat = line['cat']
        errs[cat] = {}
        errs[cat]['mean'] = line['mean']
        errs[cat]['variance'] = line['variance']
        errs[cat]['scores'] = line['scores']
    return report_dict

"""
The report dict is the star of the show.
"""
report = {
    'title': title,
    'graph': {},
    'model': {
        'name': model_name,
        'dataset': dataset
    },
    'results': {
        'linregress': {},
        'error_rates' : {
        },
    }
}

# Assumes current graph file
graph = utils.load_graph()
types = graph.get_nodes()
categories = types['Category'].values()
exhibitions = types['Exhibition']
artists = types['Artist'].values()

# Labeled and Unlabeled
# TODO this is same as `get_labeled_nodes()`
labeled_artists = get_labeled_nodes(categories)
artists_degree_gt_1 = set([a.id for a in artists if a.degrees > 2])
unlabeled_artists = artists_degree_gt_1 ^ labeled_artists

# Graph name
graph_path = os.readlink(c.CURRENT)
report['graph']['name'] = graph_path.split('/')[-1]
report['graph']['vertices'] = graph.count_edges()
report['graph']['nodes'] = graph.count_nodes()
report['graph']['density'] = graph.density()
report['graph']['exhibitions']  = len(exhibitions)
report['graph']['categories']  = len(categories)
report['graph']['artists']  = len(artists)
report['graph']['unlabeled_artists']  = len(unlabeled_artists)
report['graph']['labeled_artists']  = len(labeled_artists)

# Open model's report
# TODO the model provides some useful stats on vocab, etc
# TODO use json for gawds sakes!
with open(c.MODELS.joinpath(f'{model_name}-notes'), 'rb') as f:
    model_notes = pickle.load(f)

report['model']['sg'] = model_notes['sg']
report['model']['workers'] = model_notes['workers']
report['model']['size'] = model_notes['size']
report['model']['min_count'] = model_notes['min_count']
report['model']['epochs'] = model_notes['epochs']

# Error rates per category
labeled_nodes = get_labeled_nodes(categories)
err_by_category = []
for category in categories:
    if category.degrees > 1:
        score = score_category(graph, category, labeled_nodes)
        if score:
            err_by_category.append(score)
report = report_error_rates(err_by_category, report)

# Error rates total
all_scores = []
for category in categories:
    if category.degrees > 1:
        cat_score = score_category(graph, category, labeled_nodes)
        if cat_score:
            for x in cat_score['scores']:
                all_scores.append(x)
err_total = {
    'cat': 'all',
    'mean': mean(all_scores),
    'variance': variance(all_scores),
    'scores': all_scores
}
report = report_error_rates([err_total], report)

# Error Rate Histogram
plt.title('Error rate distribution')
plt.hist(all_scores, cumulative=False)
plt.savefig(report_dir.joinpath('./error-distribution.png'))
plt.close()

# Error rate distribution
corr_scatter_name = 'scatter-err-per-cat.png'
corr_scatter = report_dir.joinpath(corr_scatter_name)

filtered_cat_scores = [x for x in err_by_category if x['mean'] < 1]
corr_X = [s['mean'] for s in filtered_cat_scores]
corr_Y = [len(s['scores']) for s in filtered_cat_scores]

plt.title('Mean Error per Category')
plt.scatter(corr_X, corr_Y, alpha=0.2)
plt.savefig(corr_scatter)
plt.close()

lg = stats.linregress(corr_X, corr_Y)
report['results']['linregress'] = {k:v for k,v in zip(lg._fields, lg)}

# Category Graphs
category_graphs = str()
for x in err_by_category:
    if len(x['scores']) > 9:
        image_name = f"{x['cat'].replace(' ', '')}.png"
        image_path = report_dir.joinpath(image_name)
        grapher = DrawCategorySimilars(graph, x['cat'], image_path)
        grapher.run()
        category_graphs += (f'![](./{image_name})\n\n')


# And, finally!
with open(report_dir.joinpath('report.json'), 'w') as f:
    f.write(json.dumps(report))