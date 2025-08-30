import pathlib
from unittest import TestCase

import testing_data
from caches_diff_performer_impl import DefaultCachesDifferencePerformer
from commons_base import DirectoryContents
from commons_helpers import DirectoryContentsDifferencesHelper
from datas import CachesDifference, DirectoryContentsDifference, TopDirectory
from directory_contents_diff_performer_impls import DefaultContentsDifferencePerformer
from storage_inmemory import InMemoryStorageModifier, InMemoryFileContentsSupplier, InMemoryStore


class TestDefaultCachesDifferencePerformer(TestCase):
    def test_apply_empty_diff_to_empty_store(self):
        diff = CachesDifference({})
        store = InMemoryStore()

        self._do_apply_diff(diff, store)

    def test_apply_empty_diff_to_full_store(self):
        diff = CachesDifference({})

        store = InMemoryStore()
        test_data = testing_data.SomeTestingStorageElements(True, False)
        test_data.foreach_element(lambda e: store.add(e))

        self._do_apply_diff(diff, store)

        test_data.foreach_element(lambda e: self.assertEqual(e, store.get_element(e.path)))

    def test_apply_same_diff_to_full_store(self):
        root_diff = DirectoryContentsDifferencesHelper.same(
            DirectoryContents([testing_data.LIPSUM_FILE], [testing_data.FOO_DIRECTORY, testing_data.QUX_DIRECTORY]))

        foo_diff = DirectoryContentsDifferencesHelper.same(
            DirectoryContents([], [testing_data.BAR_DIRECTORY]))

        bar_diff = DirectoryContentsDifferencesHelper.same(
            DirectoryContents([], [testing_data.AUX_DIRECTORY, testing_data.BAZ_DIRECTORY]))

        baz_diff = DirectoryContentsDifferencesHelper.same(
            DirectoryContents([testing_data.LOREM_FILE], []))

        aux_diff = DirectoryContentsDifferencesHelper.same(
            DirectoryContents([testing_data.DOLOR_FILE, testing_data.IPSUM_FILE], []))

        qux_diff = DirectoryContentsDifferencesHelper.same(
            DirectoryContents([], [testing_data.QUUX_DIRECTORY]))

        quux_diff = DirectoryContentsDifferencesHelper.same(
            DirectoryContents([testing_data.SIT_FILE], []))

        caches_difference = CachesDifference({
            testing_data.ROOT_DIRECTORY_PATH: root_diff,
            testing_data.FOO_DIRECTORY.path: foo_diff,
            testing_data.BAR_DIRECTORY.path: bar_diff,
            testing_data.BAZ_DIRECTORY.path: baz_diff,
            testing_data.AUX_DIRECTORY.path: aux_diff,
            testing_data.QUX_DIRECTORY.path: qux_diff,
            testing_data.QUUX_DIRECTORY.path: quux_diff
        })

        store = InMemoryStore()
        test_data = testing_data.SomeTestingStorageElements(True, False)
        test_data.foreach_element(lambda e: store.add(e))

        self._do_apply_diff(caches_difference, store)

        test_data.foreach_element(lambda e: self.assertEqual(e, store.get_element(e.path)))

    def test_apply_adding_diff_to_empty_store(self):
        root_diff = DirectoryContentsDifferencesHelper.adding(
            DirectoryContents([testing_data.LIPSUM_FILE], [testing_data.FOO_DIRECTORY, testing_data.QUX_DIRECTORY]))

        foo_diff = DirectoryContentsDifferencesHelper.adding(
            DirectoryContents([], [testing_data.BAR_DIRECTORY]))

        bar_diff = DirectoryContentsDifferencesHelper.adding(
            DirectoryContents([], [testing_data.AUX_DIRECTORY, testing_data.BAZ_DIRECTORY]))

        baz_diff = DirectoryContentsDifferencesHelper.adding(
            DirectoryContents([testing_data.LOREM_FILE], []))

        aux_diff = DirectoryContentsDifferencesHelper.adding(
            DirectoryContents([testing_data.DOLOR_FILE, testing_data.IPSUM_FILE], []))

        qux_diff = DirectoryContentsDifferencesHelper.adding(
            DirectoryContents([], [testing_data.QUUX_DIRECTORY]))

        quux_diff = DirectoryContentsDifferencesHelper.adding(
            DirectoryContents([testing_data.SIT_FILE], []))

        caches_difference = CachesDifference({
            testing_data.ROOT_DIRECTORY_PATH: root_diff,
            testing_data.FOO_DIRECTORY.path: foo_diff,
            testing_data.BAR_DIRECTORY.path: bar_diff,
            testing_data.BAZ_DIRECTORY.path: baz_diff,
            testing_data.AUX_DIRECTORY.path: aux_diff,
            testing_data.QUX_DIRECTORY.path: qux_diff,
            testing_data.QUUX_DIRECTORY.path: quux_diff
        })

        store = InMemoryStore()
        store.add(TopDirectory())
        self._do_apply_diff(caches_difference, store)

        test_data = testing_data.SomeTestingStorageElements(True, False)
        test_data.foreach_element(lambda e: self.assertEqual(e, store.get_element(e.path)))


    def test_apply_removing_diff_to_full_store(self):
        root_diff = DirectoryContentsDifferencesHelper.removing(
            DirectoryContents([testing_data.LIPSUM_FILE], [testing_data.FOO_DIRECTORY, testing_data.QUX_DIRECTORY]))

        foo_diff = DirectoryContentsDifferencesHelper.removing(
            DirectoryContents([], [testing_data.BAR_DIRECTORY]))

        bar_diff = DirectoryContentsDifferencesHelper.removing(
            DirectoryContents([], [testing_data.AUX_DIRECTORY, testing_data.BAZ_DIRECTORY]))

        baz_diff = DirectoryContentsDifferencesHelper.removing(
            DirectoryContents([testing_data.LOREM_FILE], []))

        aux_diff = DirectoryContentsDifferencesHelper.removing(
            DirectoryContents([testing_data.DOLOR_FILE, testing_data.IPSUM_FILE], []))

        qux_diff = DirectoryContentsDifferencesHelper.removing(
            DirectoryContents([], [testing_data.QUUX_DIRECTORY]))

        quux_diff = DirectoryContentsDifferencesHelper.removing(
            DirectoryContents([testing_data.SIT_FILE], []))

        caches_difference = CachesDifference({
            testing_data.ROOT_DIRECTORY_PATH: root_diff,
            testing_data.FOO_DIRECTORY.path: foo_diff,
            testing_data.BAR_DIRECTORY.path: bar_diff,
            testing_data.BAZ_DIRECTORY.path: baz_diff,
            testing_data.AUX_DIRECTORY.path: aux_diff,
            testing_data.QUX_DIRECTORY.path: qux_diff,
            testing_data.QUUX_DIRECTORY.path: quux_diff
        })

        store = InMemoryStore()
        test_data = testing_data.SomeTestingStorageElements(True, False)
        test_data.foreach_element(lambda e: store.add(e))

        self._do_apply_diff(caches_difference, store)

        self.assertEqual(DirectoryContents([], []), store.get_children(testing_data.ROOT_DIRECTORY_PATH))


    def test_apply_modifications_diff_to_full(self):
        root_diff = DirectoryContentsDifference(
            directories_to_add=[testing_data.QUICK_DIRECTORY],
            directories_to_remove=[],
            directories_to_keep=[testing_data.FOO_DIRECTORY, testing_data.QUX_DIRECTORY],
            files_to_add=[],
            files_to_remove=[],
            files_to_update=[],
            files_to_keep=[testing_data.LIPSUM_FILE])

        foo_diff = DirectoryContentsDifference(
            directories_to_add=[],
            directories_to_remove=[],
            directories_to_keep=[testing_data.BAR_DIRECTORY],
            files_to_add=[testing_data.BROWN_FILE],
            files_to_remove=[],
            files_to_update=[],
            files_to_keep=[])

        bar_diff = DirectoryContentsDifference(
            directories_to_add=[],
            directories_to_remove=[testing_data.BAZ_DIRECTORY],
            directories_to_keep=[testing_data.AUX_DIRECTORY],
            files_to_add=[],
            files_to_remove=[],
            files_to_update=[],
            files_to_keep=[])

        baz_diff = DirectoryContentsDifferencesHelper.same(
            DirectoryContents([testing_data.LOREM_FILE], []))

        aux_diff = DirectoryContentsDifference(
            directories_to_add=[],
            directories_to_remove=[],
            directories_to_keep=[],
            files_to_add=[],
            files_to_remove=[testing_data.IPSUM_FILE],
            files_to_update=[testing_data.MODIFIED_DOLOR_FILE],
            files_to_keep=[])

        qux_diff = DirectoryContentsDifferencesHelper.same(
            DirectoryContents([], [testing_data.QUUX_DIRECTORY]))

        quux_diff = DirectoryContentsDifferencesHelper.same(
            DirectoryContents([testing_data.SIT_FILE], []))

        quick_diff = DirectoryContentsDifferencesHelper.adding(
            DirectoryContents([], []))

        caches_difference = CachesDifference({
            testing_data.ROOT_DIRECTORY_PATH: root_diff,
            testing_data.FOO_DIRECTORY.path: foo_diff,
            testing_data.BAR_DIRECTORY.path: bar_diff,
            testing_data.BAZ_DIRECTORY.path: baz_diff,
            testing_data.AUX_DIRECTORY.path: aux_diff,
            testing_data.QUX_DIRECTORY.path: qux_diff,
            testing_data.QUUX_DIRECTORY.path: quux_diff,
            testing_data.QUICK_DIRECTORY.path: quick_diff
        })

        store = InMemoryStore()
        input_test_data = testing_data.SomeTestingStorageElements(True, False)
        input_test_data.foreach_element(lambda e: store.add(e))

        self._do_apply_diff(caches_difference, store)

        modified_test_data = testing_data.SomeWithModifications(True, True, True, True, True, True)
        modified_test_data.foreach_element(lambda e: self.assertEqual(e, store.get_element(e.path)))

    def _do_apply_diff(self, diff: CachesDifference, store: InMemoryStore):
        dir_diff_peformer = DefaultContentsDifferencePerformer()
        performer = DefaultCachesDifferencePerformer(dir_diff_peformer)

        storage_modifier = InMemoryStorageModifier(store)
        contents_supplier = InMemoryFileContentsSupplier()

        performer.apply(diff, contents_supplier, storage_modifier)

