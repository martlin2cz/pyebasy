import os
import pathlib
import shutil
from datetime import datetime

from pathlib import Path

from commons_base import Storage, StorageLister, DirectoryContents, StorageModifier, FileContentsSupplier
from commons_helpers import CommonStorage, DirectoryContentsBuilder
from datas import File, Directory


class DefaultFileSystemStorageLister(StorageLister):
    """ The default implementation of the FileSystem based storage lister. """

    def list_directory(self, path: Path) -> DirectoryContents:
        result = DirectoryContentsBuilder()

        for entry in path.iterdir():
            if entry.is_file():
                file = self._to_file_data(entry)
                result.add_file(file)

            elif entry.is_dir():
                directory = self._to_directory_data(entry)
                result.add_directory(directory)

        return result.build()

    @staticmethod
    def _to_file_data(file_path: Path) -> File:
        stat_info = file_path.stat()
        return File(
            path=file_path,
            size=stat_info.st_size,
            date_of_creation=datetime.fromtimestamp(stat_info.st_ctime),
            date_of_last_modification=datetime.fromtimestamp(stat_info.st_mtime)
        )

    @staticmethod
    def _to_directory_data(dir_path: Path) -> Directory:
        stat_info = dir_path.stat()
        return Directory(
            path=dir_path,
            date_of_creation=datetime.fromtimestamp(stat_info.st_ctime)
        )


class DefaultFileSystemStorageModifier(StorageModifier):
    """ The storage modifier based on the InMemoryStore. """

    def create_directory(self, owner_directory_path: Path, directory: Directory):
        path = directory.path
        os.mkdir(path)

    def remove_directory(self, owner_directory_path: Path, directory: Directory):
        path = directory.path
        os.rmdir(path)

    def create_file(self, owner_directory_path: Path, file: File, contents_supplier: FileContentsSupplier):
        self._do_write_file(file, contents_supplier)

    def remove_file(self, owner_directory_path: Path, file: File):
        path = file.path
        os.remove(path)

    def update_file(self, owner_directory_path: Path, file: File, contents_supplier: FileContentsSupplier):
        self._do_write_file(file, contents_supplier)

    def _do_write_file(self, file: File, contents_supplier: FileContentsSupplier):
        path = file.path
        contents_path = contents_supplier.get_file_contents(file)
        if contents_supplier.is_file_contents_temporary(file):
            shutil.move(contents_path, path)
        else:
            shutil.copy(contents_path, path)


class DefaultFileSystemContentsSupplier(FileContentsSupplier):
    """ The default file system file contents supplier. """

    def __init__(self, top_location: pathlib.Path):
        self.top_location = top_location

    def get_file_contents(self, file: File) -> Path:
        file_path = file.path
        return self.top_location / file_path

    def is_file_contents_temporary(self, file: File) -> bool:
        return False


class DefaultFileSystemStorage(CommonStorage):
    """
    The default implementation of the Storage for the manipulation with the file systems.
    Manipulates with the files directories as with normal filesystem elements.
    """

    def __init__(self):
        super().__init__(DefaultFileSystemStorageLister(), DefaultFileSystemStorageModifier(), DefaultFileSystemContentsSupplier())