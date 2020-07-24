import utils
import constants as c
import pickle
from wikidata import Wikidata
from fetch_labels import FetchLabels

report_path = c.CURRENT.joinpath('fetch-movements-report.pickle')

graph = utils.load_graph('import.pickle')

nodes = [value for value in graph
                if value.type == 'Artist'
                and value.wikidataID != None
                and value.degrees > 2]

# For rerunning the process without restarting, use
# the nodes from the report, using `report_path` above.
# nodes = [graph[tk] for tk in report['unupdated']]

fetcher = FetchLabels(nodes, graph)
(new_graph, report) = fetcher.run()

utils.save_graph(new_graph, 'labeled-import.pickle')

with open(report_path, 'wb') as f:
    pickle.dump(report, f, pickle.HIGHEST_PROTOCOL)
