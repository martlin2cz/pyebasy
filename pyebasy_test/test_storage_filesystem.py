from pathlib import Path
from unittest import TestCase
import tempfile

import some_testing_data
from datas import Directory, File
from storage_filesystem import DefaultFileSystemStorageLister, DefaultFileSystemStorageModifier, \
    DefaultFileSystemContentsSupplier
from storage_inmemory import InMemoryFileContentsSupplier


class TestDefaultFileSystemStorageLister(TestCase):

    def setUp(self):
        self.lister = DefaultFileSystemStorageLister(some_testing_data.TOP_DIRECTORY_LOCATION)

    def test_list(self):
        # expect
        expected_files_paths = {
            Path("./lipsum.txt"),
        }
        expected_directories_paths = {
            Path("./foo"),
            Path("./qux"),
        }

        # call
        root = Path(".")
        contents = self.lister.list_directory(root)

        # post-process
        actual_files_paths = {item.path for item in contents.child_files}
        actual_directories_paths = {item.path for item in contents.child_directories}

        # compare
        self.assertEqual(actual_files_paths, expected_files_paths)
        self.assertEqual(actual_directories_paths, expected_directories_paths)


class TestDefaultFileSystemStorageModifier(TestCase):

    def setUp(self):
        self.modifier = DefaultFileSystemStorageModifier(some_testing_data.TOP_DIRECTORY_LOCATION)
        self.contents_supplier = InMemoryFileContentsSupplier()

    def test_directories(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)

            # testing directories
            foo_dir_path = tmpdir_path/"foo"
            foo_dir = Directory(foo_dir_path, some_testing_data.NOW)

            bar_dir_path = tmpdir_path/"foo"/"bar"
            bar_dir = Directory(bar_dir_path, some_testing_data.NOW)

            # create directories
            self.modifier.create_directory(tmpdir_path, foo_dir)
            self.assertTrue(foo_dir_path.is_dir())

            self.modifier.create_directory(foo_dir_path, bar_dir)
            self.assertTrue(bar_dir_path.is_dir())

            # remove directories
            self.modifier.remove_directory(foo_dir_path, bar_dir)
            self.assertFalse(bar_dir_path.is_dir())

            self.modifier.remove_directory(tmpdir_path, foo_dir)
            self.assertFalse(foo_dir_path.is_dir())

    def test_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)

            # testing files
            foo_dir_path = tmpdir_path/"foo"
            foo_dir_path.mkdir()

            lorem_file_path = tmpdir_path/"lorem.txt"
            lorem_file = File(lorem_file_path, some_testing_data.NOW, 52, some_testing_data.NOW)
            another_lorem_file = File(lorem_file_path, some_testing_data.NOW, 5200, some_testing_data.NOW)

            ipsum_file_path = foo_dir_path/"ipsum.txt"
            ipsum_file = File(ipsum_file_path, some_testing_data.NOW, 53, some_testing_data.NOW)
            another_ipsum_file = File(ipsum_file_path, some_testing_data.NOW, 5300, some_testing_data.NOW)

            # create files
            self.modifier.create_file(tmpdir_path, lorem_file, self.contents_supplier)
            self.assertTrue(lorem_file_path.is_file())

            self.modifier.create_file(foo_dir_path, ipsum_file, self.contents_supplier)
            self.assertTrue(ipsum_file_path.is_file())

            # update files
            self.modifier.update_file(tmpdir_path, another_lorem_file, self.contents_supplier)
            self.assertTrue(lorem_file_path.is_file())

            self.modifier.update_file(foo_dir_path, another_ipsum_file, self.contents_supplier)
            self.assertTrue(ipsum_file_path.is_file())

            # remove files
            self.modifier.remove_file(tmpdir_path, lorem_file)
            self.assertFalse(lorem_file_path.is_file())

            self.modifier.remove_file(foo_dir_path, ipsum_file)
            self.assertFalse(ipsum_file_path.is_file())


class TestDefaultFileSystemContentsSupplier(TestCase):

    def setUp(self):
        self.contents_supplier = DefaultFileSystemContentsSupplier(some_testing_data.TOP_DIRECTORY_LOCATION)

    def test_get_file_contents(self):
        file = some_testing_data.LIPSUM_FILE
        path = self.contents_supplier.get_file_contents(file)
        contents = path.read_text()
        self.assertEqual("hi\n", contents)
