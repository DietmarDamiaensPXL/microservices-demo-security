#!/usr/bin/env python3
import os
import json
import glob
from datetime import datetime
import pandas as pd
import requests

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCAN_DIR = os.path.join(base, "scans", "zap")
REPORT_DIR = os.path.join(base, "reports")
HTML_DIR = os.path.join(REPORT_DIR, "html")

os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(HTML_DIR, exist_ok=True)

# Vind de laatste ZAP-scan folder
scan_dirs = sorted(os.listdir(SCAN_DIR))
if not scan_dirs:
    print("Geen ZAP scans gevonden!")
    exit(1)

latest_dir = os.path.join(SCAN_DIR, scan_dirs[-1])
print(f"[*] Latest ZAP scan: {latest_dir}")

# Zoek het JSON ZAP-rapport (ZAP maakt 1 JSON per scan)
json_files = glob.glob(f"{latest_dir}/*.json")
if not json_files:
    print("Geen ZAP JSON rapport gevonden in de laatste scan!")
    exit(1)

report_file = json_files[0]
print(f"[*] Using report: {report_file}")

with open(report_file) as f:
    data = json.load(f)

# Severity counters (ZAP gebruikt High/Medium/Low/Informational)
counts = {"High": 0, "Medium": 0, "Low": 0, "Informational": 0}

for site in data.get("site", []):
    for alert in site.get("alerts", []):
        severity = alert.get("riskdesc", "").split(" ")[0]
        if severity in counts:
            counts[severity] += 1

df = pd.DataFrame([counts])

# Pushgateway payload
gateway = "http://pushgateway:9091/metrics/job/zap_scan"
payload = ""

for sev in ["High", "Medium", "Low", "Informational"]:
    metric = f"zap_{sev.lower()}"
    payload += f"{metric} {counts[sev]}\n"

print("[+] Pushing ZAP metrics...")
requests.post(gateway, data=payload)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

csv_file = f"{REPORT_DIR}/zap_severity_{timestamp}.csv"
md_file = f"{REPORT_DIR}/zap_severity_{timestamp}.md"
html_file = f"{HTML_DIR}/zap_severity_{timestamp}.html"

df.to_csv(csv_file, index=False)
df.to_markdown(md_file, index=False)
df.to_html(html_file, index=False)

print("[✓] CSV opgeslagen:", csv_file)
print("[✓] Markdown opgeslagen:", md_file)
print("[✓] HTML opgeslagen:", html_file)
print("[✓] ZAP metrics gepushed naar Prometheus")

