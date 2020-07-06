import pandas as pd
from nodes import Graph
from artist import Artist
from exhibition import Exhibition

# get one exhibition with N artists

G = Graph()

csv_path = "~/data1/moma/exhibitions/MoMAExhibitions1929to1989.csv"
df = pd.read_csv(csv_path, encoding="ISO-8859-1")

# The ID
exhibition = df.loc[df["ExhibitionNumber"] == str(1)]
# Don't list curators, etc
exhibition = exhibition.loc[df['ExhibitionRole'] == 'Artist']

rows = exhibition[[
    'ConstituentID', 
    'WikidataID', 
    'DisplayName', 
    'ExhibitionNumber', 
    'ExhibitionTitle'
    ]]


id = exhibition.at[1, 'ExhibitionNumber']
id = int(id)
title = exhibition.at[1, 'ExhibitionTitle']

exhibition = Exhibition(id, title)

for _index, row in rows.iterrows():
    name = row['DisplayName']
    wikidataID = row['WikidataID']
    node = Artist(name, wikidataID=wikidataID)
    
    exhibition.add_edge(node)

G.add(exhibition) 

print(G.bfs())

