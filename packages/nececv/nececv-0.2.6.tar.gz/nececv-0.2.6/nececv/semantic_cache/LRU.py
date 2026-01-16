from .cache import SemanticCache

class LRUSemanticCache(SemanticCache):
    def __init__(self, max_ram_mb=512, threshold=0.85):
        super().__init__(max_ram_mb, threshold)
        self.clock = 0

    def touch(self, idx):
        emb, val, meta = self.items[idx]
        meta["last"] = self.clock
        self.clock += 1
        self.items[idx] = (emb, val, meta)

    def evict_one(self):
        self.items.sort(key=lambda x: x[2]["last"])
        emb, val, meta = self.items.pop(0)
        self.used_ram -= self._item_size(emb, val)

    def insert(self, embedding, value):
        size = self._item_size(embedding, value)
        self._evict_until_fit(size)

        self.items.append((embedding, value, {"last": self.clock}))
        self.used_ram += size
        self.clock += 1
