from abc import ABC

import pathlib
from datetime import datetime, timedelta
from typing import Callable, List
from unittest import TestCase

from pathlib import Path

from datas import Directory, File, StorageElement, TopDirectory, TOP_DIRECTORY_RELATIVE_PATH, ADirectory

TOP_DIRECTORY_LOCATION=pathlib.Path("testing-files")

NOW = datetime.now()
LATER_NOW = NOW + timedelta(seconds=1)

ROOT_DIRECTORY_PATH = TOP_DIRECTORY_RELATIVE_PATH

# Directories
ROOT_DIRECTORY = TopDirectory()
FOO_DIRECTORY = Directory(ROOT_DIRECTORY_PATH/"foo", NOW)
BAR_DIRECTORY = Directory(ROOT_DIRECTORY_PATH/"foo"/"bar", NOW)
BAZ_DIRECTORY = Directory(ROOT_DIRECTORY_PATH/"foo"/"bar"/"baz", NOW)
AUX_DIRECTORY = Directory(ROOT_DIRECTORY_PATH/"foo"/"bar"/"_aux_", NOW)
QUX_DIRECTORY = Directory(ROOT_DIRECTORY_PATH/"qux", NOW)
QUUX_DIRECTORY = Directory(ROOT_DIRECTORY_PATH/"qux"/"quux", NOW)

# Files
LOREM_FILE = File(ROOT_DIRECTORY_PATH/"foo"/"bar"/"baz"/"lorem.txt", NOW, 123,  NOW)
IPSUM_FILE = File(ROOT_DIRECTORY_PATH/"foo"/"bar"/"_aux_"/"ipsum.txt", NOW, 789, NOW)
DOLOR_FILE = File(ROOT_DIRECTORY_PATH/"foo"/"bar"/"_aux_"/"dolor.txt", NOW, 456, NOW)
SIT_FILE = File(ROOT_DIRECTORY_PATH/"qux"/"quux"/"sit.txt", NOW, 987, NOW)
LIPSUM_FILE = File(ROOT_DIRECTORY_PATH/"lipsum.txt", NOW, 321, NOW)

# Additional directories
QUICK_DIRECTORY = Directory(ROOT_DIRECTORY_PATH/"quick", NOW)
BROWN_DIRECTORY = Directory(ROOT_DIRECTORY_PATH/"foo"/"brown", NOW)
FOX_DIRECTORY = Directory(ROOT_DIRECTORY_PATH/"foo"/"fox", NOW)

# Additional files
LAZY_FILE = File(ROOT_DIRECTORY_PATH/"lazy.txt", NOW, 111, NOW)
BROWN_FILE = File(ROOT_DIRECTORY_PATH/"foo"/"brown.txt", NOW, 222, NOW)
DOG_FILE = File(ROOT_DIRECTORY_PATH/"foo"/"dog.txt", NOW, 333, NOW)

# Modified files
MODIFIED_LOREM_FILE = File(LOREM_FILE.path, NOW, 1230, LATER_NOW)
MODIFIED_IPSUM_FILE = File(IPSUM_FILE.path, NOW, 7890, LATER_NOW)
MODIFIED_DOLOR_FILE = File(DOLOR_FILE.path, NOW, 4560, LATER_NOW)
MODIFIED_SIT_FILE = File(SIT_FILE.path, NOW, 9870, LATER_NOW)
MODIFIED_LIPSUM_FILE = File(LIPSUM_FILE.path, LATER_NOW, 3210, LATER_NOW)

# Modified additional files
MODIFIED_LAZY_FILE = File(LAZY_FILE.path, NOW, 1110, LATER_NOW)
MODIFIED_BROWN_FILE = File(BROWN_FILE.path, NOW, 2230, LATER_NOW)
MODIFIED_DOG_FILE = File(DOG_FILE.path, NOW, 3330, LATER_NOW)

# The all elements
ALL_ELEMENTS = [
    FOO_DIRECTORY, BAR_DIRECTORY, BAZ_DIRECTORY, LOREM_FILE,
    AUX_DIRECTORY, IPSUM_FILE, DOLOR_FILE,
    QUX_DIRECTORY, QUUX_DIRECTORY, SIT_FILE,
    LIPSUM_FILE
]

ALL_ADITIONAL_ELEMENTS = [
    QUICK_DIRECTORY,
    BROWN_DIRECTORY, FOX_DIRECTORY,
    LAZY_FILE,
    BROWN_FILE, DOG_FILE
]


class BaseTestingData(ABC):
    """ The superclass for the testing data producers. """

    def foreach_element(self, fn: Callable[[StorageElement], None]) -> None:
        """ Executes given function for each testing file and directory. """

        elements = self._list_elements()
        for element in elements:
            fn(element)

    def foreach_file_and_directory(self, directory_fn: Callable[[Directory], None], file_fn: Callable[[File], None]):
        """ Executes given functions for each testing file and directory. """

        elements = self._list_elements()
        for element in elements:
            if type(element) is TopDirectory:
                directory_fn(element)

            if type(element) is Directory:
                directory_fn(element)

            if type(element) is File:
                file_fn(element)

    def _list_elements(self) -> List[StorageElement]:
        """ Actually lists the elements to be part of this dataset. """
        pass


class SomeTestingStorageElements(BaseTestingData):
    """ The standard testing element set. """

    def __init__(self, include_root_dir: bool, include_aditionals: bool):
        self.include_root_dir = include_root_dir
        self.include_aditionals = include_aditionals

    def _list_elements(self) -> List[StorageElement]:
        elements = []

        if self.include_root_dir:
            elements.append(ROOT_DIRECTORY)

        elements.extend(ALL_ELEMENTS)

        if self.include_aditionals:
            elements.extend(ALL_ADITIONAL_ELEMENTS)

        return elements

