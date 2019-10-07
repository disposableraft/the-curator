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
        output = similar.get_ten(token)
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

    def test_get_neighbors(self):
        """
        Should return ten similar artists, and each artist should include another ten similar artists.
        """
        expected = {
            "token": "evahess",
            "similar": [
                {
                    "token": "josephbeui",
                    "similar": [
                        {"token": "bryanhunt"},
                        {"token": "evahess"},
                        {"token": "blinkipalermo"},
                        {"token": "johnchamberlain"},
                        {"token": "terriwinter"},
                        {"token": "christochristojavacheff"},
                        {"token": "alansaret"},
                        {"token": "brucenauman"},
                        {"token": "robertsmithson"},
                        {"token": "öyvindfahlström"},
                    ],
                },
                {
                    "token": "robertsmithson",
                    "similar": [
                        {"token": "frankstella"},
                        {"token": "twombl"},
                        {"token": "andiwarhol"},
                        {"token": "carlandr"},
                        {"token": "richardartschwag"},
                        {"token": "robertryman"},
                        {"token": "evahess"},
                        {"token": "johnchamberlain"},
                        {"token": "bryanhunt"},
                        {"token": "christochristojavacheff"},
                    ],
                },
                {
                    "token": "johnchamberlain",
                    "similar": [
                        {"token": "bryanhunt"},
                        {"token": "richardartschwag"},
                        {"token": "alansaret"},
                        {"token": "susanrothenberg"},
                        {"token": "andiwarhol"},
                        {"token": "twombl"},
                        {"token": "melbochner"},
                        {"token": "gariindiana"},
                        {"token": "alanshield"},
                        {"token": "frankstella"},
                    ],
                },
                {
                    "token": "hanndarboven",
                    "similar": [
                        {"token": "jameleebyar"},
                        {"token": "michaelheizer"},
                        {"token": "georgsegal"},
                        {"token": "melbochner"},
                        {"token": "johncage"},
                        {"token": "panamarenko"},
                        {"token": "evahess"},
                        {"token": "öyvindfahlström"},
                        {"token": "lawrencweiner"},
                        {"token": "marktansei"},
                    ],
                },
                {
                    "token": "marktansei",
                    "similar": [
                        {"token": "terriwinter"},
                        {"token": "lyndabengli"},
                        {"token": "baer"},
                        {"token": "bricemarden"},
                        {"token": "jonathanborofski"},
                        {"token": "alanshield"},
                        {"token": "evahess"},
                        {"token": "hanndarboven"},
                        {"token": "danflavin"},
                        {"token": "danielburen"},
                    ],
                },
                {
                    "token": "bryanhunt",
                    "similar": [
                        {"token": "johnchamberlain"},
                        {"token": "melbochner"},
                        {"token": "richardartschwag"},
                        {"token": "alansaret"},
                        {"token": "patsteir"},
                        {"token": "josephbeui"},
                        {"token": "alfrjensen"},
                        {"token": "ericfischl"},
                        {"token": "robertsmithson"},
                        {"token": "christochristojavacheff"},
                    ],
                },
                {
                    "token": "chuckclose",
                    "similar": [
                        {"token": "bryanhunt"},
                        {"token": "marcelbroodthaer"},
                        {"token": "michelangelopistoletto"},
                        {"token": "evahess"},
                        {"token": "carlandr"},
                        {"token": "melbochner"},
                        {"token": "rossbleckner"},
                        {"token": "johncage"},
                        {"token": "richardartschwag"},
                        {"token": "carlfredrikreuterswärd"},
                    ],
                },
                {
                    "token": "öyvindfahlström",
                    "similar": [
                        {"token": "michaelheizer"},
                        {"token": "fredsandback"},
                        {"token": "melbochner"},
                        {"token": "bryanhunt"},
                        {"token": "hanndarboven"},
                        {"token": "evahess"},
                        {"token": "johncage"},
                        {"token": "pieromanzoni"},
                        {"token": "georgsegal"},
                        {"token": "josephbeui"},
                    ],
                },
                {
                    "token": "alansaret",
                    "similar": [
                        {"token": "johnchamberlain"},
                        {"token": "bryanhunt"},
                        {"token": "richardartschwag"},
                        {"token": "robertsmithson"},
                        {"token": "dorothearockburn"},
                        {"token": "rossbleckner"},
                        {"token": "evahess"},
                        {"token": "josephbeui"},
                        {"token": "richardserra"},
                        {"token": "carlandr"},
                    ],
                },
                {
                    "token": "carlandr",
                    "similar": [
                        {"token": "frankstella"},
                        {"token": "robertsmithson"},
                        {"token": "robertrauschenberg"},
                        {"token": "andiwarhol"},
                        {"token": "robertmorri"},
                        {"token": "helenfrankenthal"},
                        {"token": "jamerosenquist"},
                        {"token": "richardserra"},
                        {"token": "alexkatz"},
                        {"token": "claeoldenburg"},
                    ],
                },
            ],
        }
        output = Similar().get_neighbors("evahess")

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
        self.assertEquals(10, len(content["similar"]))

    def test_responds_with_original_token(self):
        """
        The JSON output includes the original token.
        """
        res = self.client.get(reverse("curator:similar", args=["helenfrankenthal"]))
        content = json.loads(res.content)
        self.assertEqual("helenfrankenthal", content["token"])

    def test_responds_with_full_artist_data(self):
        """
        The JSON includes full artist data.
        """
        res = self.client.get(reverse("curator:similar", args=["helenfrankenthal"]))
        self.assertContains(res, "display_name")
        self.assertContains(res, "token")
        self.assertContains(res, "url")

