from datetime import datetime
from unittest import TestCase

from pathlib import Path

from commons_base import Cache, DirectoryContents
from datas import Directory, File
import testing_data


class SomeCacheTest:

    def __init__(self, test_case: TestCase):
        self.test_case = test_case

    def run_some_test(self, cache: Cache):
        test_data = testing_data.SomeTestingStorageElements(True, False)

        self._populate_cache(cache, test_data)
        self._check_has(cache, test_data)
        self._check_get(cache, test_data)
        self._check_get_children(cache)

    def _populate_cache(self, cache: Cache, test_data: testing_data.SomeTestingStorageElements):
        test_data.foreach_file_and_directory(
            lambda d: cache.store_directory(d),
            lambda f: cache.store_file(f)
        )

    def _check_has(self, cache: Cache, test_data: testing_data.SomeTestingStorageElements):
        test_data.foreach_element(
            lambda e: self.test_case.assertTrue(cache.has(e.path), f"Doesn't have {e.path}")
        )

    def _check_get(self,  cache: Cache, test_data: testing_data.SomeTestingStorageElements):
        test_data.foreach_element(
            lambda e: self.test_case.assertEqual(e, cache.get(e.path), f"Doesn't have {e.path}")
        )

    def _check_get_children(self, cache: Cache):
        root_contents = DirectoryContents([testing_data.LIPSUM_FILE], [testing_data.FOO_DIRECTORY, testing_data.QUX_DIRECTORY])
        self.test_case.assertEqual(root_contents, cache.get_contents(testing_data.ROOT_DIRECTORY_PATH))
