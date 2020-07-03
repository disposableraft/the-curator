from gensim.models import Word2Vec
from gensim.parsing.preprocessing import preprocess_string
from pathlib import Path

def import_categories(paths):
    """
    Accepts an interable containing paths to files.
    It expects that the filename is the category name.
     
    {
        <file_name>: [ <artist_name> ... ]
    }
    """
    categories = {}

    for path in paths:
        with open(path, mode='r', encoding='utf-8') as file:
            # Split the file path, select the name, then split off the extension
            category_name = file.name.split('/')[-1].split('.')[0]

            data = file.readlines()

            c_name = categories.setdefault(category_name, {})
            c_name['names'] = []
            # strip the artist names and append them to categories.name
            [c_name['names'].append(d.strip()) for d in data]
    return categories


def process_names(names):
    "Join names by space and preprocess into tokens"
    # process all the names at once.
    return ["".join(preprocess_string(n)) for n in names]


def tokenize_names(categories):
    for name in categories:
        category = categories[name]
        category['tokens'] = []
        tokenized_names = process_names(category['names'])
        [category['tokens'].append(n) for n in tokenized_names]
    return categories


def print_category_relevance(C, model_tokens):
    for c_name in C:
        count = 0
        for t in C[c_name]['tokens']:
            if t in model_tokens:
                count += 1
        C[c_name]['tokens_in_model'] = count
        C[c_name]['tokens_in_category'] = len(C[c_name]['tokens'])

    ab_ex = C['ab-ex-artists']
    impressionist = C['impressionist-artists']
    conceptual = C['conceptual-artists']

    print('<category name>: <model> / <category>)')
    print(f'Ab Ex: {ab_ex["tokens_in_model"]} / {ab_ex["tokens_in_category"]}')
    print(f'Impressionist: {impressionist["tokens_in_model"]} / {impressionist["tokens_in_category"]}')
    print(f'Conceptual: {conceptual["tokens_in_model"]} / {conceptual["tokens_in_category"]}')


def graph_artists(tokens, model, top_n_similar=10):
    """
    tokens: A list of tokenized artist names from a category. 
            tokens in category must be the same as in the model.
    model:  The Word2Vec model
    
    Returns object
    
    graph {
        '<token>': {
            similar: [],
            in_category_mean: <int>,
        }
    }
    """
    graph = {}
    
    vocab = list(model.wv.vocab)
    
    for a in tokens:
        if a in vocab:
            node = graph.setdefault(a, {})
            node['similar'] = set()
            similar_a = model.wv.most_similar(a, topn=top_n_similar)
            for s_a, _ in similar_a:
                if s_a in tokens:
                    node['similar'].add(s_a)
            node['in_category_mean'] = len(node['similar']) / top_n_similar
            # Remove the node if there are no similar artists
            if node['in_category_mean'] == 0:
                graph.popitem()

    return graph


base_path = Path('~/code1/the-curator/').expanduser()
category_paths = base_path.joinpath('data/historical-categories/').glob('*.txt')
model_path = base_path.joinpath('data/models/moma-combos.model')

categories = import_categories(category_paths)
categories = tokenize_names(categories)

model = Word2Vec.load(str(model_path))
graph = graph_artists(categories['ab-ex-artists']['tokens'], model)

print(graph)

