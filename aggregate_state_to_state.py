#!/usr/bin/python3.4
import sys
import csv
from statistics import mean, median


def aggregate(results_filename, reliable_rec_filename, reliable_auth_filename, geolocation_filename):
    reliable_ips = []

    with open(reliable_rec_filename, 'r', newline='\n') as f:
        r = csv.reader(f)
        next(r, None)
        reliable_ips += [row[0] for row in r]

    with open(reliable_auth_filename, 'r', newline='\n') as f:
        r = csv.reader(f)
        next(r, None)
        reliable_ips += [row[0] for row in r]

    with open(geolocation_filename, 'r', newline='\n') as f:
        r = csv.reader(f)
        next(r, None)
        location_dict = dict((row[0], row[1]) for row in r if row[0] in reliable_ips)

    # Note: valid IPs are both reliable and located, so the above combines both criteria into "location_dict"
    # If an IP is not reliable, it isn't put in that dict, even if it has a location

    aggregated_results = {}

    with open(results_filename, 'r', newline='\n') as f:
        r = csv.reader(f)
        next(r, None)

        for row in r:
            rec_ip = row[0]
            auth_ip = row[1]
            if rec_ip in location_dict and auth_ip in location_dict:
                rec_state = location_dict[rec_ip]
                auth_state = location_dict[auth_ip]
                if rec_state not in aggregated_results:
                    aggregated_results[rec_state] = {}

                if auth_state not in aggregated_results[rec_state]:
                    aggregated_results[rec_state][auth_state] = []

                aggregated_results[rec_state][auth_state].append(int(row[4]))

    for i in sorted(aggregated_results.keys()):
        for j in sorted(aggregated_results[i].keys()):
            results = aggregated_results[i][j]
            print("{},{},{},{},{:.2f},{:.2f}".format(i, j, min(results), max(results), mean(results), median(results)))


# <result_file> <reliable_recursive_ips_file> <reliable_auth_ips_file> <geolocation_file>
if __name__ == "__main__":
    aggregate(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
