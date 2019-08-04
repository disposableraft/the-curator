"""Generate text files for artist permutations"""

from pathlib import Path
from itertools import combinations
import pandas as pd

def format_line(tup):
    """Return a string of five names joined with underscores"""
    return ' '.join([format_name(t) for t in tup])


def format_name(name):
    """Join a name with an underscore"""
    return '_'.join(name.split(' ')).lower()


def output(data, exh_id):
    """Save a file"""
    # Select the rows with exhibition ID
    exh = data.loc[data['ExhibitionNumber'] == str(exh_id)]
    # From that take only the artists, leaving the curators
    artists = exh.loc[exh['ExhibitionRole'] == 'Artist']
    artist_names = artists['DisplayName'].tolist()

    # Get all combinations in sets of 5
    combos = combinations(artist_names, 5)
    print(f"artist_names: {artist_names}")

    with open('./artist_combinations_output.txt', 'a') as f:
        for line in list(combos):
            f.write(f"{format_line(line)}\n")

    f.close()


p = Path('../moma/exhibitions/MoMAExhibitions1929to1989.csv')
d = pd.read_csv(p)


# Output combinations for the first 10 exhibitions
for i in range(1, 10):
    print(f"outputing exh_id {i}")
    output(d, i)
