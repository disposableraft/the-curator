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
# Create or load an existing version.
# Versions follow the format `<dataset>.<iteration>.<variation>`.
>>> pipe = Pipeline('9.0.0')

# The current state
>>> pipe.get_state()
<class 'import_exhibitions.ImportExhibitions'>

# Get the version configurations
>>> pipe.version.config
{'combinations_r': 5,
 'epochs': 5,
 'min_count': 1,
 'pos': 0,
 'sg': 1,
 'size': 100,
 'states': ['ImportExhibitions',
            'Prune1',
            'LabelArtists',
            'Prune2',
            'ExportCorpus',
            'TrainModel',
            'ApplySimilar',
            'Report'],
 'topn': 5,
 'train_dir': 'data/train-9',
 'version': '9.0.0',
 'version_dir': 'data/versions/9.0.0',
 'workers': 5}

# Update the version configurations
>>> pipe.version.update_config(
  ('workers', 6), 
  ('size', 200), 
  ('sg', 0))

# Execute the current state and proceed to the next.
>>> pipe.proceed()
```

