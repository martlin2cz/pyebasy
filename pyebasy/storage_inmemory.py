from datetime import datetime
from typing import Union

from pathlib import Path

from commons_base import DirectoryContents, StorageLister
from commons_helpers import CommonStorage, DirectoryContentsBuilder
from datas import Directory, File, StorageElement


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
        owner_path = path.parent
        contents = self.resources[owner_path]

        builder = DirectoryContentsBuilder.from_existing(contents)
        builder.add(file_or_directory)

        self.resources[owner_path] = builder.build()

        if type(file_or_directory) == Directory:
            self.resources[path] = DirectoryContents([], [])


class InMemoryStorageLister(StorageLister):
    """ The storage lister based on the InMemoryStore. """

    def __init__(self, store: InMemoryStore):
        self.store = store

    def list_directory(self, path: Path) -> DirectoryContents:
        return self.store.get(path)

class InMemoryStorage(CommonStorage):
    """
    The storage, which doesn't actually store anything anywhere; it just mimics some real place where the files and directories are.
    Useful for mocking, testing and dry-running.
    """

    def __init__(self, store = InMemoryStore()):
        super().__init__(InMemoryStorageLister(store))