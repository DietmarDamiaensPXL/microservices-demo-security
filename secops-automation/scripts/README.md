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
