import os
import gensim
from django.conf import settings

class Similar():
    def get_ten(self, token):
        model_path = os.path.join(settings.BASE_DIR, '../../../data/models/moma-combos.model')
        model = gensim.models.Word2Vec.load(model_path)
        similar = model.wv.most_similar(token, topn=10)
        return [token for token, _score in similar]