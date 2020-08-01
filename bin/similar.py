import os
import utils
from graph import Node
from gensim.models import Word2Vec

def run(config):
    model_path = os.path.join(config['version_dir'], 'word2vec.pickle')
    model = Word2Vec.load(model_path)
    graph = utils.load_graph('labeled-import.pickle', config)
    artists = graph.get_nodes()['Artist'].values()

    for node in artists:
        try:
            node.similar = model.wv.most_similar(node.id, topn=config['topn'])
        except KeyError as err:
            print(f'Error selecting similar artist: {err}')

    utils.save_graph(graph, 'similar-labeled-import.pickle', config)