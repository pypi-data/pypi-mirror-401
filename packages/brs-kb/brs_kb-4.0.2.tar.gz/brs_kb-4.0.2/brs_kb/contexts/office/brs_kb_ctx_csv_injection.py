#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Created
Telegram: https://t.me/EasyProTech

Office Context - CSV Injection / DDE
"""

DETAILS = {
    "title": "CSV Injection (Formula Injection)",
    "severity": "medium",
    "cvss_score": 6.8,
    "cvss_vector": "CVSS:3.1/AV:N/AC:M/PR:N/UI:R/S:U/C:H/I:H/A:L",
    "cwe": ["CWE-1236"],
    "owasp": ["A03:2021"],
    "description": (
        "Improper validation of CSV file content allowing execution of arbitrary commands "
        "via spreadsheet software (Excel, LibreOffice, Google Sheets). "
        "When a cell begins with special characters (=, +, -, @), the software "
        "interprets it as a formula or DDE (Dynamic Data Exchange) command."
    ),
    "attack_vector": (
        "Attacker inputs a payload like `=cmd|' /C calc'!A0` into a form field "
        "(e.g., User Name). When an admin exports the user list to CSV and opens it "
        "in Excel, the payload executes, potentially running shell commands on the "
        "admin's machine or exfiltrating data via external hyperlinks."
    ),
    "remediation": (
        "Escape cells beginning with =, +, -, @ by prepending a single quote (') "
        "or a tab character. Ensure the export function strictly treats fields as text. "
        "Configure spreadsheet software to disable DDE and external links by default."
    ),
    "references": [
        "https://owasp.org/www-community/attacks/CSV_Injection",
        "https://hackerone.com/reports/72785",
    ],
    "tags": ["csv", "injection", "excel", "dde", "formula-injection", "office"],
}
