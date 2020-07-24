import utils
import constants as c
from graph import Node
from gensim.models import Word2Vec

model = Word2Vec.load(str(c.CURRENT.joinpath('word2vec.pickle')))

graph = utils.load_graph('labeled-import.pickle')

nodes_of_type = graph.get_nodes()
artists = nodes_of_type['Artist'].items()

for _token, node in artists:
    try:
        # Top ten is sort of arbitrary. Is there a way to select by similarity?
        node.similar = model.wv.most_similar(node.id, topn=10)
    except KeyError as err:
        print(f'Error selecting similar artist: {err}')

utils.save_graph(graph, 'similar-labeled-import.pickle')