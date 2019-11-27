#!/bin/bash

zip -r "results_$(cat results/TEST_START).zip" results
rm results/*.csv