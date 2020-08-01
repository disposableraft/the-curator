import os
import json
import gensim, logging
from smart_open import open
import utils

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class Sentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname), 'r'):
                yield line.split()

def run(config):
    sentences = Sentences(config['train_dir'])
    model = gensim.models.Word2Vec(
            sentences,
            min_count=config['min_count'],
            workers=config['workers'],
            sg=config['sg'],
            iter=config['epochs'],
            window=5,
            size=config['size']
        )
    model_path = os.path.join(config['version_dir'], 'word2vec.pickle')
    model.save(model_path)
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

    with open(os.path.join(config['version_dir'], 'training-notes.json'), 'w') as f:
        f.write(json.dumps(training_notes))
