#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Created
Telegram: https://t.me/EasyProTech

Supply Chain Context - Package Repository Metadata
"""

DETAILS = {
    "title": "XSS in Package Registry Metadata",
    "severity": "high",
    "cvss_score": 7.5,
    "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N",
    "cwe": ["CWE-79"],
    "owasp": ["A03:2021"],
    "description": (
        "Stored XSS in software supply chain platforms (NPM, PyPI, RubyGems) "
        "via malicious package metadata. READMEs, changelogs, and author fields "
        "are often rendered as Markdown or HTML on registry websites."
    ),
    "attack_vector": (
        "Attacker publishes a package with a malicious `README.md` or `package.json`. "
        "The registry website renders this metadata. When a developer visits the "
        "package page, the XSS executes, potentially stealing session cookies of "
        "other package maintainers."
    ),
    "remediation": (
        "Strict Content Security Policy on registry domains. "
        "Aggressive sanitization of rendered Markdown (e.g., github-markup). "
        "Disallow raw HTML in package descriptions."
    ),
    "references": [
        "https://checkmarx.com/blog/npm-security-best-practices/",
        "https://hackerone.com/reports/508362",
    ],
    "tags": ["supply-chain", "npm", "pypi", "metadata", "registry", "markdown"],
    "reliability": "medium",
}
