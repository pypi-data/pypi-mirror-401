#!/usr/bin/env python3

"""
Project: BRS-KB (BRS XSS Knowledge Base)
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: 2025-12-26 UTC
Status: Refactored
Telegram: https://t.me/EasyProTech

Payload database models.
Enterprise-grade data structures for XSS payload management.
Full Enum-based type system for maximum type safety.
"""

from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union


class Severity(str, Enum):
    """
    CVSS-aligned severity levels.

    Based on CVSS v3.1 qualitative severity rating scale.
    """

    CRITICAL = "critical"  # CVSS 9.0-10.0
    HIGH = "high"  # CVSS 7.0-8.9
    MEDIUM = "medium"  # CVSS 4.0-6.9
    LOW = "low"  # CVSS 0.1-3.9
    INFO = "info"  # CVSS 0.0 (informational)

    @classmethod
    def from_cvss(cls, score: float) -> "Severity":
        """
        Determine severity from CVSS score.

        Args:
            score: CVSS base score (0.0-10.0).

        Returns:
            Corresponding Severity level.
        """
        if score >= 9.0:
            return cls.CRITICAL
        elif score >= 7.0:
            return cls.HIGH
        elif score >= 4.0:
            return cls.MEDIUM
        elif score > 0.0:
            return cls.LOW
        return cls.INFO

    def __ge__(self, other: "Severity") -> bool:
        order = [Severity.INFO, Severity.LOW, Severity.MEDIUM, Severity.HIGH, Severity.CRITICAL]
        return order.index(self) >= order.index(other)

    def __gt__(self, other: "Severity") -> bool:
        order = [Severity.INFO, Severity.LOW, Severity.MEDIUM, Severity.HIGH, Severity.CRITICAL]
        return order.index(self) > order.index(other)

    def __le__(self, other: "Severity") -> bool:
        return not self.__gt__(other)

    def __lt__(self, other: "Severity") -> bool:
        return not self.__ge__(other)


class Reliability(str, Enum):
    """Payload execution reliability rating."""

    CERTAIN = "certain"  # 100% reliable, always executes
    HIGH = "high"  # >90% reliable
    MEDIUM = "medium"  # 50-90% reliable
    LOW = "low"  # <50% reliable
    EXPERIMENTAL = "experimental"  # Untested or theoretical


class Encoding(str, Enum):
    """Payload encoding type."""

    NONE = "none"
    URL = "url"
    HTML = "html"
    HTML_ENTITIES = "html-entities"
    HTML_DECIMAL = "html-decimal"
    HTML_HEX = "html-hex"
    HTML_PADDED = "html-padded"
    HTML_PADDED_HEX = "html-padded-hex"
    UNICODE = "unicode"
    UNICODE_PARTIAL = "unicode-partial"
    BASE64 = "base64"
    HEX = "hex"
    DOUBLE_URL = "double-url"
    MIXED = "mixed"
    OTHER = "other"  # For edge cases like application/xhtml+xml


class AttackSurface(str, Enum):
    """Attack surface categories."""

    CLIENT = "client"
    SERVER = "server"
    BRIDGE = "bridge"
    FEDERATION = "federation"
    PUSH = "push"
    WIDGET = "widget"
    INTEGRATION = "integration"
    WEB = "web"
    API = "api"
    # Extended Surfaces
    CHAT_UI = "chat-ui"
    DESKTOP_BRIDGE = "desktop-bridge"
    DESKTOP_APP = "desktop-app"
    IOT = "iot"
    GATEWAY = "gateway"
    WALLET = "wallet"
    DAPP = "dapp"
    SMART_CONTRACT = "smart-contract"
    FILE_EXPORT = "file-export"
    FILE_UPLOAD = "file-upload"
    CLOUD_OFFICE = "cloud-office"
    GLOBAL_SCOPE = "global-scope"
    SHARED_MEMORY = "shared-memory"
    GLOBAL_REGISTRY = "global-registry"
    DEEP_LINK = "deep-link"
    INDIRECT = "indirect"
    DEVELOPER_TOOL = "developer-tool"
    GAMING_CLIENT = "gaming-client"


def _normalize_severity(value: Union[str, Severity]) -> Severity:
    """Convert string or Severity to Severity enum."""
    if isinstance(value, Severity):
        return value
    try:
        return Severity(value.lower())
    except ValueError:
        raise ValueError(
            f"Invalid severity '{value}'. Must be one of: {[s.value for s in Severity]}"
        )


def _normalize_reliability(value: Union[str, Reliability]) -> Reliability:
    """Convert string or Reliability to Reliability enum."""
    if isinstance(value, Reliability):
        return value
    try:
        return Reliability(value.lower())
    except ValueError:
        raise ValueError(
            f"Invalid reliability '{value}'. Must be one of: {[r.value for r in Reliability]}"
        )


def _normalize_encoding(value: Union[str, Encoding]) -> Encoding:
    """Convert string or Encoding to Encoding enum."""
    if isinstance(value, Encoding):
        return value
    try:
        return Encoding(value.lower())
    except ValueError:
        raise ValueError(
            f"Invalid encoding '{value}'. Must be one of: {[e.value for e in Encoding]}"
        )


def _normalize_attack_surface(
    value: Optional[Union[str, AttackSurface]],
) -> Optional[AttackSurface]:
    """Convert string or AttackSurface to AttackSurface enum."""
    if value is None:
        return None
    if isinstance(value, AttackSurface):
        return value
    try:
        return AttackSurface(value.lower())
    except ValueError:
        raise ValueError(
            f"Invalid attack_surface '{value}'. Must be one of: {[a.value for a in AttackSurface]}"
        )


@dataclass
class PayloadEntry:
    """
    Enhanced payload entry with comprehensive metadata.

    Represents a single XSS payload with all associated metadata
    for categorization, filtering, and security assessment.
    Uses Enum types for type safety and IDE autocomplete.

    Attributes:
        payload: The actual XSS payload string.
        contexts: List of applicable injection contexts.
        severity: CVSS-aligned severity level (Enum).
        cvss_score: CVSS 3.1 base score (0.0-10.0).
        description: Human-readable payload description.
        tags: Searchable tags for categorization.
        bypasses: List of WAFs/filters this payload bypasses.
        encoding: Encoding type used in payload (Enum).
        browser_support: List of supported browsers.
        waf_evasion: Whether payload is designed for WAF evasion.
        tested_on: Platforms/frameworks tested against.
        reliability: Execution reliability rating (Enum).
        last_updated: ISO 8601 timestamp of last update.
        attack_surface: Target attack surface category (Enum).
        spec_ref: Specification reference (e.g., MSC number).
        known_affected: List of known affected versions.
        profile: Payload profile/category identifier.

    Example:
        >>> entry = PayloadEntry(
        ...     payload="<script>alert(1)</script>",
        ...     contexts=["html_content"],
        ...     severity=Severity.HIGH,  # or "high"
        ...     cvss_score=7.5,
        ...     description="Basic script injection"
        ... )
    """

    # Required fields
    payload: str
    contexts: List[str]
    severity: Union[str, Severity]
    cvss_score: float
    description: str

    # Optional fields with defaults
    tags: List[str] = field(default_factory=list)
    bypasses: List[str] = field(default_factory=list)
    encoding: Union[str, Encoding] = Encoding.NONE
    browser_support: List[str] = field(default_factory=list)
    waf_evasion: bool = False
    tested_on: List[str] = field(default_factory=list)
    reliability: Union[str, Reliability] = Reliability.HIGH
    last_updated: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

    # Extended fields for enterprise auditing
    attack_surface: Optional[Union[str, AttackSurface]] = None
    spec_ref: Optional[str] = None
    known_affected: Optional[List[str]] = None
    profile: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate and normalize fields after initialization."""
        # Validate CVSS score range
        if not 0.0 <= self.cvss_score <= 10.0:
            raise ValueError(f"cvss_score must be 0.0-10.0, got {self.cvss_score}")

        # Normalize Enum fields (accepts both str and Enum)
        self.severity = _normalize_severity(self.severity)
        self.reliability = _normalize_reliability(self.reliability)
        self.encoding = _normalize_encoding(self.encoding)
        self.attack_surface = _normalize_attack_surface(self.attack_surface)

        # Ensure contexts is a list
        if isinstance(self.contexts, str):
            self.contexts = [self.contexts]

        # Normalize context names to lowercase
        self.contexts = [c.lower() for c in self.contexts]

        # Auto-generate browser_support if empty
        if not self.browser_support:
            self.browser_support = self._infer_browser_support()

        # Auto-enhance description if too short
        if not self.description or len(self.description) <= 20:
            self.description = self._generate_description()

        # Auto-enhance tags if insufficient
        if not self.tags or len(self.tags) < 2:
            self.tags = self._enhance_tags()

    def _infer_browser_support(self) -> List[str]:
        """Infer browser support based on payload characteristics."""
        payload_lower = self.payload.lower()
        tags_lower = [t.lower() for t in self.tags] if self.tags else []

        # Legacy IE-only patterns
        if any(x in payload_lower for x in ["vbscript:", "expression(", "behavior:", ".htc", "activex"]):
            return ["ie"]

        # Check for modern-only features
        modern_only = ["shadow", "slot", "template", "dialog", "details", "module", 
                       "import", "async", "await", "fetch", "promise", "worker",
                       "wasm", "webgl", "webrtc", "websocket", "indexeddb", "serviceworker"]
        for feature in modern_only:
            if feature in payload_lower or feature in tags_lower:
                return ["chrome", "firefox", "safari", "edge"]

        # Framework-specific (modern browsers)
        frameworks = ["angular", "vue", "react", "ember", "svelte", "alpine", "htmx"]
        for fw in frameworks:
            if fw in payload_lower or fw in tags_lower:
                return ["chrome", "firefox", "safari", "edge"]

        # Legacy elements that work everywhere including IE
        legacy_universal = ["<script", "<img", "<body", "<input", "<form", "<a ", 
                          "<iframe", "<div", "<style", "<link", "<meta", "<table",
                          "onerror", "onload", "onclick", "onfocus", "onmouseover"]
        for elem in legacy_universal:
            if elem in payload_lower:
                return ["chrome", "firefox", "safari", "edge", "ie"]

        # Default to modern browsers
        return ["chrome", "firefox", "safari", "edge"]

    def _generate_description(self) -> str:
        """Generate meaningful description based on payload characteristics."""
        payload_lower = self.payload.lower()
        tags_lower = [t.lower() for t in self.tags] if self.tags else []

        # Script tag
        if "<script" in payload_lower:
            return "Script tag injection for direct JavaScript execution in HTML context"

        # Event handlers
        if "onerror" in payload_lower:
            if "<img" in payload_lower:
                return "Image element XSS via onerror event handler injection"
            if "<svg" in payload_lower:
                return "SVG element XSS via onerror event handler"
            return "Event handler XSS via onerror attribute injection"

        if "onload" in payload_lower:
            if "<svg" in payload_lower:
                return "SVG element XSS via onload event handler"
            if "<body" in payload_lower:
                return "Body element XSS via onload event handler"
            if "<iframe" in payload_lower:
                return "Iframe XSS via onload event handler"
            return "Event handler XSS via onload attribute injection"

        # Protocol handlers
        if "javascript:" in payload_lower:
            return "JavaScript protocol XSS via URL injection"
        if "data:" in payload_lower:
            return "Data URI XSS for inline content injection"

        # DOM sinks
        if "eval(" in payload_lower:
            return "Code execution via eval() JavaScript sink"
        if "innerhtml" in payload_lower:
            return "HTML injection via innerHTML DOM property"
        if "document.write" in payload_lower:
            return "HTML injection via document.write() method"
        if "settimeout" in payload_lower:
            return "Code execution via setTimeout() string argument"
        if "setinterval" in payload_lower:
            return "Code execution via setInterval() string argument"

        # Templates
        if "{{" in self.payload or "${" in self.payload:
            return "Template injection payload for expression evaluation"

        # Specific elements
        if "<svg" in payload_lower:
            return "SVG element XSS exploiting inline event handlers"
        if "<img" in payload_lower:
            return "Image element XSS via error/load event handlers"
        if "<iframe" in payload_lower:
            return "Iframe injection for cross-origin script execution"
        if "<object" in payload_lower:
            return "Object element XSS via data/classid attributes"
        if "<embed" in payload_lower:
            return "Embed element XSS for plugin-based code execution"
        if "<video" in payload_lower:
            return "Video element XSS via media error events"
        if "<audio" in payload_lower:
            return "Audio element XSS via media error events"
        if "<input" in payload_lower:
            return "Input element XSS via focus/blur event handlers"
        if "<form" in payload_lower:
            return "Form element XSS via action/formaction attributes"
        if "<a " in payload_lower or "<a>" in payload_lower:
            return "Anchor element XSS via href attribute injection"
        if "<style" in payload_lower:
            return "Style element XSS via CSS expression/import"
        if "<link" in payload_lower:
            return "Link element XSS via stylesheet injection"
        if "<meta" in payload_lower:
            return "Meta element XSS via refresh/redirect injection"
        if "<base" in payload_lower:
            return "Base element XSS for URL hijacking"
        if "<details" in payload_lower:
            return "Details element XSS via toggle event handler"
        if "<select" in payload_lower:
            return "Select element XSS via change event injection"
        if "<textarea" in payload_lower:
            return "Textarea element XSS via focus event handlers"
        if "<marquee" in payload_lower:
            return "Marquee element XSS via start/finish events"
        if "<math" in payload_lower:
            return "MathML element XSS via href/xlink attributes"
        if "<table" in payload_lower:
            return "Table element XSS via background attribute"

        # By tags
        if "polyglot" in tags_lower:
            return "Multi-context polyglot payload for various injection points"
        if "waf" in tags_lower or "bypass" in tags_lower:
            return "WAF/filter bypass payload using evasion techniques"
        if "encoding" in tags_lower:
            return "Encoded payload for filter/WAF bypass"
        if "mutation" in tags_lower or "mxss" in tags_lower:
            return "Mutation XSS exploiting browser parsing differences"
        if "prototype" in tags_lower:
            return "Prototype pollution leading to XSS execution"
        if "csp" in tags_lower:
            return "CSP bypass payload exploiting policy weaknesses"
        if "dom" in tags_lower:
            return "DOM-based XSS exploiting client-side JavaScript sinks"
        if "blind" in tags_lower:
            return "Blind XSS payload with external callback for detection"
        if "ssti" in tags_lower:
            return "Server-Side Template Injection payload"
        if "csti" in tags_lower:
            return "Client-Side Template Injection payload"

        # Frameworks
        if "angular" in tags_lower:
            return "AngularJS template injection for sandbox escape"
        if "vue" in tags_lower:
            return "Vue.js template injection for code execution"
        if "react" in tags_lower:
            return "React XSS via dangerouslySetInnerHTML or JSX injection"
        if "jquery" in tags_lower:
            return "jQuery XSS via selector/html injection"
        if "ember" in tags_lower:
            return "Ember.js template injection vulnerability"

        # Generic fallback
        return "XSS payload for cross-site scripting vulnerability exploitation"

    def _enhance_tags(self) -> List[str]:
        """Enhance tags based on payload characteristics."""
        tags = list(self.tags) if self.tags else []
        payload_lower = self.payload.lower()

        # Add tags based on payload content
        tag_patterns = {
            "<script": "script",
            "onerror": "event-handler",
            "onload": "event-handler",
            "onclick": "event-handler",
            "onfocus": "event-handler",
            "onmouseover": "event-handler",
            "javascript:": "protocol",
            "data:": "data-uri",
            "eval(": "eval",
            "innerhtml": "dom-sink",
            "document.write": "dom-sink",
            "settimeout": "timer",
            "setinterval": "timer",
            "<svg": "svg",
            "<img": "img",
            "<iframe": "iframe",
            "<object": "object",
            "<embed": "embed",
            "<video": "media",
            "<audio": "media",
            "<input": "form",
            "<form": "form",
            "<style": "css",
            "<link": "css",
            "{{": "template",
            "${": "template",
            "<%": "template",
            "constructor": "prototype",
            "__proto__": "prototype",
        }

        for pattern, tag in tag_patterns.items():
            if pattern in payload_lower and tag not in tags:
                tags.append(tag)

        # Add context-based tags
        for ctx in self.contexts:
            if ctx not in tags and ctx not in ["html_content", "default"]:
                tags.append(ctx.replace("_", "-"))

        # Ensure at least 2 tags
        if len(tags) < 2:
            tags.append("xss")
        if len(tags) < 2:
            tags.append("injection")

        return tags[:10]  # Limit to 10 tags

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary representation.
        Enum values are converted to strings for JSON serialization.

        Returns:
            Dictionary with all payload metadata.
        """
        result = asdict(self)
        # Convert Enum to string values
        result["severity"] = self.severity.value
        result["reliability"] = self.reliability.value
        result["encoding"] = self.encoding.value
        if self.attack_surface:
            result["attack_surface"] = self.attack_surface.value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PayloadEntry":
        """
        Create PayloadEntry from dictionary.
        Automatically converts string values to Enums.

        Args:
            data: Dictionary with payload metadata.

        Returns:
            New PayloadEntry instance.
        """
        return cls(**data)

    def matches_context(self, context: str) -> bool:
        """
        Check if payload applies to given context.

        Args:
            context: Context name to check.

        Returns:
            True if payload applies to context.
        """
        return context.lower() in self.contexts

    def matches_severity(self, min_severity: Union[str, Severity]) -> bool:
        """
        Check if payload meets minimum severity threshold.
        Uses Enum comparison operators.

        Args:
            min_severity: Minimum severity level.

        Returns:
            True if payload severity >= min_severity.
        """
        if isinstance(min_severity, str):
            min_severity = _normalize_severity(min_severity)
        return self.severity >= min_severity

    def has_tag(self, tag: str) -> bool:
        """
        Check if payload has specified tag.

        Args:
            tag: Tag to search for.

        Returns:
            True if tag is present.
        """
        return tag.lower() in [t.lower() for t in self.tags]

    def bypasses_waf(self, waf_name: str) -> bool:
        """
        Check if payload bypasses specified WAF.

        Args:
            waf_name: WAF name to check.

        Returns:
            True if payload bypasses the WAF.
        """
        return waf_name.lower() in [b.lower() for b in self.bypasses]

    def __repr__(self) -> str:
        """Concise string representation for debugging."""
        payload_short = self.payload[:40] + "..." if len(self.payload) > 40 else self.payload
        return (
            f"PayloadEntry("
            f"severity={self.severity.value!r}, "
            f"cvss={self.cvss_score}, "
            f"contexts={len(self.contexts)}, "
            f"payload={payload_short!r})"
        )

    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"[{self.severity.value.upper()}] {self.description}: {self.payload[:50]}..."


# Type aliases for clarity
PayloadDatabase = Dict[str, PayloadEntry]
PayloadList = List[PayloadEntry]
