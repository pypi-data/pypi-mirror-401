#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Created
Telegram: https://t.me/EasyProTech

Desktop Context - WebView2 (Windows)
"""

DETAILS = {
    "title": "XSS in Desktop WebView2 Applications",
    "severity": "critical",
    "cvss_score": 9.3,
    "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H",
    "cwe": ["CWE-79", "CWE-749"],
    "description": (
        "Cross-Site Scripting in Windows desktop applications using Microsoft Edge WebView2. "
        "Unlike standard browsers, WebView2 apps often expose native host objects "
        "via `chrome.webview.hostObjects`. An XSS vulnerability in the web context "
        "can bridge the gap to the native system, allowing arbitrary code execution "
        "on the host OS."
    ),
    "attack_vector": (
        "Attacker finds an XSS vector in the web content displayed by the app. "
        "The injected script accesses `window.chrome.webview.hostObjects.sync.nativeApi` "
        "(or similar exposed interfaces) to invoke native functions, read local files, "
        "or execute shell commands with the privileges of the desktop user."
    ),
    "remediation": (
        "Disable `enableHostObjects` if not strictly necessary. "
        "Verify origin in native message handlers (`WebMessageReceived`). "
        "Use Context Isolation. Validate all data passed from Web to Native world. "
        "Apply CSP to the loaded web content."
    ),
    "references": [
        "https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/security",
        "https://mksben.l0.cm/2020/10/webview2-vulnerability.html"
    ],
    "tags": ["desktop", "webview2", "windows", "edge", "bridge"]
}
