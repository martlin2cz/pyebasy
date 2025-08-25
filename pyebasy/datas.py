from abc import ABC

import pathlib
from dataclasses import dataclass
from datetime import datetime, date, time
from typing import List

from pathlib import Path


########################################################################################################################


@dataclass(frozen=True)
class StorageElement:
    """ The common superclass for the files, directories any other kinds of file system elements. """

    path: Path

    def __str__(self) -> str:
        return f"{type(self).__name__}[{self.path!s}]"


class ADirectory(ABC):
    """ Indicator of the storage element beeing a kind of directory (a container of further elements). """
    pass


TOP_DIRECTORY_RELATIVE_PATH = pathlib.Path(".")


@dataclass(frozen=True, init=False)
class TopDirectory(StorageElement, ADirectory):
    """ The top directory (the root of the storage, a top-level container of further elements). """

    def __init__(self):
        super().__init__(TOP_DIRECTORY_RELATIVE_PATH)


@dataclass(frozen=True)
class CommonStorageElement(StorageElement):
    """ The common storage element (either file ir directory), which actually contains the real data.
    It has a name, and date of creation and everything. """

    date_of_creation: datetime

    @property
    def name(self) -> str:
        return self.path.name


@dataclass(frozen=True)
class File(CommonStorageElement):
    """ The file. """
    size: int
    date_of_last_modification: datetime


@dataclass(frozen=True)
class Directory(CommonStorageElement, ADirectory):
    """ The directory, or a folder. """
    pass




########################################################################################################################


@dataclass(frozen=True)
class DirectoryContentsDifference:
    directories_to_add: List[Directory]
    directories_to_remove: List[Directory]
    directories_to_keep: List[Directory]

    files_to_add: List[File]
    files_to_remove: List[File]
    files_to_update: List[File]
    files_to_keep: List[File]
