BELANGRIJK OM DATA TE KUNNEN SEEDEN NAAR PROMETHEUS:

# Scanner uitvoeren
cedric@Cedric-HP-Laptop:~/Documents/4dejaar/securityExp/GIP/microservices-demo-security/secops-automation$ ./scripts/scan_trivy_k8s.sh

# Data omzetten naar .csv, .md & .html -> push naar Prometheus
cedric@Cedric-HP-Laptop:~/Documents/4dejaar/securityExp/GIP/microservices-demo-security/secops-automation$ ./scripts/trivy_report.py
