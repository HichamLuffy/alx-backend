#!/usr/bin/python3
""" 100-lfu_cache.py """
from base_caching import BaseCaching
from collections import Counter



class LFUCache(BaseCaching):
    def __init__(self):
        super().__init__()
        self.key_access_times = Counter()
        self.key_age = 0
        self.key_order = {}

    def put(self, key, item):
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS and key not in self.cache_data:
                lfu_key, _ = self.key_access_times.most_common()[-1]
                if self.key_order[lfu_key] == min(self.key_order.values()):
                    print("DISCARD:", lfu_key)
                    del self.cache_data[lfu_key]
                    del self.key_order[lfu_key]
                    del self.key_access_times[lfu_key]

            self.cache_data[key] = item
            self.key_access_times[key] += 1
            self.key_age += 1
            self.key_order[key] = self.key_age

    def get(self, key):
        if key is not None and key in self.cache_data:
            self.key_access_times[key] += 1
            self.key_age += 1
            self.key_order[key] = self.key_age
            return self.cache_data[key]
        return None
