from pathlib import Path
import analysis

base_path = Path('~/writing1/projects/the-curator/').expanduser()
# category_paths = base_path.joinpath('data/historical-categories/').glob('*.txt')
category = base_path.joinpath('data/historical-categories/abstract-expressionism.txt')
model_path = base_path.joinpath('data/models/moma-combos.model')

# category_name
# list of artists

artists = []
category_name = None

with open(category, mode='r', encoding='utf-8') as file:
    category_name = file.name.split('/')[-1].split('.')[0]
    lines = file.readlines()
    for line in lines:
        artists.append(line.strip())

abex = analysis.Category(category_name, artists)

model = analysis.Word2VecModel(model_path)

artists = abex.load_similar(model, topn=10)