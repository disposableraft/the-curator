import utils
import constants as c
from itertools import combinations

class Export:
    def __init__(self, directory):
        self.directory = directory


graph = utils.load_graph()

# Prepare the graph.
# Prune artists belonging to 2 or fewer shows
for v in graph:
    if v.type == 'Artist':
        if v.degrees <= 2:
            graph.remove_node(v)

# Loop through the exhbitions
# Do the combinations.
# Save one file of combinations per exhbition.

exhibitions = graph.get_nodes()['Exhibition'].values()

print(f'{"Index":<6s}{"Edges":<7s}{"ID":<8s}{"Title"}')

for index, e in enumerate(exhibitions):
    print(f'{index:<6d}{len(e.edges):<7d}{e.id:<8d}{e.title}')
    
    if len(e.edges) >= 5:
        lines = combinations(list(e.edges), 5)
    else:
        lines = [e.edges]

    file = c.TRAIN.joinpath(f'{e.id}.txt')
    with open(file, 'w') as f:
        for line in lines:
            f.write(" ".join(line))
            f.write("\n")

#
# Save export files ...