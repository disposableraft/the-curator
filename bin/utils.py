import os
import pickle
import matplotlib.pyplot as plt
from datetime import date
import constants as c

def date_slug():
    d = date.today()
    return f'{d.year}-{d.month}-{d.day}'

def load_graph():
    """
    Read the current version of the graph from disk.
    """
    with open(c.CURRENT, 'rb') as f:
        graph = pickle.load(f)
    return graph

def write(file, data):
    """
    Write/overwrite a binary pickle file
    """
    with open(file, 'wb') as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

def save_graph(graph, name):
    """
    Save a new graph to disk.

    Updates the hard link and returns the filename.
    """
    file = c.VERSIONS.joinpath(f'{date_slug()}-{name}.pickle')
    write(file, graph)
    try:
        os.symlink(file, c.CURRENT)
    except FileExistsError:
        os.unlink(c.CURRENT)
        os.symlink(file, c.CURRENT)

    return file


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

