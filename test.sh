#!/bin/bash

JOB_COUNT=32

MAXMIND_DB="GeoIP2-City.mmdb"
RECURSIVE_CONFIRMATION_DOMAIN="cnn.com"
RECURSIVE_RELIABILITY_DOMAIN="cnn.com"
RECURSIVE_RELIABILITY_TRIAL_COUNT=10
AUTHORITATIVE_RELIABILITY_TRIAL_COUNT=10
TEST_TRIAL_COUNT="3"
TEST_TRY_COUNT="3"

echo "Step 1"
echo "ip_address" > results/recursive_confirmed.csv
./parallel -a candidates/recursive_candidates.csv --colsep , --header '.*\n' --progress --eta --jobs $JOB_COUNT ./confirm_recursive.py {1} $RECURSIVE_CONFIRMATION_DOMAIN >> results/recursive_confirmed.csv

echo "Step 2"
echo "ip_address,domain" > results/authoritative_confirmed.csv
./parallel -a candidates/authoritative_candidates.csv --colsep , --header '.*\n' --progress --eta --jobs $JOB_COUNT ./confirm_authoritative.py {2} {1} >> results/authoritative_confirmed.csv

echo "Steps 3&4"
if python -c "import geoip2" &> /dev/null; then
    echo "ip_address,state,latitute,longitude,zip" > results/geolocation.csv
    ./geolocation.py results/recursive_confirmed.csv $MAXMIND_DB >> results/geolocation.csv
    ./geolocation.py results/authoritative_confirmed.csv $MAXMIND_DB >> results/geolocation.csv
else
    echo 'Geolocation requires the python module "geoip2". Either run ./geolocation.sh on a different machine, or install the module.'
fi

echo "Step 5"
echo "ip_address,median,mean,standard_deviation,variance" > results/recursive_reliability_results.csv
./parallel -a results/recursive_confirmed.csv --colsep , --header '.*\n' --progress --eta --jobs $JOB_COUNT ./recursive_reliability.py {1} $RECURSIVE_RELIABILITY_DOMAIN $RECURSIVE_RELIABILITY_TRIAL_COUNT >> results/recursive_reliability_results.csv

echo "Step 6"
echo "ip_address,median,mean,standard_deviation,variance" > authoritative_reliability_results.csv
./parallel -a results/authoritative_confirmed.csv --colsep , --header '.*\n' --progress --eta --jobs $JOB_COUNT ./authoritative_reliability.py {1} {2} $AUTHORITATIVE_RELIABILITY_TRIAL_COUNT >> results/authoritative_reliability_results.csv

echo "Step 7"
echo "recursive_ip,authoritative_ip,domain" > results/test_pairs.csv
./generate_pairs.py results/recursive_confirmed.csv results/authoritative_confirmed.csv $TEST_TRIAL_COUNT >> results/test_pairs.csv

echo "Step 8"
echo "recursive_ip,authoritative_ip,rtt" > results/test_results.csv
./parallel -a results/test_pairs.csv --colsep , --header '.*\n' --progress --eta --jobs $JOB_COUNT ./run_test.py {1} {2} {3} $TEST_TRY_COUNT >> results/test_results.csv
