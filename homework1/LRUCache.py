from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity: int = 10) -> None:
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: str) -> str:
        if key not in self.cache:
            return ""
        self.cache.move_to_end(key) # в конце храним самые востребуемые
        return self.cache[key]

    def set(self, key: str, value: str) -> None:
        if key in self.cache:
            self.cache[key] = value
            self.cache.move_to_end(key)
            return

        self.cache[key] = value
        if len(self.cache) == self.capacity:
            self.cache.popitem(last=False) # если кончилось место, удаляем самый невостребуемый

    def rem(self, key: str) -> None:
        if key in self.cache:
            self.cache.pop(key)
