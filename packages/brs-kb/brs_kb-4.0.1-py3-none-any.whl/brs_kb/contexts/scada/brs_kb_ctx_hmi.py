#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Created
Telegram: https://t.me/EasyProTech

SCADA/ICS Context - HMI Web Interfaces
"""

DETAILS = {
    "title": "XSS in SCADA/HMI Web Interfaces",
    "severity": "critical",
    "cvss_score": 9.6,
    "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H",
    "cwe": ["CWE-79", "CWE-74"],
    "description": (
        "Cross-Site Scripting in Human-Machine Interfaces (HMI) and Industrial "
        "Control Systems (ICS). Modern SCADA systems often use web-based HMIs "
        "(HTML5/WebSocket) to visualize process data. XSS here can lead to "
        "physical impact by allowing attackers to send control commands to PLCs."
    ),
    "attack_vector": (
        "Attacker injects a malicious payload into a tag value (e.g., sensor name "
        "or alarm message) via a low-level protocol (Modbus/OPC UA). When an operator "
        "views the alarm screen on the web HMI, the script executes, potentially "
        "sending 'STOP' commands to centrifuges or opening valves."
    ),
    "remediation": (
        "Strictly sanitize all process data before rendering in HMI. "
        "Isolate HMI networks from corporate/public networks. "
        "Implement strict Content Security Policy on HMI web servers."
    ),
    "references": [
        "https://www.cisa.gov/uscert/ics/alerts",
        "https://claroty.com/team82/research/scada-xss"
    ],
    "tags": ["scada", "ics", "hmi", "industrial", "plc", "physical-impact"],
    "reliability": "high"
}
