from commons_base import CachesDifferencePerformer, StorageModifier, FileContentsSupplier, \
    DirectoryContentsDifferencePerformer
from datas import CachesDifference


class CommonCachesDifferencePerformer(CachesDifferencePerformer):
    """ Common caches difference performer, which uses the directory difference performer to do the job. """

    def __init__(self, directory_diff_performer: DirectoryContentsDifferencePerformer):
        self.directory_diff_performer = directory_diff_performer


class DefaultCachesDifferencePerformer(CommonCachesDifferencePerformer):
    """ Default caches difference performer. """

    def __init__(self, directory_diff_performer: DirectoryContentsDifferencePerformer):
        super().__init__(directory_diff_performer)

    def apply(self, diff: CachesDifference, contents_supplier: FileContentsSupplier, storage_modifier: StorageModifier):
        for path in diff.paths():
            dir_diff = diff.change_of_directory(path)
            self.directory_diff_performer.execute(path, dir_diff, contents_supplier, storage_modifier)