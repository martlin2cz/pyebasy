import pathlib

from pathlib import Path

from commons_base import CacheUpdater, StorageLister, Cache
from datas import TopDirectory


class PrimitiveCacheUpdater(CacheUpdater):
    """ The initial, primitive, cache updater implementation. Without any optinamisations, just walks the directories three. """

    def update(self, storage_lister: StorageLister, cache: Cache):

        path = pathlib.Path(".")  #TODO remove
        top_directory = TopDirectory(path)
        cache.store_directory(top_directory)

        self._do_update(storage_lister, cache, path)

    def _do_update(self, storage_lister: StorageLister, cache: Cache, path: Path):
        """ Actually updates (Recursivelly) directory with a specified path. """

        contents = storage_lister.list_directory(path)

        for file in contents.child_files:
            cache.store_file(file)

        for directory in contents.child_directories:
            cache.store_directory(directory)

            child_directory_path = directory.path
            self._do_update(storage_lister, cache, child_directory_path)

