from datetime import datetime
import os
import shutil

import pathlib
from pathlib import Path

import loggr
from commons_base import Storage, StorageLister, DirectoryContents, StorageModifier, FileContentsSupplier
from commons_helpers import CommonStorage, DirectoryContentsBuilder
from datas import File, Directory, StorageElement


class DefaultFileSystemStorageLister(StorageLister):
    """ The default implementation of the FileSystem based storage lister. """

    def __init__(self, top_directory_location: pathlib.Path):
        self.top_directory_location = top_directory_location

    def list_directory(self, path: Path) -> DirectoryContents:
        loggr.log_technical(f"Listing directory contents of {path}")

        result = DirectoryContentsBuilder()

        full_path = self.top_directory_location / path
        for full_entry_path in full_path.iterdir():
            inner_child_path = path / full_entry_path.name

            if full_entry_path.is_file():
                file = self._to_file_data(full_entry_path, inner_child_path)
                result.add_file(file)

            elif full_entry_path.is_dir():
                directory = self._to_directory_data(full_entry_path, inner_child_path)
                result.add_directory(directory)

        return result.build()

    @staticmethod
    def _to_file_data(full_path: Path, inner_path: Path) -> File:
        stat_info = full_path.stat()
        return File(
            path=inner_path,
            size=stat_info.st_size,
            date_of_creation=datetime.fromtimestamp(stat_info.st_ctime),
            date_of_last_modification=datetime.fromtimestamp(stat_info.st_mtime)
        )

    @staticmethod
    def _to_directory_data(full_path: Path, inner_path: Path) -> Directory:
        stat_info = full_path.stat()
        return Directory(
            path=inner_path,
            date_of_creation=datetime.fromtimestamp(stat_info.st_ctime)
        )


class DefaultFileSystemStorageModifier(StorageModifier):
    """ The storage modifier based on the InMemoryStore. """

    def __init__(self, top_directory_location: pathlib.Path):
        self.top_directory_location = top_directory_location

    def create_directory(self, owner_directory_path: Path, directory: Directory):
        loggr.log_technical(f"Creating directory {directory.path}")

        resolved_path = self._resolved_path_of(directory)
        os.mkdir(resolved_path)

    def remove_directory(self, owner_directory_path: Path, directory: Directory):
        loggr.log_technical(f"Removing directory {directory.path}")

        resolved_path = self._resolved_path_of(directory)
        os.rmdir(resolved_path)

    def create_file(self, owner_directory_path: Path, file: File, contents_supplier: FileContentsSupplier):
        loggr.log_technical(f"Creating file {file.path}")

        self._do_write_file(file, contents_supplier)

    def remove_file(self, owner_directory_path: Path, file: File):
        loggr.log_technical(f"Removing file {file.path}")

        resolved_path = self._resolved_path_of(file)
        os.remove(resolved_path)

    def update_file(self, owner_directory_path: Path, file: File, contents_supplier: FileContentsSupplier):
        loggr.log_technical(f"Updating file {file.path}")

        self._do_write_file(file, contents_supplier)

    def _do_write_file(self, file: File, contents_supplier: FileContentsSupplier):
        resolved_path = self._resolved_path_of(file)
        contents_path = contents_supplier.get_file_contents(file)

        if contents_supplier.is_file_contents_temporary(file):
            shutil.move(contents_path, resolved_path)
        else:
            shutil.copy(contents_path, resolved_path)

    def _resolved_path_of(self, element: StorageElement) -> pathlib.Path:
        path = element.path
        return self.top_directory_location / path


class DefaultFileSystemContentsSupplier(FileContentsSupplier):
    """ The default file system file contents supplier. """

    def __init__(self, top_directory_location: pathlib.Path):
        self.top_directory_location = top_directory_location

    def get_file_contents(self, file: File) -> Path:
        file_path = file.path
        return self.top_directory_location / file_path

    def is_file_contents_temporary(self, file: File) -> bool:
        return False


class DefaultFileSystemStorage(CommonStorage):
    """
    The default implementation of the Storage for the manipulation with the file systems.
    Manipulates with the files directories as with normal filesystem elements.
    """

    def __init__(self, top_directory_location: pathlib.Path):
        super().__init__(
            lister=DefaultFileSystemStorageLister(top_directory_location),
            modifier=DefaultFileSystemStorageModifier(top_directory_location),
            contents_supplier=DefaultFileSystemContentsSupplier(top_directory_location))

