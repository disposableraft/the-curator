"""word2vec on artist names in exhibitions"""

import word2vec


# Train the model
word2vec.word2vec('artist_combinations_output.txt', 'word2vec_output.bin', size=100, verbose=True)


# Generates the clusters file
word2vec.word2clusters('word2vec_output.bin', 'word2vec_output_clusters.txt',
                       100, verbose=True)
