from unittest import TestCase

import testing_data
from cache_inmemory import InMemoryCache
from testing_caches import SomeTestingCaches


class TestSomeTestingCaches(TestCase):

    def setUp(self):
        self.test_data = testing_data.SomeTestingStorageElements(True, False)
        self.caches = SomeTestingCaches(InMemoryCache)

    def test_empty(self):
        cache = self.caches.empty()
        print(cache)

        self.assertTrue(cache.get(testing_data.ROOT_DIRECTORY_PATH) is None)

    def test_full(self):
        cache = self.caches.full()
        print(cache)

        self.assertEqual(testing_data.FOO_DIRECTORY, cache.get(testing_data.FOO_DIRECTORY.path))
        self.assertEqual(testing_data.LOREM_FILE, cache.get(testing_data.LOREM_FILE.path))

    def test_fuller(self):
        cache = self.caches.fuller()
        print(cache)

        self.assertEqual(testing_data.FOO_DIRECTORY, cache.get(testing_data.FOO_DIRECTORY.path))
        self.assertEqual(testing_data.QUICK_DIRECTORY, cache.get(testing_data.QUICK_DIRECTORY.path))
        self.assertEqual(testing_data.LOREM_FILE, cache.get(testing_data.LOREM_FILE.path))
        self.assertEqual(testing_data.LAZY_FILE, cache.get(testing_data.LAZY_FILE.path))
