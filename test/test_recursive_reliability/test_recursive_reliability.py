import unittest
from unittest.mock import patch, call

import dig
import recursive_reliability


class MyTestCase(unittest.TestCase):

    @patch.object(recursive_reliability, 'generate_statistics')
    @patch.object(recursive_reliability, 'run_dig')
    @patch('builtins.print')
    def test_noTrials(self, mock_print, mock_run_dig, mock_gen_stats):
        mock_run_dig.side_effect = [dig.DigResults(answer=5, authority=0, additional=0, status="NOERROR",
                                                   responding_server="", answer_section=[], authority_section=[],
                                                   additional_section=[], query_time=120, msg_size=0,
                                                   recursion_not_available=False)]

        recursive_reliability.test_reliability("a", "b", 0)

        # Primer still runs
        self.assertEqual(1, mock_run_dig.call_count)
        mock_run_dig.assert_has_calls([call(domain="b", target_server="a")])

        self.assertEqual(0, mock_gen_stats.call_count)

        self.assertEqual(0, mock_print.call_count)

    @patch.object(recursive_reliability, 'generate_statistics')
    @patch.object(recursive_reliability, 'run_dig')
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

        recursive_reliability.test_reliability("b", "a", 1)

        # Primer still runs
        dig_count = 2
        self.assertEqual(dig_count, mock_run_dig.call_count)
        mock_run_dig.assert_has_calls([call(domain="a", target_server="b")]*dig_count)

        self.assertEqual(0, mock_gen_stats.call_count)

        self.assertEqual(0, mock_print.call_count)

    @patch.object(recursive_reliability, 'generate_statistics')
    @patch.object(recursive_reliability, 'run_dig')
    @patch('builtins.print')
    def test_sixTrials_oneResult(self, mock_print, mock_run_dig, mock_gen_stats):
        mock_run_dig.side_effect = [dig.DigResults(answer=5, authority=0, additional=0, status="NOERROR",
                                                   responding_server="", answer_section=[], authority_section=[],
                                                   additional_section=[], query_time=240, msg_size=0,
                                                   recursion_not_available=False),
                                    None,
                                    dig.DigResults(answer=5, authority=0, additional=0, status="NXDOMAIN",
                                                   responding_server="", answer_section=[], authority_section=[],
                                                   additional_section=[], query_time=120, msg_size=0,
                                                   recursion_not_available=False),
                                    dig.DigResults(answer=5, authority=0, additional=0, status="NOERROR",
                                                   responding_server="", answer_section=[], authority_section=[],
                                                   additional_section=[], query_time=120, msg_size=0,
                                                   recursion_not_available=True),
                                    dig.DigResults(answer=0, authority=0, additional=0, status="NOERROR",
                                                   responding_server="", answer_section=[], authority_section=[],
                                                   additional_section=[], query_time=120, msg_size=0,
                                                   recursion_not_available=False),
                                    dig.DigResults(answer=5, authority=1, additional=0, status="NOERROR",
                                                   responding_server="", answer_section=[], authority_section=[],
                                                   additional_section=[], query_time=120, msg_size=0,
                                                   recursion_not_available=False)]

        recursive_reliability.test_reliability("b", "a", 5)

        # Primer still runs
        dig_count = 6
        self.assertEqual(dig_count, mock_run_dig.call_count)
        mock_run_dig.assert_has_calls([call(domain="a", target_server="b")]*dig_count)

        self.assertEqual(0, mock_gen_stats.call_count)

        self.assertEqual(0, mock_print.call_count)

    @patch.object(recursive_reliability, 'generate_statistics')
    @patch.object(recursive_reliability, 'run_dig')
    @patch('builtins.print')
    def test_threeTrials_oneResult(self, mock_print, mock_run_dig, mock_gen_stats):
        mock_run_dig.side_effect = [dig.DigResults(answer=5, authority=0, additional=0, status="NOERROR",
                                                   responding_server="", answer_section=[], authority_section=[],
                                                   additional_section=[], query_time=4, msg_size=0,
                                                   recursion_not_available=False),
                                    dig.DigResults(answer=5, authority=0, additional=0, status="NOERROR",
                                                   responding_server="", answer_section=[], authority_section=[],
                                                   additional_section=[], query_time=2, msg_size=0,
                                                   recursion_not_available=False),
                                    dig.DigResults(answer=5, authority=0, additional=0, status="NOERROR",
                                                   responding_server="", answer_section=[], authority_section=[],
                                                   additional_section=[], query_time=4, msg_size=0,
                                                   recursion_not_available=False),
                                    dig.DigResults(answer=5, authority=0, additional=0, status="NOERROR",
                                                   responding_server="", answer_section=[], authority_section=[],
                                                   additional_section=[], query_time=2, msg_size=0,
                                                   recursion_not_available=False)]

        mock_gen_stats.side_effect = ["generated_stats_go_here"]

        recursive_reliability.test_reliability("b", "a", 3)

        # Primer still runs
        dig_count = 4
        self.assertEqual(dig_count, mock_run_dig.call_count)
        mock_run_dig.assert_has_calls([call(domain="a", target_server="b")]*dig_count)

        self.assertEqual(1, mock_gen_stats.call_count)
        mock_gen_stats.assert_has_calls([call([2, 4, 2])])

        self.assertEqual(1, mock_print.call_count)
        mock_print.assert_has_calls([call("b,generated_stats_go_here")])
