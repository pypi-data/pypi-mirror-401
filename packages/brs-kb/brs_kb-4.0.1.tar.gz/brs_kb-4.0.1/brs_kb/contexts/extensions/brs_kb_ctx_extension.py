#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Created
Telegram: https://t.me/EasyProTech

Browser Extension Context - Privileged API Access
"""

DETAILS = {
    "title": "XSS in Browser Extensions",
    "severity": "critical",
    "cvss_score": 9.3,
    "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N",
    "cwe": ["CWE-79"],
    "description": (
        "Cross-Site Scripting within the context of a browser extension "
        "(popup, options page, or background script). Unlike normal web XSS, "
        "exploiting an extension often grants access to privileged APIs "
        "(chrome.cookies, chrome.tabs, chrome.history) or Universal XSS via host permissions."
    ),
    "attack_vector": (
        "Attacker hosts a malicious page that communicates with the extension "
        "via `postMessage` or specific DOM events. If the extension's content script "
        "blindly trusts this input and injects it into the DOM, it leads to XSS "
        "in the context of the victim's current page. If the XSS occurs in the "
        "popup/options page, it escalates to full extension privileges."
    ),
    "remediation": (
        "Enforce strict Content Security Policy in `manifest.json`. "
        "Validate origin of messages in `runtime.onMessage`. "
        "Use `innerText` instead of `innerHTML` when handling external data."
    ),
    "references": [
        "https://developer.chrome.com/docs/extensions/mv3/security/",
        "https://portswigger.net/research/ublock-i-exfiltrate-exploiting-ad-blockers-with-css"
    ],
    "tags": ["extension", "chrome", "firefox", "manifest-v3", "privilege-escalation"],
    "reliability": "high"
}
