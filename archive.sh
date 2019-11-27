#!/bin/sh

zip -r "results_$(cat results/TEST_START).zip" results
rm results/*.csv
rm results/TEST_START
rm results/TEST_END
rm results/CONFIG
