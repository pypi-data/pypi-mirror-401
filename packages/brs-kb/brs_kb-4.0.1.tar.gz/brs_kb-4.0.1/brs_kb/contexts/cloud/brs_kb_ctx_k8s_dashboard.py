#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Created
Telegram: https://t.me/EasyProTech

Cloud Dashboard Context - XSS in Admin Panels (K8s, Grafana, etc.)
"""

DETAILS = {
    "title": "Stored XSS in Cloud Admin Dashboards",
    "severity": "critical",
    "cvss_score": 9.0,
    "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H",
    "cwe": ["CWE-79"],
    "description": (
        "Stored Cross-Site Scripting in administrative dashboards such as "
        "Kubernetes Dashboard, Grafana, Kibana, or CI/CD consoles. "
        "These platforms often render logs, pod names, or metric labels which "
        "can be manipulated by lower-privileged attackers."
    ),
    "attack_vector": (
        "Attacker creates a K8s resource (Pod, Service) with a malicious name or label "
        "(e.g., `metadata.name: <script>...`). When an admin views the dashboard, "
        "the payload executes with high privileges, potentially leading to cluster takeover."
    ),
    "remediation": (
        "Update dashboard software to latest versions. "
        "Audit RBAC roles to prevent unauthorized resource creation. "
        "Treat all log data and resource metadata as untrusted input in admin UIs."
    ),
    "references": [
        "https://github.com/kubernetes/dashboard/security/advisories",
        "https://grafana.com/tags/security/"
    ],
    "tags": ["cloud", "k8s", "kubernetes", "dashboard", "admin-panel"]
}
