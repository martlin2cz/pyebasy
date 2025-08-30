from typing import Union

from commons_base import DirectoryContents, Storage, StorageLister, StorageModifier, FileContentsSupplier
from datas import Directory, File, StorageElement, CommonStorageElement, DirectoryContentsDifference


########################################################################################################################


class CommonStorage(Storage):
    """ The convience storage, which stores the lister, modifier and contents supplier as the fields. """

    def __init__(self, lister: StorageLister, modifier: StorageModifier, contents_supplier: FileContentsSupplier):
        self._lister = lister
        self._modifier = modifier
        self._contents_supplier = contents_supplier

    def lister(self) -> StorageLister:
        return self._lister

    def modifier(self) -> StorageModifier:
        return self._modifier

    def contents_supplier(self) -> FileContentsSupplier:
        return self._contents_supplier

########################################################################################################################


class DirectoryContentsBuilder:
    """ The mutable builder of the DirectoryContents instances. """

    def __init__(self, files = None, directories = None):
        self.files = files if files is not None else []
        self.directories = directories if directories is not None else []

    @staticmethod
    def from_existing(contents: DirectoryContents) -> 'DirectoryContentsBuilder':
        return DirectoryContentsBuilder(contents.child_files, contents.child_directories)

    def add_file(self, file: File):
        """ Adds a file to the builder. """
        self.files.append(file)

    def add_directory(self, directory: Directory):
        """ Adds a directory to the builder. """
        self.directories.append(directory)

    def add(self, file_or_directory: CommonStorageElement):
        """ Adds the specified file or directory to the builder. """
        if isinstance(file_or_directory, File):
            self.add_file(file_or_directory)

        if isinstance(file_or_directory, Directory):
            self.add_directory(file_or_directory)

    def build(self) -> DirectoryContents:
        """ Constructs the appropriet DirectoryContents instance. """
        return DirectoryContents(self.files, self.directories)

########################################################################################################################


class DirectoryContentsDifferencesHelper:
    """ A simple builder/factory for DirectoryContentsDifferences in some simple cases. """

    @staticmethod
    def adding(contents: DirectoryContents) -> DirectoryContentsDifference:
        """ Constructs the directory contents difference, which completelly adds specified directory contents. """
        return DirectoryContentsDifference(
            directories_to_add=contents.child_directories,
            files_to_add=contents.child_files,
            directories_to_remove=[],
            directories_to_keep=[],
            files_to_remove=[],
            files_to_update=[],
            files_to_keep=[])

    @staticmethod
    def removing(contents: DirectoryContents) -> DirectoryContentsDifference:
        """ Constructs the directory contents difference, which removes the contents of the specified directory. """
        return DirectoryContentsDifference(
            directories_to_remove=contents.child_directories,
            files_to_remove=contents.child_files,
            directories_to_add=[],
            directories_to_keep=[],
            files_to_add=[],
            files_to_update=[],
            files_to_keep=[])

    @staticmethod
    def same(contents: DirectoryContents) -> DirectoryContentsDifference:
        """ Constructs the directory contents difference, which has no changes. """
        return DirectoryContentsDifference(
            directories_to_add=[],
            files_to_add=[],
            directories_to_remove=[],
            directories_to_keep=contents.child_directories,
            files_to_remove=[],
            files_to_update=[],
            files_to_keep=contents.child_files)

