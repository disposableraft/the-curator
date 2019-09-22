import os
from django.conf import settings
from io import StringIO
from django.core.management import call_command
from django.test import TestCase

class ImportTest(TestCase):
    def test_command_output(self):
        out = StringIO()
        csv = os.path.join(settings.BASE_DIR, 'curator/tests/import_test.csv') 
        call_command('import', csv, stdout=out)
        self.assertIn('Imported 3 Exhibitions and 4 Artists', out.getvalue())