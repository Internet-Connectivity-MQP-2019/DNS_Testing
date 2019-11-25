#!/usr/bin/python3.4
import sys
import geoip2.database


def geolocate_ips(database, filename):
    geoip = geoip2.database.Reader(database)

    with open(filename) as file:
        for line in file:
            ip = line.rstrip("\n")

            try:
                response = geoip.city(ip)
                if response.country.name == "United States":
                    state = response.subdivisions.most_specific.name
                    if state is not None:
                        print("{},{},{},{},{}".format(ip, state, response.location.latitude,
                                                      response.location.longitude, response.postal.code))
            except geoip2.errors.AddressNotFoundError:
                pass


if __name__ == "__main__":
    geolocate_ips(database=sys.argv[1], filename=sys.argv[2])
