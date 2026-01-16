class SemanticRouter:
    def __init__(self, cache, next_fn):
        self.cache = cache
        self.next_fn = next_fn

    def query(self, text, embedding):
        idx, item = self.cache.find(embedding)

        if item:
            self.cache.touch(idx)
            return item[1], "cache"

        result = self.next_fn(text)
        self.cache.insert(embedding, result)
        return result, "miss"
