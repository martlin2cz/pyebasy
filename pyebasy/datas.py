from dataclasses import dataclass
from datetime import datetime, date, time
from typing import List

from pathlib import Path

########################################################################################################################


@dataclass(frozen=True)
class StorageElement:
    """ The common superclass for the file and directory. """

    path: Path
    date_of_creation: datetime

@dataclass(frozen=True)
class File(StorageElement):
    """ The file."""
    size: int
    date_of_last_modification: datetime


@dataclass(frozen=True)
class Directory(StorageElement):
    """ The directory, or a folder. """
    pass


@dataclass(frozen=True, init=False)
class TopDirectory(Directory):
    """ The top directory (the root of the storage, a top-level container of further elements) """

    def __init__(self, path: Path):
        super().__init__(path, datetime.combine(date.today(), time()))


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
