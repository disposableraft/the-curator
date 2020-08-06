import json
import utils
import constants as c
import import_exhibitions
import prune_graph
import report
import export_corpus
import train_model
import fetch_labels
import similar

class Main:
    def __init__(self, version, combinations_r=5, topn=10, sg=0, workers=4, size=100, min_count=1, epochs=8):
        """
        Create or load a version, and perform operations on the data.
        
        m = Main('5.0.0')
        """
        self.version = version
        data_version = version.split('.')[0]
        self.train_dir = c.DATA.joinpath(f'train-{data_version}')
        self.version_dir = c.DATA.joinpath(f'versions/{self.version}')
        self.config_file = self.version_dir.joinpath('config.json')

        if self.version_exists():
            print(f'Loading version: {self.version}')
            self.config = self.load_config()
        else:
            print(f'Creating new version: {self.version}')
            self.combinations_r = combinations_r
            self.topn = topn
            self.sg = sg
            self.workers = workers
            self.size = size
            self.min_count = min_count
            self.epochs = epochs

            self.config = self.create_version()


    def version_exists(self):
        """
        Checks if the version exists.
        """
        if not self.train_dir.exists():
            print(f'WARNING: No training data found for {self.version}')
        if not self.config_file.exists():
            print(f'No config file found for {self.version}')
            return False
        return True

    def load_config(self):
        """
        Load the configuration file from disk.
        """
        with open(self.config_file, 'r') as f:
            data = json.loads(f.read())
        return data

    def update_config(self, updates):
        """
        Update the config dict and save it to disk.

        `updates` is an array of tuples (key, value)
        """
        for key, value in updates:
            self.config[key] = value
        # BUG config saves are not persisted?
        self.save_config()

    def create_version(self):
        """
        Create a new version, including a directory and config file.
        """
        try:
            self.version_dir.mkdir()
        except FileExistsError as err:
            print(f'{err}')
            if not self.version_dir.exists():
                FileExistsError
        config = {
            "version": self.version,
            "version_dir": str(self.version_dir),
            "train_dir": str(self.train_dir),
            'topn': self.topn,
            "combinations_r": self.combinations_r,
            "sg": self.sg,
            "workers": self.workers,
            "size": self.size,
            "min_count": self.min_count,
            "epochs": self.epochs
            }
        with open(self.config_file, 'w') as f:
            f.write(json.dumps(config))
        return config

    def save_config(self):
        """
        Write the config file to disk.
        """
        with open(self.config_file, 'w') as f:
            f.write(json.dumps(self.config))

    def import_exhibitions(self):
        """
        Import exhibitions and artists.
        """
        import_exhibitions.run(self.config)
    
    def prune_graph(self):
        """
        Delete notes that have too few or too many degrees.
        """
        prune_graph.run(self.config)

    def export_corpus(self):
        """
        Write a corpus from exhibition data.
        """
        export_corpus.run(self.config)

    def train_model(self):
        """
        Train a model with exhibition data.
        """
        train_model.run(self.config)

    def fetch_labels(self):
        """
        Query Wikidata for movement names.
        """
        fetch_labels.run(self.config)

    def apply_similars(self):
        """
        For all artists in the vocabulary and in the graph, query
        the model for the top 10 most similar artists and apply
        their similarity scores and tokens to `<Artist>.similar`.
        """
        similar.run(self.config)

    def report(self):
        """
        Aggregate stats into a JSON doc, draw networks of similar
        artists within the same category, and draw graphs of the
        error rates.
        """
        report.run(self.config)

