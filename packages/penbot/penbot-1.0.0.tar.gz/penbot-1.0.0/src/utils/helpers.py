"""Helper utility functions."""

import re
import uuid
from urllib.parse import urlparse
from datetime import datetime


def generate_uuid() -> str:
    """
    Generate a unique identifier.

    Returns:
        UUID string

    Example:
        >>> test_id = generate_uuid()
        >>> print(test_id)
        'a1b2c3d4-e5f6-7890-abcd-ef1234567890'
    """
    return str(uuid.uuid4())


def extract_evidence(text: str, pattern: dict, max_length: int = 200) -> str:
    """
    Extract evidence snippet from text based on pattern match.

    Args:
        text: Full text to extract from
        pattern: Pattern dict with 'regex' key
        max_length: Maximum length of evidence snippet

    Returns:
        Evidence snippet with context

    Example:
        >>> pattern = {"regex": r"password"}
        >>> text = "The user's password is: secret123"
        >>> evidence = extract_evidence(text, pattern)
        >>> print(evidence)
        '...password is: secret123'
    """
    if "regex" in pattern:
        match = re.search(pattern["regex"], text, re.IGNORECASE)
        if match:
            start = max(0, match.start() - 50)
            end = min(len(text), match.end() + 50)
            snippet = text[start:end]

            if start > 0:
                snippet = "..." + snippet
            if end < len(text):
                snippet = snippet + "..."

            if len(snippet) > max_length:
                snippet = snippet[:max_length] + "..."

            return snippet

    # Return truncated text if no pattern match
    return text[:max_length] + ("..." if len(text) > max_length else "")


def validate_url(url: str) -> bool:
    """
    Validate URL format.

    Args:
        url: URL string to validate

    Returns:
        True if valid URL, False otherwise

    Example:
        >>> validate_url("https://example.com/api")
        True
        >>> validate_url("not-a-url")
        False
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def is_blocked_domain(url: str, blocked_domains: list) -> bool:
    """
    Check if URL contains a blocked domain.

    Args:
        url: URL to check
        blocked_domains: List of blocked domain strings

    Returns:
        True if domain is blocked

    Example:
        >>> is_blocked_domain("https://openai.com/chat", ["openai.com"])
        True
    """
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        return any(blocked.lower() in domain for blocked in blocked_domains)
    except Exception:
        return False


def format_timestamp(dt: datetime) -> str:
    """
    Format datetime as ISO 8601 string.

    Args:
        dt: Datetime object

    Returns:
        ISO formatted string
    """
    return dt.isoformat()


def mask_sensitive_data(text: str) -> str:
    """
    Mask potentially sensitive data in text for logging.

    Args:
        text: Text potentially containing sensitive data

    Returns:
        Text with sensitive data masked

    Example:
        >>> mask_sensitive_data("My password is secret123")
        'My password is ***MASKED***'
    """
    # Mask potential passwords
    text = re.sub(
        r"(password|passwd|pwd|secret|token|key)\s*[:=]\s*\S+",
        r"\1: ***MASKED***",
        text,
        flags=re.IGNORECASE,
    )

    # Mask potential API keys
    text = re.sub(r"(sk-[a-zA-Z0-9]{20,})", "***API_KEY***", text)

    # Mask potential emails
    text = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "***EMAIL***", text)

    return text


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text

    return text[: max_length - len(suffix)] + suffix
