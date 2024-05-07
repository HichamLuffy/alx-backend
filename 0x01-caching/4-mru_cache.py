#!/usr/bin/python3
""" 4-mru_cache.py """
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """MRU caching system"""
    def __init__(self):
        """Initiliaze"""
        super().__init__()
        self.keys = []

    def put(self, key, item):
        """ Add an item in the cache"""
        if key is not None and item is not None:
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                removed = self.keys.pop()
                self.cache_data.pop(removed)
                print("DISCARD: {}".format(removed))

            self.cache_data[key] = item
            self.keys.append(key)

    def get(self, key):
        """ Get an item by key"""
        if key is not None and key in self.cache_data:
            self.keys.remove(key)
            self.keys.append(key)
        return self.cache_data.get(key, None)
