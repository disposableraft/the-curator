"""Generate text files for artist permutations"""

import pandas as pd
import itertools


class ExhibitionData:
    def __init__(self, csv_path, outfile):
        self.data = pd.read_csv(csv_path)
        self.outfile = outfile

    def format_name(self, name):
        "Join a name with an underscore"
        return "_".join(name.split(" ")).lower()

    def format_line(self, tup):
        "Return a string of n names joined with underscores"
        return " ".join([self.format_name(t) for t in tup])

    def exhibition_numbers(self, startstop=None):
        """
        Return a list of exhibition numbers.
        count: By default return all of them.
        """
        unique_numbers = list(self.data.ExhibitionNumber.unique())
        if not startstop:
            return unique_numbers
        else:
            start, stop = startstop
            return unique_numbers[start:stop]

    def exhibition_artists(self, exh_number):
        "Return a list of artists given an exhibition number"
        exh = self.data.loc[self.data["ExhibitionNumber"] == str(exh_number)]
        # From that take only the artists (leaving the curators)
        artists = exh.loc[exh["ExhibitionRole"] == "Artist"]
        return artists["DisplayName"].tolist()

    def combinations(self, i, r=5):
        return itertools.combinations(i, r)

    def append_to_outfile(self, i):
        if len(i) == 0:
            return None

        with open(self.outfile, "a") as f:
            # There's probably a better way to do this. For tuples we want
            # a loop, for lists we just want to write it out.
            if type(i) == tuple:
                for c in i:
                    f.write(f"{self.format_line(c)}\n")
            else:
                f.write(f"{self.format_line(i)}\n")
        f.close()


def export_most_combinations():
    csv_path = "~/data1/moma/exhibitions/MoMAExhibitions1929to1989.csv"
    outfile = "../data/artist_test_combos.txt"
    Moma = ExhibitionData(csv_path, outfile)

    exh_numbers = Moma.exhibition_numbers()
    # Remove the wierd placeholder show
    exh_numbers.remove("No#")

    for en in exh_numbers:
        terms = Moma.exhibition_artists(en)
        # Don't calculate and output big lists
        if len(terms) <= 50:
            C = Moma.combinations(terms, 5)
            Moma.append_to_outfile(C)


def export_no_combinations():
    csv_path = "~/data1/moma/exhibitions/MoMAExhibitions1929to1989.csv"
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


export_no_combinations()
