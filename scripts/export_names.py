import sys
sys.path.append('/Users/khanda/writing1/projects/the-curator/bin')

import json
from gensim.models import Word2Vec
import utils
from pipeline import Pipeline

names_map_file = '/Users/khanda/writing1/projects/the-curator/data/versions/2.2.0/names_map.json'
names_file = '/Users/khanda/writing1/projects/the-curator/data/versions/2.2.0/names.json'

pipe = Pipeline('2.2.0')

model = Word2Vec.load('/Users/khanda/writing1/projects/the-curator/data/versions/2.2.0/word2vec.pickle')

tokens = [x for x in model.wv.vocab]

graph = utils.load_graph('similar-labeled-import.pickle', pipe.version.config)

tokens_map = [{graph[t].name: t} for t in tokens]

with open(names_map_file, 'w', encoding='utf8') as f:
  f.write(json.dumps(tokens_map))

names = [graph[t].name for t in tokens]

with open(names_file, 'w', encoding='utf8') as f:
  f.write(json.dumps(names))