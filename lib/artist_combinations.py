"""
Generate text files for artist combinations
"""

import pandas as pd
import itertools
from gensim.parsing.preprocessing import preprocess_string


class ExhibitionData:
    def __init__(self, csv_path, outfile):
        self.data = pd.read_csv(csv_path, encoding="ISO-8859-1")
        self.outfile = outfile

    def format_name(self, name):
        "Join a name with an underscore"
        return "".join(preprocess_string(name))

    def format_line(self, tup):
        "Return a string of n names joined with underscores"
        return " ".join([self.format_name(t) for t in tup])

    def exhibition_numbers(self):
        """
        Return a list of exhibition numbers.
        """
        return list(self.data.ExhibitionNumber.unique())

    def exhibition_artists(self, exh_number):
        "Return a list of artists given an exhibition number"
        exh = self.data.loc[self.data["ExhibitionNumber"] == str(exh_number)]
        # From that take only the artists (leaving the curators)
        artists = exh.loc[exh["ExhibitionRole"] == "Artist"]
        return artists["DisplayName"].tolist()

    def combinations(self, i, r=5):
        return itertools.combinations(i, r)

    def append_to_outfile(self, i):
        with open(self.outfile, "a") as f:
            for c in i:
                f.write(f"{self.format_line(c)}\n")
        f.close()


def export_most_combinations():
    """
    Only export combinations of exhibitions with a given number of artists.
    """
    csv_path = "~/data1/moma/exhibitions/MoMAExhibitions1929to1989.csv"
    outfile = "../data/artist_combos.txt"
    Moma = ExhibitionData(csv_path, outfile)

    exh_numbers = Moma.exhibition_numbers()
    print(f"exh_numbers: {len(exh_numbers)}")
    # Remove the wierd placeholder show
    exh_numbers.remove("No#")

    for en in exh_numbers:
        terms = Moma.exhibition_artists(en)
        print(f"terms: {len(terms)}")
        # Don't calculate and output big lists
        if len(terms) <= 50:
            C = Moma.combinations(terms, 5)
            Moma.append_to_outfile(C)


def export_no_combinations():
    """
    Export only the exhibition names but not combinations.
    """
    csv_path = "~/data1/moma/exhibitions/MoMAExhibitions1931to1989.csv"
    outfile = "../data/artist_no_combos.txt"
    Moma = ExhibitionData(csv_path, outfile)

    exh_numbers = Moma.exhibition_numbers()
    # Remove the wierd placeholder show
    exh_numbers.remove("No#")

    for en in exh_numbers:
        terms = Moma.exhibition_artists(en)
        # Don't calculate and output big lists
        if len(terms) <= 50:
            Moma.append_to_outfile(terms)


export_most_combinations()

