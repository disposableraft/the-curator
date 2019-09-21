import csv

from django.core.management.base import BaseCommand, CommandError
from curator.models import Artist, Exhibition


class Command(BaseCommand):
    help='Import Artists and Exhibitions from a CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str)

    def handle(self, *args, **options):
        # Read the CSV file
        path = options['csv_path']
        with open(path) as f:
            reader = csv.DictReader(f)
            # For each row find or create the exhibition.
            # Then find or create the artist
            for row in reader:
                exh = create_exhibition(row)
                artist = create_artist(row, exh)
                self.stdout.write(f"{row}")


"""
An artist can belong to multiple exhibitions.
Some artists are groups and don't have first and last names,
in which case they only have a display name
"""
def create_exhibition(row):
    if row['ExhibitionID'] == '':
        id = 0
    else:
        id = row['ExhibitionID']
    
    exh, _ = Exhibition.objects.get_or_create(
        title=row['ExhibitionTitle'],
        defaults={
            'moma_id': id,
            'moma_number': row['ExhibitionNumber'],
            'moma_url': row['ExhibitionURL'],
        }
    )
    return exh

def create_artist(row, exhibition):
    # Get or create the artist.
    if row['token'] == '':
        return
    artist, _ = Artist.objects.get_or_create(
        display_name=row['DisplayName'],
        defaults={
            'exhibition': exhibition,
            'first_name': row['FirstName'],
            'last_name': row['LastName'],
            'middle_name': row['MiddleName'],
            'moma_url': row['ConstituentURL'],
            'suffix': row['Suffix'],
            'token': row['token'],
        },
    )
    return artist