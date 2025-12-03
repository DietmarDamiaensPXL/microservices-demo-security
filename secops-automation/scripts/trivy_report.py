#!/usr/bin/env python3
import os
import json
import glob
from datetime import datetime
import pandas as pd
import requests

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCAN_DIR = os.path.join(base, "scans", "trivy")
REPORT_DIR = os.path.join(base, "reports")
HTML_DIR = os.path.join(REPORT_DIR, "html")
os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(HTML_DIR, exist_ok=True)

# Vind de laatste scan
scan_dirs = sorted(os.listdir(SCAN_DIR))
if not scan_dirs:
    print("Geen scans!")
    exit(1)

latest_dir = os.path.join(SCAN_DIR, scan_dirs[-1])
print(f"[*] Latest scan: {latest_dir}")

severity_data = []

for json_file in glob.glob(f"{latest_dir}/*.json"):
    with open(json_file) as f:
        data = json.load(f)

    image = os.path.basename(json_file).replace(".json", "")
    counts = {s: 0 for s in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "UNKNOWN"]}

    for result in data.get("Results", []):
        for vuln in result.get("Vulnerabilities", []) or []:
            sev = vuln.get("Severity", "UNKNOWN").upper()
            if sev not in counts:
                sev = "UNKNOWN"
            counts[sev] += 1

    severity_data.append({"Image": image, **counts})

df = pd.DataFrame(severity_data)
df = df.sort_values(by=["CRITICAL", "HIGH"], ascending=False)

# Pushgateway payload
gateway = "http://localhost:9091/metrics/job/trivy_scan"
payload = ""

for _, row in df.iterrows():
    image = row["Image"].replace('"', '\\"')
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "UNKNOWN"]:
        metric = f"trivy_{sev.lower()}"
        payload += f'{metric}{{image="{image}"}} {row[sev]}\n'

print("[+] Pushing metrics...")
requests.post(gateway, data=payload)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

csv_file = f"{REPORT_DIR}/trivy_severity_{timestamp}.csv"
md_file = f"{REPORT_DIR}/trivy_severity_{timestamp}.md"
html_file = f"{HTML_DIR}/trivy_severity_{timestamp}.html"

df.to_csv(csv_file, index=False)
df.to_markdown(md_file, index=False)
df.to_html(html_file, index=False)

print("[✓] CSV opgeslagen:", csv_file)
print("[✓] Markdown opgeslagen:", md_file)
print("[✓] HTML opgeslagen:", html_file)
print("[✓] Metrics gepushed naar Prometheus")

