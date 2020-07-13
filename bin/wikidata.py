import requests
from string import Template
from random import randrange

class Wikidata:
    def __init__(self, id):
        self.id = id
        self.categories = []

    def __str__(self):
        return str({'id': self.id})

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
            if len(results) > 0:
                categories = [i['movementLabel']['value'] for i in results]
                return categories
        except Exception as E:
            print(f'Error fetching {self.id}. Error: {E}. Object: {self}')
