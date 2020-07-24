from pathlib import Path

USER_PATH = Path('~/').expanduser()

MOMA_DATA = USER_PATH.joinpath('data1/moma')
MOMA_EXHIBITIONS_CSV = MOMA_DATA.joinpath('exhibitions/MoMAExhibitions1929to1989.csv')

PROJECT = USER_PATH.joinpath('writing1/projects/the-curator')
DATA = PROJECT.joinpath('data')
TRAIN = DATA.joinpath('train-01')
PROJECT_TMP = DATA.joinpath('tmp')

PROJECT_DATA_IMAGES = DATA.joinpath('images')

MODELS = DATA.joinpath('models')
PICKLES = DATA.joinpath('pickles')
VERSIONS = PICKLES.joinpath('versions')
CURRENT = PICKLES.joinpath('versions/current.pickle')

WORD2VEC = MODELS.joinpath('20200721.word2vec')