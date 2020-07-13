import utils
import constants as c
import matplotlib.pyplot as plt

graph_pickle = c.PROJECT_DATA_PICKLES.joinpath('2020712-moma-exhibitions.pickle')
graph = utils.load_graph(graph_pickle)

nodes_of_type = graph.get_nodes()

X0 = [n.degrees for n in nodes_of_type['Artist'].values() if n.degrees > 2]
X1 = [n.degrees for n in nodes_of_type['Exhibition'].values()]

plt.title(f'Node Degrees')
plt.boxplot([X0, X1], labels=[f'Artists > 2 ({len(X0)})', f'Exhibitions ({len(X1)})'])
plt.show()

