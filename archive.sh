#!/bin/bash

zip -r "results_$(date +"%s").zip" results
rm results/*.csv