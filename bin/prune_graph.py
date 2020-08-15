import utils

class Prune1:
    def __init__(self, pipeline):
        self.pipeline = pipeline

    def proceed(self):
        config = self.pipeline.version.config
        graph = utils.load_graph('labeled-import.pickle', config)

        nodes_by_type = graph.get_nodes()
        exhibitions = nodes_by_type['Exhibition'].values()
        artists = nodes_by_type['Artist'].values()

        # Artists with fewer than 3 exhibitions
        graph.prune([a for a in artists if a.degrees < 3])
        # Exhibitions with fewer than 2 artists
        graph.prune([e for e in exhibitions if e.degrees < 2])
        
        utils.save_graph(graph, 'labeled-import-prune', config)
        
        self.pipeline.update() 

class Prune2:
    def __init__(self, pipeline):
        self.pipeline = pipeline

    def proceed(self):
        config = self.pipeline.version.config
        graph = utils.load_graph('labeled-import.pickle', config)
        artists = graph.get_nodes()['Artist'].values()
        # Artists without a category
        graph.prune([a for a in artists if len(a.categories) < 1])
        utils.save_graph(graph, 'labeled-import-prune', config)
        self.pipeline.update() 

