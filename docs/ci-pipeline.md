# CI Pipeline Documentatie

## Overzicht

Deze repository maakt gebruik van een **GitHub Actions CI/CD pipeline** die automatisch wordt uitgevoerd bij elke push naar de `main` branch of handmatig kan worden gestart via `workflow_dispatch`.

De pipeline bestaat uit drie hoofdfasen die sequentieel worden uitgevoerd:
1. **Code Tests** - Unit tests voor alle microservices
2. **Security Tests** - Beveiligingsscans met Trivy
3. **Smoke Tests** - End-to-end integratie tests in een Kubernetes cluster

---

## Pipeline Architectuur

```
┌──────────────────┐
│   Code Tests     │
│  (Unit Testing)  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Security Tests   │
│ (Trivy Scanning) │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Smoke Tests     │
│ (E2E Testing)    │
└──────────────────┘
```

---

## Fase 1: Code Tests

**Job:** `code-tests`
**Runtime:** Ubuntu Latest
**Timeout:** 10 minuten per test

### Doelstellingen
- Valideren dat alle unit tests slagen
- Controleren van code kwaliteit

### Services die getest worden

#### Go Services
- **shippingservice** - Verzendservice
- **productcatalogservice** - Product catalogus service

**Stappen:**
1. Checkout van de repository
2. Setup Go 1.25
3. Download en tidy Go dependencies
4. Uitvoeren van `go test` voor elke service

#### .NET Services
- **cartservice** - Winkelwagen service (C#)

**Stappen:**
1. Setup .NET 9.0
2. Uitvoeren van `dotnet test src/cartservice/`

### Faalcriteria
De pipeline stopt als één van de unit tests faalt.

---

## Fase 2: Security Tests

**Job:** `security-tests`
**Runtime:** Ubuntu Latest
**Dependencies:** Vereist succesvolle `code-tests`
**Permissions:** `contents: write` (voor het committen van rapporten)

### Doelstellingen
- Identificeren van kwetsbaarheden in dependencies en code
- Genereren van gedetailleerde security rapporten
- Automatisch archiveren van security scan resultaten

### Security Scanning Tools

#### Trivy Scanner
Aquasecurity Trivy scant het volledige bestandssysteem op:
- **CRITICAL** - Kritieke kwetsbaarheden
- **HIGH** - Hoge risico kwetsbaarheden
- **MEDIUM** - Gemiddelde risico kwetsbaarheden
- **LOW** - Lage risico kwetsbaarheden
- **UNKNOWN** - Onbekende kwetsbaarheden

**Configuratie:**
- Scan type: Filesystem (`fs`)
- Ignore unfixed: `true` (negeert kwetsbaarheden zonder fix)
- Exit code: `0` (pipeline faalt niet bij kwetsbaarheden)

### Report Generatie

#### 1. JSON Report
```bash
trivy-report.json
```
Bevat gestructureerde data voor verdere verwerking

#### 2. HTML Report
```bash
trivy-report.html
```
Visueel rapport voor menselijke review, gegenereerd met de Trivy HTML template

### Python Dependencies
De pipeline installeert Python libraries voor rapportage:
- `pandas` - Data manipulatie
- `reportlab` - PDF generatie
- `matplotlib` - Visualisaties

### Artifact Storage

**Artifacts worden opgeslagen op twee locaties:**

1. **GitHub Actions Artifacts** (tijdelijk)
   - trivy-report.json
   - trivy-report.html
   - Beschikbaar als download in de workflow run

2. **Repository (permanent)**
   ```
   secops-automation/
   ├── scans/trivy/
   │   └── trivy-report.json
   └── reports/html/
       └── trivy-report.html
   ```

### Automatische Commits
De pipeline commit automatisch alle security rapporten terug naar de repository met:
- **Author:** github-actions[bot]
- **Message:** "Update all security reports [skip ci]"
- **Skip CI:** `[skip ci]` voorkomt oneindige loops

---

## Fase 3: Smoke Tests

**Job:** `smoke-tests`
**Runtime:** Ubuntu Latest
**Dependencies:** Vereist succesvolle `security-tests`
**Timeout:** Variabel per stap (tot 300 seconden voor pods)

### Doelstellingen
- End-to-end validatie van de volledige applicatie
- Controleren dat alle services correct samenwerken
- Detecteren van integratie problemen

### Test Omgeving Setup

#### 1. Kind Cluster
**Kubernetes in Docker (Kind)** wordt gebruikt voor lokale Kubernetes testing:
```bash
kind v0.20.0
Cluster naam: test-cluster
Wait time: 2 minuten
```

#### 2. Skaffold Deployment
**Skaffold** deployt alle microservices naar het Kind cluster:
```bash
skaffold run --default-repo=local
```

### Deployed Services
De pipeline wacht tot alle deployments beschikbaar zijn:

| Service                  | Type       | Timeout |
|-------------------------|------------|---------|
| redis-cart              | Database   | 300s    |
| adservice               | Microservice | 300s  |
| cartservice             | Microservice | 300s  |
| checkoutservice         | Microservice | 300s  |
| currencyservice         | Microservice | 300s  |
| emailservice            | Microservice | 300s  |
| frontend                | Microservice | 300s  |
| loadgenerator           | Test Tool  | 300s    |
| paymentservice          | Microservice | 300s  |
| productcatalogservice   | Microservice | 300s  |
| recommendationservice   | Microservice | 300s  |
| shippingservice         | Microservice | 300s  |

### Load Testing

#### Loadgenerator
De `loadgenerator` service simuleert gebruikersverkeer:
- Stuurt HTTP requests naar alle endpoints
- Logt statistieken in artifact

#### Success Criteria
```bash
Minimum requests: 50
Maximum errors: 0
Max wait time: 300 seconden (60 pogingen × 5 sec)
```

### Test Validatie

**Request Count Check:**
```bash
REQUEST_COUNT=$(kubectl logs -l app=loadgenerator | grep Aggregated | awk '{print $2}')
```

**Error Count Check:**
```bash
ERROR_COUNT=$(kubectl logs -l app=loadgenerator | grep Aggregated | awk '{print $3}')
```

### Smoke Test Report
Een tekstrapport wordt gegenereerd met:
- Datum en tijd
- Totaal aantal requests
- Totaal aantal errors
- Test resultaat (PASSED/FAILED)

**Locatie:** `smoke-test-report.txt` (geüpload als artifact)

### Cleanup
De Kind cluster wordt altijd opgeruimd, zelfs bij failures:
```bash
kind delete cluster --name test-cluster
```

---

## Pipeline Triggers

### Automatische Triggers
```yaml
on:
  push:
    branches:
      - main
```
Pipeline wordt gestart bij elke push naar de main branch.

### Handmatige Triggers
```yaml
on:
  workflow_dispatch:
```
Pipeline kan handmatig gestart worden via de GitHub Actions UI.
