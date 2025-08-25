import pathlib
from pathlib import Path
from unittest import TestCase

import some_testing_data
from cache_inmemory import InMemoryCache
from cache_updater_impls import PrimitiveCacheUpdater
from datas import Directory, TopDirectory
from storage_inmemory import InMemoryStorageLister, InMemoryStore


class TestPrimitiveCacheUpdater(TestCase):
    def test_update(self):
        lister_store = InMemoryStore()

        some_testing_data.foreach_element(True, False,
              lambda e: lister_store.add(e)
        )

        storage_lister = InMemoryStorageLister(lister_store)
        cache = InMemoryCache()

        updater = PrimitiveCacheUpdater()
        updater.update(storage_lister, cache)

        some_testing_data.foreach_element(True, False,
              lambda e: self.assertTrue(cache.has(e.path), f"Cache doesn't have {e.path}")
        )
        some_testing_data.foreach_element(True, False,
              lambda e: self.assertEqual(e, cache.get(e.path), f"Cache doesn't have {e.path}")
        )

