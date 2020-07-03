from gensim.parsing.preprocessing import preprocess_string

class Artist(object):
    def __init__(self, name):
        self.name = name
        self.token = self.tokenize()
        self.similar = dict()
    
    def tokenize(self):
        token = "".join(preprocess_string(self.name))
        return token
    
    def add_similar(self, token, rank):
        self.similar['token'] = SimilarArtist(token, rank)
