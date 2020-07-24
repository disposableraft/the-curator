import os
import pickle
import utils
from scipy import stats
import matplotlib.pyplot as plt
import constants as c
from draw_category_similars import DrawCategorySimilars

"""
CONFIGS
"""
report_dir = c.DATA.joinpath('report-02')
title = 'Report 01 for 20200721-skipgram.word2vec'
model_name = '20200721-skipgram.word2vec'
dataset = 'train-01'
# TODO possibly look for this dir and create if necessary
"""
/CONFIGS
"""

# Yolo
try:
    os.mkdir(report_dir)
except FileExistsError:
    print(f'Directory exists: {report_dir}')

"""
The graph and the model
"""

# Assumes current graph file
graph = utils.load_graph()
types = graph.get_nodes()
categories = types['Category']
exhibitions = types['Exhibition']
artists = types['Artist']

# Graph name
graph_path = os.readlink(c.CURRENT)
graph_name = graph_path.split('/')[-1]

# The model
with open(c.MODELS.joinpath(f'{model_name}-notes'), 'rb') as f:
    model_notes = pickle.load(f)

# Labeled and Unlabeled
labeled_artists = set()
for c in categories.values():
    for m in c.edges:
        labeled_artists.add(m)
artists_degree_gt_1 = set([a.id for a in artists.values() if a.degrees > 2])
unlabeled_artists = artists_degree_gt_1 ^ labeled_artists

# Error rates

def get_labeled_nodes(cat):
    labeled = set()
    for c in cat:
        for m in c.edges:
            labeled.add(m)
    return labeled

def mean(s):
    return sum([x for x in s]) / len(s)

def diff_sq(s):
    return [(x - mean(s))**2 for x in s]

def variance(s):
    return sum(diff_sq(s)) / len(s)

def score_category(graph, cat, all_labeled_nodes):
    # Score is misses / (hits + misses)
    scores = []
    for m in cat.edges:
        A = graph[m]
        hits = []
        misses = []
        for token, score in A.similar:
            # Hits: token is in cat.edges
            if token in cat.edges:
                hits.append(score)
            # Misses: token is labeled but not as this category
            if token in all_labeled_nodes and token not in cat.edges:
                misses.append(score)
        if len(misses) + len(hits) == 0:
            # Return 1 for a full on error
            # score = 1
            continue
        else:
            score = len(misses) / (len(hits) + len(misses))
            scores.append(score)

    if len(scores) == 0:
        return None

    return {
        'cat': cat.id,
        'degrees': cat.degrees,
        'mean': mean(scores),
        'variance': variance(scores),
        'scores': scores,
        'total_hits_misses': len(hits) + len(misses)
    }

def report_error_rates(lines):
    output = str()
    output += f'{"Category":<15s} {"Mean":>14s} {"Variance":>14s} {"N":>3s}\n'
    output += '---------------------------------------------------\n'
    for line in lines:
        output += f"{line['cat']:<25s} {line['mean']:<10f} {line['variance']:<10f} {len(line['scores']):<10d}\n"
    return output

# Error rates per category
labeled_nodes = get_labeled_nodes(categories.values())
err_by_category = []

for category in categories.values():
    if category.degrees > 1:
        score = score_category(graph, category, labeled_nodes)
        if score:
            err_by_category.append(score)

# Error rates total
all_scores = []

for category in categories.values():
    if category.degrees > 1:
        cat_score = score_category(graph, category, labeled_nodes)
        if cat_score:
            for x in cat_score['scores']:
                all_scores.append(x)

err_total = {
    'cat': 'all',
    'mean': mean(all_scores),
    'variance': variance(all_scores),
    'scores': all_scores
#     Add hits and misses and cat degrees to reports?
}

# Error Rate Histogram
plt.title('Error rate distribution')
plt.hist(all_scores, cumulative=False)
plt.savefig(report_dir.joinpath('./error-distribution.png'))
plt.close()

# Error rate distribution
corr_scatter_name = 'scatter-err-per-cat.png'
corr_scatter = report_dir.joinpath(corr_scatter_name)

filtered_cat_scores = [x for x in err_by_category if x['mean'] < 1]
corr_X = [s['mean'] for s in filtered_cat_scores]
corr_Y = [len(s['scores']) for s in filtered_cat_scores]

plt.title('Mean Error per Category')
plt.scatter(corr_X, corr_Y, alpha=0.2)
plt.savefig(corr_scatter)
plt.close()

lev_mode = 'median'
lev_statistic, lev_pvalue = stats.levene(corr_X, corr_Y, center=lev_mode)
lr_slope, lr_intercept, lr_rvalue, lr_pvalue, lr_stderr = stats.linregress(corr_X, corr_Y)

# Category Graphs
category_graphs = str()
for x in err_by_category:
    if len(x['scores']) > 9:
        image_name = f"{x['cat'].replace(' ', '')}.png"
        image_path = report_dir.joinpath(image_name)
        grapher = DrawCategorySimilars(graph, x['cat'], image_path)
        grapher.run()
        category_graphs += (f'![](./{image_name})\n\n')


"""
------------
THE TEMPLATE
------------
"""
markdown = f"""

# {title}

### Data: {dataset}

### Graph: {graph_name}

- edges: {graph.count_edges()}
- vertices: {graph.count_nodes()}
- density: {graph.density()}
- exhibition: {len(exhibitions)}
- category: {len(categories)}
- artist: {len(artists)}
- edges between artist nodes: TK?
- unlabeled: {len(unlabeled_artists)}
- labeled: {len(labeled_artists)}
- percent of labeled artists (with degrees > 2): {len(labeled_artists) / (len(unlabeled_artists) + len(labeled_artists))}

### Model: {model_name}

Params:

- sg: {model_notes['sg']}
- workers: {model_notes['workers']}
- size: {model_notes['size']}
- min_count: {model_notes['min_count']}
- epochs: {model_notes['epochs']}

## Error Rates

### Total

```txt
{report_error_rates([err_total])}
```

### By category (where category.degrees > N):

```txt
{report_error_rates([x for x in err_by_category if len(x['scores']) > 9])}
```

## Error Rate Distribution

![all scores](./error-distribution.png)

## Correlation between category error rate and category.degrees

![correlation scatter plot](./{corr_scatter_name})

## Regressions Results​

### Levene Test

- mode: {lev_mode}
- stat: {lev_statistic}
- p-value: {lev_pvalue}

### Linear Regression

- slope: {lr_slope}
- intercept: {lr_intercept}
- r-value: {lr_rvalue}
- p-value: {lr_pvalue}
- std error: {lr_stderr}

### Category Networks

(To be included, a category must have > N members.)

{category_graphs}

"""

# And, finally!
with open(report_dir.joinpath('report.md'), 'w') as f:
    f.write(markdown)