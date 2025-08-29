from pathlib import Path

from commons_base import Storage, StorageModifier, StorageLister, FileContentsSupplier
from datas import File, Directory


class DryRunStorageModidifier(StorageModifier):
    """ The storage modifier for the dry-run mode. Doesn't actualy do the things, just prints that. """

    def create_directory(self, owner_directory_path: Path, directory: Directory):
        print(f"Will create directory {directory.path}")

    def remove_directory(self, owner_directory_path: Path, directory: Directory):
        print(f"Will remove directory {directory.path}")

    def create_file(self, owner_directory_path: Path, file: File, contents_supplier: FileContentsSupplier):
        print(f"Will create file {file.path}")

    def remove_file(self, owner_directory_path: Path, file: File):
        print(f"Will remove file {file.path}")

    def update_file(self, owner_directory_path: Path, file: File, contents_supplier: FileContentsSupplier):
        print(f"Will update file {file.path}")


class DryRunStorage(Storage):
    """ A dry-run storage. Wraps existing storage, but, replaces its modifier by the dry-run one."""

    def __init__(self, wrapped_storage: Storage):
        self._wrapped_storage = wrapped_storage
        self._modifier = DryRunStorageModidifier()

    @staticmethod
    def wrap(wrapped_storage: Storage):
        return DryRunStorage(wrapped_storage)

    def lister(self) -> StorageLister:
        return self._wrapped_storage.lister()

    def modifier(self) -> StorageModifier:
        return self._modifier

    def contents_supplier(self) -> FileContentsSupplier:
        return self._wrapped_storage.contents_supplier()

