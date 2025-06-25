from abc import ABC
from dataclasses import dataclass
from pathlib import Path
from typing import List

from datas import File, Directory

########################################################################################################################

@dataclass(frozen=True)
class DirectoryContents:
    """ The contents of a directory (A list of child files and directories). """

    child_files: List[File]
    child_directories: List[Directory]


class StorageLister(ABC):
    """ The abstract storage lister. Performs the quering of the current status of the storage."""

    def list_directory(self, path: Path) -> DirectoryContents:
        """ Lists contents of the specified directory. """
        pass


class Storage(ABC):
    """ The abstract storage. Provides only the lister (for now). """

    def lister(self) -> StorageLister:
        """ Returns the lister. """
        pass

########################################################################################################################
