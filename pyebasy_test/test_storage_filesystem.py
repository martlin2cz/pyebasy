from pathlib import Path
from unittest import TestCase

from storage_filesystem import DefaultFileSystemStorageLister


class TestDefaultFileSystemStorageLister(TestCase):

    def setUp(self):
        self.lister = DefaultFileSystemStorageLister()

    def test_list(self):
        # expect
        expected_files_paths = {
            Path("testing-files/lipsum.txt"),
        }
        expected_directories_paths = {
            Path("testing-files/foo"),
            Path("testing-files/qux"),
        }

        # call
        root = Path("testing-files")
        contents = self.lister.list_directory(root)

        # post-process
        actual_files_paths = {item.path for item in contents.child_files}
        actual_directories_paths = {item.path for item in contents.child_directories}

        # compare
        self.assertEqual(actual_files_paths, expected_files_paths)
        self.assertEqual(actual_directories_paths, expected_directories_paths)

