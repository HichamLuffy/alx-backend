#!/usr/bin/python3
""" 1-fifo_cache.py """
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """FIFO caching system"""
    def __init__(self):
        super().__init__()
        self.keys = []

    def put(self, key, item):
        if key is not None and item is not None:
            if key not in self.cache_data:
                self.keys.append(key)
            self.cache_data[key] = item
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                discarded = self.keys.pop(0)
                del self.cache_data[discarded]
                print("DISCARD:", discarded)

    def get(self, key):
        return self.cache_data.get(key, None)
