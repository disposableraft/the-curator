import json
from pathlib import Path

USR = Path('~/').expanduser()
MOMA_EXHIBITIONS_CSV = USR.joinpath('data1/moma/exhibitions/MoMAExhibitions1929to1989.csv')
DOME_EXHIBITIONS_CSV = USR.joinpath('data1/dome/Exhibitions.csv')
DOME_ARTISTS_CSV = USR.joinpath('data1/dome/Artists.csv')
PROJECT = USR.joinpath('writing1/projects/the-curator')
DATA = PROJECT.joinpath('data')

MOMA_EXHIBITIONS_CSV_TEST = DATA.joinpath('testing/moma.csv')
DOME_ARTISTS_CSV_TEST = DATA.joinpath('testing/dome-artists.csv')
DOME_EXHIBITIONS_CSV_TEST = DATA.joinpath('testing/dome-exhibitions.csv')