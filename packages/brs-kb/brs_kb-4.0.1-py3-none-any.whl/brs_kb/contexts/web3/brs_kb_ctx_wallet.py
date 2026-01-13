#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Created
Telegram: https://t.me/EasyProTech

Web3 Wallet Context - XSS via Wallet Connect/Signatures
"""

DETAILS = {
    "title": "XSS in Web3 Wallet Contexts",
    "severity": "critical",
    "cvss_score": 9.2,
    "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N",
    "cwe": ["CWE-79", "CWE-116"],
    "description": (
        "Execution of malicious JavaScript within Web3 wallet interfaces "
        "(MetaMask, WalletConnect, Phantom) or dApp signing requests. "
        "Occurs when untrusted data (token names, NFT metadata, ENS domains) "
        "is rendered without sanitization in the wallet UI or dApp confirmation screens."
    ),
    "attack_vector": (
        "Attacker mints a token or NFT with a malicious payload in metadata "
        "(name, description, image URL). When a user attempts to sign a transaction "
        "involving this asset, the wallet software renders the payload."
    ),
    "remediation": (
        "Strictly sanitize all on-chain data before rendering in UI. "
        "Treat all data from blockchain nodes as untrusted user input. "
        "Use text-only rendering for transaction confirmation screens."
    ),
    "references": [
        "https://blog.oceanprotocol.com/xss-in-web3-wallets",
        "https://github.com/MetaMask/metamask-extension/security/advisories"
    ],
    "tags": ["web3", "wallet", "nft", "blockchain", "dapp"],
    "reliability": "high"
}
