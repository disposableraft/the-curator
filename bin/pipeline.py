from version import Version
from import_exhibitions import ImportExhibitions
from prune_graph import Prune1, Prune2
from fetch_labels import LabelArtists
from export_corpus import ExportCorpus
from train_model import TrainModel
from similar import ApplySimilar
from report import Report

class Pipeline:
    """
    Create a new or load an existing pipeling.

    See Version for kwargs.

    Examples:

    Create a new pipeline.

    ```
    p = Pipeline(<version_id>)
    ```
    
    Execute the current state and then update position to next state.
    
    ```
    p.proceed()
    ```

    States:

    Each state implements a `proceed` method, which must call 
    `pipeline.update()`. For example:

    ```
    class Label:
        def __init__(self, pipeline):
            self.pipeline = pipeline

        def proceed(self):
            # Do stuff
            self.pipeline.update()
    ```
    """
    def __init__(self, version_id, **kwargs):
        self.version = Version(self, version_id, **kwargs)
        self.states = self.load_states()

    def get_pos(self):
        return self.version.config['pos']

    def load_states(self):
        states = self.version.config['states']
        return [eval(s)(self) for s in states]

    def get_state(self, offset=0):
        return self.states[self.get_pos() + offset]

    def proceed(self):
        try:
            self.states[self.get_pos()].proceed()
        except IndexError:
            print('The End')

    def update(self):
        self.version.update_config(('pos', self.get_pos() + 1))
        print(f'Updated state to {self.get_state()}')
