import utils
import constants as c
from category import Category
from wikidata import Wikidata

path = c.PROJECT_DATA_PICKLES.joinpath('202078-moma-exhibitions.pickle')
graph = utils.load_graph(path)

artist_nodes = [value for value in graph.nodes.values()
                if value.type == 'Artist'
                and value.wikidataID != None]
report = {
    'edges_added': 0,
    'categories_added': set(),
    'artists_not_updated': set()
    }
for artist_node in artist_nodes:
    labels = Wikidata(artist_node.wikidataID).stub_fetch()
    if len(labels) == 0:
        report['artists_not_updated'].add(artist_node.id)
    else:
        artist_node.categories.add(labels)
        for label in labels:
            category_id = hash(label)
            if category_id not in graph.nodes:
                graph.add(Category(label))
                report['categories_added'].add(label)
            graph.add_edge(category_id, artist_node)
            report['edges_added'] += 1

# Save the graph