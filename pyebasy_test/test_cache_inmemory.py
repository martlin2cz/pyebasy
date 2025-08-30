from unittest import TestCase

import testing_data
from cache_inmemory import InMemoryCache
from cache_test_helpers import SomeCacheTest


class TestInMemoryCache(TestCase):

    def test_some_cache(self):
        cache = InMemoryCache()

        test = SomeCacheTest(self)
        test.run_some_test(cache)

