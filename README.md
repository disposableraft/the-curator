# The Curator

## Blog Posts

- https://lancewakeling.net/blog/2020-07-04-the-curator/
- https://lancewakeling.net/blog/2020-07-16-the-curator-2/
- https://lancewakeling.net/blog/2020-08-02-the-curator-3/


## Current Results

    version  (^) error rate   epochs  size  sg  labeled_artists topn
    ---------------------------------------------------------------
    1.8.2    0.7311694547944  10      100   1   415             2
    1.9.2    0.7573232532431  8       100   0   415             2
    1.8.1    0.7773750646133  10      100   1   415             5
    1.9.1    0.7908791627494  8       100   0   415             5
    1.9      0.8015390856248  8       100   0   415             10
    1.6      0.8028021296547  5       100   0   415             10
    1.7      0.8037271207213  5       100   1   415             10
    1.5      0.8049702039073  6       50    1   415             10
    1.8      0.8080196009939  10      100   1   415             10
    1.4      0.8115719523557  6       50    0   415             10
    1.2      0.8173910299259  3       50    1   415             10
    1.3      0.8177789513482  3       50    0   415             10
    1.1      0.8287832172081  1       50    0   415             10
    1.0      0.8334238260025  1       50    1   415             10
    1.10     0.8458323245597  1       10    0   415             10


## Versioning

`<dataset>.<iteration>.<variation>`

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