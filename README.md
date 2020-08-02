# The Curator

## Blog Posts

- https://lancewakeling.net/blog/2020-07-04-the-curator/
- https://lancewakeling.net/blog/2020-07-16-the-curator-2/
- https://lancewakeling.net/blog/2020-08-02-the-curator-3/


## Usage

```python
"""
Initialize a version.

Arguments:
    - combinations_r:  the length of each combination. See `itertools.combinations` and `Main.export_corpus`.
    - topn: the number of similar artists. See `model.wv.most_similar`.
    - sg: (0|1). 0 for CBOW. 1 for Skip-Gram. See `Word2Vec`.
    - workers: training workers. See `Word2Vec`.
    - size: the size of the vector. See `Word2Vec`.
    - min_count: smallest count allowed for a term. See `Word2Vec`.
    - epochs: word2vec epochs. See `Word2Vec`.
"""
m = Main('1.0')

# Import the moma exhibition csv into a graph
m.import_moma()

# Export a corpus
m.export_corpus()

# Train word2vec on corpus
m.train_model()

# Fetch labels (art historical movements) from Wikidata
m.fetch_labels()

# Update the graph with similar artists from word2vec
m.apply_similars()

# Generate a report, which includes mean error rates
m.report()
```