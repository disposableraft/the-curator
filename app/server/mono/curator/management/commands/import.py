import csv

from django.core.management.base import BaseCommand, CommandError
from curator.models import Artist, Exhibition


class Command(BaseCommand):
    help='Import Artists and Exhibitions from a CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str)
        parser.add_argument(
            '--debug',
            # Treat the presence of this flag as True
            action='store_true',
            help="Print each row of the CSV as it's input."
        )

    def handle(self, *args, **options):
        path = options['csv_path']
        exh_count = 0
        artists_count = 0
        with open(path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                exh, exh_created = create_exhibition(row)
                _, artist_created = create_artist(row, exh)
                if exh_created:
                    exh_count += 1
                if artist_created:
                    artists_count += 1
                if options['debug']:
                    self.stdout.write(f"{row}")
        self.stdout.write(f"Imported {exh_count} Exhibitions and {artists_count} Artists'")


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
    
    exh, created = Exhibition.objects.get_or_create(
        title=row['ExhibitionTitle'],
        defaults={
            'moma_id': id,
            'moma_number': row['ExhibitionNumber'],
            'moma_url': row['ExhibitionURL'],
        }
    )
    return exh, created

def create_artist(row, exhibition):
    artist, created = Artist.objects.get_or_create(
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
    return artist, created