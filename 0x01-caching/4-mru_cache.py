#!/usr/bin/python3
""" 4-mru_cache.py """
from base_caching import BaseCaching



class MRUCache(BaseCaching):
    """MRU caching system"""
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
                discarded = self.keys.pop(-1)
                del self.cache_data[discarded]
                print("DISCARD:", discarded)

    def get(self, key):
        if key is not None and key in self.cache_data:
            self.keys.remove(key)
            self.keys.append(key)
        return self.cache_data.get(key, None)
