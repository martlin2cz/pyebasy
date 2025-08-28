from typing import Callable, Tuple

import pathlib
import functools

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
        paths_sorted = sorted(diff.paths(), key=lambda p: self.compute_sort_key(diff, p))

        for path in paths_sorted:
            dir_diff = diff.change_of_directory(path)

            self.directory_diff_performer.execute(path, dir_diff, contents_supplier, storage_modifier)

    #TODO: the key sorting should get extracted into standalone component
    def compute_sort_key(self, diff: CachesDifference, path) -> Tuple[int, pathlib.Path, str]:
        action = self.compute_action(diff, path)

        priority = None
        if action == "remove":
            priority = -1
        if action == "add":
            priority = +1
        if action == "keep":
            priority = 0

        depth = len(path.parents)

        return priority * depth, path, action

    def compute_action(self, diff: CachesDifference, path: pathlib.Path):
        if path == pathlib.Path("."):
            return "keep"

        parent = path.parent
        parent_diff = diff.change_of_directory(parent)
        if path in [e.path for e in parent_diff.directories_to_remove]:
            return "remove"
        if path in [e.path for e in parent_diff.directories_to_add]:
            return "add"
        if path in [e.path for e in parent_diff.directories_to_keep]:
            return "keep"

        raise ValueError(f"Unrecognised path: {path}")
