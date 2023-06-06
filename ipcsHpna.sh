#!/bin/bash

# Create a unique key for the shared memory segment
key=$(date +%s)

# Allocate a shared memory segment
shmid=$(ipcs -m | awk -v key="$key" '$1 == "0x00000000" && $3 == key {print $2}')
if [ -z "$shmid" ]; then
    shmid=$(ipcmk -M -K $key)
fi

# Attach the shared memory segment to a variable
data=$(ipcs -m | awk -v shmid="$shmid" '$2 == shmid {print $6}')
if [ -z "$data" ]; then
    data=$(ipcrm -m $shmid &>/dev/null && ipcs -m | awk -v shmid="$shmid" '$2 == shmid {print $6}')
    if [ -z "$data" ]; then
        echo "Failed to allocate shared memory segment"
        exit 1
    fi
fi

# Write data to the shared memory segment
echo "Hello, shared memory!" > $data

# Read the data from the shared memory segment
read_data=$(cat $data)
echo "Data read from shared memory: $read_data"

# Detach and remove the shared memory segment
ipcrm -m $shmid
