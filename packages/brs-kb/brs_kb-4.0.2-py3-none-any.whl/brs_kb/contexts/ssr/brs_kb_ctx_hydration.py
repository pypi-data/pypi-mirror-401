#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Created
Telegram: https://t.me/EasyProTech

SSR Hydration Context - XSS via Hydration Mismatch
"""

DETAILS = {
    "title": "XSS via SSR Hydration Mismatch",
    "severity": "high",
    "cvss_score": 7.5,
    "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N",
    "cwe": ["CWE-79", "CWE-116"],
    "owasp": ["A03:2021"],
    "description": (
        "Vulnerability arising from discrepancies between Server-Side Rendered (SSR) HTML "
        "and Client-Side Rendered (CSR) virtual DOM. In frameworks like React/Vue/Next.js, "
        "hydration mismatches can cause the client framework to fallback or patch the DOM "
        "incorrectly, potentially exposing sanitized markup as raw HTML."
    ),
    "attack_vector": (
        "Attacker injects a payload that renders differently on server and client "
        "(e.g., using `typeof window`). The framework detects a mismatch during hydration "
        "and may aggressively patch the DOM, inadvertently executing the payload that was "
        "previously safe string-literal."
    ),
    "remediation": (
        "Ensure deterministic rendering between server and client. "
        "Avoid using `dangerouslySetInnerHTML` on hydration-sensitive components. "
        "Use suppression attributes like `suppressHydrationWarning` with extreme caution."
    ),
    "references": [
        "https://react.dev/reference/react-dom/client/hydrateRoot#handling-different-client-and-server-content",
        "https://github.com/facebook/react/issues/24515",
    ],
    "tags": ["ssr", "hydration", "react", "vue", "nextjs"],
}
