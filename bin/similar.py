import utils
import constants as c
from graph import Node
from gensim.models import Word2Vec

class Similar(Node):
    def __init__(self, id):
        pass

# Load the model
# Load the graph
# For each artist node in the graph
#   Query word2vec model for similar artists
#   Record the similar artist token and cosim in a dictionary of the artist node in the graph
# Save the updated graph

model = Word2Vec.load(str(c.WORD2VEC))
graph = utils.load_graph()

nodes_of_type = graph.get_nodes()
artists = nodes_of_type['Artist'].items()

for _token, node in artists:
    try:
        # Top ten is sort of arbitrary. Is there a way to select by similarity?
        node.similar = model.wv.most_similar(node.id, topn=10)
    except KeyError as err:
        print(f'Error selecting similar artist: {err}')

utils.save_graph(graph, name='moma-exhibitions-categories-word2vec')