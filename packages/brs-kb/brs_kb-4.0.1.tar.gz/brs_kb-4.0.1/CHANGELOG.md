# Changelog

All notable changes to BRS-KB will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.0.1] - 2026-01-10

### Quality & Detection Improvements

Major quality release with 100% metadata completeness and enhanced detection capabilities.

### Added

- **+716 Payloads** — Web3, SCADA/ICS, ERP, Deep Learning, Supply Chain, mXSS, LLM Injection
- **+18 Contexts** — Web3 Wallet, IPFS Gateway, SSR Hydration, K8s Dashboard, Micro-Frontend, CSV Injection, IoT Embedded, EPUB
- **+65 WAF Bypasses** — New evasion techniques
- **+34 Detection Patterns** — JavaScript string breakout, DOM sinks, eval-like functions

### Fixed

- **CRITICAL**: JavaScript string breakout payloads now correctly classified as CRITICAL severity
- DOM XSS via eval/setTimeout/setInterval now properly detected
- Payloads like `1');alert('XSS` now return CRITICAL instead of LOW

### Improved

- **100% Metadata Completeness** — All payloads now have:
  - Description (>20 chars): 100%
  - Tags (>=2): 100%
  - Contexts: 100%
  - CVSS Score: 100%
  - Reliability: 100%
  - Browser Support: 100%
- Auto-generation of missing metadata in PayloadEntry model
- Enhanced pattern matching for DOM-based XSS detection

### Statistics

| Metric | Before | After | Growth |
|--------|--------|-------|--------|
| Payloads | 4,215 | 4,931 | +17.0% |
| Contexts | 151 | 169 | +11.9% |
| WAF Bypasses | 1,934 | 1,999 | +3.4% |
| Detection Patterns | 28 | 62 | +121% |

---

## [4.0.0] - 2025-12-28

### Initial Public Release

First stable release of BRS-KB.

** Public API:** [brs-kb.easypro.tech](https://brs-kb.easypro.tech)

### Features

- **4,200+ XSS Payloads** — unique, deduplicated, with full metadata
- **151 XSS Contexts** — full coverage across all attack vectors
- **WAF Bypass Database** — 1,300+ techniques for Cloudflare, Akamai, AWS WAF, Imperva, ModSecurity
- **REST API** — full-featured HTTP API with 13 endpoints
- **CLI Tool** — 12 commands for command-line usage
- **Zero Dependencies** — pure Python 3.8+

### Payload Categories

| Category | Count | Description |
|----------|-------|-------------|
| Core | 200+ | Essential XSS vectors |
| WAF Bypass | 1,300+ | All major WAFs |
| Modern Browser | 200+ | ES6+, WebAssembly, Service Workers |
| Context-Specific | 800+ | DOM, Template, GraphQL, WebSocket, SSE |
| Exotic | 200+ | mXSS, DOM Clobbering, Prototype Pollution |
| Frameworks | 300+ | React, Vue, Angular, Svelte, HTMX, Alpine |
| Event Handlers | 105 | All HTML event handlers |
| Obfuscation | 100+ | Encoding, charcode, JSFuck |

### Context Categories

| Category | Contexts | Description |
|----------|----------|-------------|
| HTML | 15 | HTML injection contexts |
| JavaScript | 15 | JS execution contexts |
| DOM | 15 | DOM-based XSS |
| Frameworks | 25 | Framework-specific |
| API | 20 | API/Realtime contexts |
| Browser | 20 | Browser API contexts |
| Security | 15 | Security bypass contexts |
| Injection | 12 | Various injection types |
| Other | 14 | Specialized contexts |

### API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/info` | System information |
| `GET /api/health` | Health check |
| `GET /api/contexts` | List all contexts |
| `GET /api/contexts/{id}` | Context details |
| `GET /api/payloads` | List payloads |
| `GET /api/payloads/search` | Search payloads |
| `POST /api/analyze` | Analyze payload |
| `GET /api/defenses` | Get defenses |
| `GET /api/stats` | Statistics |

### Infrastructure

- Modern build system with Hatch (PEP 621)
- GitHub Actions CI/CD pipeline
- Multi-Python version support (3.8-3.13)
- Type hints with `py.typed` marker
- 81% test coverage (334 tests)
- Docker and Kubernetes configurations
- Prometheus metrics integration

### Integrations

- **BRS-XSS Scanner** — seamless integration as payload source
- **Burp Suite** — plugin for real-time analysis
- **OWASP ZAP** — automated scanning plugin
- **Nuclei** — template-based testing
- **SIEM** — Splunk, Elasticsearch, Graylog connectors

---

**Project**: BRS-KB (BRS XSS Knowledge Base)  
**Company**: EasyProTech LLC (www.easypro.tech)  
**Developer**: Brabus  
**API**: https://brs-kb.easypro.tech  
**Telegram**: https://t.me/easyprotech  
**License**: MIT  
