import utils
import pickle
import constants as c
from category import Category
from wikidata import Wikidata
from fetch_labels import FetchLabels

report_path = c.PROJECT_TMP.joinpath('fetch-movements-report.pickle')

graph = utils.load_graph()

nodes = [value for value in graph
                if value.type == 'Artist'
                and value.wikidataID != None
                and value.degrees > 2]

# For rerunning the process without restarting, use
# the nodes from the report, using `report_path` above.
# nodes = [graph[tk] for tk in report['unupdated']]

fetcher = FetchLabels(nodes, graph)
(new_graph, report) = fetcher.run()

utils.save_graph(new_graph, name='moma-exhibitions-movements')

with open(report_path, 'wb') as f:
    pickle.dump(report, f, pickle.HIGHEST_PROTOCOL)
