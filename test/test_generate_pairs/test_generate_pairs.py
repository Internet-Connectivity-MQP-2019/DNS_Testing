import sys
import unittest
from unittest.mock import patch, call
import generate_pairs


def swap_first_two(l):
    l[0], l[1] = l[1], l[0]


class MyTestCase(unittest.TestCase):

    @patch('random.shuffle')
    @patch('builtins.print')
    @patch.object(generate_pairs, 'file_to_list')
    def test_1x1x1(self, mock_file_to_list, mock_print, mock_shuffle):
        mock_file_to_list.side_effect = [["a"], ["b"]]

        mock_shuffle.side_effect = [("a", "b")]

        filename1 = "file_one"
        filename2 = "file_two"
        generate_pairs.generate_pairs(filename1, filename2, 1)

        self.assertEqual(2, mock_file_to_list.call_count)
        mock_file_to_list.assert_has_calls([call(filename1), call(filename2)])

        self.assertEqual(1, mock_shuffle.call_count)
        mock_shuffle.assert_has_calls([call([("a", "b")])])

        self.assertEqual(1, mock_print.call_count)
        mock_print.assert_has_calls([call("a,b")])

    @patch('random.shuffle')
    @patch('builtins.print')
    @patch.object(generate_pairs, 'file_to_list')
    def test_1x2x1(self, mock_file_to_list, mock_print, mock_shuffle):
        mock_file_to_list.side_effect = [["a"], ["b", "c"]]

        mock_shuffle.side_effect = swap_first_two

        filename1 = "file_one"
        filename2 = "file_two"
        generate_pairs.generate_pairs(filename1, filename2, 1)

        self.assertEqual(2, mock_file_to_list.call_count)
        mock_file_to_list.assert_has_calls([call(filename1), call(filename2)])

        self.assertEqual(1, mock_shuffle.call_count)
        # Note: mock does not save the parameter, so it too is affected by side-effects
        mock_shuffle.assert_has_calls([call([("a", "c"), ("a", "b")])])

        self.assertEqual(2, mock_print.call_count)
        mock_print.assert_has_calls([call("a,c"), call("a,b")])

    @patch('random.shuffle')
    @patch('builtins.print')
    @patch.object(generate_pairs, 'file_to_list')
    def test_2x2x1(self, mock_file_to_list, mock_print, mock_shuffle):
        mock_file_to_list.side_effect = [["a", "b"], ["c", "d"]]

        mock_shuffle.side_effect = swap_first_two

        filename1 = "file_one"
        filename2 = "file_two"
        generate_pairs.generate_pairs(filename1, filename2, 1)

        self.assertEqual(2, mock_file_to_list.call_count)
        mock_file_to_list.assert_has_calls([call(filename1), call(filename2)])

        self.assertEqual(1, mock_shuffle.call_count)
        # Note: mock does not save the parameter, so it too is affected by side-effects
        mock_shuffle.assert_has_calls([call([("a", "d"), ("a", "c"), ("b", "c"), ("b", "d")])])

        self.assertEqual(4, mock_print.call_count)
        mock_print.assert_has_calls([call("a,d"), call("a,c"), call("b,c"), call("b,d")])

    @patch('random.shuffle')
    @patch('builtins.print')
    @patch.object(generate_pairs, 'file_to_list')
    def test_2x2x2(self, mock_file_to_list, mock_print, mock_shuffle):
        mock_file_to_list.side_effect = [["a", "b"], ["c", "d"]]

        mock_shuffle.side_effect = swap_first_two

        filename1 = "file_one"
        filename2 = "file_two"
        generate_pairs.generate_pairs(filename1, filename2, 2)

        self.assertEqual(2, mock_file_to_list.call_count)
        mock_file_to_list.assert_has_calls([call(filename1), call(filename2)])

        self.assertEqual(1, mock_shuffle.call_count)
        # Note: mock does not save the parameter, so it too is affected by side-effects
        mock_shuffle.assert_has_calls([call([("a", "d"), ("a", "c"), ("b", "c"), ("b", "d"), ("a", "c"), ("a", "d"),
                                             ("b", "c"), ("b", "d")])])

        self.assertEqual(8, mock_print.call_count)
        mock_print.assert_has_calls([call("a,d"), call("a,c"), call("b,c"), call("b,d"),
                                     call("a,c"), call("a,d"), call("b,c"), call("b,d")])
