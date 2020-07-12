import utils
import constants as c
import matplotlib.pyplot as plt

graph_pickle = c.PROJECT_DATA_PICKLES.joinpath('2020712-moma-word2vec.pickle')

data = utils.load_graph(graph_pickle)

artists = data.get_nodes()['Artist']

Y = []
X = []
for n in artists.values():
    if n.degrees > 5 and n.degrees < 50:
        Y.append(n.cosim_mean())
        X.append(n.degrees)

r_value = utils.pearson_r(X, Y)

print(r_value)

plt.title(f'Correlation of mean cosine similarity and degree. R={round(r_value,3)}')

plt.scatter(X, Y, alpha=0.3)

# plt.hist(Y)
plt.show()

