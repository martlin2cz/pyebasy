from typing import Type

import testing_data
from commons_base import Cache


class SomeTestingCaches:
    """ The bundle of testing caches. Gets populated by the data form the SomeTestingStorageElements. """

    def __init__(self, cache_type: Type[Cache]):
        self.cache_type = cache_type

    def empty(self) -> Cache:
        cache = self.cache_type()

        return cache

    def full(self) -> Cache:
        cache = self.cache_type()

        test_data = testing_data.SomeTestingStorageElements(True, False)
        test_data.foreach_file_and_directory(
                                                     lambda d: cache.store_directory(d),
                                                     lambda f: cache.store_file(f))

        return cache

    def modified_full(self) -> Cache:
        cache = self.cache_type()

        test_data = testing_data.SomeWithModifications(True, True, True, True, True, True)
        test_data.foreach_file_and_directory(
            lambda d: cache.store_directory(d),
            lambda f: cache.store_file(f))

        return cache

    def fuller(self) -> Cache:
        cache = self.cache_type()

        test_data = testing_data.SomeTestingStorageElements(True, True)
        test_data.foreach_file_and_directory(
                                                     lambda d: cache.store_directory(d),
                                                     lambda f: cache.store_file(f))

        return cache
