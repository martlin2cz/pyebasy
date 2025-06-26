from datetime import datetime
from unittest import TestCase

from pathlib import Path

from commons_base import Cache
from datas import Directory, File

NOW = datetime.now()

# Directories
FOO_DIRECTORY = Directory(Path("testing-files/foo"), NOW)
BAR_DIRECTORY = Directory(Path("testing-files/foo/bar"), NOW)
BAZ_DIRECTORY = Directory(Path("testing-files/foo/bar/baz"), NOW)
AUX_DIRECTORY = Directory(Path("testing-files/foo/bar/_aux_"), NOW)
QUX_DIRECTORY = Directory(Path("testing-files/qux"), NOW)
QUUX_DIRECTORY = Directory(Path("testing-files/qux/quux"), NOW)

# Files
LOREM_FILE = File(Path("testing-files/foo/bar/baz/lorem.txt"), NOW, 123,  NOW)
IPSUM_FILE = File(Path("testing-files/foo/bar/_aux_/ipsum.txt"), NOW,789, NOW)
DOLOR_FILE = File(Path("testing-files/foo/bar/_aux_/dolor.txt"), NOW,456, NOW)
SIT_FILE = File(Path("testing-files/qux/quux/sit.txt"), NOW, 987, NOW)
LIPSUM_FILE = File(Path("testing-files/lipsum.txt"), NOW, 321, NOW)

ALL_ELEMENTS = [
    FOO_DIRECTORY, BAR_DIRECTORY, BAZ_DIRECTORY, LOREM_FILE,
    AUX_DIRECTORY, IPSUM_FILE, DOLOR_FILE,
    QUX_DIRECTORY, QUUX_DIRECTORY, SIT_FILE,
    LIPSUM_FILE
]


class SomeCacheTestMixin:
    def populate_cache(self, cache: Cache):
        # /foo/bar/baz/*
        cache.store_directory(FOO_DIRECTORY)
        cache.store_directory(BAR_DIRECTORY)
        cache.store_directory(BAZ_DIRECTORY)
        cache.store_file(LOREM_FILE)

        # /foo/bar/_aux_/*
        cache.store_directory(AUX_DIRECTORY)
        cache.store_file(IPSUM_FILE)
        cache.store_file(DOLOR_FILE)

        # /qux/quux/*
        cache.store_directory(QUX_DIRECTORY)
        cache.store_directory(QUUX_DIRECTORY)
        cache.store_file(SIT_FILE)

        # /*
        cache.store_file(LIPSUM_FILE)

    def check_has(self: TestCase, cache: Cache):
        for element in ALL_ELEMENTS:
            self.assertTrue(cache.has(element.path), f"Doesn't have {element.path}")

    def check_get(self: TestCase, cache: Cache):
        for element in ALL_ELEMENTS:
            self.assertEqual(element, cache.get(element.path), f"Doesn't have {element.path}")