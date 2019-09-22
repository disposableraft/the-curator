import os
from django.conf import settings
from io import StringIO
from django.core.management import call_command
from django.test import TestCase
from curator.models import Exhibition, Artist

class ImportTest(TestCase):
    csv = os.path.join(settings.BASE_DIR, 'curator/tests/import_test.csv') 
    
    def test_command_output(self):
        out = StringIO()
        call_command('import', self.csv, stdout=out)
        self.assertIn('Imported 4 Exhibitions and 5 Artists', out.getvalue())
    
    def test_command_creates_single_artist(self):
        call_command('import', self.csv)
        warhol = Exhibition.objects.get(moma_number=1510)
        self.assertEqual(1, warhol.artist_set.count())
    
    def test_command_creates_5_artists(self):
        call_command('import', self.csv)
        count = Artist.objects.count()
        self.assertEqual(5, count)
    
    def test_command_creates_4_exhibitions(self):
        call_command('import', self.csv)
        count = Exhibition.objects.count()
        self.assertEqual(4, count)
