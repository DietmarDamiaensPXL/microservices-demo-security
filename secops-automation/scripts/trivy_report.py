#!/usr/bin/env python3
import os
import json
import glob
from datetime import datetime
import pandas as pd

# Path naar laatste Trivy scan
SCAN_DIR = "secops-automation/scans/trivy"
REPORT_DIR = "secops-automation/reports"
os.makedirs(REPORT_DIR, exist_ok=True)

# Vind nieuwste scanmap
scan_timestamps = sorted(os.listdir(SCAN_DIR))
if not scan_timestamps:
    print("Geen Trivy scans gevonden.")
    exit(1)

latest_scan_dir = os.path.join(SCAN_DIR, scan_timestamps[-1])
print(f"[*] Latest scan: {latest_scan_dir}")

# Parse JSON files
severity_data = []

for json_file in glob.glob(f"{latest_scan_dir}/*.json"):
    with open(json_file) as f:
        data = json.load(f)
    image = os.path.basename(json_file).replace(".json","")
    
    # Tel vulnerabilities per severity
    counts = {"CRITICAL":0, "HIGH":0, "MEDIUM":0, "LOW":0, "UNKNOWN":0}
    for vuln in data.get("Results", []):
        for v in vuln.get("Vulnerabilities", []) or []:
            sev = v.get("Severity", "UNKNOWN").upper()
            if sev not in counts:
                sev = "UNKNOWN"
            counts[sev] += 1

    severity_data.append({
        "Image": image,
        **counts
    })

# Zet om naar dataframe
df = pd.DataFrame(severity_data)
df = df.sort_values(by=["CRITICAL","HIGH"], ascending=False)

# Sla op als CSV en Markdown
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
csv_file = os.path.join(REPORT_DIR, f"trivy_severity_{timestamp}.csv")
md_file = os.path.join(REPORT_DIR, f"trivy_severity_{timestamp}.md")

df.to_csv(csv_file, index=False)
df.to_markdown(md_file, index=False)

print(f"[✓] Severity tabel opgeslagen als CSV: {csv_file}")
print(f"[✓] Severity tabel opgeslagen als Markdown: {md_file}")

