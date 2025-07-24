from datetime import datetime
from typing import Union

import tempfile

import pathlib
from pathlib import Path

from commons_base import DirectoryContents, StorageLister, StorageModifier, FileContentsSupplier
from commons_helpers import CommonStorage, DirectoryContentsBuilder
from datas import Directory, File, StorageElement, TopDirectory


class InMemoryStore:
    """ THe helper structure holding the imaginary, in memory, storage data. """

    def __init__(self):
        self.resources = {}

    def _verify_path(self, path):
        """ Makes sure the specified path points to an existing directory """
        if path not in self.resources:
            raise KeyError(f"No such directory {path} in {self.resources.keys()}")

        directory = self.resources[path]
        if not isinstance(directory, Directory):
            raise KeyError(f"The {path} is not directory, but {directory}")

    def get_element(self, path: Path) -> StorageElement:
        """ Returns the file/directory with the given path """
        return self.resources[path]

    def get_children(self, path: Path) -> DirectoryContents:
        """ Returns the contents of the specified directory path. """

        self._verify_path(path)

        children = [e for p, e in self.resources.items() if p.parent == path]
        child_directories = [e for e in children if isinstance(e, Directory) and e.path != path] #FIXME: for the parent = "." case
        child_files = [e for e in children if isinstance(e, File)]

        return DirectoryContents(child_files, child_directories)

    def add(self, file_or_directory: StorageElement):
        """ Adds new file or directory. """

        path = file_or_directory.path
        if len(self.resources) > 0:  # we allways allow to add when empty
            parent_path = path.parent
            self._verify_path(parent_path)

        self.resources[path] = file_or_directory

    def remove(self, file_or_directory: StorageElement):
        """ Removes the existing file or directory. """

        path = file_or_directory.path
        parent_path = path.parent
        self._verify_path(parent_path)

        del self.resources[path]

    def replace(self, original_file_or_directory: StorageElement, new_file_or_directory: StorageElement):
        """ Replaces the existing file or directory by another one. """

        self.remove(original_file_or_directory)
        self.add(new_file_or_directory)

    def __str__(self):
        return str([str(p) for p in self.resources.keys()])


class InMemoryStorageLister(StorageLister):
    """ The storage lister based on the InMemoryStore. """

    def __init__(self, store=InMemoryStore()):
        self.store = store

    def list_directory(self, path: Path) -> DirectoryContents:
        return self.store.get_children(path)


class InMemoryStorageModifier(StorageModifier):
    """ The storage modifier based on the InMemoryStore. """

    def __init__(self, store=InMemoryStore()):
        self.store = store

    def create_directory(self, owner_directory_path: Path, directory: Directory):
        self.store.add(directory)

    def remove_directory(self, owner_directory_path: Path, directory: Directory):
        self.store.remove(directory)

    def create_file(self, owner_directory_path: Path, file: File, contents_supplier: FileContentsSupplier):
        self.store.add(file)

    def remove_file(self, owner_directory_path: Path, file: File):
        self.store.remove(file)

    def update_file(self, owner_directory_path: Path, file: File, contents_supplier: FileContentsSupplier):
        current_file = self.store.get_element(file.path)

        self.store.replace(current_file, file)


class InMemoryFileContentsSupplier(FileContentsSupplier):
    """ THe default file contents supplier, which simply creates temporary file with some sample contents. """

    def get_file_contents(self, file: File) -> Path:
        file_name = file.path.name
        file_size = file.size
        contents = f"Boo, this is sample file {file_name} which shall have {file_size} bytes.\n"

        with tempfile.NamedTemporaryFile(suffix=file_name, delete=False, mode='w+b') as temp_file:
            bytes_ = contents.encode("utf-8")
            temp_file.write(bytes_)

        return Path(temp_file.name)

    def is_file_contents_temporary(self, file: File) -> bool:
        return True


class InMemoryStorage(CommonStorage):
    """
    The storage, which doesn't actually store anything anywhere; it just mimics some real place where the files and directories are.
    Useful for mocking, testing and dry-running.
    """

    def __init__(self, store = InMemoryStore()):
        super().__init__(InMemoryStorageLister(store), InMemoryStorageModifier(store), InMemoryFileContentsSupplier())