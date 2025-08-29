import sys

import pathlib

from cache_sqlite import SqliteCache
from storage_filesystem import DefaultFileSystemStorage
from synchronizer_impls import DefaultSynchronizer

source_cache = SqliteCache(pathlib.Path('source.db'))
destination_cache = SqliteCache(pathlib.Path('destination.db'))

synchronizer = DefaultSynchronizer(
    source_cache=source_cache,
    destination_cache=destination_cache,
    update_source_cache=True,
    update_destination_cache=True)

source_top_path = pathlib.Path(sys.argv[1])
source_storage = DefaultFileSystemStorage(source_top_path)

destination_top_path = pathlib.Path(sys.argv[2])
destination_storage = DefaultFileSystemStorage(destination_top_path)

synchronizer.synchronize(source_storage, destination_storage)
