#!/bin/sh

export LANG="C"

if [ ! -f results/geolocation.csv ]; then
    echo "Geolocation file required!"
    exit 1
fi

COV_MAX="0.2"
JOB_COUNT=32

echo "Step 13"
echo "recursive_state,authoritative_state,min_rtt,max_rtt,mean_rtt,median_rtt" > results/aggregation_state_to_state.csv
./aggregate_state_to_state.py results/test_results.csv results/reliable_recursive_ips.csv results/reliable_authoritative_ips.csv results/geolocation.csv >> results/aggregation_state_to_state.csv
