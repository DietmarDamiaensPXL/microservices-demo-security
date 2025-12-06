#!/bin/bash
set -euo pipefail

TARGET="http://host.docker.internal:8081"
TS=$(date +%F_%H-%M-%S)

OUT_DIR="scans/zap/$TS"
mkdir -p "$OUT_DIR"

echo "[i] Running ZAP baseline scan on: $TARGET"

docker run --rm \
    --add-host=host.docker.internal:host-gateway \
    -v "$PWD/$OUT_DIR:/zap/wrk:rw" \
    zaproxy/zap-stable \
    zap-baseline.py \
        -t "$TARGET" \
        -r report.html \
        -J report.json

echo "[✓] ZAP scan finished"
echo "Output saved in $OUT_DIR"



##!/bin/bash
#set -euo pipefail

# Config
#TARGET=${1:-http://localhost:8081}   # frontend target, default naar je port-forward
#TS=$(date +%F_%H-%M-%S)

#Output directories
#SCAN_OUT="secops-automation/scans/zap/${TS}"
#REPORT_HTML="secops-automation/reports/html/zap_${TS}.html"
#REPORT_JSON="secops-automation/reports/zap_${TS}.json"

#mkdir -p "$SCAN_OUT"
#mkdir -p "secops-automation/reports/html"
#mkdir -p "secops-automation/reports"

#echo "[i] Running ZAP Baseline Scan on: $TARGET"
#echo "[i] Output:"
#echo "    - $SCAN_OUT"
#echo "    - $REPORT_HTML"
#echo "    - $REPORT_JSON"

# Run ZAP baseline using docker image (stable)
# outputs HTML and JSON
#docker run --rm -v "$PWD/$SCAN_OUT":/zap/wrk/:rw owasp/zap2docker-stable \
#    zap-baseline.py \
#    -t "$TARGET" \
#    -r "/zap/wrk/report.html" \
#    -J "/zap/wrk/report.json"

# Move results to final report folders
#mv "$SCAN_OUT/report.html" "$REPORT_HTML"
#mv "$SCAN_OUT/report.json" "$REPORT_JSON"

#echo "[✓] ZAP Baseline scan complete!"
#echo "HTML report → $REPORT_HTML"
#echo "JSON report → $REPORT_JSON"
#echo "Raw files   → $SCAN_OUT"
