import os
import utils
from itertools import combinations

class ExportCorpus:
    def __init__(self, pipeline):
        self.pipeline = pipeline
    
    def proceed(self):
        config = self.pipeline.version.config
        combinations_r = config['combinations_r']
        train_dir = config['train_dir']
        # This can change :(
        graph = utils.load_graph('labeled-import-prune.pickle', config)
        exhibitions = graph.get_nodes()['Exhibition'].values()

        print(f'{"Index":<6s}{"Edges":<7s}{"Title"} {"ID"}')

        for index, e in enumerate(exhibitions):
            print(f'{index:<6}{len(e.edges):<7} {e.title} {e.id}')

            if e.degrees >= combinations_r:
                lines = combinations(list(e.edges), combinations_r)
            else:
                lines = [e.edges]

            file = os.path.join(train_dir, f'{e.id}.txt')
            with open(file, 'w') as f:
                for line in lines:
                    f.write(" ".join(line))
                    f.write("\n")

        self.pipeline.update()

