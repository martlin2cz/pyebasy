from datetime import datetime
from typing import Union

import tempfile

import pathlib
from pathlib import Path

import loggr
from commons_base import DirectoryContents, StorageLister, StorageModifier, FileContentsSupplier
from commons_helpers import CommonStorage, DirectoryContentsBuilder
from datas import Directory, File, StorageElement, TopDirectory, ADirectory


class InMemoryStore:
    """ THe helper structure holding the imaginary, in memory, storage data. """

    def __init__(self):
        self.resources = {}

    def _ensure_existing(self, path: pathlib.Path, directory_required: bool) -> None:
        """ Makes sure the specified path points to an existing element """
        if path not in self.resources:
            raise KeyError(f"No such element {path} in {self.resources.keys()}")

        if directory_required:
            element = self.resources[path]
            if not isinstance(element, ADirectory):
                raise KeyError(f"The element {path} is not directory, but {type(element)} in {self.resources.keys()}")

    def _ensure_nonexisting(self, path: pathlib.Path) -> None:
        """ Makes sure the specified path doesn't exist here """
        if path in self.resources:
            raise KeyError(f"Element {path} already exists in {self.resources.keys()}")

    def get_element(self, path: Path) -> StorageElement:
        """ Returns the file/directory with the given path """
        loggr.log_technical(f"Looks for the {path} in the store")

        return self.resources[path]

    def get_children(self, path: Path) -> DirectoryContents:
        """ Returns the contents of the specified directory path. """
        loggr.log_technical(f"Gets children of {path} in the store")

        self._ensure_existing(path, True)

        children = [e for p, e in self.resources.items() if p.parent == path]
        child_directories = [e for e in children if isinstance(e, Directory) and e.path != path] #FIXME: for the parent = "." case
        child_files = [e for e in children if isinstance(e, File)]

        return DirectoryContents(child_files, child_directories)

    def add(self, file_or_directory: StorageElement):
        """ Adds new file or directory. """
        loggr.log_technical(f"Adds element {file_or_directory.path} into the store")

        if len(self.resources) == 0 and not isinstance(file_or_directory, TopDirectory):
            raise ValueError("The store is empty, start by adding the TopDirectory first")

        path = file_or_directory.path
        self._ensure_nonexisting(path)

        if not isinstance(file_or_directory, TopDirectory):
            parent_path = path.parent
            self._ensure_existing(parent_path, True)

        self.resources[path] = file_or_directory

    def remove(self, file_or_directory: StorageElement):
        """ Removes the existing file or directory. """
        loggr.log_technical(f"Removing element {file_or_directory.path} from the store")

        if len(self.resources) > 0 and isinstance(file_or_directory, TopDirectory):
            raise ValueError("The store is NOT empty, you cannot remove its TopDirectory")

        path = file_or_directory.path
        self._ensure_existing(path, False)

        if not isinstance(file_or_directory, TopDirectory):
            parent_path = path.parent
            self._ensure_existing(parent_path, True)

        del self.resources[path]

    def replace(self, original_file_or_directory: StorageElement, new_file_or_directory: StorageElement):
        """ Replaces the existing file or directory by another one. """
        loggr.log_technical(f"Replaces element {original_file_or_directory.path} in the store")

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
        loggr.log_detailed(f"Creating directory {directory.path}")

        self.store.add(directory)

    def remove_directory(self, owner_directory_path: Path, directory: Directory):
        loggr.log_detailed(f"Removing directory {directory.path}")

        self.store.remove(directory)

    def create_file(self, owner_directory_path: Path, file: File, contents_supplier: FileContentsSupplier):
        loggr.log_detailed(f"Creating file {file.path}")

        self.store.add(file)

    def remove_file(self, owner_directory_path: Path, file: File):
        loggr.log_detailed(f"Removing file {file.path}")

        self.store.remove(file)

    def update_file(self, owner_directory_path: Path, file: File, contents_supplier: FileContentsSupplier):
        loggr.log_detailed(f"Updating directory {file.path}")

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