import requests
from string import Template

class FetchCategories:
    def __init__(self, id):
        self.id = id
        self.categories = self.fetch()
        
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
        
        params = {'format': 'json', 'query': query}
        req = requests.get(url, params=params)
        data = req.json()   
        
        results = data['results']['bindings']
        categories = [i['movementLabel']['value'] for i in results]
        
        return categories
        
