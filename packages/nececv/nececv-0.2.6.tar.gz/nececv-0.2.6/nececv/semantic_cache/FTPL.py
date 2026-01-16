import random
from .cache import SemanticCache

class FTPLSemanticCache(SemanticCache):
    def __init__(self, max_ram_mb=512, threshold=0.85, eta=0.2):
        super().__init__(max_ram_mb, threshold)
        self.eta = eta

    def touch(self, idx):
        emb, val, meta = self.items[idx]
        meta["hits"] += 1
        self.items[idx] = (emb, val, meta)

    def evict_one(self):
        scores = []
        for emb, val, meta in self.items:
            score = meta["hits"] + random.uniform(-self.eta, self.eta)
            scores.append(score)

        evict = scores.index(min(scores))
        emb, val, meta = self.items.pop(evict)
        self.used_ram -= self._item_size(emb, val)

    def insert(self, embedding, value):
        size = self._item_size(embedding, value)
        self._evict_until_fit(size)

        self.items.append((embedding, value, {"hits": 1}))
        self.used_ram += size
