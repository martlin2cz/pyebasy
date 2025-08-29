from abc import ABC

import pathlib
from dataclasses import dataclass
from datetime import datetime, date, time
from typing import List, Set, Dict

import pathlib
from pathlib import Path


########################################################################################################################


@dataclass(frozen=True, order=True)
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
    """ The difference between two directories. Contains files and directories which are same, modified, missing in one
     and present in the other. """

    directories_to_add: List[Directory]
    directories_to_remove: List[Directory]
    directories_to_keep: List[Directory]

    files_to_add: List[File]
    files_to_remove: List[File]
    files_to_update: List[File]
    files_to_keep: List[File]

    def all_directories(self) -> List[Directory]:
        """ Returns the all directories involved. """
        return sorted({*self.directories_to_add, *self.directories_to_remove, *self.directories_to_keep})

    def all_files(self) -> List[Directory]:
        """ Returns all the files involved. """
        return sorted({*self.files_to_add, *self.files_to_remove, *self.files_to_update, *self.files_to_keep})

    def changes(self):
        """ Returns all the changed files and directories. """
        return [*self.directories_to_add, *self.directories_to_remove,
                *self.files_to_add, *self.files_to_remove, *self.files_to_update]

    def has_some_changes(self) -> bool:
        """ Returns true, if contains some changes."""
        return len(self.changes()) > 0

    def __str__(self):
        return (f"DirectoryContentsDifference: "
                f"directories {len(self.all_directories())} ("
                f"add: {len(self.directories_to_add)}, "
                f"remove: {len(self.directories_to_remove)}, "
                f"keep: {len(self.files_to_add)}"
                f"), "
                f"files: {len(self.all_files())} ("
                f"add: {len(self.files_to_add)}, "
                f"remove: {len(self.files_to_remove)}, "
                f"update: {len(self.files_to_update)}, "
                f"keep: {len(self.files_to_update)}"
                ")")



@dataclass(frozen=True)
class CachesDifference:
    """ The different of two caches. Contains the directory differences for each directory. """

    directories_changes: Dict[pathlib.Path, DirectoryContentsDifference]

    def paths(self) -> List[Path]:
        return sorted(self.directories_changes.keys())

    def change_of_directory(self, path: Path) -> DirectoryContentsDifference:
        return self.directories_changes[path]

    def __len__(self):
        return len(self.directories_changes.keys())

    def __str__(self):
        return (f"CachesDifference: "
                f"directories: {len(self.directories_changes)}, "
                f"with some changes {(len([dch for dch in self.directories_changes.values() if dch.has_some_changes()]))}")

