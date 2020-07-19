import utils
import matplotlib.pyplot as plt

graph = utils.load_graph()

nodes_of_type = graph.get_nodes()

X0 = [n.degrees for n in nodes_of_type['Artist'].values() if n.degrees > 2]
X1 = [n.degrees for n in nodes_of_type['Exhibition'].values()]

plt.title(f'Node Degrees')
plt.boxplot([X0, X1], labels=[f'Artists > 2 ({len(X0)})', f'Exhibitions ({len(X1)})'])
plt.show()

