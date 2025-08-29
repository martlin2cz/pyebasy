import sys

import pathlib

import argparser
import loggr
from cache_inmemory import InMemoryCache
from cache_sqlite import SqliteCache
from storage_dry_run import DryRunStorage
from storage_filesystem import DefaultFileSystemStorage
from synchronizer_impls import DefaultSynchronizer


def prepare_cache(cache_kind: str, name: str):
    loggr.log_detailed(f"Will use {cache_kind} cache for {name}")

    if cache_kind == argparser.SQLITE_CACHE:
        cache_file = pathlib.Path(f"{name}.db")
        SqliteCache.drop_existing(cache_file)

        return SqliteCache(cache_file)

    if cache_kind == argparser.IN_MEMORY_CACHE:
        return InMemoryCache()


def prepare_storage(storage_path_str: str, name: str, dry_run: bool = False):
    loggr.log_detailed(f"Will use {storage_path_str} path for {name} storage{' with dry run enabled' if dry_run else ''}")

    storage_path = pathlib.Path(storage_path_str)
    if not storage_path.is_dir():
        raise ValueError(f"Directory {storage_path} doesn't exist")

    storage = DefaultFileSystemStorage(storage_path)
    if dry_run:
        storage = DryRunStorage.wrap(storage)
    return storage


def run():
    parsed = argparser.parse_args()

    source_cache = prepare_cache(parsed.source_cache_format, "source")
    destination_cache = prepare_cache(parsed.source_cache_format, "destination")

    source_storage = prepare_storage(parsed.SOURCE_PATH, "source")
    destination_storage = prepare_storage(parsed.DESTINATION_PATH, "destination", parsed.dry_run)

    synchronizer = DefaultSynchronizer(
        source_cache=source_cache,
        destination_cache=destination_cache,
        update_source_cache=parsed.update_source_cache,
        update_destination_cache=parsed.update_destination_cache)

    synchronizer.synchronize(source_storage, destination_storage)


if __name__ == '__main__':
    run()

