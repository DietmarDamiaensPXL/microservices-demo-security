Trivy: Scan alle Docker images van de microservices demo.
Trivy: Is een open-source security-scanner. Het is ontworpen om kwetsbaarheden, misconfiguraties en secrets te detecteren in alles wat relevant is binnen de cloud-native stack (tools to build & run software scallable). Trivy heeft een kubernetes cluster scanner die direct je cluster analyseert, het kijkt naar:
 - misconfiguratie in workloads (deployments, pods, ...)
 - Non-compliant security settings (pod security, network policies, capabilities)
 - ...

Grype: image scanning
nmap: Scan de interne Docker network van de microservices.
OWASP ZAP: Automatisch de frontend scannen op XSS, CSRF, injection.


Steps:
Install software:

# systeemtools
sudo apt update
sudo apt install -y jq nmap python3 python3-pip

# trivy
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sudo sh -s -- -b /usr/local/bin

# grype
curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sudo sh -s -- -b /usr/local/bin

# ZAP (optioneel)
sudo snap install zaproxy --classic

# Python packages
pip3 install reportlab tabulate

# Panda (installed with pip)
python3 -m pip install --user pandas

# Pandoc
sudo apt install pandoc

# Maak SCRIPT files uitvoerbaar.
chmod +x secops-automation/scripts/scan_trivy_k8s.sh





# Scans
### Trivy
Na het uitvoeren van ons Trivy scanner script worden er nu volledige Trivy JSON-scanresultaten van ALLE images die in onze kubernetes cluster draaien toegevoegd in de scans map.

Met het script `trivy_report.py` kunnen we nu deze JSON files omzetten naar een .cvs file of .md file. Dit doen we door de volgende lijn uit te voeren:

`python3 secops-automation/scripts/trivy_report.py`

# reports
Na het uitvoeren van het `trivy_report.py` bestand beschikken we over .cvs en .md file in de report map.  

Bijkomende optie: We kunnen ook een .html file genereren door een omzetting aan de hand van de tool pandoc. We maken een verwijzing naar de folder met de .cvs en .md file met het volgende commando `pandoc secops-automation/reports/trivy_severity_2025-12-01_22-40-40.md -o secops-automation/reports/trivy_severity.html`




