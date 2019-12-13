import unittest
from unittest.mock import patch, call

import dig
import run_test


def build_result(rtt, msg_size=0):
    return dig.DigResults(answer=0, authority=12, additional=0, status="NOERROR",
                          responding_server="", answer_section=[], authority_section=[],
                          additional_section=[], query_time=rtt, msg_size=msg_size,
                          recursion_not_available=False)


class MyTestCase(unittest.TestCase):

    @patch.object(run_test, 'rand_subdomain')
    @patch.object(run_test, 'run_dig')
    @patch('builtins.print')
    def test_noTries(self, mock_print, mock_run_dig, mock_rand_subdomain):
        num_tries = 0

        mock_run_dig.side_effect = [None]

        rand_subdomains = ["rand_{}".format(i) for i in range(num_tries)]
        mock_rand_subdomain.side_effect = rand_subdomains

        recursive_ip = "a"
        auth_ip = "b"
        domain = "c"
        run_test.run_test(recursive_ip, auth_ip, domain, num_tries)

        self.assertEqual((num_tries * 2) + 1, mock_run_dig.call_count)
        dig_calls = [call(domain=domain, target_server=recursive_ip, time=run_test.TIME_LIMIT)] + \
                    [call(domain=domain, target_server=recursive_ip, time=run_test.TIME_LIMIT)] * num_tries + \
                    [call(domain="{}.{}".format(rand_subdomains[i], domain), target_server=recursive_ip,
                          time=run_test.TIME_LIMIT) for i in range(num_tries)]
        mock_run_dig.assert_has_calls(dig_calls)

        self.assertEqual(num_tries, mock_rand_subdomain.call_count)

        self.assertEqual(0, mock_print.call_count)

    @patch.object(run_test, 'rand_subdomain')
    @patch.object(run_test, 'run_dig')
    @patch('builtins.print')
    def test_tooFewLatency(self, mock_print, mock_run_dig, mock_rand_subdomain):
        num_tries = 2

        mock_run_dig.side_effect = [None,  # Primer
                                    None, None,  # Latencies
                                    build_result(12), build_result(32)]  # Totals

        rand_subdomains = ["rand_{}".format(i) for i in range(num_tries)]
        mock_rand_subdomain.side_effect = rand_subdomains

        recursive_ip = "a"
        auth_ip = "b"
        domain = "c"
        run_test.run_test(recursive_ip, auth_ip, domain, num_tries)

        self.assertEqual((num_tries * 2) + 1, mock_run_dig.call_count)
        dig_calls = [call(domain=domain, target_server=recursive_ip, time=run_test.TIME_LIMIT)] + \
                    [call(domain=domain, target_server=recursive_ip, time=run_test.TIME_LIMIT)] * num_tries + \
                    [call(domain="{}.{}".format(rand_subdomains[i], domain), target_server=recursive_ip,
                          time=run_test.TIME_LIMIT) for i in range(num_tries)]
        mock_run_dig.assert_has_calls(dig_calls)

        self.assertEqual(num_tries, mock_rand_subdomain.call_count)

        self.assertEqual(0, mock_print.call_count)

    @patch.object(run_test, 'rand_subdomain')
    @patch.object(run_test, 'run_dig')
    @patch('builtins.print')
    def test_tooFewTotal(self, mock_print, mock_run_dig, mock_rand_subdomain):
        num_tries = 2

        mock_run_dig.side_effect = [None,  # Primer
                                    build_result(12), build_result(32),  # Latencies
                                    None, None]  # Totals

        rand_subdomains = ["rand_{}".format(i) for i in range(num_tries)]
        mock_rand_subdomain.side_effect = rand_subdomains

        recursive_ip = "a"
        auth_ip = "b"
        domain = "c"
        run_test.run_test(recursive_ip, auth_ip, domain, num_tries)

        self.assertEqual((num_tries * 2) + 1, mock_run_dig.call_count)
        dig_calls = [call(domain=domain, target_server=recursive_ip, time=run_test.TIME_LIMIT)] + \
                    [call(domain=domain, target_server=recursive_ip, time=run_test.TIME_LIMIT)] * num_tries + \
                    [call(domain="{}.{}".format(rand_subdomains[i], domain), target_server=recursive_ip,
                          time=run_test.TIME_LIMIT) for i in range(num_tries)]
        mock_run_dig.assert_has_calls(dig_calls)

        self.assertEqual(num_tries, mock_rand_subdomain.call_count)

        self.assertEqual(0, mock_print.call_count)

    @patch.object(run_test, 'rand_subdomain')
    @patch.object(run_test, 'run_dig')
    @patch('builtins.print')
    def test_oneGoodEach(self, mock_print, mock_run_dig, mock_rand_subdomain):
        num_tries = 2

        mock_run_dig.side_effect = [None,  # Primer
                                    build_result(12, 42), None,  # Latencies
                                    None, build_result(32, 13)]  # Totals

        rand_subdomains = ["rand_{}".format(i) for i in range(num_tries)]
        mock_rand_subdomain.side_effect = rand_subdomains

        recursive_ip = "a"
        auth_ip = "b"
        domain = "c"
        run_test.run_test(recursive_ip, auth_ip, domain, num_tries)

        self.assertEqual((num_tries * 2) + 1, mock_run_dig.call_count)
        dig_calls = [call(domain=domain, target_server=recursive_ip, time=run_test.TIME_LIMIT)] + \
                    [call(domain=domain, target_server=recursive_ip, time=run_test.TIME_LIMIT)] * num_tries + \
                    [call(domain="{}.{}".format(rand_subdomains[i], domain), target_server=recursive_ip,
                          time=run_test.TIME_LIMIT) for i in range(num_tries)]
        mock_run_dig.assert_has_calls(dig_calls)

        self.assertEqual(num_tries, mock_rand_subdomain.call_count)

        self.assertEqual(1, mock_print.call_count)
        mock_print.assert_has_calls([call("{},{},12,42,32,13,20".format(recursive_ip, auth_ip))])

    @patch.object(run_test, 'rand_subdomain')
    @patch.object(run_test, 'run_dig')
    @patch('builtins.print')
    def test_multipleGoodEach(self, mock_print, mock_run_dig, mock_rand_subdomain):
        num_tries = 3

        mock_run_dig.side_effect = [None,  # Primer
                                    build_result(1,6), build_result(2,7), build_result(3,5),  # Latencies
                                    build_result(6,3), build_result(5,12), build_result(4,64)]  # Totals

        rand_subdomains = ["rand_{}".format(i) for i in range(num_tries)]
        mock_rand_subdomain.side_effect = rand_subdomains

        recursive_ip = "a"
        auth_ip = "b"
        domain = "c"
        run_test.run_test(recursive_ip, auth_ip, domain, num_tries)

        self.assertEqual((num_tries * 2) + 1, mock_run_dig.call_count)
        dig_calls = [call(domain=domain, target_server=recursive_ip, time=run_test.TIME_LIMIT)] + \
                    [call(domain=domain, target_server=recursive_ip, time=run_test.TIME_LIMIT)] * num_tries + \
                    [call(domain="{}.{}".format(rand_subdomains[i], domain), target_server=recursive_ip,
                          time=run_test.TIME_LIMIT) for i in range(num_tries)]
        mock_run_dig.assert_has_calls(dig_calls)

        self.assertEqual(num_tries, mock_rand_subdomain.call_count)

        self.assertEqual(1, mock_print.call_count)
        mock_print.assert_has_calls([call("{},{},1,6,4,64,3".format(recursive_ip, auth_ip))])
