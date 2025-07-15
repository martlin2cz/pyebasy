from abc import ABC
from dataclasses import dataclass
from pathlib import Path
from typing import List, Union

from datas import File, Directory, StorageElement


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


class Cache(ABC):
    """ The local cache of the storage data. """

    def store_file(self, file: File):
        """ Stores the specified file into the cache. """
        pass

    def store_directory(self, directory: Directory):
        """ Stores the specified directory into the cache. """
        pass

    def has(self, path: Path) -> bool:
        """ Tells whether file or directory with a specified path exists in the cache or not. """
        pass

    def get(self, path: Path) -> StorageElement:
        """ Retrieves either the specified file or directory. """
        pass

########################################################################################################################


class CacheUpdater(ABC):
    """ The tool which utilise the StorageLister to fill and update the Cache instance. """

    def update(self, storage_lister: StorageLister, cache: Cache):
        """ By using the storage lister, updates the cache. """
        pass
