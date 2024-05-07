#!/usr/bin/python3
""" 3-lru_cache.py """
from base_caching import BaseCaching
from collections import OrderedDict



class LRUCache(BaseCaching):
    """LRU caching system"""
    def __init__(self):
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        if key is not None and item is not None:
            if key in self.cache_data:
                del self.cache_data[key]
            self.cache_data[key] = item
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                discarded = next(iter(self.cache_data))
                del self.cache_data[discarded]
                print("DISCARD:", discarded)

    def get(self, key):
        if key is not None and key in self.cache_data:
            self.cache_data.move_to_end(key)
        return self.cache_data.get(key, None)
