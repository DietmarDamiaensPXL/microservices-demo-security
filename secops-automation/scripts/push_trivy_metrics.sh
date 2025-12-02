#!/bin/bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPORT_DIR="$ROOT/reports"
PUSHGATEWAY="http://pushgateway.default.svc.cluster.local:9091"
JOB_NAME="trivy_image_scan"

csv_file=$(ls -t "$REPORT_DIR"/trivy_severity_*.csv | head -n1)

if [ -z "$csv_file" ]; then
  echo "No CSV found"
  exit 1
fi

echo "[*] Using CSV: $csv_file"
metrics=""

while IFS=, read -r Image CRITICAL HIGH MEDIUM LOW UNKNOWN; do
  if [ "$Image" = "Image" ]; then continue; fi
  img_label=$(echo "$Image" | sed 's/"/\\"/g')
  metrics+="trivy_critical{image=\"$img_label\"} $CRITICAL
trivy_high{image=\"$img_label\"} $HIGH
trivy_medium{image=\"$img_label\"} $MEDIUM
trivy_low{image=\"$img_label\"} $LOW
trivy_unknown{image=\"$img_label\"} $UNKNOWN
"
done < "$csv_file"

echo -e "$metrics" | curl --data-binary @- "$PUSHGATEWAY/metrics/job/$JOB_NAME"

echo "[✓] Pushed metrics to Prometheus via Pushgateway"

