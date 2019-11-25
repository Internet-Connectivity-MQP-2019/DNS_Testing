#!/bin/bash

echo "Steps 3&4"
echo "ip_address,state,latitute,longitude,zip" > results/geolocation.csv
./geolocation.py results/recursive_confirmed.csv $MAXMIND_DB >> results/geolocation.csv
./geolocation.py results/authoritative_confirmed.csv $MAXMIND_DB >> results/geolocation.csv