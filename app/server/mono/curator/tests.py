import json

from django.test import TestCase
from django.urls import reverse

from .models import Artist, Exhibition

def create_exhibition(title):
    return Exhibition.objects.create(title=title)

class ExhibitionDetailViewTests(TestCase):
    def test_exhibition_json(self):
        """
        Returns a JSON object with an error field.
        """
        exh = create_exhibition("13 Foos")
        res = self.client.get(reverse('curator:exhibition', args=[exh.pk]))
        self.assertContains(res, "errors")

    def test_exhibition_title(self):
        """
        There's an exhibition title.
        """
        exh = create_exhibition("13 Foos")
        res = self.client.get(reverse('curator:exhibition', args=[exh.pk]))
        self.assertContains(res, exh.title)
    
    def test_exhibition_without_pk(self):
        """
        An exhibition without a valid ID fails.
        """
        res = self.client.get(reverse('curator:exhibition', args=[int(9e20)]))
        raw = json.loads(res.content)['errors']
        self.assertEqual(raw, "Resource does not exist.")
    
    def test_exhibition_artists(self):
        """
        There's a list of exhibition artists.
        """
        exh = create_exhibition("13 Primes")
        exh.artist_set.create(
            first_name="Helen",
            last_name="Frankenthaler",
            token="helenfranknthal",
        )
        exh.artist_set.create(
            first_name="Elaine",
            last_name="de Kooning",
            token="elaindkooning",
        )
        res = self.client.get(reverse('curator:exhibition', args=[exh.pk]))
        self.assertContains(res, "Frankenthaler")
        self.assertContains(res, "de Kooning")

