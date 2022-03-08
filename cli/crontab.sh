#!/bin/bash

LOG="$1"
if [ "x" == "x$LOG" ]; then
    DATE=$(date "+%Y-%m-%d")
    LOG="out/monitorapa.$PID.$DATE.log"
fi

CURRENT_DIR=$(./cli/point1.py |tee -a $LOG)

if [ ! -f "$CURRENT_DIR/enti.tsv" ]; then
    echo "Error in point1: no enti.tsv in $CURRENT_DIR" | tee -a $LOG
    exit 1
fi

python3 -u ./cli/point2parallel.py check/google_analytics.js $CURRENT_DIR/enti.tsv 13000 >> $LOG 2>&1

# ./cli/point4.py check/google_analytics.js $CURRENT_DIR/enti.tsv 30 >> $LOG 2>&1
