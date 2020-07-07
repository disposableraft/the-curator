import pickle
from pathlib import Path
from datetime import date
import pandas as pd
from nodes import Graph
from artist import Artist
from exhibition import Exhibition

class Moma:
    def __init__(self, dataframe):
        self.df = dataframe

    def list_exhibitions(self):
        return list(self.df.ExhibitionID.unique())

    def graph_exhibition(self, ex_number, graph):
        # Get the group of rows with `number` and have the artist role.
        ex_df = self.df.loc[self.df["ExhibitionID"] == ex_number]
        ex_df = ex_df.loc[ex_df['ExhibitionRole'] == 'Artist']

        count, _cols = ex_df.shape
        if ex_df.empty or count < 2 or count > 50:
            return

        # Set up and create the exhibition node
        # The first argument of `at` is the Series index, which can begin anywhere from 1 to N.
        # print(ex_df)
        id = ex_df.at[ex_df.index[0], 'ExhibitionID']
        title = ex_df.at[ex_df.index[0], 'ExhibitionTitle']
        # Some exhibition numbers contain string values :(, so leave `id` as string
        ex_node = Exhibition(int(id), title)

        for _index, row in ex_df.iterrows():
            # Set up and create the artist node
            name = row['DisplayName']
            wikidataID = row['WikidataID']
            artist_node = Artist(name, wikidataID=wikidataID)
            # Create an edge from exhibition to artist
            ex_node.add_edge(artist_node)

        # Add the exhibition node to the graph
        graph.add(ex_node)

        return graph


csv_path = Path("~/data1/moma/exhibitions/MoMAExhibitions1929to1989.csv")
moma = Moma(pd.read_csv(csv_path, encoding="ISO-8859-1"))

d = date.today()
basepath = Path('~/writing1/projects/the-curator/data').expanduser()
outfile = basepath.joinpath(f'{d.year}{d.month}{d.day}-moma-exhibitions.pickle')

graph = Graph()

for ex in moma.list_exhibitions():
    moma.graph_exhibition(ex, graph)

with open(outfile, mode='wb') as file:
    pickle.dump(graph, file, pickle.HIGHEST_PROTOCOL)

with open(outfile, 'rb') as file:
    data = pickle.load(file)

# for key, value in data.nodes.items():
#     print(f'{key:<7d} {len(value.edges):<10d} {value.title}')

print(f'Nodes: {len(data.nodes)}')