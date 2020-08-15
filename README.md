# The Curator

## Blog Posts

- [Can Word2Vec Describe Art-Historical Categories?](https://lancewakeling.net/blog/2020-07-04-the-curator/)
- [Abusing Word2Vec, Part II](https://lancewakeling.net/blog/2020-07-16-the-curator-2/)
- [Calculating Error Rates: The Curator](https://lancewakeling.net/blog/2020-08-02-the-curator-3/)


## Benchmarks

    version  ^ mean    stddev  epochs  size  sg  labeled_artists  topn
    ------------------------------------------------------------------
    1.8.2  0.731169  0.400759      10   100   1              415     2
    1.9.2  0.757323  0.381546       8   100   0              415     2
    1.8.1  0.777375  0.311037      10   100   1              415     5
    1.9.1  0.790879  0.303636       8   100   0              415     5
    2.0.0  0.793170  0.323632       4   100   0             1065     5
    3.1.0  0.797092  0.275271      10   100   0             1065     5
      1.9  0.801539  0.251177       8   100   0              415    10
      1.6  0.802802  0.246046       5   100   0              415    10
      1.7  0.803727  0.270047       5   100   1              415    10
      1.5  0.804970  0.276699       6    50   1              415    10
    3.0.0  0.805366  0.261353       4   100   0             1065     5
      1.8  0.808020  0.267684      10   100   1              415    10
      1.4  0.811572  0.245559       6    50   0              415    10
      1.2  0.817391  0.274402       3    50   1              415    10
      1.3  0.817779  0.232192       3    50   0              415    10
      1.1  0.828783  0.233289       1    50   0              415    10
      1.0  0.833424  0.258153       1    50   1              415    10
     1.10  0.845832  0.215527       1    10   0              415    10



## Versions

`<dataset>.<iteration>.<variation>`

### Dataset 1

Labeled and unlabled terms from the MoMA dataset.

### Dataset 2

Labeled and unlabled terms from the MoMA and DOME datasets.

### Dataset 3

Only labled terms from the MoMA and DOME datasets.

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