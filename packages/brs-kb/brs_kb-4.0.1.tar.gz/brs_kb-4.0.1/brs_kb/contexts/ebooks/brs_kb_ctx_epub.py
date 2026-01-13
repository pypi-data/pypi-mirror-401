#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Created
Telegram: https://t.me/EasyProTech

E-Book Context - EPUB Script Execution
"""

DETAILS = {
    "title": "XSS in EPUB Readers",
    "severity": "medium",
    "cvss_score": 6.1,
    "cvss_vector": "CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:L/A:N",
    "cwe": ["CWE-79"],
    "description": (
        "Execution of JavaScript within EPUB (Electronic Publication) files. "
        "Since EPUB is based on XHTML, many readers utilize web view components "
        "to render books, often failing to disable script execution."
    ),
    "attack_vector": (
        "Attacker creates an EPUB book containing `<script>` tags or event handlers "
        "in the XHTML chapters. When opened in a vulnerable reader (desktop or mobile), "
        "the script executes, potentially accessing local files (file://) or "
        "exfiltrating reading habits."
    ),
    "remediation": (
        "Disable JavaScript support in EPUB rendering engines by default. "
        "Sandboxing of the rendering view. "
        "Validate EPUB contents against strict schema excluding scripts."
    ),
    "references": [
        "https://idpf.org/epub/30/spec/epub30-contentdocs.html#sec-scripted-content",
        "https://sjoerdlangkemper.nl/2017/02/01/malicious-epub-files/"
    ],
    "tags": ["epub", "ebook", "xhtml", "reader", "local-file-access"],
    "reliability": "high"
}
