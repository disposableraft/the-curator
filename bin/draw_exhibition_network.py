import constants
from pygraphviz import AGraph
import utils

file = constants.PROJECT_DATA_PICKLES.joinpath('2020712-moma-exhibitions-categories-word2vec.pickle')
data = utils.load_graph(file)
G4 = AGraph()

nodes_of_type = data.get_nodes()

for _token, node in nodes_of_type['Exhibition'].items():
    # if node.degrees > 0:
    G4.add_node(node.id, shape='point', color='black')
    for m in node.edges:
        if data[m].degrees == 2:
            G4.add_node(m, shape='point', color='red')
            G4.add_edge(node.id, m, color="#CCCCCC", alpha=0.1)
    if len(G4.edges(node.id)) < 1:
        G4.remove_node(node.id)

G4.layout()
image = constants.PROJECT_DATA_IMAGES.joinpath('raw-exhibition-data.png')
G4.draw(str(image))