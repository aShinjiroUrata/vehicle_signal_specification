#!/bin/bash

cat ../vss_rel_1.0.csv | grep -v "Row5" | grep -v "Row4" | grep -v "Row3" | grep -v "Row2" \
                       | grep -v "Pos5" | grep -v "Pos4" | grep -v "Pos3" | grep -v "Pos2" \
                       | grep -v "branch" > vss_rel_1.0_reduce.csv

