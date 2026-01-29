"""
TruthGit Input Validation Module.

Provides validation functions for user inputs to ensure data integrity
and prevent invalid data from entering the system.
"""

import re
from typing import Any


class ValidationError(Exception):
    """Raised when input validation fails."""

    def __init__(self, field: str, message: str, value: Any = None):
        self.field = field
        self.message = message
        self.value = value
        super().__init__(f"{field}: {message}")


def validate_claim_content(content: str, max_length: int = 10000) -> str:
    """
    Validate claim content.

    Args:
        content: The claim text to validate
        max_length: Maximum allowed length (default 10000)

    Returns:
        Validated and stripped content

    Raises:
        ValidationError: If content is invalid
    """
    if content is None:
        raise ValidationError("content", "Content cannot be None")

    if not isinstance(content, str):
        raise ValidationError("content", f"Content must be a string, got {type(content).__name__}")

    content = content.strip()

    if not content:
        raise ValidationError("content", "Content cannot be empty")

    if len(content) > max_length:
        raise ValidationError(
            "content", f"Content exceeds maximum length of {max_length} characters", len(content)
        )

    return content


def validate_confidence(confidence: float) -> float:
    """
    Validate confidence value.

    Args:
        confidence: Confidence score to validate

    Returns:
        Validated confidence (clamped to [0, 1])

    Raises:
        ValidationError: If confidence is not a number
    """
    if confidence is None:
        raise ValidationError("confidence", "Confidence cannot be None")

    try:
        confidence = float(confidence)
    except (TypeError, ValueError):
        raise ValidationError(
            "confidence", f"Confidence must be a number, got {type(confidence).__name__}"
        )

    # Clamp to valid range
    return max(0.0, min(1.0, confidence))


def validate_domain(domain: str, max_length: int = 100) -> str:
    """
    Validate domain string.

    Args:
        domain: Domain to validate
        max_length: Maximum allowed length

    Returns:
        Validated domain (lowercase, stripped)

    Raises:
        ValidationError: If domain is invalid
    """
    if domain is None:
        return "general"

    if not isinstance(domain, str):
        raise ValidationError("domain", f"Domain must be a string, got {type(domain).__name__}")

    domain = domain.strip().lower()

    if not domain:
        return "general"

    if len(domain) > max_length:
        raise ValidationError("domain", f"Domain exceeds maximum length of {max_length} characters")

    # Domain should be alphanumeric with dots and underscores
    if not re.match(r"^[a-z0-9._-]+$", domain):
        raise ValidationError(
            "domain", "Domain must contain only letters, numbers, dots, underscores, and hyphens"
        )

    return domain


def validate_hash(hash_value: str, field_name: str = "hash") -> str:
    """
    Validate a SHA-256 hash string.

    Args:
        hash_value: Hash to validate
        field_name: Name of the field for error messages

    Returns:
        Validated hash (lowercase)

    Raises:
        ValidationError: If hash is invalid
    """
    if hash_value is None:
        raise ValidationError(field_name, "Hash cannot be None")

    if not isinstance(hash_value, str):
        raise ValidationError(field_name, f"Hash must be a string, got {type(hash_value).__name__}")

    hash_value = hash_value.strip().lower()

    if len(hash_value) != 64:
        raise ValidationError(field_name, f"Hash must be 64 characters, got {len(hash_value)}")

    if not re.match(r"^[a-f0-9]+$", hash_value):
        raise ValidationError(field_name, "Hash must be hexadecimal (a-f, 0-9)")

    return hash_value


def validate_hash_prefix(prefix: str, min_length: int = 4) -> str:
    """
    Validate a hash prefix (partial hash for lookup).

    Args:
        prefix: Hash prefix to validate
        min_length: Minimum prefix length

    Returns:
        Validated prefix (lowercase)

    Raises:
        ValidationError: If prefix is invalid
    """
    if prefix is None:
        raise ValidationError("prefix", "Hash prefix cannot be None")

    if not isinstance(prefix, str):
        raise ValidationError(
            "prefix", f"Hash prefix must be a string, got {type(prefix).__name__}"
        )

    prefix = prefix.strip().lower()

    if len(prefix) < min_length:
        raise ValidationError("prefix", f"Hash prefix must be at least {min_length} characters")

    if len(prefix) > 64:
        raise ValidationError("prefix", "Hash prefix cannot exceed 64 characters")

    if not re.match(r"^[a-f0-9]+$", prefix):
        raise ValidationError("prefix", "Hash prefix must be hexadecimal (a-f, 0-9)")

    return prefix


def validate_validators_list(validators: list | None, min_count: int = 1) -> list[str]:
    """
    Validate a list of validator names.

    Args:
        validators: List of validator names
        min_count: Minimum number of validators required

    Returns:
        Validated list of validator names

    Raises:
        ValidationError: If list is invalid
    """
    if validators is None:
        raise ValidationError("validators", "Validators list cannot be None")

    if not isinstance(validators, list):
        raise ValidationError(
            "validators", f"Validators must be a list, got {type(validators).__name__}"
        )

    if len(validators) < min_count:
        raise ValidationError(
            "validators", f"At least {min_count} validator(s) required, got {len(validators)}"
        )

    validated = []
    for i, v in enumerate(validators):
        if not isinstance(v, str):
            raise ValidationError(
                f"validators[{i}]", f"Validator name must be a string, got {type(v).__name__}"
            )
        name = v.strip().upper()
        if not name:
            raise ValidationError(f"validators[{i}]", "Validator name cannot be empty")
        validated.append(name)

    return validated


def validate_verifier_results(
    results: dict | None,
) -> dict[str, tuple[float, str]]:
    """
    Validate verifier results dictionary.

    Args:
        results: Dictionary of verifier name to (confidence, reasoning) tuples

    Returns:
        Validated results dictionary

    Raises:
        ValidationError: If results are invalid
    """
    if results is None:
        raise ValidationError("verifier_results", "Verifier results cannot be None")

    if not isinstance(results, dict):
        raise ValidationError(
            "verifier_results",
            f"Verifier results must be a dictionary, got {type(results).__name__}",
        )

    if not results:
        raise ValidationError("verifier_results", "Verifier results cannot be empty")

    validated = {}
    for name, value in results.items():
        # Validate name
        if not isinstance(name, str) or not name.strip():
            raise ValidationError("verifier_results", "Verifier name must be a non-empty string")

        # Validate value is tuple of (confidence, reasoning)
        if not isinstance(value, (tuple, list)) or len(value) != 2:
            raise ValidationError(
                f"verifier_results[{name}]",
                "Value must be a tuple of (confidence, reasoning)",
            )

        confidence, reasoning = value
        validated_confidence = validate_confidence(confidence)

        if not isinstance(reasoning, str):
            raise ValidationError(
                f"verifier_results[{name}].reasoning",
                f"Reasoning must be a string, got {type(reasoning).__name__}",
            )

        validated[name.strip().upper()] = (validated_confidence, reasoning.strip())

    return validated


def validate_sources(sources: list | None) -> list[dict]:
    """
    Validate a list of source dictionaries.

    Args:
        sources: List of source dicts with url, title, etc.

    Returns:
        Validated sources list

    Raises:
        ValidationError: If sources are invalid
    """
    if sources is None:
        return []

    if not isinstance(sources, list):
        raise ValidationError("sources", f"Sources must be a list, got {type(sources).__name__}")

    validated = []
    for i, source in enumerate(sources):
        if not isinstance(source, dict):
            raise ValidationError(
                f"sources[{i}]", f"Source must be a dictionary, got {type(source).__name__}"
            )

        validated_source = {
            "url": str(source.get("url", "")).strip(),
            "title": str(source.get("title", "")).strip(),
            "type": str(source.get("type", "PRIMARY")).strip().upper(),
            "reliability": validate_confidence(source.get("reliability", 0.8)),
        }
        validated.append(validated_source)

    return validated
