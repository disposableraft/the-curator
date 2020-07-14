import utils
import constants as c
from category import Category
from wikidata import Wikidata
from fetch_labels import FetchLabels

path = c.PROJECT_DATA_PICKLES.joinpath('2020713-moma-exhibitions-categories.pickle')
graph = utils.load_graph(path)

# nodes = [value for value in graph
#                 if value.type == 'Artist'
#                 and value.wikidataID != None
#                 and value.degrees > 2]

report = utils.load_graph(
    c.PROJECT_DATA_PICKLES.joinpath('2020713-moma-exhibitions-categories-report.pickle')
)

nodes = [graph[tk] for tk in report['unupdated']]

fetcher = FetchLabels(nodes, graph)
(new_graph, report) = fetcher.run()

utils.save_graph(
    new_graph,
    c.PROJECT_DATA_PICKLES.joinpath('2020713-moma-exhibitions-categories.pickle')
    )

utils.save_graph(
    report,
    c.PROJECT_DATA_PICKLES.joinpath('2020713-moma-exhibitions-categories-report.pickle')
    )
