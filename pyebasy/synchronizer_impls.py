import pathlib

import loggr
from cache_comparer_impl import DefaultCacheComparer
from cache_updater_impls import PrimitiveCacheUpdater
from caches_diff_performer_impl import DefaultCachesDifferencePerformer
from commons_base import Synchronizer, Storage, Cache, CacheComparer, FileContentsSupplier, StorageLister, \
    StorageModifier, CachesSynchronizer, CachesDifferencePerformer
from directory_contents_diff_performer_impls import DefaultContentsDifferencePerformer
from dirs_differ_simple import SimpleDirectoryContentsComparer


class CommonCachesSynchronizer(CachesSynchronizer):
    """ The common caches synchronizer. """

    def __init__(self, caches_comparer: CacheComparer, caches_diff_performer: CachesDifferencePerformer):
        self.caches_comparer = caches_comparer
        self.caches_diff_performer = caches_diff_performer

    def execute(self, source_cache: Cache,  destination_cache: Cache, source_contents_supplier: FileContentsSupplier, destination_modifier: StorageModifier):
        loggr.log_overall("Comparing the caches ...")
        caches_diff = self.caches_comparer.compute(source_cache, destination_cache)
        loggr.log_overall("Compared!")

        loggr.log_overall("Applying the changes ...")
        self.caches_diff_performer.apply(caches_diff, source_contents_supplier, destination_modifier)
        loggr.log_overall("Applied!")


class DefaultCachesSynchronizer(CommonCachesSynchronizer):
    """ The default caches synchronizer. """

    def __init__(self, caches_comparer: DefaultCacheComparer, caches_diff_performer: DefaultCachesDifferencePerformer):
        super().__init__(caches_comparer, caches_diff_performer)

    @staticmethod
    def create():
        """ Creates an instance. """
        dirs_comparer = SimpleDirectoryContentsComparer()
        caches_comparer = DefaultCacheComparer(dirs_comparer)

        dir_diff_performer = DefaultContentsDifferencePerformer()
        caches_diff_performer = DefaultCachesDifferencePerformer(dir_diff_performer)

        return DefaultCachesSynchronizer(caches_comparer, caches_diff_performer)

#######################################################################################################################


class DefaultSynchronizer(Synchronizer):
    """ The default synchronizer. """

    def __init__(self, source_cache: Cache, destination_cache: Cache, update_source_cache: bool, update_destination_cache: bool):
        self.source_cache = source_cache
        self.destination_cache = destination_cache

        self.caches_synchronizer = DefaultCachesSynchronizer.create()

        self.update_source_cache = update_source_cache
        self.update_destination_cache = update_destination_cache

    def synchronize(self, source: Storage, destination: Storage):
        caches_updater = PrimitiveCacheUpdater()

        if self.update_source_cache:
            loggr.log_overall("Updating the source cache ...")
            source_lister = source.lister()
            caches_updater.update(source_lister, self.source_cache)
            loggr.log_overall("Updated the source cache!")
        else:
            loggr.log_overall("Source cache update skipped")

        if self.update_destination_cache:
            loggr.log_overall("Updating the destination cache ...")
            destination_lister = destination.lister()
            caches_updater.update(destination_lister, self.destination_cache)
            loggr.log_overall("Updated the destination cache!")
        else:
            loggr.log_overall("Destination cache update skipped")

        source_contents_supplier = source.contents_supplier()
        destination_modifier = destination.modifier()

        loggr.log_overall("Synchronizing the cached storage ...")
        self.caches_synchronizer.execute(self.source_cache, self.destination_cache, source_contents_supplier, destination_modifier)
        loggr.log_overall("Synchronized the cached storage!")
