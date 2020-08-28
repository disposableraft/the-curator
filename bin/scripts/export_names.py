import sys
sys.path.append('/Users/khanda/writing1/projects/the-curator/bin')

import json
from gensim.models import Word2Vec
import utils
from pipeline import Pipeline

tokens_to_names_file = '/Users/khanda/writing1/projects/the-curator/data/versions/2.2.0/tokens_to_names.json'
names_to_tokens_file = '/Users/khanda/writing1/projects/the-curator/data/versions/2.2.0/names_to_tokens.json'
names_file = '/Users/khanda/writing1/projects/the-curator/data/versions/2.2.0/names.json'

model = Word2Vec.load('/Users/khanda/writing1/projects/the-curator/data/versions/2.2.0/word2vec.pickle')
tokens = [x for x in model.wv.vocab]

pipe = Pipeline('2.2.0')
graph = utils.load_graph('similar-labeled-import.pickle', pipe.version.config)

# Construct two maps: of tokens to names, and the opposite.
tokens_to_names = {t: graph[t].name for t in tokens}
with open(tokens_to_names_file, 'w', encoding='utf8') as f:
  f.write(json.dumps(tokens_to_names))

names_to_tokens = {graph[t].name: t for t in tokens}
with open(names_to_tokens_file, 'w', encoding='utf8') as f:
  f.write(json.dumps(names_to_tokens))

# Construct a list of names.
names = [graph[t].name for t in tokens]
with open(names_file, 'w', encoding='utf8') as f:
  f.write(json.dumps(names))