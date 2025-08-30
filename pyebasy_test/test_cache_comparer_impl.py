from typing import Dict
from unittest import TestCase

import testing_data
from cache_comparer_impl import DefaultCacheComparer
from cache_inmemory import InMemoryCache
from commons_base import Cache, DirectoryContents
from commons_helpers import DirectoryContentsDifferencesHelper
from datas import CachesDifference, DirectoryContentsDifference
from dirs_differ_simple import SimpleDirectoryContentsComparer
from testing_caches import SomeTestingCaches


class TestDefaultCacheComparer(TestCase):
    def setUp(self):
        self.test_data = testing_data.SomeTestingStorageElements(True, False)
        self.caches = SomeTestingCaches(InMemoryCache)

        directory_contents_comparer = SimpleDirectoryContentsComparer()
        self.comparer = DefaultCacheComparer(directory_contents_comparer)

    def test_compute_empty_to_empty(self):
        self._do_test(self.caches.empty(), self.caches.empty(),{
            testing_data.ROOT_DIRECTORY_PATH: DirectoryContentsDifference(
                directories_to_add=[],
                directories_to_remove=[],
                directories_to_keep=[],
                files_to_add=[],
                files_to_remove=[],
                files_to_update=[],
                files_to_keep=[])
        })

    def test_compute_full_to_full(self):
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

        self._do_test(self.caches.full(), self.caches.full(), {
            testing_data.ROOT_DIRECTORY_PATH: root_diff,
            testing_data.FOO_DIRECTORY.path: foo_diff,
            testing_data.BAR_DIRECTORY.path: bar_diff,
            testing_data.BAZ_DIRECTORY.path: baz_diff,
            testing_data.AUX_DIRECTORY.path: aux_diff,
            testing_data.QUX_DIRECTORY.path: qux_diff,
            testing_data.QUUX_DIRECTORY.path: quux_diff
        })

    def test_compute_empty_to_full(self):
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

        self._do_test(self.caches.empty(), self.caches.full(), {
            testing_data.ROOT_DIRECTORY_PATH: root_diff,
            testing_data.FOO_DIRECTORY.path: foo_diff,
            testing_data.BAR_DIRECTORY.path: bar_diff,
            testing_data.BAZ_DIRECTORY.path: baz_diff,
            testing_data.AUX_DIRECTORY.path: aux_diff,
            testing_data.QUX_DIRECTORY.path: qux_diff,
            testing_data.QUUX_DIRECTORY.path: quux_diff
        })

    def test_compute_full_to_empty(self):
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

        self._do_test( self.caches.full(), self.caches.empty(), {
            testing_data.ROOT_DIRECTORY_PATH: root_diff,
            testing_data.FOO_DIRECTORY.path: foo_diff,
            testing_data.BAR_DIRECTORY.path: bar_diff,
            testing_data.BAZ_DIRECTORY.path: baz_diff,
            testing_data.AUX_DIRECTORY.path: aux_diff,
            testing_data.QUX_DIRECTORY.path: qux_diff,
            testing_data.QUUX_DIRECTORY.path: quux_diff
        })

    def test_compute_full_to_modified_full(self):
        root_diff = DirectoryContentsDifference(
                directories_to_add=[],
                directories_to_remove=[testing_data.QUICK_DIRECTORY],
                directories_to_keep=[testing_data.FOO_DIRECTORY, testing_data.QUX_DIRECTORY],
                files_to_add=[],
                files_to_remove=[],
                files_to_update=[],
                files_to_keep=[testing_data.LIPSUM_FILE])

        foo_diff = DirectoryContentsDifference(
                directories_to_add=[],
                directories_to_remove=[],
                directories_to_keep=[testing_data.BAR_DIRECTORY],
                files_to_add=[],
                files_to_remove=[testing_data.BROWN_FILE],
                files_to_update=[],
                files_to_keep=[])

        bar_diff = DirectoryContentsDifference(
                directories_to_add=[testing_data.BAZ_DIRECTORY],
                directories_to_remove=[],
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
                files_to_add=[testing_data.IPSUM_FILE],
                files_to_remove=[],
                files_to_update=[testing_data.DOLOR_FILE],
                files_to_keep=[])

        qux_diff = DirectoryContentsDifferencesHelper.same(
            DirectoryContents([], [testing_data.QUUX_DIRECTORY]))

        quux_diff = DirectoryContentsDifferencesHelper.same(
            DirectoryContents([testing_data.SIT_FILE], []))

        quick_diff = DirectoryContentsDifferencesHelper.adding(
            DirectoryContents([], []))

        self._do_test(self.caches.full(), self.caches.modified_full(), {
            testing_data.ROOT_DIRECTORY_PATH: root_diff,
            testing_data.FOO_DIRECTORY.path: foo_diff,
            testing_data.BAR_DIRECTORY.path: bar_diff,
            testing_data.BAZ_DIRECTORY.path: baz_diff,
            testing_data.AUX_DIRECTORY.path: aux_diff,
            testing_data.QUX_DIRECTORY.path: qux_diff,
            testing_data.QUUX_DIRECTORY.path: quux_diff,
            testing_data.QUICK_DIRECTORY.path: quick_diff
        })

    def test_compute_modified_full_to_full(self):
        root_diff = DirectoryContentsDifference(directories_to_add=[testing_data.QUICK_DIRECTORY],
                                                directories_to_remove=[],
                                                directories_to_keep=[testing_data.FOO_DIRECTORY, testing_data.QUX_DIRECTORY],
                                                files_to_add=[],
                                                files_to_remove=[],
                                                files_to_update=[],
                                                files_to_keep=[testing_data.LIPSUM_FILE])

        foo_diff = DirectoryContentsDifference(directories_to_add=[],
                                               directories_to_remove=[],
                                               directories_to_keep=[testing_data.BAR_DIRECTORY],
                                               files_to_add=[testing_data.BROWN_FILE],
                                               files_to_remove=[],
                                               files_to_update=[],
                                               files_to_keep=[])

        bar_diff = DirectoryContentsDifference(directories_to_add=[],
                                               directories_to_remove=[testing_data.BAZ_DIRECTORY],
                                               directories_to_keep=[testing_data.AUX_DIRECTORY],
                                               files_to_add=[],
                                               files_to_remove=[],
                                               files_to_update=[],
                                               files_to_keep=[])

        baz_diff = DirectoryContentsDifferencesHelper.same(
            DirectoryContents([testing_data.LOREM_FILE], []))

        aux_diff = DirectoryContentsDifference(directories_to_add=[],
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

        quick_diff = DirectoryContentsDifferencesHelper.removing(
            DirectoryContents([], []))

        self._do_test(self.caches.modified_full(), self.caches.full(), {
            testing_data.ROOT_DIRECTORY_PATH: root_diff,
            testing_data.FOO_DIRECTORY.path: foo_diff,
            testing_data.BAR_DIRECTORY.path: bar_diff,
            testing_data.BAZ_DIRECTORY.path: baz_diff,
            testing_data.AUX_DIRECTORY.path: aux_diff,
            testing_data.QUX_DIRECTORY.path: qux_diff,
            testing_data.QUUX_DIRECTORY.path: quux_diff,
            testing_data.QUICK_DIRECTORY.path: quick_diff
        })

    def _do_test(self, source: Cache, destination: Cache, expected_diff_dict: Dict):
        actual_diff = self.comparer.compute(source, destination)
        expected_diff = CachesDifference(expected_diff_dict)

        self.assertEqual(expected_diff.paths(), actual_diff.paths(), "Paths processed mismatch: ")

        for p in expected_diff.paths():
            self.assertEqual(expected_diff.change_of_directory(p), actual_diff.change_of_directory(p), f"For path {p}:")

        self.assertEqual(expected_diff, actual_diff)



