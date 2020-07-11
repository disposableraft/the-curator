import constants
from pygraphviz import AGraph 
import utils

file = constants.PROJECT_DATA_PICKLES.joinpath('2020710-moma-exhibitions.pickle')
data = utils.load_graph(file)

G4 = AGraph()    

for node in data:
    if len(node.edges) > 1 and len(node.edges) < 6:
        G4.add_node(node.id, shape='point', color='black')
        for m in node.edges:
            if m:
                G4.add_node(m, shape='point', color='red')
                G4.add_edge(node.id, m, color="#CCCCCC")

G4.layout()
image = constants.PROJECT_DATA_IMAGES.joinpath('raw-exhibition-data.png')
G4.draw(str(image))