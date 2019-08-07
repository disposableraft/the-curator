# The Curator

The curator is a word2vec model trained with exhibition data from MoMA.

Word2vec can describe similarities between terms using a measure of distance, which is their cosine similarity. Word2vec can also describe analogies between terms, with the common example being `king - man + woman` resulting in `queen`. Or, `paris + germany - france` resulting in `berlin`.

This implementation of word2vec is experimental in the way it treats terms. Usually the training corpus is comprised of natural language, such as Wikipedia articles, books, essays, chat logs, emails, etc. For each context window of five words, say "The fish went back home," word2vec (using the continuous bag of words mode) assigns numeric values to each word in the set. Each word in the corpus is represented as a size 100 vector. So according to continuous bag of words, "home went fish the back" is the same sentence as "the fish went back home."

For each exhibition there is a set of n artists, which comprise the exhibition. This implementation assumes that the relationships between artists in an exhibition is significant in the same way a word in an NLP corpus is significant based on its context. But it differs in the sense that the order of artists does not count for anything, whereas in an NLP corpus, this proximity does matter.

Given a show of 6 artists, each name must be associated equally with all the others. Assume [a, b, c, d, e, f] is a size six exhibition and therefore one component larger than the context window of five words. Using python's `itertools.combinations` the dataset was recompiled such that each artist in an exhibition appeared equally with all artists in that exhibition. (For computational resources, only shows with < 25 artists were used.)

```python

>>> from  itertools import combinations as combos

>>> a = ['a', 'b', 'c', 'd', 'e', 'f']

>>> list(combos(a, 5))

Out:
[('a', 'b', 'c', 'd', 'e'),
 ('a', 'b', 'c', 'd', 'f'),
 ('a', 'b', 'c', 'e', 'f'),
 ('a', 'b', 'd', 'e', 'f'),
 ('a', 'c', 'd', 'e', 'f'),
 ('b', 'c', 'd', 'e', 'f')]

```

This yields surprising results when looking at the similarities between artists. For instance, John Cage is in seven exhibitions. Out of those seven shows, three artists appeared four times: Robert Morris, Sol LeWitt, and William T. Wiley. Because of this one might assume those four are closer to Cage than others but they are not. The closest in similarity according to the model is Art & Language! Out of these four, Wiley has the closest similarity (~0.5). But Wiley falls in place 18 when looking at the 20 most similar artists. Moreover, before Wiley, falling at place 14 is Kazuko, who does not share even one exhibition with Cage. (Leon Polk Smith, at place 20 from Cage, also does not share an exhibition.)

