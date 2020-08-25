import os
import time
import json
import utils
from category import Category
from wikidata_source import Wikidata

class FetchLabels:
    def __init__(self, nodes, graph, config):
        """
        Fetch labels from Wikidata

        `nodes` is expected to include a `wikidataID`.

        `graph` is expected to contain the nodes which are being
            updated with labels.
        """
        self.nodes = nodes
        self.graph = graph
        self.config = config
        self.total_nodes = len(nodes)
        self.progress = 0
        self.edges_added = 0
        self.categories_added = set()
        self.unupdated = set()
        self.artists_updated = 0
        self.unlabeled = set()

    def get_report(self):
        return {
            'total_nodes': self.total_nodes,
            'progress': self.progress,
            'edges_added': self.edges_added,
            'categories_added': list(self.categories_added),
            'unupdated': list(self.unupdated),
            'artists_updated': self.artists_updated,
            'unlabled': list(self.unupdated),
        }

    def save_tmp_file(self, obj, name):
        path = os.path.join(self.config['version_dir'], name)
        utils.write(path, obj)

    def run(self):
        for node in self.nodes:
            time.sleep(1)
            self.progress += 1

            if self.progress % 50 == 0:
                print(f'Progress: {self.progress} / {self.total_nodes}. Updated: {self.artists_updated}. Unupdated: {len(self.unupdated)}. Unlabeled: {len(self.unlabeled)}')
                self.save_tmp_file(self.graph, 'tmp-graph.pickle')
                self.save_tmp_file(self.get_report(), 'tmp-report.pickle')

            if str(node.wikidataID) == 'nan':
                continue

            wd = Wikidata(node.wikidataID)
            labels = wd.fetch()

            if labels == False:
                self.unupdated.add(node.id)
            elif len(labels) == 0:
                self.unlabeled.add(node.id)
            else:
                for label in labels:
                    node.categories.add(label)
                    if label not in self.graph.nodes:
                        self.graph.add(Category(label))
                        self.categories_added.add(label)
                    self.graph.add_edge(label, node)
                    self.edges_added += 1
                self.artists_updated += 1

        return self.graph, self.get_report()

class LabelArtists:
    def __init__(self, pipeline):
        self.pipeline = pipeline

    def proceed(self):
        config = self.pipeline.version.config
        report_path = os.path.join(config['version_dir'], 'fetch-report.json')

        graph = utils.load_graph('import.pickle', config)

        nodes = [value for value in graph
                        if value.type == 'Artist'
                        and value.wikidataID != None
                        and value.degrees > 2]

        # For rerunning the process without restarting, use
        # the nodes from the report, using `report_path` above.
        # nodes = [graph[tk] for tk in report['unupdated']]

        fetch = FetchLabels(nodes, graph, config)
        (new_graph, report) = fetch.run()

        utils.save_graph(new_graph, 'labeled-import.pickle', config)

        with open(report_path, 'wb') as f:
            f.write(json.dumps(report))
        self.pipeline.update() 
