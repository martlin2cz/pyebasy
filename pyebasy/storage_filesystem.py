from datetime import datetime

from pathlib import Path

from commons_base import Storage, StorageLister, DirectoryContents
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


class DefaultFileSystemStorage(CommonStorage):
    """
    The default implementation of the Storage for the manipulation with the file systems.
    Manipulates with the files directories as with normal filesystem elements.
    """

    def __init__(self):
        super().__init__(DefaultFileSystemStorageLister())