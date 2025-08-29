from typing import Callable, Tuple

import pathlib
import functools

import loggr
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
        loggr.log_informative(f"Performing the {len(diff)} changes in the cache ...")

        root_path = pathlib.Path(".")
        self._do_apply(root_path, diff, contents_supplier, storage_modifier)
        loggr.log_informative("Performed the changes in the cache!")

    def _do_apply(self, path: pathlib.Path, diff, contents_supplier, storage_modifier):
        loggr.log_detailed(f"Performing the changes of the directory {path}")

        dir_diff = diff.change_of_directory(path)
        children = dir_diff.all_directories()

        self.directory_diff_performer.do_before_subtree(path, dir_diff, contents_supplier, storage_modifier)

        for child in children:
            child_path = child.path
            self._do_apply(child_path, diff, contents_supplier, storage_modifier)

        self.directory_diff_performer.do_after_subtree(path, dir_diff, contents_supplier, storage_modifier)

        loggr.log_detailed(f"Performed the changes of the directory {path}")

