import utils
import constants as c

graph_pickle = c.PROJECT_DATA_PICKLES.joinpath('2020710-moma-exhibitions.pickle')

data = utils.load_graph(graph_pickle)

def artist_incoming_edges(artists, exhibitions):
    """
    Returns an object { 'tokenizedname': int } where int is a count of 
    how many times token appear in exhibition nodes.
    """
    incoming = dict()
    for token, _node in artists:
        incoming.setdefault(token, 0)
        for exhibition_node in exhibitions:
            if token in exhibition_node.edges:
                incoming[token] += 1
    return incoming

degrees = [n.degrees for n in data if n.type == 'Exhibition']
X = sorted(degrees)

artists = [(key, value) for key, value in data.nodes.items()  if value.type == 'Artist']
exhibitions = [n for n in data if n.type == 'Exhibition']

artist_incoming = artist_incoming_edges(artists, exhibitions)

artist_incoming_frequencies = [count for _token, count in artist_incoming.items()]

utils.draw_hist(artist_incoming_frequencies, show=True)
