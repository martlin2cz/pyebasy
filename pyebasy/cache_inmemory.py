from typing import Union

from pathlib import Path

import loggr
from commons_base import Cache
from commons_base import Cache, DirectoryContents
from datas import File, Directory, StorageElement, ADirectory, TopDirectory


class InMemoryCache(Cache):
    """ The simple, in-memory cache implmentation. """

    def __init__(self):
        self.files = {}
        self.directories = {}

    def store_file(self, file: File):
        loggr.log_detailed(f"Storing file {file.path} into cache")
        self.files[file.path] = file

    def store_directory(self, directory: ADirectory):
        loggr.log_detailed(f"Storing directory {directory.path} into cache")
        self.directories[directory.path] = directory

    def has(self, path: Path) -> bool:
        return path in self.files or path in self.directories

    def get(self, path: Path) -> StorageElement:
        return self.files.get(path) or self.directories.get(path)

    def get_contents(self, path: Path) -> DirectoryContents:
        files = [f for p, f in self.files.items() if p.parent == path]
        # exclude top directory, because that can never be a child of anything
        directories = [d for p, d in self.directories.items() if p.parent == path and not isinstance(d, TopDirectory)]

        return DirectoryContents(files, directories)

    def __str__(self):
        return f"InMemoryCache: files={len(self.files)}, directories={len(self.directories)})"
