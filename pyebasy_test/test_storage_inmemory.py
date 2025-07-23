import unittest
from unittest import TestCase

from pathlib import Path
from datetime import datetime

import some_testing_data
from datas import Directory, File
from storage_inmemory import InMemoryStore, InMemoryStorageLister



class TestInMemoryStore(TestCase):
    def test_in_memory_store_structure(self):
        store = InMemoryStore()
        some_testing_data.foreach_element(True,False,
            lambda e: store.add(e)
        )

        # Check contents of a few directories
        foo_contents = store.get(Path("testing-files"))
        self.assertIn(some_testing_data.FOO_DIRECTORY, foo_contents.child_directories)
        self.assertIn(some_testing_data.QUX_DIRECTORY, foo_contents.child_directories)
        self.assertIn(some_testing_data.LIPSUM_FILE, foo_contents.child_files)

        bar_contents = store.get(Path("testing-files/foo/bar"))
        self.assertIn(some_testing_data.BAZ_DIRECTORY, bar_contents.child_directories)
        self.assertIn(some_testing_data.AUX_DIRECTORY, bar_contents.child_directories)

        aux_contents = store.get(Path("testing-files/foo/bar/_aux_"))
        self.assertIn(some_testing_data.DOLOR_FILE, aux_contents.child_files)
        self.assertIn(some_testing_data.IPSUM_FILE, aux_contents.child_files)


class TestInMemoryStorageLister(TestCase):
    def test_list_directory(self):
        store = InMemoryStore()
        some_testing_data.foreach_element(True,False,
            lambda e: store.add(e)
        )

        lister = InMemoryStorageLister(store)

        contents = lister.list_directory(some_testing_data.ROOT_DIRECTORY_PATH)
        self.assertIn(some_testing_data.FOO_DIRECTORY, contents.child_directories)
        self.assertIn(some_testing_data.LIPSUM_FILE, contents.child_files)
