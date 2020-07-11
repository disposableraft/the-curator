import constants
from pygraphviz import AGraph 
import utils

file = constants.PROJECT_DATA_PICKLES.joinpath('202078-moma-exhibitions.pickle')
data = utils.load_graph(file)

G4 = AGraph()    

for key, node in data.nodes.items():
    if len(node.edges) > 1 and len(node.edges) < 6:
        G4.add_node(key, shape='point', color='black')
        for m in node.edges:
            if m:
                G4.add_node(m, shape='point', color='red')
                G4.add_edge(key, m, color="#CCCCCC")

G4.layout()
image = constants.PROJECT_DATA_IMAGES.joinpath('raw-exhibition-data.png')
G4.draw(image)