import pandas as pd
from nodes import Graph
from artist import Artist
from exhibition import Exhibition

# get one exhibition with N artists

def import_exhibition(graph, number, dataframe):
    # Get the group of rows with `number` and have the artist role.
    ex_df = dataframe.loc[dataframe["ExhibitionNumber"] == str(number)]
    ex_df = ex_df.loc[df['ExhibitionRole'] == 'Artist']
    
    # Set up and create the exhibition node
    # The first argument of `at` is the Series index, which can begin anywhere from 1 to N.
    id = ex_df.at[ex_df.index[0], 'ExhibitionNumber']
    title = ex_df.at[ex_df.index[0], 'ExhibitionTitle']
    ex_node = Exhibition(int(id), title)

    rows = ex_df[[
        'WikidataID', 
        'DisplayName', 
        ]]

    for _index, row in rows.iterrows():
        # Set up and create the artist node
        name = row['DisplayName']
        wikidataID = row['WikidataID']
        artist_node = Artist(name, wikidataID=wikidataID)
        # Create an edge from exhibition to artist
        ex_node.add_edge(artist_node)
    
    # Add the exhibition node to the graph
    graph.add(ex_node) 

    return graph


csv_path = "~/data1/moma/exhibitions/MoMAExhibitions1929to1989.csv"
df = pd.read_csv(csv_path, encoding="ISO-8859-1")

G = import_exhibition(Graph(), 2, df)

print(G.nodes)

