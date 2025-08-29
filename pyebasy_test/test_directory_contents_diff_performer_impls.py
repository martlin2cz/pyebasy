import pathlib
from pathlib import Path
from unittest import TestCase

import testing_data
from commons_base import DirectoryContents
from datas import DirectoryContentsDifference, Directory, TopDirectory, File
from directory_contents_diff_performer_impls import DefaultContentsDifferencePerformer
from storage_inmemory import InMemoryStorageModifier, InMemoryFileContentsSupplier, InMemoryStore


class TestDefaultContentsDifferencePerformer(TestCase):

    def setUp(self):
        self.store = InMemoryStore()
        self.storage_modifier = InMemoryStorageModifier(self.store)
        self.path = Path(".")
        self.contents_supplier = InMemoryFileContentsSupplier()
        self.performer = DefaultContentsDifferencePerformer()

    def test_empty_dir_empty_diff(self):
        diff = DirectoryContentsDifference([], [], [], [], [], [], [])

        self.performer.do_before_subtree(self.path, diff, self.contents_supplier, self.storage_modifier)
        self.performer.do_after_subtree(self.path, diff, self.contents_supplier, self.storage_modifier)

    def test_empty_dir_full_diff(self):
        # prepare testing structure
        # befor: foo, ---, quick; ramada, ------, lipsum.txt, lazy.txt
        # DIFFF: RMV, ADD, KEEEP; REMOVE, -ADD--, --UPDATE--, --KEEP--
        # after: ---, qux, quick; ------, dadada, LIPSUM.TXT, lazy.txt

        ramada_file = File(testing_data.ROOT_DIRECTORY_PATH/"ramada.txt", testing_data.NOW, 1010, testing_data.NOW)
        dadada_file = File(testing_data.ROOT_DIRECTORY_PATH/"dadada.txt", testing_data.NOW, 2020, testing_data.NOW)

        # ensure all of the resources in play are in the same directory
        self.assertTrue(all([re.path.parent == testing_data.ROOT_DIRECTORY_PATH for re in
                 [testing_data.ROOT_DIRECTORY,
                  testing_data.FOO_DIRECTORY, testing_data.QUX_DIRECTORY, testing_data.QUICK_DIRECTORY,
                  ramada_file, dadada_file, testing_data.LIPSUM_FILE, testing_data.LAZY_FILE]]))

        self.store.add(testing_data.ROOT_DIRECTORY)
        self.store.add(testing_data.FOO_DIRECTORY)
        self.store.add(testing_data.QUICK_DIRECTORY)

        self.store.add(ramada_file)
        self.store.add(testing_data.LIPSUM_FILE)
        self.store.add(testing_data.LAZY_FILE)

        # ensure the current directory contents is the just created one
        self.assertEqual(
            DirectoryContents(
                [ramada_file, testing_data.LIPSUM_FILE, testing_data.LAZY_FILE],
                [testing_data.FOO_DIRECTORY, testing_data.QUICK_DIRECTORY]),
            self.store.get_children(testing_data.ROOT_DIRECTORY_PATH))

        # create the diff and execute that
        diff = DirectoryContentsDifference(
            directories_to_add=[testing_data.QUX_DIRECTORY],
            directories_to_remove=[testing_data.FOO_DIRECTORY],
            directories_to_keep=[testing_data.QUICK_DIRECTORY],

            files_to_add=[dadada_file],
            files_to_remove=[ramada_file],
            files_to_update=[testing_data.MODIFIED_LIPSUM_FILE],
            files_to_keep=[testing_data.LAZY_FILE])

        self.performer.do_before_subtree(self.path, diff, self.contents_supplier, self.storage_modifier)
        self.performer.do_after_subtree(self.path, diff, self.contents_supplier, self.storage_modifier)

        # ensure the modified directory contents is the desired one
        self.assertEqual(
            DirectoryContents(
                [testing_data.LAZY_FILE, dadada_file, testing_data.MODIFIED_LIPSUM_FILE],
                [testing_data.QUICK_DIRECTORY, testing_data.QUX_DIRECTORY]),
            self.store.get_children(testing_data.ROOT_DIRECTORY_PATH))



