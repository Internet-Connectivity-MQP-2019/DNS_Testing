import os
import unittest
from unittest.mock import patch, call

import aggregate_state_to_state


def expand_filename(filename):
    return os.path.join(os.path.dirname(__file__), filename)


def make_call(directory):
    aggregate_state_to_state.aggregate(expand_filename(directory + "/results.csv"),
                                       expand_filename(directory + "/rec.csv"),
                                       expand_filename(directory + "/auth.csv"),
                                       expand_filename(directory + "/geolocation.csv"))


class MyTestCase(unittest.TestCase):

    @patch('builtins.print')
    def test_simpleNoFilters(self, mock_print):
        # Test description: one authoritative, one recursive ip - neither are filtered, both have locations
        # Expect one print: "New York,Wyoming,10,10,10,10
        make_call("test1_files")

        self.assertEqual(1, mock_print.call_count)
        mock_print.assert_has_calls([call("New York,Wyoming,10,10,10.00,10.00")])

    @patch('builtins.print')
    def test_simpleRecursiveFiltered(self, mock_print):
        # Test description: one authoritative, one recursive ip - recursive ip is not in the reliable list
        # Expect no prints
        make_call("test2_files")

        self.assertEqual(0, mock_print.call_count)

    @patch('builtins.print')
    def test_simpleAuthoritativeFiltered(self, mock_print):
        # Test description: one authoritative, one recursive ip - authoritative ip is not in the reliable list
        # Expect no prints
        make_call("test3_files")

        self.assertEqual(0, mock_print.call_count)

    @patch('builtins.print')
    def test_simpleBothFiltered(self, mock_print):
        # Test description: one authoritative, one recursive ip - both are not on the reliable lists
        # Expect no prints
        make_call("test4_files")

        self.assertEqual(0, mock_print.call_count)

    @patch('builtins.print')
    def test_simpleNoLocationRecursive(self, mock_print):
        # Test description: one authoritative, one recursive ip - both on the reliable lists, recursive has no location
        # Expect no prints
        make_call("test5_files")

        self.assertEqual(0, mock_print.call_count)

    @patch('builtins.print')
    def test_simpleNoLocationAuthoritative(self, mock_print):
        # Test description: one authoritative, one recursive ip - both on the reliable lists, auth has no location
        # Expect no prints
        make_call("test6_files")

        self.assertEqual(0, mock_print.call_count)

    @patch('builtins.print')
    def test_simpleNoLocationBoth(self, mock_print):
        # Test description: one authoritative, one recursive ip - both on the reliable lists, both have no location
        # Expect no prints
        make_call("test7_files")

        self.assertEqual(0, mock_print.call_count)

    @patch('builtins.print')
    def test_simpleBothNoLocationAndFiltered(self, mock_print):
        # Test description: one authoritative, one recursive ip - neither on the reliable lists, both have no location
        # Expect no prints
        make_call("test8_files")

        self.assertEqual(0, mock_print.call_count)

    @patch('builtins.print')
    def test_complex1(self, mock_print):
        # Test description: 12 results, 3 auth ips, 4 rec ips. 1 of each is filtered, 1 of each lacks location
        # -- Auth lacking location is same as auth not on list. Two auths are the same state
        # Expect 2 prints
        make_call("test9_files")


        mock_print.assert_has_calls([call("Georgia,Wyoming,2,3,2.50,2.50"),
                                     call("New Hampshire,Wyoming,0,1,0.50,0.50")])
        self.assertEqual(2, mock_print.call_count)

    @patch('builtins.print')
    def test_complex2(self, mock_print):
        # Test description: 36 results, 6 auth ips, 6 rec ips. No filtering
        # Expect 20 prints
        make_call("test10_files")

        self.assertEqual(20, mock_print.call_count)

        expected_strings = ["Georgia,Alaska,2,2,2.00,2.00",
                            "Georgia,Arizona,3,3,3.00,3.00",
                            "Georgia,North Dakota,5,5,5.00,5.00",
                            "Georgia,Wyoming,1,6,3.67,4.00",
                            "Idaho,Alaska,8,9,8.50,8.50",
                            "Idaho,Arizona,8,9,8.50,8.50",
                            "Idaho,North Dakota,6,11,8.50,8.50",
                            "Idaho,Wyoming,0,12,7.00,7.50",
                            "New Hampshire,Alaska,14,14,14.00,14.00",
                            "New Hampshire,Arizona,15,15,15.00,15.00",
                            "New Hampshire,North Dakota,2,2,2.00,2.00",
                            "New Hampshire,Wyoming,1,13,5.67,3.00",
                            "Vermont,Alaska,5,5,5.00,5.00",
                            "Vermont,Arizona,6,6,6.00,6.00",
                            "Vermont,North Dakota,8,8,8.00,8.00",
                            "Vermont,Wyoming,4,9,6.67,7.00",
                            "Wyoming,Alaska,3,3,3.00,3.00",
                            "Wyoming,Arizona,2,2,2.00,2.00",
                            "Wyoming,North Dakota,12,12,12.00,12.00",
                            "Wyoming,Wyoming,1,14,6.33,4.00"]

        mock_print.assert_has_calls([call(i) for i in expected_strings])


if __name__ == '__main__':
    unittest.main()
