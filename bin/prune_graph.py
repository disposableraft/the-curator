import utils

def run(config):
    """
    Delete nodes from graph.
    """
    graph = utils.load_graph('import.pickle', config)

    exhibitions = graph.get_nodes()['Exhibition'].values()
    artists = graph.get_nodes()['Artist'].values()

    del_artists = [a for a in artists if a.degrees < 3]
    del_exhibitions = [e for e in exhibitions if e.degrees < 2 or e.degrees > 50]

    print(f'Pruning {len(del_artists + del_exhibitions)} nodes.')

    graph.prune(del_artists + del_exhibitions)
    utils.save_graph(graph, 'import.pickle', config)
