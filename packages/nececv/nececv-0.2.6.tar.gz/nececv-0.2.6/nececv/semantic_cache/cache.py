import numpy as np
import sys

def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

class SemanticCache:
    def __init__(self, max_ram_mb=512, threshold=0.85):
        self.max_ram = max_ram_mb * 1024 * 1024
        self.threshold = threshold
        self.items = []
        self.used_ram = 0

    def _item_size(self, emb, val):
        return emb.nbytes + sys.getsizeof(val)

    def find(self, query_embedding):
        best_idx = None
        best_sim = 0

        for i, (emb, val, meta) in enumerate(self.items):
            sim = cosine(query_embedding, emb)
            if sim > best_sim:
                best_sim = sim
                best_idx = i

        if best_sim >= self.threshold:
            return best_idx, self.items[best_idx]

        return None, None

    def _evict_until_fit(self, required):
        while self.used_ram + required > self.max_ram and self.items:
            self.evict_one()

    def evict_one(self):
        raise NotImplementedError

    def insert(self, embedding, value):
        raise NotImplementedError
