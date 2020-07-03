from pathlib import Path
from gensim.models import Word2Vec
from artist import Artist

"""
Abstract Expressionism
{toby, alice, juilia, cassandra, enid}
"""

class Word2VecModel:
    def __init__(self, path):
        self.path = Path(path)
        self.vocab = None
        self.model = self.load()


    def in_vocab(self, token):
        return token in self.vocab


    def load(self):
        print('loading model')
        model = Word2Vec.load(str(self.path))
        self.vocab = list(model.wv.vocab)
        return model


    def get_vocab(self):
        return self.model.wv.vocab


    def topn(self, token, topn=10):
        return self.model.wv.most_similar(token, topn=topn)

class SimilarArtist(Artist):
    def __init__(self, token, rank=None):
        # Similar artists coming from the model don't have names, only tokens
        self.name = None
        self.token = token
        self.rank = rank


class Category(object):
    def __init__(self, name, artists=[]):
        self.name = name
        self.artists = dict()
        self.create_artists(artists)


    def create_artists(self, artists):
        for y in artists:
            self.add(y)


    def add(self, artist):
        x = Artist(artist)
        self.artists[x.token] = x
        return self.artists


    def list_names(self):
        return [x.name for x in self.artists]


    def list_tokens(self):
        return [x.token for x in self.artists]


    def remove(self, artist):
        del self.artists[artist]
        return self.artists


    def __len__(self):
        return len(self.artists)


    def is_member(self, artist):
        word = None
        if isinstance(artist, Artist):
            word = artist.token
        else:
            word = artist
        return word in self.artists


    def load_similar(self, model, topn=10):
        """
        For all artists in category, query model for topn similar artists.
        Keeps similar artists who are in-category.
        Saves a rank of 0 to topn.
        Returns category artists.
        """
        if not isinstance(model, Word2VecModel):
            raise ValueError(f'something happened loading the model: {model}')
        
        for A_i in self.artists:
            rank = 0
            similar_tokens = model.topn(A_i, topn)
            for s_token, _matrix in similar_tokens:
                # This check for membership  won't be necessary when the 
                # classifications flow from the model artists.
                if self.is_member(s_token):
                    self.artists[A_i].add_similar(s_token, rank)
                rank += 1
        return self.artists
            


    
    



    

