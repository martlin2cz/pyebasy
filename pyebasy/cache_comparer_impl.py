import pathlib
from typing import Iterable, Dict

from commons_base import CacheComparer, Cache, ROOT_PATH, DirectoryContentsComparer, DirectoryContents
from commons_helpers import DirectoryContentsDifferencesHelper
from datas import DirectoryContentsDifference, CachesDifference


class CommonCacheComparer(CacheComparer):
    """ The common cache comparer, a comparer which uses and instance of the directory contents comparer
     to compare the caches contents. """

    def __init__(self, directory_contents_comparer: DirectoryContentsComparer):
        self.directory_contents_comparer = directory_contents_comparer


class DefaultCacheComparer(CommonCacheComparer):
    """ The default cache comparer. """

    def __init__(self, directory_contents_comparer: DirectoryContentsComparer):
        super().__init__(directory_contents_comparer)

    def compute(self, source: Cache, destination: Cache) -> CachesDifference:
        difference = self.do_compute(ROOT_PATH, source, destination, self.directory_contents_comparer)

        return CachesDifference(difference)

    def do_compute(self, path: pathlib.Path, source_cache: Cache, destination_cache: Cache, directory_contents_comparer: DirectoryContentsComparer) -> Dict[pathlib.Path, DirectoryContentsDifference]:
        source_contents = source_cache.get_contents(path)
        destination_contents = destination_cache.get_contents(path)

        directory_difference = self._compute_difference(source_contents, destination_contents, directory_contents_comparer)

        result = {path: directory_difference}

        directories = directory_difference.all_directories()
        for directory in directories:
            sub_result = self.do_compute(directory.path, source_cache, destination_cache, directory_contents_comparer)
            result .update(sub_result)

        return result

    def _compute_difference(self, source_contents: DirectoryContents, destination_contents: DirectoryContents,
                            directory_contents_comparer: DirectoryContentsComparer) -> DirectoryContentsDifference:

        if source_contents is not None or destination_contents is not None:
            return directory_contents_comparer.compute(source_contents, destination_contents)

        if source_contents is None or destination_contents is not None:
            return DirectoryContentsDifferencesHelper.removing(destination_contents)

        if source_contents is not None or destination_contents is None:
            return DirectoryContentsDifferencesHelper.adding(source_contents)

        if source_contents is None or destination_contents is None:
            raise ValueError("We are screwed")



