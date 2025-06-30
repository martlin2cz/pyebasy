from unittest import TestCase

import some_testing_data as testdata
from commons_base import DirectoryContents
from commons_helpers import DirectoryContentsBuilder
from datas import Directory, File, DirectoryContentsDifference
from dirs_differ_simple import SimpleDirectoryContentsComparer


class AbstractCommonTestSimpleDirectoryContentsComparer(TestCase):

    def setUp(self) -> None:
        self.differ = SimpleDirectoryContentsComparer()

    def _execute(self, source_contents: DirectoryContents, destination_contents: DirectoryContents,
                 expected_diff: DirectoryContentsDifference) -> DirectoryContentsDifference:

        diff = self.differ.compute(source_contents, destination_contents)

        diff_dict = diff.__dict__
        expected_diff_dict = expected_diff.__dict__

        for key in diff_dict:
            self.assertEqual(set(expected_diff_dict[key]), set(diff_dict[key]), f"Mismatch in {key}")

        # self.assertEqual(diff, expected_diff)

        return diff

    def _create_empty_directory_contents(self):
        builder = DirectoryContentsBuilder()

        return builder.build()

    def _create_partial_directory_contents(self):
        builder = DirectoryContentsBuilder()

        builder.add_directory(testdata.FOO_DIRECTORY)
        builder.add_directory(testdata.QUX_DIRECTORY)
        builder.add_file(testdata.LIPSUM_FILE)

        return builder.build()

    def _create_full_directory_contents(self):
        builder = DirectoryContentsBuilder()

        self.foo43directory = Directory(testdata.ROOT_DIRECTORY_PATH / 'foo43', testdata.NOW)
        self.lipsum44file = File(testdata.ROOT_DIRECTORY_PATH / 'lipsum44', testdata.NOW, 44, testdata.NOW)

        builder.add_directory(testdata.FOO_DIRECTORY)
        builder.add_directory(self.foo43directory)
        builder.add_directory(testdata.QUX_DIRECTORY)

        builder.add_file(testdata.LIPSUM_FILE)
        builder.add_file(self.lipsum44file)

        return builder.build()


class TestSimpleDirectoryContentsComparerEmptyToOthers(AbstractCommonTestSimpleDirectoryContentsComparer):

    def test_compare_empty_to_empty(self):
        self._execute(
            source_contents=self._create_empty_directory_contents(),
            destination_contents=self._create_empty_directory_contents(),
            expected_diff=DirectoryContentsDifference(
                directories_to_add=[],
                directories_to_remove=[],
                directories_to_keep=[],

                files_to_add=[],
                files_to_remove=[],
                files_to_update=[],
                files_to_keep=[])
        )

    def test_compare_empty_to_partial(self):
        self._execute(
            source_contents=self._create_empty_directory_contents(),
            destination_contents=self._create_partial_directory_contents(),
            expected_diff=DirectoryContentsDifference(
                directories_to_add=[],
                directories_to_remove=[testdata.FOO_DIRECTORY, testdata.QUX_DIRECTORY],
                directories_to_keep=[],

                files_to_add=[],
                files_to_remove=[testdata.LIPSUM_FILE],
                files_to_update=[],
                files_to_keep=[])
        )

    def test_compare_empty_to_full(self):
        self._execute(
            source_contents=self._create_empty_directory_contents(),
            destination_contents=self._create_full_directory_contents(),
            expected_diff=DirectoryContentsDifference(
                directories_to_add=[],
                directories_to_remove=[testdata.FOO_DIRECTORY, testdata.QUX_DIRECTORY, self.foo43directory],
                directories_to_keep=[],

                files_to_add=[],
                files_to_remove=[testdata.LIPSUM_FILE, self.lipsum44file],
                files_to_update=[],
                files_to_keep=[])
        )


class TestSimpleDirectoryContentsComparerComparingPartialToOthers(AbstractCommonTestSimpleDirectoryContentsComparer):
    def test_compare_partial_to_empty(self):
        self._execute(
            source_contents=self._create_partial_directory_contents(),
            destination_contents=self._create_empty_directory_contents(),
            expected_diff=DirectoryContentsDifference(
                directories_to_add=[testdata.FOO_DIRECTORY, testdata.QUX_DIRECTORY],
                directories_to_remove=[],
                directories_to_keep=[],

                files_to_add=[testdata.LIPSUM_FILE],
                files_to_remove=[],
                files_to_update=[],
                files_to_keep=[])
        )

    def test_compare_partial_to_partial(self):
        self._execute(
            source_contents=self._create_partial_directory_contents(),
            destination_contents=self._create_partial_directory_contents(),
            expected_diff=DirectoryContentsDifference(
                directories_to_add=[],
                directories_to_remove=[],
                directories_to_keep=[testdata.FOO_DIRECTORY, testdata.QUX_DIRECTORY],

                files_to_add=[],
                files_to_remove=[],
                files_to_update=[],
                files_to_keep=[testdata.LIPSUM_FILE])
        )

    def test_compare_partial_to_full(self):
        self._execute(
            source_contents=self._create_partial_directory_contents(),
            destination_contents=self._create_full_directory_contents(),
            expected_diff=DirectoryContentsDifference(
                directories_to_add=[],
                directories_to_remove=[self.foo43directory],
                directories_to_keep=[testdata.FOO_DIRECTORY, testdata.QUX_DIRECTORY],

                files_to_add=[],
                files_to_remove=[self.lipsum44file],
                files_to_update=[],
                files_to_keep=[testdata.LIPSUM_FILE])
        )


class TestSimpleDirectoryContentsComparerComparingFullToOthers(AbstractCommonTestSimpleDirectoryContentsComparer):

    def test_compare_full_to_empty(self):
        self._execute(
            source_contents=self._create_full_directory_contents(),
            destination_contents=self._create_empty_directory_contents(),
            expected_diff=DirectoryContentsDifference(
                directories_to_add=[testdata.FOO_DIRECTORY, testdata.QUX_DIRECTORY, self.foo43directory],
                directories_to_remove=[],
                directories_to_keep=[],

                files_to_add=[testdata.LIPSUM_FILE, self.lipsum44file],
                files_to_remove=[],
                files_to_update=[],
                files_to_keep=[])
        )

    def test_compare_full_to_partial(self):
        self._execute(
            source_contents=self._create_full_directory_contents(),
            destination_contents=self._create_partial_directory_contents(),
            expected_diff=DirectoryContentsDifference(
                directories_to_add=[self.foo43directory],
                directories_to_remove=[],
                directories_to_keep=[testdata.FOO_DIRECTORY, testdata.QUX_DIRECTORY],

                files_to_add=[self.lipsum44file],
                files_to_remove=[],
                files_to_update=[],
                files_to_keep=[testdata.LIPSUM_FILE])
        )

    def test_compare_full_to_full(self):
        self._execute(
            source_contents=self._create_full_directory_contents(),
            destination_contents=self._create_full_directory_contents(),
            expected_diff=DirectoryContentsDifference(
                directories_to_add=[],
                directories_to_remove=[],
                directories_to_keep=[testdata.FOO_DIRECTORY, testdata.QUX_DIRECTORY, self.foo43directory],

                files_to_add=[],
                files_to_remove=[],
                files_to_update=[],
                files_to_keep=[testdata.LIPSUM_FILE, self.lipsum44file])
        )


class TestSimpleDirectoryContentsComparerComparingAnotherFullToOthers(AbstractCommonTestSimpleDirectoryContentsComparer):

    def _create_another_full_directory_contents(self):
        builder = DirectoryContentsBuilder()

        self.foo430directory = Directory(testdata.ROOT_DIRECTORY_PATH / 'FOO_430', testdata.NOW)
        self.lipsum4400file = File(testdata.ROOT_DIRECTORY_PATH / 'lipsum44', testdata.NOW, 4400, testdata.NOW)
        self.dolorsit45file = File(testdata.ROOT_DIRECTORY_PATH / 'dolorsit45', testdata.NOW, 45, testdata.NOW)

        builder.add_directory(testdata.FOO_DIRECTORY)
        builder.add_directory(self.foo430directory)
        builder.add_directory(testdata.QUX_DIRECTORY)

        builder.add_file(testdata.LIPSUM_FILE)
        builder.add_file(self.lipsum4400file)
        builder.add_file(self.dolorsit45file)

        return builder.build()

    def test_compare_full_to_another_full(self):
        self._execute(
            source_contents=self._create_full_directory_contents(),
            destination_contents=self._create_another_full_directory_contents(),
            expected_diff=DirectoryContentsDifference(
                directories_to_add=[self.foo43directory],
                directories_to_remove=[self.foo430directory],
                directories_to_keep=[testdata.FOO_DIRECTORY, testdata.QUX_DIRECTORY],

                files_to_add=[],
                files_to_remove=[self.dolorsit45file],
                files_to_update=[self.lipsum44file],
                files_to_keep=[testdata.LIPSUM_FILE])
        )

    def test_compare_another_full_to_full(self):
        self._execute(
            source_contents=self._create_another_full_directory_contents(),
            destination_contents=self._create_full_directory_contents(),
            expected_diff=DirectoryContentsDifference(
                directories_to_add=[self.foo430directory],
                directories_to_remove=[self.foo43directory],
                directories_to_keep=[testdata.FOO_DIRECTORY, testdata.QUX_DIRECTORY],

                files_to_add=[self.dolorsit45file],
                files_to_remove=[],
                files_to_update=[self.lipsum4400file],
                files_to_keep=[testdata.LIPSUM_FILE])
        )
