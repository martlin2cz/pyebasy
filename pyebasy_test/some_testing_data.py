from datetime import datetime
from typing import Callable
from unittest import TestCase

from pathlib import Path

from datas import Directory, File, StorageElement

NOW = datetime.now()
ROOT_DIRECTORY_PATH = Path("testing-files")

# Directories
ROOT_DIRECTORY = Directory(ROOT_DIRECTORY_PATH, NOW)
FOO_DIRECTORY = Directory(ROOT_DIRECTORY_PATH/"foo", NOW)
BAR_DIRECTORY = Directory(ROOT_DIRECTORY_PATH/"foo"/"bar", NOW)
BAZ_DIRECTORY = Directory(ROOT_DIRECTORY_PATH/"foo"/"bar"/"baz", NOW)
AUX_DIRECTORY = Directory(ROOT_DIRECTORY_PATH/"foo"/"bar"/"_aux_", NOW)
QUX_DIRECTORY = Directory(ROOT_DIRECTORY_PATH/"qux", NOW)
QUUX_DIRECTORY = Directory(ROOT_DIRECTORY_PATH/"qux"/"quux", NOW)

# Files
LOREM_FILE = File(ROOT_DIRECTORY_PATH/"foo"/"bar"/"baz"/"lorem.txt", NOW, 123,  NOW)
IPSUM_FILE = File(ROOT_DIRECTORY_PATH/"foo"/"bar"/"_aux_"/"ipsum.txt", NOW,789, NOW)
DOLOR_FILE = File(ROOT_DIRECTORY_PATH/"foo"/"bar"/"_aux_"/"dolor.txt", NOW,456, NOW)
SIT_FILE = File(ROOT_DIRECTORY_PATH/"qux"/"quux"/"sit.txt", NOW, 987, NOW)
LIPSUM_FILE = File(ROOT_DIRECTORY_PATH/"lipsum.txt", NOW, 321, NOW)

ALL_ELEMENTS = [
    FOO_DIRECTORY, BAR_DIRECTORY, BAZ_DIRECTORY, LOREM_FILE,
    AUX_DIRECTORY, IPSUM_FILE, DOLOR_FILE,
    QUX_DIRECTORY, QUUX_DIRECTORY, SIT_FILE,
    LIPSUM_FILE
]


def foreach_element(include_root_dir: bool, fn: Callable[[StorageElement], None]):
    """ Executes given function for each testing file and directory. """

    if include_root_dir:
        fn(ROOT_DIRECTORY)

    for element in ALL_ELEMENTS:
        fn(element)


def foreach_file_and_directory(include_root_dir: bool, directory_fn: Callable[[Directory], None], file_fn: Callable[[File], None]):
    """ Executes given functions for each testing file and directory. """

    if include_root_dir:
        directory_fn(ROOT_DIRECTORY)

    for element in ALL_ELEMENTS:
        if type(element) is Directory:
            directory_fn(element)

        if type(element) is File:
            file_fn(element)


class TestSomeTestingData(TestCase):

    def test_foreach_element(self):
        foreach_element(True,
            lambda e: print(f"Element (root incl.): {e}")
        )

        foreach_element(False,
            lambda e: print(f"Element (root excl.): {e}")
        )

    def test_foreach_directory_and_file(self):
        foreach_file_and_directory(True,
            lambda d: print(f"Directory (root incl.): {d}"),
            lambda f: print(f"File      (root incl.): {f}")
        )

        foreach_file_and_directory(False,
            lambda d: print(f"Directory (root excl.): {d}"),
            lambda f: print(f"File:     (root excl.): {f}")
        )