import utils
import constants
import requests
from graph import Node
from random import randrange
from string import Template

class Wikidata:
    def __init__(self, id):
        self.id = id
        self.categories = []

    def stub_fetch(self):
        # Return an array with 1 to 3 items, each item being a random number between 1 and 23 representing a category
        stop = randrange(0,4)
        categories = []
        for _ in range(stop):
            categories.append(str(randrange(1,23)))
        return categories

    def fetch(self):
        url = 'https://query.wikidata.org/sparql'
        query = Template("""
            SELECT ?movementLabel WHERE {
                wd:${id} wdt:P135 ?movement.
                SERVICE wikibase:label {
                    bd:serviceParam wikibase:language "en" .
                }
            }
        """)
        query = query.substitute(id=self.id)

        try:
            params = {'format': 'json', 'query': query}
            req = requests.get(url, params=params)
            data = req.json()

            results = data['results']['bindings']
            categories = [i['movementLabel']['value'] for i in results]

            return categories
        except Exception as E:
            print(f'An error occured fetching {self.id}. \nError:\n{E}\n')
            return []


class Category(Node):
    def __init__(self, title):
        self.title = title
        self.id = hash(title)
        super().__init__(self.id)

path = constants.PROJECT_DATA_PICKLES.joinpath('202078-moma-exhibitions.pickle')
graph = utils.load_graph('../data/202078-moma-exhibitions.pickle')

# For each Artist node that does not have category data
# Get the wikidataID
# Fetch the category from wikidata
# Search for an existing Category node
# If not found, then create a new Category node
# Add the category to the graph
# Add an edge to the Artist node
# Report how many artists were updated
# Report all the names of categories
# Report how many artists were not updated

artist_nodes = [value for value in graph.nodes.values()
                if value.__class__.__name__ == 'Artist'
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