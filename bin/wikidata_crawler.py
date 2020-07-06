"""
SELECT ?artist ?artistLabel ?identifier ?identifierLabel ?movement ?movementLabel WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    ?artist wdt:P170 wd:Q35548.
  ?identifier wdt:P31 wd:Q853614.
  ?identifier wdt:P106 wd:Q2500638.
  OPTIONAL { ?identifier wdt:P135 ?movement. }
}
LIMIT 100


select ?artist
where {
  ?movement ?hasmember ?artist
}


Movements P135:
https://www.wikidata.org/wiki/Q166713


Given a list of artists from MoMA dataset, for each artist select the wikidata ID, query wikidata for the movements to which that artist belongs, and, finally, update the record with new data.
"""

