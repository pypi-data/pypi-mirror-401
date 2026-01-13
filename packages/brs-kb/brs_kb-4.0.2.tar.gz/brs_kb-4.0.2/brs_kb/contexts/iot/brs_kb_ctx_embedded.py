#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Created
Telegram: https://t.me/EasyProTech

IoT Context - Embedded Web Servers
"""

DETAILS = {
    "title": "XSS in Embedded IoT Web Servers",
    "severity": "high",
    "cvss_score": 8.0,
    "cvss_vector": "CVSS:3.1/AV:A/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H",
    "cwe": ["CWE-79", "CWE-20"],
    "owasp": ["A03:2021"],
    "description": (
        "Cross-Site Scripting vulnerabilities in lightweight embedded web servers "
        "(uhttpd, Boa, GoAhead) common in routers, IP cameras, and smart home devices. "
        "These devices often lack robust WAFs or input sanitization libraries due to "
        "resource constraints, leading to Reflected and Stored XSS in admin interfaces."
    ),
    "attack_vector": (
        "Attacker sends a malicious request to the local network IP of an IoT device "
        "(via CSRF or DNS Rebinding). The payload is reflected in the device's "
        "admin login page or status dashboard. If an authenticated user views it, "
        "the attacker gains control of the device settings (DNS, port forwarding)."
    ),
    "remediation": (
        "Implement strict input validation on firmware level. "
        "Use Content-Security-Policy even on embedded interfaces. "
        "Ensure authentication cookies have SameSite=Strict and HttpOnly flags. "
        "Avoid echoing raw input in error messages."
    ),
    "references": [
        "https://owasp.org/www-project-internet-of-things/",
        "https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=router+xss",
    ],
    "tags": ["iot", "embedded", "router", "firmware", "uhttpd"],
}
