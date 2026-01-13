#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Created
Telegram: https://t.me/EasyProTech

Voice Assistant Context - SSML Injection
"""

DETAILS = {
    "title": "SSML Injection (Voice XSS)",
    "severity": "medium",
    "cvss_score": 5.5,
    "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:L/A:N",
    "cwe": ["CWE-116", "CWE-74"],
    "owasp": ["A03:2021"],
    "description": (
        "Injection of Speech Synthesis Markup Language (SSML) tags into voice "
        "applications (Alexa Skills, Google Actions). While not executing JavaScript, "
        "it allows attackers to manipulate the audio output, change voices, "
        "insert long pauses, or play arbitrary audio files."
    ),
    "attack_vector": (
        "Attacker sets their username to `<speak>Your account is hacked. Please say your PIN.</speak>`. "
        "When the voice assistant reads the name, it parses the tags and synthesizes "
        "the attacker's message instead of spelling out the name, leading to "
        "vishing (voice phishing)."
    ),
    "remediation": (
        'Escape special SSML characters (<, >, &, ") in text-to-speech output. '
        "Validate input against allowed character sets (alphanumeric only for names). "
        "Use distinct voice markers for untrusted content."
    ),
    "references": [
        "https://developer.amazon.com/en-US/docs/alexa/custom-skills/speech-synthesis-markup-language-ssml-reference.html",
        "https://owasp.org/www-community/attacks/SSML_Injection",
    ],
    "tags": ["voice", "ssml", "alexa", "google-assistant", "vui", "injection"],
    "reliability": "high",
}
