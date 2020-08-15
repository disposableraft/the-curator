import json
import constants as c

class Version:
    def __init__(self, pipeline, version_id, topn=5, combinations_r=5, sg=1, workers=5, size=100, min_count=1, epochs=5):
        """
        Create and prepare a new version, or manage an existing one.

        Arguments:

        `combinations_r`:  the length of each combination. See `itertools.combinations` and `Main.export_corpus`.
        
        `topn`: the number of similar artists. See `model.wv.most_similar`.
        
        `sg`: (0|1). 0 for CBOW. 1 for Skip-Gram. See `Word2Vec`.
        
        `workers`: training workers. See `Word2Vec`.
        
        `size`: the size of the vector. See `Word2Vec`.
        
        `min_count`: smallest count allowed for a term. See `Word2Vec`.
        
        `epochs`: word2vec epochs. See `Word2Vec`.
        
        """
        self.config = None
        self.id = version_id
        self.train_dir = c.DATA.joinpath(f'train-{version_id.split(".")[0]}')
        self.version_dir = c.DATA.joinpath(f'versions/{self.id}')
        self.config_file = self.version_dir.joinpath('config.json')

        if not self.exists(self.train_dir):
            print(f'Creating training directory: {self.train_dir}.')
            self.create_dir(self.train_dir)

        if self.exists(self.config_file):
            print(f'Loading version: {self.id}.')
            self.config = self.load_config()
        else:
            print(f'Creating version {self.id}.')
            self.config = {
                "version": version_id,
                "states": [
                    'ImportExhibitions',
                    'Prune1',
                    'LabelArtists',
                    'Prune2',
                    'ExportCorpus',
                    'TrainModel',
                    'ApplySimilar',
                    'Report'
                    ],
                "pos": 0,
                "version_dir": str(self.version_dir),
                "train_dir": str(self.train_dir),
                'topn': topn,
                "combinations_r": combinations_r,
                "sg": sg,
                "workers": workers,
                "size": size,
                "min_count": min_count,
                "epochs": epochs,
                }
            if not self.exists(self.version_dir):
                print(f'Creating version directory: {self.version_dir}.')
                self.create_dir(self.version_dir)
            self.save_config()

    def exists(self, resource):
        if not resource.exists():
            return False
        return True

    def load_config(self):
        with open(self.config_file, 'r') as f:
            data = json.loads(f.read())
        return data

    def save_config(self):
        with open(self.config_file, 'w') as f:
            f.write(json.dumps(self.config))

    def create_dir(self, dir):
        dir.mkdir()

    def update_config(self, *args):
        """
        Update the config dict and save it to disk.

        `args` -> one or more tuples (<key>, <value>)
        """
        updates = list(args)
        for key, value in updates:
            self.config[key] = value
        self.save_config()