import os
import sys
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import matplotlib.pyplot as plt
import glob

# Get the most recent CSV from the reports directory
REPORT_DIR = os.getenv("REPORT_DIR", "./secops-automation/reports")
PDF_OUTPUT = os.getenv("PDF_OUTPUT", "./security-report.pdf")

# Find the latest CSV file
csv_files = sorted(glob.glob(f"{REPORT_DIR}/*.csv"))
if not csv_files:
    print("No CSV files found in reports directory")
    sys.exit(1)

latest_csv = csv_files[-1]
print(f"Processing: {latest_csv}")

df = pd.read_csv(latest_csv)

# Create PDF
doc = SimpleDocTemplate(PDF_OUTPUT, pagesize=A4)
styles = getSampleStyleSheet()
flow = []

# Title
title = Paragraph("<b>Security Vulnerability Report</b>", styles["Title"])
flow.append(title)
flow.append(Spacer(1, 20))

# Overview
flow.append(Paragraph("Overview of vulnerabilities per container image:", styles["Heading2"]))
flow.append(Spacer(1, 10))

# Summary statistics
total_critical = df["CRITICAL"].sum()
total_high = df["HIGH"].sum()
total_medium = df["MEDIUM"].sum()
total_low = df["LOW"].sum()

summary_data = [
    ["Severity", "Count"],
    ["CRITICAL", str(total_critical)],
    ["HIGH", str(total_high)],
    ["MEDIUM", str(total_medium)],
    ["LOW", str(total_low)]
]

summary_table = Table(summary_data)
summary_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 14),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))

flow.append(summary_table)
flow.append(Spacer(1, 20))

# Create chart
plt.figure(figsize=(10, 6))
severity_totals = [total_critical, total_high, total_medium, total_low]
severity_labels = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
colors_list = ['#d32f2f', '#f57c00', '#fbc02d', '#388e3c']

plt.bar(severity_labels, severity_totals, color=colors_list)
plt.ylabel('Count')
plt.title('Total Vulnerabilities by Severity')
plt.tight_layout()

chart_path = "/tmp/severity_chart.png"
plt.savefig(chart_path)
plt.close()

flow.append(Image(chart_path, width=400, height=250))
flow.append(Spacer(1, 20))

# Detailed table
flow.append(Paragraph("Detailed Results:", styles["Heading2"]))
flow.append(Spacer(1, 10))

# Convert dataframe to table data
table_data = [df.columns.tolist()] + df.values.tolist()
detail_table = Table(table_data)
detail_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))

flow.append(detail_table)

# Build PDF
doc.build(flow)
print(f"[✓] PDF Report generated: {PDF_OUTPUT}")