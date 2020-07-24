import os
import pickle
from datetime import date
import constants as c

def date_slug():
    d = date.today()
    return f'{d.year}-{d.month}-{d.day}'

def load_graph(fn=None):
    """
    Read the current version of the graph from disk.
    """
    file = fn if fn else c.CURRENT
    with open(file, 'rb') as f:
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
    print(f'Linking current.pickle -> {file}')
    return file


