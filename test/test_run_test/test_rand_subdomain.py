import unittest
from unittest.mock import patch, call
import string

import run_test


class MyTestCase(unittest.TestCase):

    @patch('random.choice')
    def test_zero(self, mock_choice):
        length = 0

        result = run_test.rand_subdomain(length=length)

        self.assertEqual("", result)
        self.assertEqual(0, mock_choice.call_count)

    @patch('random.choice')
    def test_one(self, mock_choice):
        length = 1

        mock_choice.side_effect = [c for c in string.ascii_letters[0:length]]

        result = run_test.rand_subdomain(length=length)

        self.assertEqual(string.ascii_letters[0:length], result)
        self.assertEqual(length, mock_choice.call_count)
        mock_choice.assert_has_calls([call(string.ascii_letters)]*length)

    @patch('random.choice')
    def test_twelve(self, mock_choice):
        length = 12

        mock_choice.side_effect = [c for c in string.ascii_letters[0:length]]

        result = run_test.rand_subdomain(length=length)

        self.assertEqual(string.ascii_letters[0:length], result)
        self.assertEqual(length, mock_choice.call_count)
        mock_choice.assert_has_calls([call(string.ascii_letters)]*length)

    @patch('random.choice')
    def test_one_hundred(self, mock_choice):
        length = 100

        mock_choice.side_effect = [c for c in (string.ascii_letters*2)[0:length]]

        result = run_test.rand_subdomain(length=length)

        self.assertEqual((string.ascii_letters*2)[0:length], result)
        self.assertEqual(length, mock_choice.call_count)
        mock_choice.assert_has_calls([call(string.ascii_letters)]*length)
