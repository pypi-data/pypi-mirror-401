"""
Domain pattern matching utility for test access key header injection.

Supports patterns like:
- api.example.com (exact match)
- *.example.com (wildcard subdomain match)
- api.example.com:8080 (with port)
"""

from __future__ import annotations

from urllib.parse import urlparse


def extract_host_with_port(url: str) -> str:
    """
    Extract host (with port if present) from URL.

    Args:
        url: Full URL string

    Returns:
        Host string, optionally with port (e.g., "api.example.com" or "api.example.com:8080")
    """
    try:
        parsed = urlparse(url)
        host = parsed.hostname or ""
        port = parsed.port

        # Include port only if it's non-standard
        if port:
            # Standard ports: 80 for http, 443 for https
            scheme = parsed.scheme.lower()
            if (scheme == "http" and port != 80) or (scheme == "https" and port != 443):
                return f"{host}:{port}"

        return host
    except Exception:
        return ""


def matches_domain_pattern(url: str, pattern: str) -> bool:
    """
    Check if URL matches the domain pattern.

    Args:
        url: Full URL to check (e.g., "https://api.example.com/v1/users")
        pattern: Domain pattern (e.g., "api.example.com" or "*.example.com")

    Returns:
        True if URL host matches the pattern

    Examples:
        >>> matches_domain_pattern("https://api.example.com/v1", "api.example.com")
        True
        >>> matches_domain_pattern("https://api.example.com/v1", "*.example.com")
        True
        >>> matches_domain_pattern("https://staging.example.com/v1", "*.example.com")
        True
        >>> matches_domain_pattern("https://api.other.com/v1", "*.example.com")
        False
    """
    host = extract_host_with_port(url)
    if not host:
        return False

    pattern = pattern.lower().strip()
    host = host.lower()

    # Exact match
    if pattern == host:
        return True

    # Wildcard match (*.example.com)
    if pattern.startswith("*."):
        # Convert *.example.com to fnmatch pattern
        base_domain = pattern[2:]  # Remove "*."

        # Match: host ends with .base_domain OR host equals base_domain
        if host == base_domain:
            return True
        if host.endswith(f".{base_domain}"):
            return True

    return False


def matches_any_domain_pattern(url: str, patterns: list[str]) -> bool:
    """
    Check if URL matches any of the domain patterns.

    Args:
        url: Full URL to check
        patterns: List of domain patterns

    Returns:
        True if URL matches any pattern
    """
    return any(matches_domain_pattern(url, pattern) for pattern in patterns)
