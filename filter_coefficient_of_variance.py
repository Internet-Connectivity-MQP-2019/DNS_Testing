#!/usr/bin/python3.4

import sys
from stat_utils import calculate_coefficient_of_variation


def filter_cov(ip, mean, stdev, max_cov):
    if calculate_coefficient_of_variation(mean, stdev) <= max_cov:
        print(ip)


# Input: ip_address (1), median (2), mean (3), standard_deviation (4), variance (5), max CoV (6)
if __name__ == "__main__":
    filter_cov(sys.argv[1], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[6]))
