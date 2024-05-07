#!/usr/bin/python3
""" 2-lifo_cache.py """
from base_caching import BaseCaching



class LIFOCache(BaseCaching):
    def __init__(self):
        super().__init__()
        self.keys = []

    def put(self, key, item):
        if key is not None and item is not None:
            self.cache_data[key] = item
            if key in self.keys:
                self.keys.remove(key)
            self.keys.append(key)
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                discarded = self.keys.pop(-2)
                del self.cache_data[discarded]
                print("DISCARD:", discarded)

    def get(self, key):
        return self.cache_data.get(key, None)
