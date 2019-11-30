#!/usr/bin/python3.4
import sys
from statistics import mean, stdev

from dig import run_dig
from stat_utils import generate_statistics, calculate_coefficient_of_variation


def test_reliability(target_ip, domain, trials, max_cov):
    results = []

    for _ in range(trials):
        result = run_dig(domain=domain, target_server=target_ip)

        if result is not None and result.status == "NOERROR" and result.AUTHORITY > 0:
            results.append(result.query_time)

    if len(results) >= 2 and calculate_coefficient_of_variation(mean(results), stdev(results)) <= max_cov:
        print("{},{}".format(target_ip, generate_statistics(results)))


if __name__ == "__main__":
    test_reliability(sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4]))
