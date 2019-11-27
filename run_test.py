#!/usr/bin/python3.4
import random
import string
import sys
from dig import run_dig

TIME_LIMIT = 2


def rand_subdomain(length=12):
    """
    Generate a random subdomain
    :param length: the length of the random string to generate. Default: 12
    :return: a random subdomain (string of lower and uppercase characters)
    """
    ret = ""
    for i in range(length):
        ret += random.choice(string.ascii_letters)
    return ret


def run_test(recursive_ip, auth_ip, domain, tries):
    """
    Run a test between two servers
    :param recursive_ip: the recursive server to target
    :param auth_ip: the authoritative server to target
    :param domain: a domain that the authoritative server has authority over
    :param tries: number of attempts to get latency and total
    :return: Nothing
    """

    # Step 1: Prime the cache
    run_dig(domain=domain, target_server=recursive_ip, time=TIME_LIMIT)

    # Step 2: Measure latency
    latency_results = [r.query_time for r in
                       [run_dig(domain=domain, target_server=recursive_ip, time=TIME_LIMIT) for _ in range(tries)]
                       if r is not None]

    # Step 3: Measure total time
    total_results = [r.query_time for r in
                     [run_dig(domain="{}.{}".format(rand_subdomain(), domain),
                              target_server=recursive_ip, time=TIME_LIMIT) for _ in range(tries)]
                     if r is not None]

    # Report the results if we got enough data
    if len(latency_results) > 0 and len(total_results) > 0:
        latency = min(latency_results)
        total = min(total_results)
        rtt = total - latency

        print("{},{},{},{},{}".format(recursive_ip, auth_ip, latency, total, rtt))


if __name__ == "__main__":
    if len(sys.argv) > 5:
        TIME_LIMIT = int(sys.argv[5])

    run_test(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]))
