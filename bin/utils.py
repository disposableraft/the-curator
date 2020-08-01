import os
import pickle
from datetime import date

def date_slug():
    d = date.today()
    return f'{d.year}-{d.month}-{d.day}'

def load_graph(name, config):
    """
    Read the current version of the graph from disk.
    """
    file = os.path.join(config['version_dir'], name)
    with open(file, 'rb') as f:
        graph = pickle.load(f)
    return graph

def write(file, data):
    """
    Write/overwrite a binary pickle file
    """
    with open(file, 'wb') as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

def save_graph(graph, name, config):
    """
    Save a new graph to the current version dir.
    """
    file = os.path.join(config['version_dir'], name)
    write(file, graph)
    return file

def get_labeled_nodes(cats):
    labeled = set()
    for c in cats:
        for m in c.edges:
            labeled.add(m)
    return labeled
