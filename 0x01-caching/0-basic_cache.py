#!/usr/bin/python3
""" BasicCache module"""
from base_caching import BaseCaching



class BasicCache(BaseCaching):
    """ BasicCache defines:"""
    def put(self, key, item):
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        return self.cache_data.get(key, None)
