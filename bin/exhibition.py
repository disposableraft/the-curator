import unittest
from nodes import Node
from artist import Artist

class Exhibition(Node):
    def __init__(self, id, title):
        super().__init__(id)
        self.title = title



# class TestExhibition(unittest.TestCase):
#     def test_exhibition(self):
#         id = 1
#         title = "New Paintings"
#         artists = ['foo j bar', 'ell p mad']
#         e = Exhibition(id, title, artists)
#         self.assertEqual(e.title, title)
#         self.assertEqual(len(e.artists), 2)
    
#     def test_members_count(self):
#         id = 1
#         title = "New Paintings"
#         artists = ['foo j bar', 'ell p mad']
#         e = Exhibition(id, title, artists)
#         self.assertEqual(2, e.members)

if __name__ == '__main__':
    unittest.main()
