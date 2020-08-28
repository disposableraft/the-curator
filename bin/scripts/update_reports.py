import main
from pprint import pprint

versions = ['1.0', '1.1', '1.10', '1.2', '1.3', '1.4', '1.5', '1.6', '1.7', '1.8', '1.8.1', '1.8.2', '1.9', '1.9.1', '1.9.2', '2.0.0', '3.0.0', '3.1.0']

for v in versions:
    m = main.Main(v)
    model = main.similar.Word2Vec.load(f'{m.config["version_dir"]}/word2vec.pickle')
    main.train_model.export_training_notes(m.config, model)
    m.report()
