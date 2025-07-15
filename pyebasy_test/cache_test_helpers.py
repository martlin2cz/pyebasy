from datetime import datetime
from unittest import TestCase

from pathlib import Path

from commons_base import Cache
from datas import Directory, File
import some_testing_data


class SomeCacheTestMixin:
    def populate_cache(self, cache: Cache):
        some_testing_data.foreach_file_and_directory(True,
            lambda d: cache.store_directory(d),
            lambda f: cache.store_file(f)
        )

    def check_has(self: TestCase, cache: Cache):
        some_testing_data.foreach_element(True,
            lambda e: self.assertTrue(cache.has(e.path), f"Doesn't have {e.path}")
        )

    def check_get(self: TestCase, cache: Cache):
        some_testing_data.foreach_element(True,
            lambda e: self.assertEqual(e, cache.get(e.path), f"Doesn't have {e.path}")
        )
