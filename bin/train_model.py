import os
import json
import gensim, logging
from smart_open import open
import utils
import constants as c

"""
CONFIGS
"""
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

model.save(str(c.CURRENT.joinpath('word2vec.pickle')))

with open(c.CURRENT.joinpath('training-notes.json'), 'w') as f:
    f.write(json.dumps(params))
