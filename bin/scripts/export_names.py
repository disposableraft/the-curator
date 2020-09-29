import sys
sys.path.append('/Users/khanda/writing1/projects/the-curator/bin')

import json
from gensim.models import Word2Vec
import utils
from pipeline import Pipeline

version = '1.8.2'

top_12_map_file = f'/Users/khanda/writing1/projects/the-curator/data/versions/{version}/top_12_map.json'
names_file = f'/Users/khanda/writing1/projects/the-curator/data/versions/{version}/names.json'

model = Word2Vec.load(f'/Users/khanda/writing1/projects/the-curator/data/versions/{version}/word2vec.pickle')
tokens = [x for x in model.wv.vocab]

pipe = Pipeline(version)
graph = utils.load_graph('similar-labeled-import.pickle', pipe.version.config)

# Export a map of top 12 similar artists for each artist.
# { "Jill Boo": ["Jane Fan", "Bill Pen" ...]}
top_12_map = {}

for token in tokens:
  similar_tokens = model.wv.most_similar(token, topn=12)
  similar_names = [graph[t].name for (t, _) in similar_tokens]
  top_12_map[graph[token].name] = similar_names

with open(top_12_map_file, 'w', encoding='utf8') as f:
  f.write(json.dumps(top_12_map))

# Export a list of names.
names = [graph[t].name for t in tokens]
with open(names_file, 'w', encoding='utf8') as f:
  f.write(json.dumps(names))