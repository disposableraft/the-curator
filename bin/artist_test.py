import unittest
from artist import Artist

class TestArtist(unittest.TestCase):
    def test_artist(self):
        x = Artist('Elaine De Kooning')
        self.assertEqual(x.name, 'Elaine De Kooning')
        self.assertEqual(x.token, 'elainkoon')


if __name__ == '__main__':
    unittest.main()