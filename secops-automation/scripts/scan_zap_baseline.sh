#!/bin/bash
set -euo pipefail

# Config
TARGET=${1:-http://localhost:8081}   # frontend target, default naar je port-forward
OUTDIR="secops-automation/scans/zap/$(date +%F_%H-%M-%S)"
mkdir -p "$OUTDIR"

# Run ZAP baseline using docker image (stable)
# outputs HTML and JSON
docker run --rm -v "$PWD/$OUTDIR":/zap/wrk/:rw owasp/zap2docker-stable zap-baseline.py -t "$TARGET" -r /zap/wrk/report.html -J /zap/wrk/report.json

echo "[✓] ZAP baseline finished. Reports: $OUTDIR/report.html and $OUTDIR/report.json"

