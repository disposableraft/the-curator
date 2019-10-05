import json

from django.test import TestCase
from django.urls import reverse

from curator.models import Artist, Exhibition


def create_exhibition(title, url=None):
    return Exhibition.objects.create(title=title, moma_url=url)


class ExhibitionDetailViewTests(TestCase):
    def test_exhibition_json(self):
        """
        Returns a JSON object with an error field.
        """
        exh = create_exhibition("13 Foos")
        res = self.client.get(reverse("curator:exhibition", args=[exh.pk]))
        self.assertContains(res, "errors")

    def test_exhibition_title(self):
        """
        There's an exhibition title.
        """
        exh = create_exhibition("13 Foos")
        res = self.client.get(reverse("curator:exhibition", args=[exh.pk]))
        self.assertContains(res, exh.title)

    def test_exhibition_artists(self):
        """
        There's a list of exhibition artists.
        """
        exh = create_exhibition("13 Primes")
        exh.artist_set.create(display_name="Helen Frankenthaler", token="bar")
        exh.artist_set.create(display_name="Elaine de Kooning", token="foo")
        res = self.client.get(reverse("curator:exhibition", args=[exh.pk]))
        self.assertContains(res, "Helen Frankenthaler")
        self.assertContains(res, "Elaine de Kooning")

    def test_exhibition_displays_title_and_moma_url(self):
        """
        The JSON output includes the title and a link to the resource.
        """
        title = "13 Primes"
        url = "example.com/13-primes"
        exh = create_exhibition(title, url)
        res = self.client.get(reverse("curator:exhibition", args=[exh.pk]))
        self.assertContains(res, title)
        self.assertContains(res, url)
