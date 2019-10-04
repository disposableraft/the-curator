from django.test import TestCase
from curator.similar import Similar


class SimilarTest(TestCase):
    def test_get_ten_returns_ten(self):
        token = 'marcelduchamp'
        similar = Similar()
        similarities = similar.get_ten(token)
        output = [t for t, _ in similarities]
        expected = [
            "eliotelisofon",
            "étiennjulemarei",
            "hilairgermainedgardega",
            "hagenguth",
            "internnewphoto",
            "thomaeakin",
            "lászlómoholinagi",
            "johanntheodorbaargeldalfremanuelferdinandgruenwald",
            "gerhardrichter",
            "francipicabia",
        ]
        self.assertEqual(expected, output)
