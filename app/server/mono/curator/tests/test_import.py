import os
from django.conf import settings
from io import StringIO
from django.core.management import call_command
from django.test import TestCase
from curator.models import Exhibition, Artist


def import_command(csv):
    out = StringIO()
    call_command('import', csv, stdout=out)
    return out


class ImportTest(TestCase):
    csv = os.path.join(settings.BASE_DIR, 'curator/tests/import_test.csv')

    def test_command_output(self):
        out = import_command(self.csv)
        self.assertIn('Imported 5 Exhibitions and 5 Artists', out.getvalue())

    def test_command_creates_5_artists(self):
        out = import_command(self.csv)
        count = Artist.objects.count()
        self.assertEqual(5, count)

    def test_command_creates_5_exhibitions(self):
        out = import_command(self.csv)
        count = Exhibition.objects.count()
        self.assertEqual(5, count)

    def test_command_links_artists_to_exhibitions(self):
        out = import_command(self.csv)
        a = Exhibition.objects.get(title='Exhibition A')
        b = Exhibition.objects.get(title='Exhibition B')
        c = Exhibition.objects.get(title='Exhibition C')
        d = Exhibition.objects.get(title='Exhibition D')
        e = Exhibition.objects.get(title='Exhibition E')
        self.assertEqual(3, a.artist_set.count())
        self.assertEqual(2, b.artist_set.count())
        self.assertEqual(3, c.artist_set.count())
        self.assertEqual(1, d.artist_set.count())
        self.assertEqual(1, e.artist_set.count())
