import unittest
from nodes import Node
from gensim.parsing.preprocessing import preprocess_string

class Artist(Node):
    def __init__(self, name, wikidataID=None):
        self.name = name
        self.id = self.tokenize()
        self.wikidataID = wikidataID

        super().__init__(self.id)
    
    def tokenize(self):
        token = "".join(preprocess_string(self.name))
        return token
        

class TestArtist(unittest.TestCase):
    def test_artist(self):
        x = Artist('Elaine De Kooning')
        self.assertEqual(x.name, 'Elaine De Kooning')
        self.assertEqual(x.id, 'elainkoon')


if __name__ == '__main__':
    unittest.main()