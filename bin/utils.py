import pickle
import matplotlib.pyplot as plt

def load_graph(file):
    with open(file, 'rb') as f:
        graph = pickle.load(f)
    return graph

def save_graph(graph, file):
    with open(file, 'wb') as f:
        pickle.dump(graph, f, pickle.HIGHEST_PROTOCOL)

def draw_hist(X, show=False, **kwargs):
    # Get a list of all the artists' degrees
    hist = plt.hist(X, **kwargs)
    if show:
        plt.show()
    else:
        return hist

def draw_boxplot(X, show=False, **kwargs):
    # Get a list of all the artists' degrees
    boxplot = plt.boxplot(X, **kwargs)
    if show:
        plt.show()
    else:
        return boxplot