import os
import json
import gensim, logging
from smart_open import open
import utils
import constants as c

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class Sentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname), 'r'):
                yield line.split()

params = c.config['params']

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

training_notes = {
    'total_train_time': model.total_train_time,
    'epochs': model.epochs,
    'size': model.vector_size,
    'sg': model.sg,
    'workers': model.workers,
    'window': model.window,
    'wv': {
        'vocab_length': len(model.wv.vocab),
    }
}

with open(c.CURRENT.joinpath('training-notes.json'), 'w') as f:
    f.write(json.dumps(training_notes))
