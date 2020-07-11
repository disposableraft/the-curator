from pathlib import Path

USER_PATH = Path('~/').expanduser()

MOMA_DATA = USER_PATH.joinpath('data1/moma')
MOMA_EXHIBITIONS_CSV = MOMA_DATA.joinpath('exhibitions/MoMAExhibitions1929to1989.csv')

PROJECT_PATH = USER_PATH.joinpath('writing1/projects/the-curator')
PROJECT_BIN = PROJECT_PATH.joinpath('bin')
PROJECT_DATA = PROJECT_PATH.joinpath('data')
PROJECT_DATA_IMAGES = PROJECT_PATH.joinpath('images')
PROJECT_DATA_MODELS = PROJECT_DATA.joinpath('models')
PROJECT_DATA_PICKLES = PROJECT_DATA.joinpath('pickles')