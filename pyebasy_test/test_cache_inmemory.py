from unittest import TestCase

from cache_inmemory import InMemoryCache
from cache_test_helpers import SomeCacheTestMixin


class TestInMemoryCache(TestCase, SomeCacheTestMixin):
    def test_some_cache(self):
        cache = InMemoryCache()
        self.populate_cache(cache)
        self.check_has(cache)
        self.check_get(cache)

