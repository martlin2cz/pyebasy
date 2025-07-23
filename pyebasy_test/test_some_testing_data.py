from unittest import TestCase

import some_testing_data


class TestSomeTestingDataSimple(TestCase):

    def test_print_foreach_element_flat(self):
        print("print_foreach_element_flat:")
        some_testing_data.foreach_element(False, False, print)
        print()

    def test_print_foreach_element_full(self):
        print("print_foreach_element_full:")
        some_testing_data.foreach_element(True, True, print)
        print()

    def test_print_foreach_foreach_file_and_directory_flat(self):
        print("print_foreach_foreach_file_and_directory_flat:")
        some_testing_data.foreach_file_and_directory(False, False, print, print)
        print()

    def test_print_foreach_foreach_file_and_directory_full(self):
        print("print_foreach_foreach_file_and_directory_full:")
        some_testing_data.foreach_file_and_directory(True, True, print, print)
        print()

class TestSomeTestingDataAdvanced(TestCase):

    def test_foreach_element_root_excluded_aditionals_exluded(self):
        some_testing_data.foreach_element(False, False,
            lambda e: print(f"Element (no extras): {e}")
        )

    def test_foreach_element_root_included_aditionals_exluded(self):
        some_testing_data.foreach_element(True, False,
          lambda e: print(f"Element (root included): {e}")
        )

    def test_foreach_element_root_excluded_aditionals_included(self):
        some_testing_data.foreach_element(False, True,
            lambda e: print(f"Element (aditionals included): {e}")
        )

    def test_foreach_element_root_included_aditionals_included(self):
        some_testing_data.foreach_element(True, True,
            lambda e: print(f"Element (root and aditionals included): {e}")
        )

    def test_foreach_file_and_directory_root_excluded_aditionals_exluded(self):
        some_testing_data.foreach_file_and_directory(False, False,
            lambda e: print(f"Directory (no extras): {e}"),
            lambda e: print(f"File (no extras): {e}"),
        )

    def test_foreach_file_and_directory_root_included_aditionals_exluded(self):
        some_testing_data.foreach_file_and_directory(True, False,
            lambda e: print(f"Directory (root included): {e}"),
            lambda e: print(f"File (root included): {e}")
        )

    def test_foreach_file_and_directory_root_excluded_aditionals_included(self):
        some_testing_data.foreach_file_and_directory(False, True,
            lambda e: print(f"Directory (aditionals included): {e}"),
            lambda e: print(f"File (aditionals included): {e}")
        )

    def test_foreach_file_and_directory_root_included_aditionals_included(self):
        some_testing_data.foreach_file_and_directory(True, True,
            lambda e: print(f"Directory (root and aditionals included): {e}"),
            lambda e: print(f"File (root and aditionals included): {e}")
        )
