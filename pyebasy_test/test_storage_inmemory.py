import unittest
from unittest import TestCase

from pathlib import Path
from datetime import datetime

from datas import Directory, File
from storage_inmemory import InMemoryStore, InMemoryStorageLister

# Use current timestamp
NOW = datetime.now()

# Constants for directories
ROOT_DIRECTORY = Directory(Path("testing-files"), NOW)
FOO_DIRECTORY = Directory(Path("testing-files/foo"), NOW)
BAR_DIRECTORY = Directory(Path("testing-files/foo/bar"), NOW)
BAZ_DIRECTORY = Directory(Path("testing-files/foo/bar/baz"), NOW)
AUX_DIRECTORY = Directory(Path("testing-files/foo/bar/_aux_"), NOW)
QUX_DIRECTORY = Directory(Path("testing-files/qux"), NOW)
QUUX_DIRECTORY = Directory(Path("testing-files/qux/quux"), NOW)

# Constants for files
LOREM_FILE = File(Path("testing-files/foo/bar/baz/lorem.txt"), NOW, 12, NOW)
DOLOR_FILE = File(Path("testing-files/foo/bar/_aux_/dolor.txt"), NOW, 23, NOW)
IPSUM_FILE = File(Path("testing-files/foo/bar/_aux_/ipsum.txt"), NOW, 34, NOW)
LIPSUM_FILE = File(Path("testing-files/lipsum.txt"), NOW, 45, NOW)
QUX_DOLOR_FILE = File(Path("testing-files/qux/dolor.txt"), NOW, 56, NOW)
SIT_FILE = File(Path("testing-files/qux/quux/sit.txt"), NOW, 67, NOW)


class TestInMemoryStore(TestCase):
    def test_in_memory_store_structure(self):
        store = InMemoryStore()

        # Add directories and files
        store.add(ROOT_DIRECTORY)
        store.add(FOO_DIRECTORY)
        store.add(BAR_DIRECTORY)
        store.add(BAZ_DIRECTORY)
        store.add(AUX_DIRECTORY)
        store.add(QUX_DIRECTORY)
        store.add(QUUX_DIRECTORY)

        store.add(LOREM_FILE)
        store.add(IPSUM_FILE)
        store.add(DOLOR_FILE)
        store.add(SIT_FILE)
        store.add(LIPSUM_FILE)

        # Check contents of a few directories
        foo_contents = store.get(Path("testing-files"))
        self.assertIn(FOO_DIRECTORY, foo_contents.child_directories)
        self.assertIn(QUX_DIRECTORY, foo_contents.child_directories)
        self.assertIn(LIPSUM_FILE, foo_contents.child_files)

        bar_contents = store.get(Path("testing-files/foo/bar"))
        self.assertIn(BAZ_DIRECTORY, bar_contents.child_directories)
        self.assertIn(AUX_DIRECTORY, bar_contents.child_directories)

        aux_contents = store.get(Path("testing-files/foo/bar/_aux_"))
        self.assertIn(DOLOR_FILE, aux_contents.child_files)
        self.assertIn(IPSUM_FILE, aux_contents.child_files)


class TestInMemoryStorageLister(TestCase):
    def test_list_directory(self):
        store = InMemoryStore()

        # Add directories and files
        store.add(ROOT_DIRECTORY)
        store.add(FOO_DIRECTORY)
        store.add(LIPSUM_FILE)

        lister = InMemoryStorageLister(store)

        contents = lister.list_directory(ROOT_DIRECTORY.path)
        self.assertIn(FOO_DIRECTORY, contents.child_directories)
        self.assertIn(LIPSUM_FILE, contents.child_files)