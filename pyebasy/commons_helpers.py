from typing import Union

from commons_base import DirectoryContents, Storage, StorageLister
from datas import Directory, File, StorageElement


########################################################################################################################


class CommonStorage(Storage):
    """ The convience storage, which stores the lister as a field. """

    def __init__(self, lister: StorageLister):
        self.lister = lister

    def lister(self) -> StorageLister:
        return self.lister


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

    def add(self, file_or_directory: StorageElement):
        """ Adds the specified file or directory to the builder. """
        if isinstance(file_or_directory, File):
            self.add_file(file_or_directory)

        if isinstance(file_or_directory, Directory):
            self.add_directory(file_or_directory)

    def build(self) -> DirectoryContents:
        """ Constructs the appropriet DirectoryContents instance. """
        return DirectoryContents(self.files, self.directories)

########################################################################################################################