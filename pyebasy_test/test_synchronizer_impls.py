from unittest import TestCase

import testing_data
from cache_inmemory import InMemoryCache
from storage_inmemory import InMemoryStorage, InMemoryStore
from synchronizer_impls import DefaultSynchronizer


class TestDefaultSynchronizer(TestCase):
    def test_minimal(self):
        source_store = InMemoryStore()
        source_store.add(testing_data.ROOT_DIRECTORY)

        destination_store = InMemoryStore()
        destination_store.add(testing_data.ROOT_DIRECTORY)

        self._do_synchronize(source_store, destination_store)

        self.assertEqual(testing_data.ROOT_DIRECTORY, destination_store.get_element(testing_data.ROOT_DIRECTORY_PATH))

    def test_empty_to_empty(self):
        source_data = testing_data.EmptyTestingStorageElements(True)
        destination_data = testing_data.EmptyTestingStorageElements(True)

        self._create_data_synchronize_and_check(source_data, destination_data)

    def test_full_to_full(self):
        source_data = testing_data.SomeTestingStorageElements(True, False)
        destination_data = testing_data.SomeTestingStorageElements(True, False)

        self._create_data_synchronize_and_check(source_data, destination_data)

    def test_empty_to_full(self):
        source_data = testing_data.EmptyTestingStorageElements(True)
        destination_data = testing_data.SomeTestingStorageElements(True, False)

        self._create_data_synchronize_and_check(source_data, destination_data)

    def test_full_to_empty(self):
        source_data = testing_data.SomeTestingStorageElements(True, False)
        destination_data = testing_data.EmptyTestingStorageElements(True)

        self._create_data_synchronize_and_check(source_data, destination_data)


    def _create_data_synchronize_and_check(self, source_elements: testing_data.BaseTestingData, destination_elements: testing_data.BaseTestingData):
        source_store = InMemoryStore()
        source_elements.foreach_element(lambda e: source_store.add(e))

        destination_store = InMemoryStore()
        destination_elements.foreach_element(lambda e: destination_store.add(e))

        self._do_synchronize(source_store, destination_store)

        source_elements.foreach_element(lambda e: self.assertEqual(e, destination_store.get_element(e.path)))

    def _do_synchronize(self, source_store: InMemoryStore, destination_store: InMemoryStore):
        source_storage = InMemoryStorage(source_store)
        destination_storage = InMemoryStorage(destination_store)

        source_cache = InMemoryCache()
        destination_cache = InMemoryCache()

        synchronizer = DefaultSynchronizer(source_cache, destination_cache, True, True)
        synchronizer.synchronize(source_storage, destination_storage)
