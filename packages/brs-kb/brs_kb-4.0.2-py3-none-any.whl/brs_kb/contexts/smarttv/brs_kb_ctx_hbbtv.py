#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Created
Telegram: https://t.me/EasyProTech

Smart TV Context - HbbTV / Smart Apps
"""

DETAILS = {
    "title": "XSS in HbbTV and Smart TV Applications",
    "severity": "medium",
    "cvss_score": 6.5,
    "cvss_vector": "CVSS:3.1/AV:A/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N",
    "cwe": ["CWE-79"],
    "owasp": ["A03:2021"],
    "description": (
        "Vulnerabilities in Hybrid Broadcast Broadband TV (HbbTV) standards and "
        "Smart TV web runtimes. HbbTV allows broadcast signals to trigger web content "
        "execution. Malicious DVB-T signals or compromised ad streams can inject "
        "XSS payloads into the TV's browser context."
    ),
    "attack_vector": (
        "Attacker injects a malicious AIT (Application Information Table) entry "
        "into a broadcast stream (requires physical proximity or compromised broadcaster). "
        "The TV parses the URL in the AIT and loads the payload. Or, XSS in a "
        "Smart TV app allows accessing local tuner APIs via `oipfObjectFactory`."
    ),
    "remediation": (
        "Validate AIT signatures. "
        "Sandboxing of HbbTV applications. "
        "Restrict access to sensitive OIPF (Open IPTV Forum) APIs."
    ),
    "references": [
        "https://www.hbbtv.org/resource-library/",
        "https://fahrplan.events.ccc.de/congress/2014/Fahrplan/events/6169.html",
    ],
    "tags": ["smart-tv", "hbbtv", "dvb", "broadcast", "oipf", "embedded"],
    "reliability": "low",
}
