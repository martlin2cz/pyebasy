from typing import Union

from pathlib import Path

from base_commons import Cache
from datas import File, Directory


class InMemoryCache(Cache):
    def __init__(self):
        self._store = {}

    def store_file(self, file: File):
        if file.path in self._store:
            raise KeyError(f'File {file.path} already in the cache')

        self._store[file.path] = file

    def store_directory(self, directory: Directory):
        if directory.path in self._store:
            raise KeyError(f'Directory {directory.path} already in the cache')

        self._store[directory.path] = directory

    def has(self, path: Path):
        return path in self._store

    def get(self, path: Path) -> Union[File, Directory]:
        if path not in self._store:
            raise KeyError(f'No file or directory with a path {path} in the cache')

        return self._store.get(path)
