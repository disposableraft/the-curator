import utils
import constants as c
from category import Category
from wikidata import Wikidata

path = c.PROJECT_DATA_PICKLES.joinpath('2020712-moma-exhibitions.pickle')
graph = utils.load_graph(path)

report = {
    'edges_added': 0,
    'categories_added': set(),
    'artists_not_updated': set()
    }

artist_nodes = [value for value in graph
                if value.type == 'Artist'
                and value.wikidataID != None
                and value.degrees > 2]

print(f'Total artist nodes: {len(artist_nodes)}')

for index, artist_node in enumerate(artist_nodes):
    if index % 50 == 0:
        print(f'Saving tmp file {index / 50}...')
        utils.save_graph(graph, c.PROJECT_DATA_PICKLES.joinpath('tmp-fetch-movements.pickle'))
        utils.save_graph(report, c.PROJECT_DATA_PICKLES.joinpath('tmp-fetch-movements-report.pickle'))
    if str(artist_node.wikidataID) == 'nan':
        continue
    labels = Wikidata(artist_node.wikidataID).fetch()
    if not labels:
        report['artists_not_updated'].add(artist_node.id)
    else:
        for label in labels:
            artist_node.categories.add(label)
            category_id = hash(label)
            if category_id not in graph.nodes:
                graph.add(Category(label))
                report['categories_added'].add(label)
            graph.add_edge(category_id, artist_node)
            report['edges_added'] += 1

# Save the graph