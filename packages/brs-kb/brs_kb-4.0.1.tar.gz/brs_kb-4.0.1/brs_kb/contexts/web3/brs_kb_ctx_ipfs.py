#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Created
Telegram: https://t.me/EasyProTech

IPFS Context - XSS via IPFS Gateways
"""

DETAILS = {
    "title": "XSS via IPFS Gateway Context",
    "severity": "high",
    "cvss_score": 8.2,
    "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N",
    "cwe": ["CWE-79"],
    "description": (
        "Cross-Site Scripting via IPFS (InterPlanetary File System) gateways. "
        "Attackers upload malicious HTML/SVG content to IPFS and trick users "
        "into viewing it via a public gateway. If the gateway serves content "
        "on the same origin (subdomain) as the main app, it leads to XSS."
    ),
    "attack_vector": (
        "Attacker uploads a file with XSS payload to IPFS. "
        "Victim visits `https://gateway.example.com/ipfs/<hash>`. "
        "The gateway renders the file as `text/html` instead of forcing download, "
        "executing scripts in the context of the gateway domain."
    ),
    "remediation": (
        "Serve IPFS content from a distinct, sandboxed domain (e.g., `ipfsusercontent.com`). "
        "Enforce `Content-Security-Policy: sandbox` on gateway responses. "
        "Force `Content-Disposition: attachment` for potentially dangerous MIME types."
    ),
    "references": [
        "https://docs.ipfs.tech/concepts/ipfs-gateway/#cross-site-scripting-xss",
        "https://github.com/ipfs/go-ipfs/issues/1367"
    ],
    "tags": ["web3", "ipfs", "gateway", "distributed-web"]
}
