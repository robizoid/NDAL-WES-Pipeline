#!/bin/bash

log_message() {
    local LOG_FILE=$1
    local MESSAGE=$2
    echo "$(date): $MESSAGE" >> "$LOG_FILE"
}

