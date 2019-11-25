#!/bin/bash

zip -r "results_$(date +"%Y-%m-%d").zip" results
rm results/*.csv