#!/usr/bin/python3.4
import sys
from statistics import mean, stdev

from DigForPy.dig import run_dig
from stat_utils import generate_statistics, calculate_coefficient_of_variation


def test_reliability(recursive_ip, domain, trials, max_cov):
    results = []

    # Prime the recursive_server
    run_dig(domain=domain, target_server=recursive_ip)

    for _ in range(trials):
        result = run_dig(domain=domain, target_server=recursive_ip)

        if result is not None \
                and result.status == "NOERROR" and not result.recursion_not_available \
                and result.ANSWER > 0 and result.AUTHORITY == 0:
            results.append(result.query_time)

    if len(results) >= 2 and calculate_coefficient_of_variation(mean(results), stdev(results)) <= max_cov:
        print("{},{}".format(recursive_ip, generate_statistics(results)))


if __name__ == "__main__":
    test_reliability(sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4]))
