from abc import ABC
from dataclasses import dataclass
from pathlib import Path
from typing import List, Union, Iterable, Dict

from datas import File, Directory, StorageElement, DirectoryContentsDifference, CommonStorageElement, ADirectory, \
    CachesDifference

""" The path to the root of the synchronisation. """
ROOT_PATH=Path(".")

########################################################################################################################

@dataclass(frozen=True)
class DirectoryContents:
    """ The contents of a directory (A list of child files and directories). """

    child_files: List[File]
    child_directories: List[Directory]

    def get(self, name: str) -> CommonStorageElement:
        the_files = [f for f in self.child_files if f.path.name == name]
        the_directories = [d for d in self.child_directories if d.path.name == name]

        elements = [*the_files, *the_directories]
        return elements[0]

    def is_empty(self) -> bool:
        """ Returns true if the contents of a directory is empty. """
        return len(self.child_files) == 0 and len(self.child_directories) == 0


class StorageLister(ABC):
    """ The abstract storage lister. Performs the quering of the current status of the storage."""

    def list_directory(self, path: Path) -> DirectoryContents:
        """ Lists contents of the specified directory. """
        pass


class FileContentsSupplier(ABC):
    """ The helper of the storage, which tells where the actual file contents is stored,
    and if nescessary stores (downloads) it somewhere temporary. """

    def get_file_contents(self, file: File) -> Path:
        """ Returns the path of the local filesystem file containing the specified file's contents.
        Keep in mind that if such file doesn't exist (for example, the file is somewhere in the cloud or something),
        this method will ensure its creation. """
        pass

    def is_file_contents_temporary(self, file: File) -> bool:
        """ Returns true whether the contents file contains is temporary or permanent. """
        pass


class StorageModifier(ABC):
    """ The abstract storage modifier. Performs the modification of the current status of the storage. """

    def create_directory(self, owner_directory_path: Path, directory: Directory):
        """ Creates the specified child directory in the given directory. """
        pass

    def remove_directory(self, owner_directory_path: Path, directory: Directory):
        """ Removes the specified child directory from the given directory. """
        pass

    def create_file(self, owner_directory_path: Path, file: File, contents_supplier: FileContentsSupplier):
        """ Creates the specified child file in the given directory to have the specified contents. """
        pass

    def remove_file(self, owner_directory_path: Path, file: File):
        """ Removes the specified child file from the given directory. """
        pass

    def update_file(self, owner_directory_path: Path, file: File, contents_supplier: FileContentsSupplier):
        """ Updates the specified child file in the given directory, to have the specified contents. """
        pass


class Storage(ABC):
    """ The abstract storage. Provides only the lister, modifier and contents supplier. """

    def lister(self) -> StorageLister:
        """ Returns the lister. """
        pass

    def modifier(self) -> StorageModifier:
        """ Returns the modifier. """
        pass

    def contents_supplier(self) -> FileContentsSupplier:
        """ Returns the contents supplier. """
        pass


########################################################################################################################


class Cache(ABC):
    """ The local cache of the storage data. """

    def store_file(self, file: File):
        """ Stores the specified file into the cache. """
        pass

    def store_directory(self, directory: ADirectory):
        """ Stores the specified directory into the cache. """
        pass

    def has(self, path: Path) -> bool:
        """ Tells whether file or directory with a specified path exists in the cache or not. """
        pass

    def get(self, path: Path) -> StorageElement:
        """ Retrieves either the specified file or directory. """
        pass

    def get_contents(self, path: Path) -> DirectoryContents:
        """ Assuming the path points to a directory, retrieves the contents of that directory. """
        pass

########################################################################################################################


class CacheUpdater(ABC):
    """ The tool which utilise the StorageLister to fill and update the Cache instance. """

    def update(self, storage_lister: StorageLister, cache: Cache):
        """ By using the storage lister, updates the cache. """
        pass

########################################################################################################################

class DirectoryContentsComparer(ABC):
    """ The tool which computes DirectoryContentsDifference for the two DirectoryContents (source and destination) """

    def compute(self, source_contents: DirectoryContents, destination_contents: DirectoryContents) -> DirectoryContentsDifference:
        """ Computes the difference between the source and destination directory contents. """
        pass


class CacheComparer(ABC):
    """ The tool which computes stream of DirectoryContentsDifference (the CachesDifference) for the two Caches (source and destination) """

    def compute(self, source: Cache, destination: Cache) -> CachesDifference:
        """ Computes the difference between the source and destination caches. """
        pass

########################################################################################################################


class DirectoryContentsDifferencePerformer(ABC):
    """ The tool which applies the directory contents difference to a particular storage directory. """

    def execute(self, directory_path: Path, diff: DirectoryContentsDifference, contents_supplier: FileContentsSupplier, storage_modifier: StorageModifier):
        """ Executes the directory contents difference in the specified storage. """
        pass


class CachesDifferencePerformer(ABC):
    """ The tool which applies the caches difference to a particular storage. """

    def apply(self, diff: CachesDifference, contents_supplier: FileContentsSupplier, storage_modifier: StorageModifier):
        """ Applies the difference to the specified storage. """
        pass

########################################################################################################################

class CachesSynchronizer(ABC):
    """ The synchronizer of the caches (actually, executor of changes between them in the destination storage). """

    def execute(self, source_cache: Cache,  destination_cache: Cache, contents_supplier: FileContentsSupplier, storage_modifier: StorageModifier):
        """ Computes the difference between theese two caches and executes them. """
        pass


class Synchronizer(ABC):
    """ The actual sychronizer. """

    def synchronize(self, source: Storage, destination: Storage):
        """ Synchronizes the source storage with the destionation. """
        pass