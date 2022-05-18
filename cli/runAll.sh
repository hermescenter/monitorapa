#!/bin/bash

LOG="$1"
if [ "x" == "x$LOG" ]; then
    DATE=$(date "+%Y-%m-%d")
    LOG="out/monitorapa.$PID.$DATE.log"
fi

CURRENT_ENTI=$(./cli/point1.py |tee -a $LOG)

if [ ! -f "$CURRENT_ENTI" ]; then
    echo "Error in point1: no $CURRENT_DIR" | tee -a $LOG
    exit 1
fi

python3 -u ./cli/point2parallel.py check/google_analytics.js $CURRENT_ENTI 13000 >> $LOG 2>&1

# ./cli/point4.py check/google_analytics.js $CURRENT_ENTI 30 >> $LOG 2>&1
