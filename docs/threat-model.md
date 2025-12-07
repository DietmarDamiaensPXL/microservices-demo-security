# Threat Model - Online Boutique Microservices Application

**Date:** December 7, 2025
**Application:** Online Boutique
**Status:** Initial Assessment

---

## Inhoudstabel

1. [Executive Summary](#executive-summary)
2. [System Overview](#system-overview)
3. [Assets & Data Classification](#assets--data-classification)
4. [Attack Surface Analysis](#attack-surface-analysis)

---

## Executive Summary

Dit threat model analyseert de security van de Online Boutique app. Het is een e-commerce platform dat bestaat uit 11 microservices wat lokaal op kubernetes draait. In deze analyse kijken we naar kritische vulnerabilities en mogelijke attack vectors.

**Key Findings:**
- geen authentication/authorization mechanisme
- Meerderen internet-facing attack vectors via frontend service
- Cart data wordt unencrypted opgeslagen in Redis
- Internal service-to-service communicatie over unencrypted gRPC

---

## System Overview

### Architecture

De Online Boutique bestaat uit 11 microservices die via gRPC communiceren, frontend is bereikbaar via http voor de eindgebruiker.

### Technology Stack

| Service | Language | Framework | Port | Protocol |
|---------|----------|-----------|------|----------|
| Frontend | Go | net/http | 8080 | HTTP |
| CartService | C# | ASP.NET | 7070 | gRPC |
| CheckoutService | Go | gRPC | 5050 | gRPC |
| PaymentService | Node.js | Express | 50051 | gRPC |
| ShippingService | Go | gRPC | 50051 | gRPC |
| EmailService | Python | gRPC | 5000 | gRPC |
| ProductCatalogService | Go | gRPC | 3550 | gRPC |
| CurrencyService | Node.js | gRPC | 7000 | gRPC |
| RecommendationService | Python | gRPC | 8080 | gRPC |
| AdService | Java | gRPC | 9555 | gRPC |
| LoadGenerator | Python | Locust | - | HTTP |

### Supporting Infrastructure

- **Redis (Alpine):** session en cart storage
- **OpenTelemetry Collector:** observability
- **Prometheus, Grafana, Loki, Tempo:** monitoring stack
- **MailHog:** email testing
- **Kubernetes:** orchestration platform

---

## Assets & Data Classification

### Critical Assets

| Asset | Sensitivity | Impact if Compromised | Current Protection |
|-------|-------------|----------------------|-------------------|
| **Customer Cart Data** | HIGH | User privacy violation, cart manipulation | Redis zonder encryption |
| **Payment Information** | CRITICAL | Financial fraud (mock data) | Mock service, no real data |
| **Session IDs** | MEDIUM | Session hijacking, account takeover | UUID in cookie, no HTTPS enforcement |
| **Product Catalog** | LOW | Data integrity, availability | JSON file, no encryption |
| **Order History** | MEDIUM | Privacy violation | No persistent storage |
| **Service Configuration** | HIGH | System compromise | Environment variables |

---

## Attack Surface Analysis

### External Attack Surface (Internet-Facing)

#### 1. Frontend HTTP Service (Port 8080)
**Exposure:** Public LoadBalancer
**Endpoints:**
- `/` - Homepage
- `/product/{productid}` - Product pages
- `/cart` - Shopping cart
- `/checkout` - Checkout flow
- `/_healthz` - Health check endpoint

**Attack Vectors:**
- XSS (Cross-Site Scripting)
- Session fixation/hijacking
- DDoS

### Internal Attack Surface (Service-to-Service)

#### 1. gRPC Service Endpoints
**Exposure:** Internal cluster network
**Risk Level:** HIGH

**Services with High Risk:**
- **CheckoutService:** Orchestrates payment, shipping, email
- **PaymentService:** Processes payment data (mock)

**Attack Vectors:**
- gRPC reflection abuse (maakt services toegankelijk en laat interactie toe)
- Resource exhaustion (geen rate limiting op gRPC services)
- Man-in-the-middle (geen mTLS (Mutual Transport Layer Security))
- Lateral movement na initial compromise

#### 2. Redis Data Store
**Exposure:** Internal cluster network
**Port:** 6379
**Authentication:** Not configured

**Attack Vectors:**
- Unauthorized data access
- Data manipulation
- Redis command injection
- Data exfiltration
