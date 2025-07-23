from datetime import datetime
from typing import Union

import tempfile
from pathlib import Path

from commons_base import DirectoryContents, StorageLister, StorageModifier, FileContentsSupplier
from commons_helpers import CommonStorage, DirectoryContentsBuilder
from datas import Directory, File, StorageElement, TopDirectory


class InMemoryStore:
    """ THe helper structure holding the imaginary, in memory, storage data. """

    def __init__(self):
        self.resources = {Path("."): DirectoryContents([], [])}

    def get(self, path: Path) -> DirectoryContents:
        """ Returns the contents of the specified directory path. """
        return self.resources[path]

    def add(self, file_or_directory: StorageElement):
        """ Adds new file or directory. """

        path = file_or_directory.path

        if not isinstance(file_or_directory, TopDirectory):
            owner_path = path.parent
            contents = self.resources[owner_path]

            builder = DirectoryContentsBuilder.from_existing(contents)
            builder.add(file_or_directory)

            self.resources[owner_path] = builder.build()

        if isinstance(file_or_directory, Directory):
            self.resources[path] = DirectoryContents([], [])

    def remove(self, file_or_directory: StorageElement):
        """ Removes the existing file or directory. """

        path = file_or_directory.path

        # verify the operation can be safelly performed
        if isinstance(file_or_directory, TopDirectory):
            raise ValueError("You cannot delete the TopDirectory!")

        if isinstance(file_or_directory, Directory):
            contents = self.get(path)
            if not contents.is_empty():
                raise ValueError("Directory not empty")

        # remove from the parent list
        parent_path = path.parent
        parent_children = self.get(parent_path)

        if isinstance(file_or_directory, Directory):
            parent_children.child_directories.remove(file_or_directory)

        if isinstance(file_or_directory, File):
            parent_children.child_files.remove(file_or_directory)

        # if directory, remove its contents
        if isinstance(file_or_directory, Directory):
            del self.resources[path]

    def replace(self, original_file_or_directory: StorageElement, new_file_or_directory: StorageElement):
        """ Replaces the existing file or directory by another one. """

        self.remove(original_file_or_directory)
        self.add(new_file_or_directory)

    def __str__(self):
        return str([str(p) for p in self.resources.keys()])


class InMemoryStorageLister(StorageLister):
    """ The storage lister based on the InMemoryStore. """

    def __init__(self, store: InMemoryStore):
        self.store = store

    def list_directory(self, path: Path) -> DirectoryContents:
        return self.store.get(path)


class InMemoryStorageModifier(StorageModifier):
    """ The storage modifier based on the InMemoryStore. """

    def __init__(self, store: InMemoryStore):
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
        current_parent_children = self.store.get(owner_directory_path)
        current_file = current_parent_children.get(file.path.name)

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