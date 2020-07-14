import constants
from pygraphviz import AGraph
import utils

file = constants.PROJECT_DATA_PICKLES.joinpath('2020713-moma-exhibitions-categories-word2vec.pickle')
graph = utils.load_graph(file)

G4 = AGraph(directed=True, concentrate=True)
G4.graph_attr['bgcolor']='aliceblue'
G4.graph_attr['overlap']='scale'
G4.graph_attr['K']=0.75

def get_category(category):
    for n in graph.get_nodes()['Category'].values():
        if n.title == category:
            return n

category = get_category('Dada')

G4.add_node(
    category.id,
    shape='circle',
    color='#FFFFFF',
    label="Dada",
    fontname="courier",
    fontsize=12,
    style='filled',
    bgcolor="#FFFFFF",
    )

def get_connected(N :list, data :dict):
    """
    Return a set of connected artists for all nodes in N.

    N, a list of nodes.
    data, the class Graph
    """
    connected = set()
    for n in N:
        for token, _score in n.similar:
            if data[token] in N:
                connected.add(n)
                connected.add(data[token])
    return connected

artist_nodes = set([graph[m] for m in category.edges])
connected = get_connected(artist_nodes, graph)

for ca in connected:
    G4.add_node(
        ca.id,
        shape='circle',
        fixedsize=True,
        style='filled',
        bgcolor='#FFFFFF',
        width=0.25,
        color='#f08080',
        xlabel=ca.id,
        label='',
        fontsize=8,
        fontname="courier",
        )

for ca in connected:
    for token, score in ca.similar:
        if graph[token] in connected:
            G4.add_edge(
                ca.id,
                graph[token].id,
                color="pink",
                arrowsize=0.5,
                )

G4.layout(prog='fdp')
image = constants.PROJECT_DATA_IMAGES.joinpath('categories-similar.png')
G4.draw(str(image))