#!/bin/bash
OUTPUT_DIR="../scans/trivy"
IMAGES=$(docker images --format '{{.Repository}}:{{.Tag}}')

mkdir -p $OUTPUT_DIR

echo "[INFO] Running Trivy scans..."

for IMAGE in $IMAGES; do
    SAFE_NAME=$(echo $IMAGE | tr '/:' '__')
    trivy image --severity CRITICAL,HIGH --format json -o "$OUTPUT_DIR/${SAFE_NAME}.json" $IMAGE
    echo "[DONE] Scanned $IMAGE"
done

