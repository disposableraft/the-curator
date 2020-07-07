# Notes for The Curator

## To-do

### Graphing 

- Update in-group mean to be a measurement of error. For instance now if 4/10 $A_s$ are in-category the in-group mean is .4. But it would be better to measure the error of 0.6.
- In the graph data, add weighted edges — either in the form of a value or the weight of line, or both. 

### Data Collection

- Some categories might be derived from the exhibition titles themselves
- For categories, only use union of C and M, such that all C are a subset of M.

Oh, wow. This query took forever! Show the movements for Q235281, aka Helen Frankenthaler.

```sparkl
SELECT ?movement ?movementLabel WHERE {
   wd:Q235281 wdt:P135 ?movement.
   SERVICE wikibase:label {
     bd:serviceParam wikibase:language "en" .
   }
}
```

### Data Transformation

- Transform diacritics
- Adding the Tate data to the model would be a good opportunity to refactor that part of the codebase, which is messy.

* * * 

## Definitions

$A_n$ = *An artist, usually synonymous with $A_{cm}$*

$A_s$ = *Set of artists predicted by the model to be similar to a given artist*

$A_M$ = *All artists in the model*

$A_C$ = *All artists in a category*

$A_{CM}$ = *All artists in both category and model*

*Similar*: Artist similarity is a function of the model. The cosine similarity between two vectors is the distance to which they are similar or dissimilar. 

## On an Assumption Concerning CBOW and Skip-Gram

In the first blog post on the curator, I said that the context window would split a 10-word sequence into two groups. But this presents a problem. What about sentences that are not equally divided by ten? 

What I think really might be going on, is the context window slides one word forward each iteration. $I_1 = {0,1,2,3,4}$ then $I_2 = {1,2,3,4,5}$.

Update: This assumption is correct. I pulled the cbow function from the [python implementation](./notebooks/word2vec-cbow.ipynb) to inspect the iteration across sentences. My original intuition that the last artist in a show would not be associated with the first artist was correct. *But* this approach of running all combinations might be overkill. For instance, combinations of 5 might be overkill, while 5+n would be ideal.

## More Descriptive Edges 

One way the graph of similar artists could be more descriptive would be to add weights to the edges. Currently many edges are undirected: arrows point in both directions. But a weight could be derived from the distance in the cosine similarity between two artists. For instance, two artists: 

```python
A['similar'] = {x (0.9), y (0.8), B (0.7)} 

B['similar'] = {A (0.9), p (0.5), q (0.4)}
```

`A -> B` would have a lighter edge and `B -> A` would have a heavier edge because the rank of their order.

**Calculating the Edge Weight**

**UPDATE:** The below equation for measuring rank is based on a scale of one to ten, which is basically an ordinal scale, because the distances between intervals is inconsistent. The top result of one node could have a cosim of 0.0003, while the top result of another node could have a cosim of 0.9. Therefore, it would be more accurate and descriptive to use a ratio scale based on cosim. (See journal pages 44, 46-7)

$$ weight = \frac{N - i}{N} $$

![Error Variables](2020-06-30-error-variables.png)

```python

import matplotlib.pyplot as plt

# in order for the last element to be > 0 index must start at 0.
edge_indices = list(range(10))
n = len(edge_indices)

weights = [(n - i) / n for i in edge_indices]
# [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]

plt.plot(weights)
plt.show()

```

## The In-Group Mean vs. In-Group Error

The so-called `in-group mean` gives a measurement of possible error. Nodes outside of the in-group mean could be 1) unclassified or 2) classified as part of another art historical movement. 

Currently, the mean is calculated by `similar/top_n_artists`. The median value at the moment is 0.4, where four out of ten similar arists are both in the model and in the category. Looked at from the opposite direction six out of ten artists are possible errors.

Knowing who those artists are by increasing the classification categories could diminish this error rate. This gray zone seems to be quite interesting. 

Actionable items include:
 
- Increasing classification categories 
- Look at multiple categories at once (now I'm only looking at one, Abstract Expressionism)