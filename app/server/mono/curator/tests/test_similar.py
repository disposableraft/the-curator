import json

from django.test import TestCase
from django.urls import reverse

from curator.models import Artist
from curator.similar import Similar

"""
Tests for the Similar utility, which contacts the gensim model.
The next class below tests the view.
"""


class SimilarTest(TestCase):
    def test_get_ten_returns_ten(self):
        """
        Similar gets ten artists similar to the token.
        Don't test the scores, because they differ slightly on each request.
        """
        token = "marcelduchamp"
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


class SimilarViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        artists = []
        tokens = [
            "carlandr",
            "louisnevelson",
            "claeoldenburg",
            "robertmotherwel",
            "joanmitchel",
            "allanarcangelo",
            "robertmorri",
            "larririver",
            "willemkoon",
            "robertrauschenberg",
        ]
        for t in tokens:
            artists.append(
                Artist.objects.create(
                    display_name=f"display_name: {t}",
                    token=t,
                    moma_url=f"moma_url: {t}",
                )
            )
        cls.artists = artists

    def test_responds_with_artists_list(self):
        """
        The JSON output includes a list of ten artist names.
        """
        res = self.client.get(reverse("curator:similar", args=["helenfrankenthal"]))
        content = json.loads(res.content)
        self.assertEquals(10, len(content["artists"]))

    def test_responds_with_original_token(self):
        """
        The JSON output includes the original token.
        """
        res = self.client.get(reverse("curator:similar", args=["helenfrankenthal"]))
        content = json.loads(res.content)
        self.assertEqual("helenfrankenthal", content["original_token"])

    def test_responds_with_full_artist_data(self):
        """
        The JSON includes full artist data.
        """
        res = self.client.get(reverse("curator:similar", args=["helenfrankenthal"]))
        self.assertContains(res, "display_name")
        self.assertContains(res, "token")
        self.assertContains(res, "url")

