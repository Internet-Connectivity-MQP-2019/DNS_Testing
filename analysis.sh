#!/bin/sh

export LANG="C"

if [ ! -f results/geolocation.csv ]; then
    echo "Geolocation file required!"
    exit 1
fi

COV_MAX="0.2"
JOB_COUNT=32

echo "Steps 9 & 10"
echo "recursive_ip" > results/reliable_recursive_ips.csv
./parallel -a results/recursive_reliability_results.csv --colsep , --header '.*\n' --progress --eta --jobs $JOB_COUNT ./filter_coefficient_of_variance.py {1} {2} {3} {4} {5} $COV_MAX >> results/reliable_recursive_ips.csv

echo "authoritative_ip" > results/reliable_authoritative_ips.csv
./parallel -a results/authoritative_reliability_results.csv --colsep , --header '.*\n' --progress --eta --jobs $JOB_COUNT ./filter_coefficient_of_variance.py {1} {2} {3} {4} {5} $COV_MAX >> results/reliable_authoritative_ips.csv

echo "Step 11"
echo "recursive_state,authoritative_state,min_rtt,max_rtt,mean_rtt,median_rtt" > results/aggregation_state_to_state.csv
./aggregate_state_to_state.py results/test_results.csv results/reliable_recursive_ips.csv results/reliable_authoritative_ips.csv results/geolocation.csv >> results/aggregation_state_to_state.csv
