#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Created
Telegram: https://t.me/EasyProTech

Micro-Frontend Context - Webpack Module Federation & Shared State
"""

DETAILS = {
    "title": "XSS in Micro-Frontend Architectures",
    "severity": "high",
    "cvss_score": 8.1,
    "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N",
    "cwe": ["CWE-79", "CWE-1321"],
    "description": (
        "Vulnerabilities arising from shared state and remote module loading in "
        "Micro-Frontend architectures (Webpack Module Federation, Single-SPA). "
        "Lack of isolation between micro-apps allows a compromised sub-module "
        "to pollute the global scope, shared window objects, or intercept "
        "inter-module communications."
    ),
    "attack_vector": (
        "Attacker compromises a less secure micro-app (e.g., a legacy footer widget) "
        "or injects code via a shared dependency. The injected script leverages "
        "shared global variables (window.System, __webpack_share_scopes__) to "
        "overwrite exports used by the host application (Shell), achieving "
        "execution in the context of the main authenticated session."
    ),
    "remediation": (
        "Enforce strict strict Shadow DOM encapsulation for all micro-apps. "
        "Use iframe-based isolation (Sandboxed Micro-Frontends) where possible. "
        "Validate integrity of remote modules via Subresource Integrity (SRI). "
        "Freeze shared prototypes and global state objects."
    ),
    "references": [
        "https://webpack.js.org/concepts/module-federation/#security-considerations",
        "https://martinfowler.com/articles/micro-frontends.html#Cross-applicationCommunication"
    ],
    "tags": ["micro-frontend", "webpack", "module-federation", "single-spa", "isolation-break"]
}
