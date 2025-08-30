from unittest import TestCase

import testing_data


class TestSomeTestingDataSimple(TestCase):

    def test_print_foreach_element_flat(self):
        print("print_foreach_element_flat:")

        td = testing_data.SomeTestingStorageElements(False, False)
        td.foreach_element(print)

        print()

    def test_print_foreach_element_full(self):
        print("print_foreach_element_full:")

        td = testing_data.SomeTestingStorageElements(True, True)
        td.foreach_element(print)

        print()

    def test_print_foreach_foreach_file_and_directory_flat(self):
        print("print_foreach_foreach_file_and_directory_flat:")

        td = testing_data.SomeTestingStorageElements(False, False)
        td.foreach_file_and_directory(print, print)

        print()

    def test_print_foreach_foreach_file_and_directory_full(self):
        print("print_foreach_foreach_file_and_directory_full:")

        td = testing_data.SomeTestingStorageElements(True, True)
        td.foreach_file_and_directory(print, print)

        print()


class TestSomeTestingDataAdvanced(TestCase):

    def test_foreach_element_root_excluded_aditionals_exluded(self):
        td = testing_data.SomeTestingStorageElements(False, False)
        td.foreach_element(
            lambda e: print(f"Element (no extras): {e}")
        )

    def test_foreach_element_root_included_aditionals_exluded(self):
        td = testing_data.SomeTestingStorageElements(True, False)
        td.foreach_element(
            lambda e: print(f"Element (root included): {e}")
        )

    def test_foreach_element_root_excluded_aditionals_included(self):
        td = testing_data.SomeTestingStorageElements(False, True)
        td.foreach_element(
            lambda e: print(f"Element (aditionals included): {e}")
        )

    def test_foreach_element_root_included_aditionals_included(self):
        td = testing_data.SomeTestingStorageElements(True, True)
        td.foreach_element(
            lambda e: print(f"Element (root and aditionals included): {e}")
        )

    def test_foreach_file_and_directory_root_excluded_aditionals_exluded(self):
        td = testing_data.SomeTestingStorageElements(False, False)
        td.foreach_file_and_directory(
            lambda e: print(f"Directory (no extras): {e}"),
            lambda e: print(f"File (no extras): {e}"),
        )

    def test_foreach_file_and_directory_root_included_aditionals_exluded(self):
        td = testing_data.SomeTestingStorageElements(True, False)
        td.foreach_file_and_directory(
            lambda e: print(f"Directory (root included): {e}"),
            lambda e: print(f"File (root included): {e}")
        )

    def test_foreach_file_and_directory_root_excluded_aditionals_included(self):
        td = testing_data.SomeTestingStorageElements(False, True)
        td.foreach_file_and_directory(
            lambda e: print(f"Directory (aditionals included): {e}"),
            lambda e: print(f"File (aditionals included): {e}")
        )

    def test_foreach_file_and_directory_root_included_aditionals_included(self):
        td = testing_data.SomeTestingStorageElements(True, True)
        td.foreach_file_and_directory(
            lambda e: print(f"Directory (root and aditionals included): {e}"),
            lambda e: print(f"File (root and aditionals included): {e}")
        )


class TestSomeWithModifications(TestCase):

    def test_no_modifications(self):
        td = testing_data.SomeWithModifications(False, False, False, False, False, False)
        expected_elements = testing_data.ALL_ELEMENTS

        actual_elements = []
        td.foreach_element(
            lambda e: actual_elements.append(e)
        )
        self.assertEqual(expected_elements, actual_elements)

    def test_all_modifications(self):
        td = testing_data.SomeWithModifications(False, True, True, True, True, True)
        expected_elements = [
            testing_data.FOO_DIRECTORY, testing_data.BAR_DIRECTORY, testing_data.LOREM_FILE,
            testing_data.AUX_DIRECTORY, testing_data.MODIFIED_DOLOR_FILE,
            testing_data.QUX_DIRECTORY, testing_data.QUUX_DIRECTORY, testing_data.SIT_FILE,
            testing_data.LIPSUM_FILE, testing_data.QUICK_DIRECTORY, testing_data.BROWN_FILE
        ]
        actual_elements = []
        td.foreach_element(
            lambda e: actual_elements.append(e)
        )
        self.assertEqual(expected_elements, actual_elements)
