import os
from unittest import TestCase

from pathlib import Path

import some_testing_data
from datas import Directory, File
from storage_inmemory import InMemoryStore, InMemoryStorageLister, InMemoryStorageModifier, \
    InMemoryFileContentsSupplier


class TestInMemoryStore(TestCase):
    def test_add_remove_directory(self):
        store = InMemoryStore()
        store.add(some_testing_data.ROOT_DIRECTORY)
        store.add(some_testing_data.FOO_DIRECTORY)

        # before BAR added
        foo_contents_before_bar_added = store.get(some_testing_data.FOO_DIRECTORY.path)
        self.assertNotIn(some_testing_data.BAR_DIRECTORY, foo_contents_before_bar_added.child_directories)

        store.add(some_testing_data.BAR_DIRECTORY)

        # after BAR added
        foo_contents_after_bar_added = store.get(some_testing_data.FOO_DIRECTORY.path)
        self.assertIn(some_testing_data.BAR_DIRECTORY, foo_contents_after_bar_added.child_directories)

        store.remove(some_testing_data.BAR_DIRECTORY)

        # after BAR removed
        foo_contents_after_bar_removed = store.get(some_testing_data.FOO_DIRECTORY.path)
        self.assertNotIn(some_testing_data.BAR_DIRECTORY, foo_contents_after_bar_removed.child_directories)

    def test_add_remove_replace_file(self):
        store = InMemoryStore()
        store.add(some_testing_data.ROOT_DIRECTORY)

        # before LIPSUM added
        root_contents = store.get(some_testing_data.ROOT_DIRECTORY_PATH)
        self.assertNotIn(some_testing_data.LIPSUM_FILE, root_contents.child_files)
        self.assertNotIn(some_testing_data.MODIFIED_LIPSUM_FILE, root_contents.child_files)

        store.add(some_testing_data.LIPSUM_FILE)

        # after LIPSUM added
        root_contents = store.get(some_testing_data.ROOT_DIRECTORY_PATH)
        self.assertIn(some_testing_data.LIPSUM_FILE, root_contents.child_files)
        self.assertNotIn(some_testing_data.MODIFIED_LIPSUM_FILE, root_contents.child_files)

        store.replace(some_testing_data.LIPSUM_FILE, some_testing_data.MODIFIED_LIPSUM_FILE)

        # after LIPSUM replaced
        root_contents = store.get(some_testing_data.ROOT_DIRECTORY_PATH)
        self.assertNotIn(some_testing_data.LIPSUM_FILE, root_contents.child_files)
        self.assertIn(some_testing_data.MODIFIED_LIPSUM_FILE, root_contents.child_files)

        store.remove(some_testing_data.MODIFIED_LIPSUM_FILE)

        # after LIPSUM removed
        root_contents = store.get(some_testing_data.ROOT_DIRECTORY_PATH)
        self.assertNotIn(some_testing_data.LIPSUM_FILE, root_contents.child_files)
        self.assertNotIn(some_testing_data.MODIFIED_LIPSUM_FILE, root_contents.child_files)

    def test_get(self):
        store = InMemoryStore()
        some_testing_data.foreach_element(True, False,
            lambda e: store.add(e)
        )

        # Check contents of a few directories
        foo_contents = store.get(Path("testing-files"))
        self.assertIn(some_testing_data.FOO_DIRECTORY, foo_contents.child_directories)
        self.assertIn(some_testing_data.QUX_DIRECTORY, foo_contents.child_directories)
        self.assertIn(some_testing_data.LIPSUM_FILE, foo_contents.child_files)

        bar_contents = store.get(Path("testing-files/foo/bar"))
        self.assertIn(some_testing_data.BAZ_DIRECTORY, bar_contents.child_directories)
        self.assertIn(some_testing_data.AUX_DIRECTORY, bar_contents.child_directories)

        aux_contents = store.get(Path("testing-files/foo/bar/_aux_"))
        self.assertIn(some_testing_data.DOLOR_FILE, aux_contents.child_files)
        self.assertIn(some_testing_data.IPSUM_FILE, aux_contents.child_files)


class TestInMemoryStorageLister(TestCase):

    def setUp(self):
        store = InMemoryStore()
        some_testing_data.foreach_element(True, False,
            lambda e: store.add(e)
        )

        self.lister = InMemoryStorageLister(store)

    def test_list_directory(self):
        contents = self.lister.list_directory(some_testing_data.ROOT_DIRECTORY_PATH)
        self.assertIn(some_testing_data.FOO_DIRECTORY, contents.child_directories)
        self.assertIn(some_testing_data.LIPSUM_FILE, contents.child_files)


class TestInMemoryStorageModifier(TestCase):

    def setUp(self):
        self.store = InMemoryStore()
        some_testing_data.foreach_element(True,False,
                                          lambda e: self.store.add(e)
                                          )
        self.modifier = InMemoryStorageModifier(self.store)
        self.contents_supplier = InMemoryFileContentsSupplier()

    def test_create_directory(self):
        self.modifier.create_directory(some_testing_data.BROWN_DIRECTORY.path.parent, some_testing_data.BROWN_DIRECTORY)

        owner_contents = self.store.get(some_testing_data.FOO_DIRECTORY.path)
        self.assertIn(some_testing_data.BROWN_DIRECTORY, owner_contents.child_directories)

    def test_remove_directory(self):
        self.modifier.remove_file(some_testing_data.LOREM_FILE.path.parent, some_testing_data.LOREM_FILE)
        self.modifier.remove_directory(some_testing_data.BAZ_DIRECTORY.path.parent, some_testing_data.BAZ_DIRECTORY)

        owner_contents = self.store.get(some_testing_data.BAR_DIRECTORY.path)
        self.assertNotIn(some_testing_data.BAZ_DIRECTORY, owner_contents.child_directories)

    def test_create_file(self):
        self.modifier.create_file(some_testing_data.BROWN_FILE.path.parent, some_testing_data.BROWN_FILE, self.contents_supplier)

        owner_contents = self.store.get(some_testing_data.FOO_DIRECTORY.path)
        self.assertIn(some_testing_data.BROWN_FILE, owner_contents.child_files)

    def test_remove_file(self):
        self.modifier.remove_file(some_testing_data.LOREM_FILE.path.parent, some_testing_data.LOREM_FILE)

        owner_contents = self.store.get(some_testing_data.BAZ_DIRECTORY.path)
        self.assertNotIn(some_testing_data.LOREM_FILE, owner_contents.child_files)

    def test_update_file(self):
        self.modifier.update_file(some_testing_data.LIPSUM_FILE.path.parent, some_testing_data.MODIFIED_LIPSUM_FILE, self.contents_supplier)

        owner_contents = self.store.get(some_testing_data.ROOT_DIRECTORY_PATH)
        self.assertNotIn(some_testing_data.LIPSUM_FILE, owner_contents.child_files)
        self.assertIn(some_testing_data.MODIFIED_LIPSUM_FILE, owner_contents.child_files)


class TestInMemoryFileContentsSupplier(TestCase):

    def setUp(self):
        self.contents_supplier = InMemoryFileContentsSupplier()

    def test_get_file_contents(self):
        file = some_testing_data.LIPSUM_FILE

        path = self.contents_supplier.get_file_contents(file)
        contents = path.read_text()

        self.assertTrue(self.contents_supplier.is_file_contents_temporary(file))
        self.assertEqual("Boo, this is sample file lipsum.txt which shall have 321 bytes.\n", contents)
