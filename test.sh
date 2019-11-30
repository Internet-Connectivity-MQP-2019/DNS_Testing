#!/bin/sh

export LANG="C"

JOB_COUNT=32

MAXMIND_DB="GeoIP2-City.mmdb"
RECURSIVE_CONFIRMATION_DOMAIN="cnn.com"
RECURSIVE_RELIABILITY_DOMAIN="cnn.com"
RECURSIVE_RELIABILITY_TRIAL_COUNT=20
AUTHORITATIVE_RELIABILITY_TRIAL_COUNT=20
TEST_TRIAL_COUNT="5"
TEST_TRY_COUNT="3"
TIMEOUT="3"
MAX_COV="0.2"
COV_MAX="0.2"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
echo $TIMESTAMP > results/TEST_START

echo "MAXMIND_DB: $MAXMIND_DB\nRECURSIVE_CONFIRMATION_DOMAIN: $RECURSIVE_CONFIRMATION_DOMAIN\nRECURSIVE_RELIABILITY_DOMAIN: $RECURSIVE_RELIABILITY_DOMAIN\nRECURSIVE_RELIABILITY_TRIAL_COUNT: $RECURSIVE_RELIABILITY_TRIAL_COUNT\nAUTHORITATIVE_RELIABILITY_TRIAL_COUNT: $AUTHORITATIVE_RELIABILITY_TRIAL_COUNT\nTEST_TRIAL_COUNT: $TEST_TRIAL_COUNT\nTEST_TRY_COUNT: $TEST_TRY_COUNT\nTIMEOUT: $TIMEOUT" > results/CONFIG

cp candidates/recursive_candidates.csv results/
cp candidates/authoritative_candidates.csv results/

echo "Step 1"
echo "ip_address" > results/recursive_confirmed.csv
./parallel -a results/recursive_candidates.csv --colsep , --header '.*\n' --progress --eta --jobs $JOB_COUNT ./confirm_recursive.py {1} $RECURSIVE_CONFIRMATION_DOMAIN >> results/recursive_confirmed.csv

echo "Step 2"
echo "ip_address,domain" > results/authoritative_confirmed.csv
./parallel -a results/authoritative_candidates.csv --colsep , --header '.*\n' --progress --eta --jobs $JOB_COUNT ./confirm_authoritative.py {2} {1} >> results/authoritative_confirmed.csv

echo "Steps 3&4"
if python -c "import geoip2" &> /dev/null; then
    echo "ip_address,state,latitude,longitude,zip" > results/geolocation.csv
    ./geolocation.py $MAXMIND_DB results/recursive_confirmed.csv >> results/geolocation.csv
    ./geolocation.py $MAXMIND_DB results/authoritative_confirmed.csv >> results/geolocation.csv
else
    echo 'Geolocation requires the python module "geoip2". Either run ./geolocation.sh on a different machine, or install the module.'
fi

echo "Step 5"
echo "ip_address,median,mean,standard_deviation,variance" > results/recursive_reliability_results.csv
./parallel -a results/recursive_confirmed.csv --colsep , --header '.*\n' --progress --eta --jobs $JOB_COUNT ./recursive_reliability.py {1} $RECURSIVE_RELIABILITY_DOMAIN $RECURSIVE_RELIABILITY_TRIAL_COUNT $MAX_COV >> results/recursive_reliability_results.csv

echo "Step 6"
echo "ip_address,median,mean,standard_deviation,variance" > results/authoritative_reliability_results.csv
./parallel -a results/authoritative_confirmed.csv --colsep , --header '.*\n' --progress --eta --jobs $JOB_COUNT ./authoritative_reliability.py {1} {2} $AUTHORITATIVE_RELIABILITY_TRIAL_COUNT $MAX_COV >> results/authoritative_reliability_results.csv

echo "Steps 7 & 8"
echo "recursive_ip" > results/reliable_recursive_ips.csv
./parallel -a results/recursive_reliability_results.csv --colsep , --header '.*\n' --progress --eta --jobs $JOB_COUNT ./filter_coefficient_of_variance.py {1} {2} {3} {4} {5} $COV_MAX >> results/reliable_recursive_ips.csv
echo "authoritative_ip" > results/reliable_authoritative_ips.csv
./parallel -a results/authoritative_reliability_results.csv --colsep , --header '.*\n' --progress --eta --jobs $JOB_COUNT ./filter_coefficient_of_variance.py {1} {2} {3} {4} {5} $COV_MAX >> results/reliable_authoritative_ips.csv

echo "Actually Filtering..."
echo "Step 9"
echo "ip_address" > results/reliable_recursive_half.csv
./parallel -a results/reliable_recursive_ips.csv --colsep , --header '.*\n' --progress --eta --jobs $JOB_COUNT grep {1} results/recursive_confirmed.csv >> results/reliable_recursive_half.csv
echo "Step 10"
echo "ip_address,domain" > results/reliable_authoritative_half.csv
./parallel -a results/reliable_authoritative_ips.csv --colsep , --header '.*\n' --progress --eta --jobs $JOB_COUNT grep {1} results/authoritative_confirmed.csv >> results/reliable_authoritative_half.csv

echo "Step 11"
echo "recursive_ip,authoritative_ip,domain" > results/test_pairs.csv
./generate_pairs.py results/reliable_recursive_half.csv results/reliable_authoritative_half.csv $TEST_TRIAL_COUNT >> results/test_pairs.csv

echo "Step 12"
echo "recursive_ip,authoritative_ip,latency,total,rtt" > results/test_results.csv
./parallel -a results/test_pairs.csv --colsep , --header '.*\n' --progress --eta --jobs $JOB_COUNT ./run_test.py {1} {2} {3} $TEST_TRY_COUNT $TIMEOUT >> results/test_results.csv

echo $(date +"%Y%m%d_%H%M%S") > results/TEST_END

./analysis.sh

./archive.sh

cp results_$TIMESTAMP.zip ~/public_html/
chmod ugo+r ~/public_html/results_$TIMESTAMP.zip

echo "DNS test started at $TIMESTAMP and is now complete! Results filepath is: https://users.wpi.edu/~stgoldman/results_$TIMESTAMP.zip. Enjoy!" | nail -s "DNS Test Complete" stgoldman@wpi.edu
