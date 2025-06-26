from typing import Union

from pathlib import Path

from commons_base import Cache
from datas import File, Directory, StorageElement


class InMemoryCache(Cache):
    """ The simple, in-memory cache implmentation. """

    def __init__(self):
        self.files = {}
        self.directories = {}

    def store_file(self, file: File):
        self.files[file.path] = file

    def store_directory(self, directory: Directory):
        self.directories[directory.path] = directory

    def has(self, path: Path) -> bool:
        return path in self.files or path in self.directories

    def get(self, path: Path) -> StorageElement:
        return self.files.get(path) or self.directories.get(path)

    def __str__(self):
        return f"InMemoryCache: files={len(self.files)}, directories={len(self.directories)})"
