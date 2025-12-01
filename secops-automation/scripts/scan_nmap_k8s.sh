#!/bin/bash
OUTPUT_DIR="../scans/nmap"
TARGETS=$(docker network inspect <naam docker netwerk> | jq -r '.[0].Containers[].IPv4Address' | sed 's|/.*||')
mkdir -p $OUTPUT_DIR

echo "[INFO] Running Nmap scans..."

for IP in $TARGETS; do
    nmap -sV -O -oN "$OUTPUT_DIR/nmap_$IP.txt" $IP
    echo "[DONE] Scanned $IP"
done

