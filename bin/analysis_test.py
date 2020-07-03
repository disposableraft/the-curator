import category as analysis
import unittest

class TestArtist(unittest.TestCase):
    def test_artist(self):
        x = analysis.Artist('Elaine De Kooning')
        self.assertEqual(x.name, 'Elaine De Kooning')
        self.assertEqual(x.token, 'elainkoon')

class TestCategory(unittest.TestCase):
    def test_category(self):
        x = analysis.Category('abex', ['Elaine De Kooning', 'Eva Hesse'])
        self.assertEqual(x.name, 'abex')
        self.assertEqual(len(x), 2)
    
    def test_add(self):
        x = analysis.Category('abex')
        x.add('Jacky Pollock')
        self.assertTrue('jackipollock' in x.artists)
    
    def test_is_member(self):
        x = analysis.Category('abex', ['foo bar', 'baz pax'])
        y = x.artists['bazpax']
        self.assertTrue(x.is_member(y))

if __name__ == '__main__':
    unittest.main()