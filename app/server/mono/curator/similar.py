import os
import gensim
from django.conf import settings


class Similar:
    def get_ten(self, token):
        model_path = os.path.join(
            settings.BASE_DIR, "../../../data/models/moma-combos.model"
        )
        model = gensim.models.Word2Vec.load(model_path)
        similar = model.wv.most_similar(token, topn=10)
        return [token for token, _score in similar]

    def get_neighbors(self, token):
        "Get similar artists, then, for each, get their similar artists."
        data = {"token": token, "similar": []}
        for t in self.get_ten(token):
            data["similar"].append(
                {"token": t, "similar": [{"token": a} for a in self.get_ten(t)]}
            )
        return data
