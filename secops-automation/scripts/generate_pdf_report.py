#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
import os

REPORT_DIR = "secops-automation/reports"
PDF_DIR = f"{REPORT_DIR}/pdf"
HTML_DIR = f"{REPORT_DIR}/html"
os.makedirs(PDF_DIR, exist_ok=True)

latest_csv = sorted(
    [f for f in os.listdir(REPORT_DIR) if f.endswith(".csv")]
)[-1]

df = pd.read_csv(f"{REPORT_DIR}/{latest_csv}")

pdf_path = f"{PDF_DIR}/Security_Report.pdf"

doc = SimpleDocTemplate(pdf_path, pagesize=A4)
styles = getSampleStyleSheet()
flow = []

title = Paragraph("<b>Security Vulnerability Report</b>", styles["Title"])
flow.append(title)
flow.append(Spacer(1, 20))

flow.append(Paragraph("Overzicht van kwetsbaarheden per container image:", styles["Heading2"]))
flow.append(Spacer(1, 10))

html_preview = f"{HTML_DIR}/{latest_csv.replace('.csv','.html')}"
flow.append(Paragraph(f"HTML versie: {html_preview}", styles["Normal"]))
flow.append(Spacer(1, 20))

# Maak grafiek
plt.figure(figsize=(10,6))
df.set_index("Image")[["CRITICAL","HIGH","MEDIUM","LOW"]].sum().plot(kind="bar")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("/tmp/severity_chart.png")
plt.close()

flow.append(Image("/tmp/severity_chart.png", width=400, height=250))
flow.append(Spacer(1, 20))

doc.build(flow)
print(f"[✓] PDF Report gegenereerd: {pdf_path}")

