#!/bin/bash
set -euo pipefail

timestamp=$(date +"%Y-%m-%d_%H-%M-%S")
outdir="secops-automation/scans/trivy/$timestamp"
mkdir -p "$outdir"

echo "[*] Ophalen images uit Kubernetes..."
images=$(kubectl get pods --all-namespaces -o jsonpath="{range .items[*]}{.spec.containers[*].image}{'\n'}{end}" | sort -u)

if [ -z "$images" ]; then
  echo "Geen images gevonden in cluster."
  exit 1
fi

echo "[*] Te scannen images:"
echo "$images"

for img in $images; do
  # schone bestandsnaam
  fname=$(echo "$img" | sed 's/[\/:@]/_/g')
  out="$outdir/${fname}.json"
  echo "[*] Trivy scan: $img -> $out"
  # scan remote of local image
  trivy image --format json -o "$out" "$img" || echo "[!] Trivy had fout op $img (ga door)"
done

echo "[✓] Trivy scans opgeslagen in: $outdir"

