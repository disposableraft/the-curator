import utils
import constants as c
from graph import Node
from gensim.models import Word2Vec

model = Word2Vec.load(str(c.MODELS.joinpath('20200721-skipgram.word2vec')))

fn = c.VERSIONS.joinpath('2020-7-21-moma-exhibitions-categories.pickle')
graph = utils.load_graph(fn)

nodes_of_type = graph.get_nodes()
artists = nodes_of_type['Artist'].items()

for _token, node in artists:
    try:
        # Top ten is sort of arbitrary. Is there a way to select by similarity?
        node.similar = model.wv.most_similar(node.id, topn=10)
    except KeyError as err:
        print(f'Error selecting similar artist: {err}')

utils.save_graph(graph, name='moma-exhibitions-categories-word2vec-sg')