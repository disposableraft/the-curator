import utils
from itertools import combinations

def run(config):
    combinations_r = config['combinations_r']
    train_dir = config['corpus']['train_dir']
    graph = utils.load_graph('import.pickle', config)
    # Prune artists belonging to 2 or fewer shows
    for v in graph:
        if v.type == 'Artist':
            if v.degrees <= 2:
                graph.remove_node(v)

    exhibitions = graph.get_nodes()['Exhibition'].values()

    print(f'{"Index":<6s}{"Edges":<7s}{"ID":<8s}{"Title"}')

    # Save one file of combinations per exhbition.
    for index, e in enumerate(exhibitions):
        print(f'{index:<6d}{len(e.edges):<7d}{e.id:<8d}{e.title}')

        # For nodes with fewer degrees than combos, simply list their symbols.
        if e.degrees >= combinations_r:
            lines = combinations(list(e.edges), combinations_r)
        else:
            lines = [e.edges]

        file = train_dir.joinpath(f'{e.id}.txt')
        with open(file, 'w') as f:
            for line in lines:
                f.write(" ".join(line))
                f.write("\n")

    return True

