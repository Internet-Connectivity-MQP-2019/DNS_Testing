#!/bin/bash

MAXMIND_DB="GeoIP2-City.mmdb"

echo "Steps 3&4"
echo "ip_address,state,latitute,longitude,zip" > results/geolocation.csv
python3.6 geolocation.py $MAXMIND_DB results/recursive_confirmed.csv >> results/geolocation.csv
python3.6 geolocation.py $MAXMIND_DB results/authoritative_confirmed.csv >> results/geolocation.csv
