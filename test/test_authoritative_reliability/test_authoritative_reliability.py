import unittest
from unittest.mock import patch, call

import dig
import authoritative_reliability


class MyTestCase(unittest.TestCase):

    @patch.object(authoritative_reliability, 'generate_statistics')
    @patch.object(authoritative_reliability, 'run_dig')
    @patch('builtins.print')
    def test_noTrials(self, mock_print, mock_run_dig, mock_gen_stats):
        mock_run_dig.side_effect = [dig.DigResults(answer=5, authority=0, additional=0, status="NOERROR",
                                                   responding_server="", answer_section=[], authority_section=[],
                                                   additional_section=[], query_time=120, msg_size=0,
                                                   recursion_not_available=False)]

        trials = 0
        authoritative_reliability.test_reliability("a", "b", trials)

        self.assertEqual(0, mock_run_dig.call_count)

        self.assertEqual(0, mock_gen_stats.call_count)

        self.assertEqual(0, mock_print.call_count)

    @patch.object(authoritative_reliability, 'generate_statistics')
    @patch.object(authoritative_reliability, 'run_dig')
    @patch('builtins.print')
    def test_oneTrial(self, mock_print, mock_run_dig, mock_gen_stats):
        mock_run_dig.side_effect = [dig.DigResults(answer=5, authority=0, additional=0, status="NOERROR",
                                                   responding_server="", answer_section=[], authority_section=[],
                                                   additional_section=[], query_time=120, msg_size=0,
                                                   recursion_not_available=False),
                                    dig.DigResults(answer=5, authority=0, additional=0, status="NOERROR",
                                                   responding_server="", answer_section=[], authority_section=[],
                                                   additional_section=[], query_time=240, msg_size=0,
                                                   recursion_not_available=False)                                    ]

        trials = 1
        authoritative_reliability.test_reliability("b", "a", trials)

        self.assertEqual(trials, mock_run_dig.call_count)
        mock_run_dig.assert_has_calls([call(domain="a", target_server="b")]*trials)

        self.assertEqual(0, mock_gen_stats.call_count)

        self.assertEqual(0, mock_print.call_count)

    @patch.object(authoritative_reliability, 'generate_statistics')
    @patch.object(authoritative_reliability, 'run_dig')
    @patch('builtins.print')
    def test_threeTrials_oneResult(self, mock_print, mock_run_dig, mock_gen_stats):
        mock_run_dig.side_effect = [dig.DigResults(answer=0, authority=12, additional=0, status="NOERROR",
                                                   responding_server="", answer_section=[], authority_section=[],
                                                   additional_section=[], query_time=240, msg_size=0,
                                                   recursion_not_available=False),
                                    None,
                                    dig.DigResults(answer=0, authority=31, additional=0, status="NXDOMAIN",
                                                   responding_server="", answer_section=[], authority_section=[],
                                                   additional_section=[], query_time=120, msg_size=0,
                                                   recursion_not_available=False),
                                    dig.DigResults(answer=0, authority=0, additional=0, status="NOERROR",
                                                   responding_server="", answer_section=[], authority_section=[],
                                                   additional_section=[], query_time=120, msg_size=0,
                                                   recursion_not_available=True)]

        trials = 3
        authoritative_reliability.test_reliability("b", "a", trials)

        self.assertEqual(trials, mock_run_dig.call_count)
        mock_run_dig.assert_has_calls([call(domain="a", target_server="b")]*trials)

        self.assertEqual(0, mock_gen_stats.call_count)

        self.assertEqual(0, mock_print.call_count)

    @patch.object(authoritative_reliability, 'generate_statistics')
    @patch.object(authoritative_reliability, 'run_dig')
    @patch('builtins.print')
    def test_threeTrials_multipleResults(self, mock_print, mock_run_dig, mock_gen_stats):
        mock_run_dig.side_effect = [dig.DigResults(answer=0, authority=4, additional=0, status="NOERROR",
                                                   responding_server="", answer_section=[], authority_section=[],
                                                   additional_section=[], query_time=4, msg_size=0,
                                                   recursion_not_available=False),
                                    dig.DigResults(answer=0, authority=1, additional=0, status="NOERROR",
                                                   responding_server="", answer_section=[], authority_section=[],
                                                   additional_section=[], query_time=2, msg_size=0,
                                                   recursion_not_available=False),
                                    dig.DigResults(answer=0, authority=53, additional=0, status="NOERROR",
                                                   responding_server="", answer_section=[], authority_section=[],
                                                   additional_section=[], query_time=4, msg_size=0,
                                                   recursion_not_available=False)]

        mock_gen_stats.side_effect = ["generated_stats_go_here"]

        trials = 3
        authoritative_reliability.test_reliability("b", "a", trials)

        self.assertEqual(trials, mock_run_dig.call_count)
        mock_run_dig.assert_has_calls([call(domain="a", target_server="b")]*trials)

        self.assertEqual(1, mock_gen_stats.call_count)
        mock_gen_stats.assert_has_calls([call([4, 2, 4])])

        self.assertEqual(1, mock_print.call_count)
        mock_print.assert_has_calls([call("b,generated_stats_go_here")])
