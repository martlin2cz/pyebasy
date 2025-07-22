from pathlib import Path

from commons_base import DirectoryContentsDifferencePerformer, StorageModifier, FileContentsSupplier
from datas import DirectoryContentsDifference


class DefaultContentsDifferencePerformer(DirectoryContentsDifferencePerformer):
    """ The default implementation of the directory contents difference performer.  """

    def execute(self, directory_path: Path, diff: DirectoryContentsDifference, contents_supplier: FileContentsSupplier, storage_modifier: StorageModifier):
        for file in diff.files_to_add:
            storage_modifier.create_file(directory_path, file, contents_supplier)

        for file in diff.files_to_remove:
            storage_modifier.remove_file(directory_path, file)

        for file in diff.files_to_update:
            storage_modifier.update_file(directory_path, file, contents_supplier)

        for directory in diff.directories_to_add:
            storage_modifier.create_directory(directory_path, directory)

        for directory in diff.directories_to_remove:
            storage_modifier.remove_directory(directory_path, directory)
