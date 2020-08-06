import unittest
import constants
import utils
import pandas as pd
from graph import Graph
from artist import Artist
from exhibition import Exhibition

class Importer:
    def __init__(self, *importers):
        self.graph = Graph()
        self.importers = list(importers)

    def run(self):
        for importer in self.importers:
            for row in importer:
                (id, title, source), artists = row
                print(f'Importing "{title}" from {source}')
                exh_node = self.graph.add(Exhibition(id, title, source))
                nodes = []
                for a in artists:
                    name, wikidata_id = a
                    node = self.graph.add(Artist(name, wikidataID=wikidata_id))
                    nodes.append(node)
                self.graph.add_edges(exh_node, nodes)

class Dome:
    def __init__(self, artist_path, exh_path):
        self.artist_df = pd.read_csv(artist_path)
        self.exh_df = pd.read_csv(exh_path)
        self.source = 'dome'
        self.exhibitions = self.load_data()

    def __iter__(self):
        yield from self.exhibitions

    def load_data(self):
        exhibitions = []
        for _index, exh in self.exh_df.iterrows():
            exhibitions.append(self.build_exhibition(exh))
        return exhibitions

    def transform_name(self, name):
        names = name.split(',')
        names.reverse()
        return ' '.join(names).strip()

    def build_exhibition(self, exh):
        id = exh.ID
        title = exh.Title
        members = self.artist_df.loc[self.artist_df.ExhibitionID == id]
        artists = []
        for _, a in members.iterrows():
            name = self.transform_name(a.Name)
            artists.append((name, a.Wikidata))
        # [(id, title, source), [(name, wikidata_id), ...]]
        return [(id, title, self.source), artists]

class Moma:
    def __init__(self, path):
        self.df = pd.read_csv(path, encoding="ISO-8859-1")
        self.source = 'moma'
        self.exhibitions = self.load_data()

    def __iter__(self):
        yield from self.exhibitions

    def load_data(self):
        exhibitions = []
        for id in self.get_ids():
            exhibition = self.get_exhibition(id)
            if exhibition:
                exhibitions.append(exhibition)
        return exhibitions

    def get_ids(self):
        return list(self.df.ExhibitionID.unique())

    def get_exhibition(self, exh_id):
        # [(id, title, source), [(name, wikidata_id), ...]]
        exhibition = self.df.loc[self.df['ExhibitionID'] == exh_id]
        if len(exhibition) < 2:
            return False
        id = exhibition.ExhibitionID.to_list()[0]
        title = exhibition.ExhibitionTitle.to_list()[0]
        artists = []
        for _i, row in exhibition.iterrows():
            artists.append((row['DisplayName'], row['WikidataID']))
        return [(id, title, self.source), artists]


def run(config):
    moma = Moma(constants.MOMA_EXHIBITIONS_CSV)
    dome = Dome(
        constants.DOME_ARTISTS_CSV,
        constants.DOME_EXHIBITIONS_CSV
        )
    importer = Importer(moma, dome)
    importer.run()
    utils.save_graph(importer.graph, 'import.pickle', config)

class TestImporter(unittest.TestCase):
    def test_importer_init(self):
        moma = Moma(constants.MOMA_EXHIBITIONS_CSV_TEST)
        importer = Importer(moma)
        self.assertEqual(len(importer.importers), 1)

    def test_importer_run(self):
        moma = Moma(constants.MOMA_EXHIBITIONS_CSV_TEST)
        dome = Dome(
            constants.DOME_ARTISTS_CSV_TEST,
            constants.DOME_EXHIBITIONS_CSV_TEST
        )
        importer = Importer(moma, dome)
        importer.run()
        self.assertEqual(importer.graph.count_nodes(), 47)
        self.assertEqual(importer.graph.count_edges(), 43)

class TextDome(unittest.TestCase):
    def test_transform_name(self):
        name = 'Gauguin, Paul'
        expected = 'Paul Gauguin'
        self.assertEqual(Dome.transform_name(dict, name), expected)

    def test_dome_init(self):
        dome = Dome(
            constants.DOME_ARTISTS_CSV_TEST,
            constants.DOME_EXHIBITIONS_CSV_TEST
        )
        self.assertEqual(dome.source, 'dome')
        self.assertEqual(len(dome.exhibitions), 3)

    def test_dome_load_iter(self):
        dome = Dome(
            constants.DOME_ARTISTS_CSV_TEST,
            constants.DOME_EXHIBITIONS_CSV_TEST
            )
        artists = []
        for exh in dome:
            (_), members = exh
            for m in members:
                artists.append(m)
        self.assertEqual(len(artists), 20)

class TestMoma(unittest.TestCase):
    def test_moma_init(self):
        moma = Moma(constants.MOMA_EXHIBITIONS_CSV_TEST)
        self.assertEqual(moma.source, 'moma')
        self.assertEqual(len(moma.exhibitions), 3)

    def test_moma_load_iter(self):
        moma = Moma(constants.MOMA_EXHIBITIONS_CSV_TEST)
        artists = []
        for exh in moma:
            (_), members = exh
            for m in members:
                artists.append(m)
        self.assertEqual(len(artists), 23)

if __name__ == '__main__':
    unittest.main()