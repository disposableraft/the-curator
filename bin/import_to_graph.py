import constants
import utils
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

    def graph_exhibition(self, graph, ex_number):
        # Get the group of rows with `number` and have the artist role.
        ex_df = self.df.loc[self.df["ExhibitionID"] == ex_number]
        ex_df = ex_df.loc[ex_df['ExhibitionRole'] == 'Artist']

        count, _cols = ex_df.shape
        if ex_df.empty or count < 2 or count > 50:
            return

        # Set up and create the exhibition node
        # The first argument of `at` is the Series index, which can begin anywhere from 1 to N.
        id = ex_df.at[ex_df.index[0], 'ExhibitionID']
        title = ex_df.at[ex_df.index[0], 'ExhibitionTitle']
        # Some exhibition numbers contain string values :(, so leave `id` as string
        ex_node = Exhibition(int(id), title)

        # Add the exhibition node to the graph
        graph.add(ex_node)

        for _index, row in ex_df.iterrows():
            # Set up and create the artist node
            name = row['DisplayName']
            wikidataID = row['WikidataID']
            artist_node = Artist(name, wikidataID=wikidataID)
            # Create an edge from exhibition to artist
            graph.add_edge(ex_node.id, artist_node)

        return graph


csv_path = constants.MOMA_EXHIBITIONS_CSV
moma = Moma(pd.read_csv(csv_path, encoding="ISO-8859-1"))

data_dir = constants.PROJECT_DATA
d = date.today()
outfile = data_dir.joinpath(f'{d.year}{d.month}{d.day}-moma-exhibitions.pickle')

graph = Graph()

for exhibition_number in moma.list_exhibitions():
    moma.graph_exhibition(graph, exhibition_number)

utils.save_graph(graph, outfile)
