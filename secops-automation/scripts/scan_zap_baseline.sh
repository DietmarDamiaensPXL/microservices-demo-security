#!/bin/bash
set -euo pipefail

TARGET="http://host.docker.internal:8080"
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