#!/bin/bash

# This script kills any process whose command line contains /256- or /512-
# Useful for terminating specific gem5 simulations continuously

PATTERN='/(256|512)-'
INTERVAL=5  # seconds between checks

echo "Monitoring and killing processes with pattern '$PATTERN' every $INTERVAL seconds..."

while true; do
    # List processes, filter by regex
    PIDS=$(ps axww | grep -E "$PATTERN" | grep gem5.opt | grep -v grep | awk '{print $1}')
    
    if [ -n "$PIDS" ]; then
        echo "Found matching PIDs: $PIDS"
        for pid in $PIDS; do
            echo "Killing PID: $pid"
            kill -9 "$pid"
        done
    fi

    sleep "$INTERVAL"
done
