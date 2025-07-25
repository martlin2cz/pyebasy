import dataclasses
from dataclasses import asdict
from typing import List, Any, Dict, Callable, TypeVar

import datacompy
import pandas as pd
import pathlib

from commons_base import DirectoryContentsComparer, DirectoryContents
from datas import DirectoryContentsDifference, StorageElement, File, Directory

SET = TypeVar('SET')


class ListCompareResult:
    """ A quick result of comparing two lists of elements. """

    def __init__(self):
        self.only_in_source = []
        self.only_in_destination = []
        self.same = []
        self.modified = []

    def add_only_in_source(self, path: pathlib.Path):
        self.only_in_source.append(path)

    def add_only_in_destination(self, path: pathlib.Path):
        self.only_in_destination.append(path)

    def add_same(self, path: pathlib.Path):
        self.same.append(path)

    def add_modified(self, path: pathlib.Path):
        self.modified.append(path)


def files_are_same(source_file: File, destination_file: File) -> bool:
    """ Function comparing two files. """
    if source_file.size != destination_file.size:
        return False
    if source_file.date_of_last_modification != destination_file.date_of_last_modification:
        return False

    return True


def directories_are_same(source_directory: Directory, destination_directory: Directory) -> bool:
    """ Function comparing two directories. """
    return True


class SimpleDirectoryContentsComparer(DirectoryContentsComparer):
    """ The simple implementation of the DirectoryContentsComparer. Uses the native way (literal lists comparasion). """

    def compute(self, source_contents: DirectoryContents, destination_contents: DirectoryContents) \
            -> DirectoryContentsDifference:

        source_files_dict = {f.path: f for f in source_contents.child_files}
        source_directories_dict = {d.path: d for d in source_contents.child_directories}
        destination_files_dict = {f.path: f for f in destination_contents.child_files}
        destination_directories_dict = {d.path: d for d in destination_contents.child_directories}

        files_diff = self._do_compare(source_files_dict, destination_files_dict, files_are_same)
        directories_diff = self._do_compare(source_directories_dict, destination_directories_dict, directories_are_same)

        return self._to_report(source_files_dict, destination_files_dict,
                               source_directories_dict, destination_directories_dict,
                               files_diff, directories_diff)

    @staticmethod
    def _do_compare(source_elements_dict: Dict[pathlib.Path, SET],
                    destination_elements_dict: Dict[pathlib.Path, SET],
                    comparer: Callable[[SET, SET], bool]) -> ListCompareResult:

        """ Compares the two lists of either files or directories. """

        all_paths = sorted({*(source_elements_dict.keys()), *(destination_elements_dict.keys())})
        result = ListCompareResult()

        for path in all_paths:
            in_source = path in source_elements_dict
            in_destination = path in destination_elements_dict

            if in_source and in_destination:
                same = comparer(source_elements_dict[path], destination_elements_dict[path])
                if same:
                    result.add_same(path)
                else:
                    result.add_modified(path)

            if in_source and not in_destination:
                result.add_only_in_source(path)

            if not in_source and in_destination:
                result.add_only_in_destination(path)

            if not in_source and not in_destination:
                raise ValueError("We are doomed!")

        return result

    @staticmethod
    def _to_report(source_files_dict: Dict[pathlib.Path, File], destination_files_dict: Dict[pathlib.Path, File],
                   source_directories_dict: Dict[pathlib.Path, Directory], destination_directories_dict: Dict[pathlib.Path, Directory],
                   files_diff: ListCompareResult, directories_diff: ListCompareResult) -> DirectoryContentsDifference:

        """ Converts the files and directories list compare results into the actual directory contents difference. """

        directories_to_add = [source_directories_dict[p] for p in directories_diff.only_in_source]
        directories_to_remove = [destination_directories_dict[p] for p in directories_diff.only_in_destination]
        directories_to_keep = [destination_directories_dict[p] for p in directories_diff.same]

        files_to_add = [source_files_dict[p] for p in files_diff.only_in_source]
        files_to_remove = [destination_files_dict[p] for p in files_diff.only_in_destination]
        files_to_keep = [destination_files_dict[p] for p in files_diff.same]
        files_to_update = [source_files_dict[p] for p in files_diff.modified]

        return DirectoryContentsDifference(
            directories_to_add,
            directories_to_remove,
            directories_to_keep,

            files_to_add,
            files_to_remove,
            files_to_update,
            files_to_keep
        )
