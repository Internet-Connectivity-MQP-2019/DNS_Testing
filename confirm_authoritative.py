#!/usr/bin/python3.4
import sys
from DigForPy.dig import run_dig


def confirm_authoritative(authoritative_ip, domain):
    result = run_dig(domain=domain, target_server=authoritative_ip)

    if result is not None and result.status == "NOERROR" and result.AUTHORITY > 0:
        print("{},{}".format(authoritative_ip, domain))


if __name__ == "__main__":
    confirm_authoritative(sys.argv[1], sys.argv[2])
