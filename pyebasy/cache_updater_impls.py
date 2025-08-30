from pathlib import Path

import loggr
from commons_base import CacheUpdater, StorageLister, Cache
from datas import TopDirectory


class PrimitiveCacheUpdater(CacheUpdater):
    """ The initial, primitive, cache updater implementation. Without any optinamisations, just walks the directories three. """

    def update(self, storage_lister: StorageLister, cache: Cache):
        loggr.log_informative("Updating the cache ... ")

        top_directory = TopDirectory()
        cache.store_directory(top_directory)

        path = Path(".")
        self._do_update(storage_lister, cache, path)

        loggr.log_informative("Updated cache!")

    def _do_update(self, storage_lister: StorageLister, cache: Cache, path: Path):
        """ Actually updates (Recursivelly) directory with a specified path. """

        loggr.log_detailed(f"Updating cache of {path}")

        contents = storage_lister.list_directory(path)

        for file in contents.child_files:
            cache.store_file(file)

        for directory in contents.child_directories:
            cache.store_directory(directory)

            child_directory_path = directory.path
            self._do_update(storage_lister, cache, child_directory_path)

