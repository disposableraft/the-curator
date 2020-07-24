import os
import gensim, logging
from smart_open import open
import utils
import constants as c

"""
CONFIGS
"""
model_name = '20200721-skipgram.word2vec'

# TODO: Add params to model
params = {
    'sg': 1,
    'workers': 3,
    'size': 100,
    'min_count': 1,
    'epochs': 5
}

"""
/CONFIGS
"""

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class Sentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname), 'r'):
                yield line.split()

sentences = Sentences(c.TRAIN)

model = gensim.models.Word2Vec(
        sentences, 
        min_count=params['min_count'], 
        workers=params['workers'], 
        sg=params['sg'],
        iter=params['epochs'],
        window=5
    )

model.save(str(c.MODELS.joinpath(model_name)))

# This would be cooler as json
utils.write(c.MODELS.joinpath(f'{model_name}-notes'), params)
