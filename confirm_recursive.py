#!/usr/bin/python3.4
import sys
from dig import run_dig


def confirm_recursive(recursive_ip, domain):
    result = run_dig(domain=domain, target_server=recursive_ip)

    if result is not None and result.status == "NOERROR" and not result.recursion_not_available and (result.ANSWER > 0 or result.AUTHORITY > 0):
        print(recursive_ip)


if __name__ == "__main__":
    confirm_recursive(sys.argv[1], sys.argv[2])
