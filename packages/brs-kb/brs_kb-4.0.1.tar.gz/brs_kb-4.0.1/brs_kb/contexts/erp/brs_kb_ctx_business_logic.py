#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Created
Telegram: https://t.me/EasyProTech

ERP/CRM Context - SAP / Salesforce / Oracle
"""

DETAILS = {
    "title": "XSS in Enterprise Resource Planning (ERP)",
    "severity": "critical",
    "cvss_score": 9.0,
    "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N",
    "cwe": ["CWE-79"],
    "description": (
        "Cross-Site Scripting in large-scale ERP systems like SAP NetWeaver, "
        "Salesforce, and Oracle E-Business Suite. These systems often handle "
        "trillions of dollars in transactions. XSS here leads to financial fraud, "
        "payroll manipulation, or supply chain sabotage."
    ),
    "attack_vector": (
        "Attacker (often an insider or partner) injects XSS into a Purchase Order "
        "comment or Vendor Name. When a CFO or Payroll Admin approves the workflow, "
        "the script executes, automatically approving fraudulent transactions or "
        "creating new admin users."
    ),
    "remediation": (
        "Apply strict output encoding in ABAP/Apex/PL-SQL layers. "
        "Use vendor-supplied security patches immediately. "
        "Implement four-eyes principle for critical changes."
    ),
    "references": [
        "https://www.onapsis.com/research/threat-intelligence",
        "https://help.sap.com/viewer/security"
    ],
    "tags": ["erp", "sap", "salesforce", "oracle", "crm", "finance", "insider-threat"],
    "reliability": "medium"
}
