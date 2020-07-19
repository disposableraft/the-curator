import time
import utils
import constants as c
from category import Category
from wikidata import Wikidata

class FetchLabels:
    def __init__(self, nodes, graph):
        self.nodes = nodes
        self.graph = graph
        self.total_nodes = len(nodes)
        self.progress = 0
        self.edges_added = 0
        self.categories_added = set()
        self.unupdated = set()
        self.artists_updated = 0
        self.unlabeled = set()

    def get_report(self):
        return {
            'total_nodes' : self.total_nodes,
            'progress': self.progress,
            'edges_added': self.edges_added,
            'categories_added': self.categories_added,
            'unupdated': self.unupdated,
            'artists_updated': self.artists_updated,
            'unlabled': self.unupdated,
        }

    def save_tmp_file(self, obj, name):
        utils.write(c.PROJECT_TMP.joinpath(name), obj)

    def run(self):
        for node in self.nodes:
            time.sleep(0.5)
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



