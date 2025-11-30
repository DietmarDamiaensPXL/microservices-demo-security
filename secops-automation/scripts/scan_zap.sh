#!/bin/bash
OUTPUT_DIR="../scans/zap"
mkdir -p $OUTPUT_DIR

TARGET_URL="http://localhost:8080"

echo "[INFO] Starting OWASP ZAP baseline scan..."

docker run -v $(pwd)/$OUTPUT_DIR:/zap/wrk \
    zaproxy/zap-stable zap-baseline.py \
    -t $TARGET_URL \
    -r zap_report.html \
    -J zap_report.json

echo "[DONE] ZAP scan completed."


// ADJUST TARGET_URL etc
