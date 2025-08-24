from pathlib import Path
from unittest import TestCase

import testing_data
from cache_inmemory import InMemoryCache
from cache_updater_impls import PrimitiveCacheUpdater
from storage_inmemory import InMemoryStorageLister, InMemoryStore


class TestPrimitiveCacheUpdater(TestCase):

    def setUp(self):
        self.test_data = testing_data.SomeTestingStorageElements(True, False)

    def test_update(self):
        lister_store = InMemoryStore()
        self.test_data.foreach_element(
            lambda e: lister_store.add(e)
        )

        storage_lister = InMemoryStorageLister(lister_store)
        cache = InMemoryCache()

        updater = PrimitiveCacheUpdater()
        updater.update(storage_lister, cache)

        self.test_data.foreach_element(
            lambda e: self.assertTrue(cache.has(e.path), f"Cache doesn't have {e.path}")
        )
        self.test_data.foreach_element(
            lambda e: self.assertEqual(e, cache.get(e.path), f"Cache doesn't have {e.path}")
        )