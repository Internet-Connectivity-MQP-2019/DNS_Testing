import unittest
from unittest.mock import patch, call
import confirm_authoritative
import dig


class MyTestCase(unittest.TestCase):

    @patch.object(confirm_authoritative, 'run_dig')
    @patch('builtins.print')
    def test_badResult(self, mock_print, mock_run_dig):
        mock_run_dig.side_effect = [None]
        confirm_authoritative.confirm_authoritative("1.1.1.1", "cnn.com")

        self.assertEqual(mock_run_dig.call_count, 1)
        mock_run_dig.assert_has_calls([call(domain="cnn.com", target_server="1.1.1.1")])
        self.assertEqual(mock_print.call_count, 0)

    @patch.object(confirm_authoritative, 'run_dig')
    @patch('builtins.print')
    def test_NXDOMAIN(self, mock_print, mock_run_dig):
        mock_run_dig.side_effect = [dig.DigResults(answer=0, authority=0, additional=0, status="NXDOMAIN",
                                                   responding_server="", answer_section=[], authority_section=[],
                                                   additional_section=[], query_time=0, msg_size=0,
                                                   recursion_not_available=False)]

        confirm_authoritative.confirm_authoritative("1.1.1.1", "cnn.com")

        self.assertEqual(mock_run_dig.call_count, 1)
        mock_run_dig.assert_has_calls([call(domain="cnn.com", target_server="1.1.1.1")])
        self.assertEqual(mock_print.call_count, 0)

    @patch.object(confirm_authoritative, 'run_dig')
    @patch('builtins.print')
    def test_noAuthority(self, mock_print, mock_run_dig):
        mock_run_dig.side_effect = [dig.DigResults(answer=0, authority=0, additional=0, status="NOERROR",
                                                   responding_server="", answer_section=[], authority_section=[],
                                                   additional_section=[], query_time=0, msg_size=0,
                                                   recursion_not_available=False)]

        confirm_authoritative.confirm_authoritative("1.1.1.1", "cnn.com")

        self.assertEqual(mock_run_dig.call_count, 1)
        mock_run_dig.assert_has_calls([call(domain="cnn.com", target_server="1.1.1.1")])
        self.assertEqual(mock_print.call_count, 0)

    @patch.object(confirm_authoritative, 'run_dig')
    @patch('builtins.print')
    def test_positiveAuthority(self, mock_print, mock_run_dig):
        mock_run_dig.side_effect = [dig.DigResults(answer=0, authority=1, additional=0, status="NOERROR",
                                                   responding_server="", answer_section=[], authority_section=[],
                                                   additional_section=[], query_time=0, msg_size=0,
                                                   recursion_not_available=False)]

        confirm_authoritative.confirm_authoritative("42.1.42.1", "cnn.com")

        self.assertEqual(mock_run_dig.call_count, 1)
        mock_run_dig.assert_has_calls([call(domain="cnn.com", target_server="42.1.42.1")])
        self.assertEqual(mock_print.call_count, 1)
        mock_print.assert_has_calls([call("42.1.42.1,cnn.com")])