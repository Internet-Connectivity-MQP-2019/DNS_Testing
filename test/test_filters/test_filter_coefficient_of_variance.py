import random
import unittest
from unittest.mock import patch, call

import filter_coefficient_of_variance


class MyTestCase(unittest.TestCase):

    @patch.object(filter_coefficient_of_variance, 'calculate_coefficient_of_variation')
    @patch("builtins.print")
    def test_aboveMax(self, mock_print, mock_calculate):
        max = [1.0, 0.5, 20.0, 100]
        cov = [i + random.random() for i in max]

        ips = ["ip_address_{}".format(i) for i in range(len(max))]
        means = [i for i in range(len(max))]
        stdevs = [i**2 for i in range(len(max))]

        mock_calculate.side_effect = cov

        for i in range(len(max)):
            filter_coefficient_of_variance.filter_cov(ips[i], means[i], stdevs[i], max[i])

        self.assertEqual(len(max), mock_calculate.call_count)
        mock_calculate.assert_has_calls([call(means[i], stdevs[i]) for i in range(len(max))])

        self.assertEqual(0, mock_print.call_count)

    @patch.object(filter_coefficient_of_variance, 'calculate_coefficient_of_variation')
    @patch("builtins.print")
    def test_belowAndEqualToMax(self, mock_print, mock_calculate):
        max = [1.0, 0.5, 20.0, 100]
        cov = [0.99, 0, 20.0, 50]

        ips = ["ip_address_{}".format(i) for i in range(len(max))]
        means = [i for i in range(len(max))]
        stdevs = [i**2 for i in range(len(max))]

        mock_calculate.side_effect = cov

        for i in range(len(max)):
            filter_coefficient_of_variance.filter_cov(ips[i], means[i], stdevs[i], max[i])

        self.assertEqual(len(max), mock_calculate.call_count)
        mock_calculate.assert_has_calls([call(means[i], stdevs[i]) for i in range(len(max))])

        self.assertEqual(4, mock_print.call_count)
        mock_print.assert_has_calls([call(ip) for ip in ips])

