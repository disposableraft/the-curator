import json
from pathlib import Path

USR = Path('~/').expanduser()

MOMA_EXHIBITIONS_CSV = USR.joinpath('data1/moma/exhibitions/MoMAExhibitions1929to1989.csv')

PROJECT = USR.joinpath('writing1/projects/the-curator')
DATA = PROJECT.joinpath('data')
TRAIN = DATA.joinpath('train-01')

PROJECT_DATA_IMAGES = DATA.joinpath('images')

with open(PROJECT.joinpath('bin/config.json'), 'r') as f:
    config = json.loads(f.read())

# <train version>.<model version>
VERSION_NUMBER = config['version']

CURRENT = DATA.joinpath(f'versions/{str(VERSION_NUMBER)}')