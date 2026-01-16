"""
Tests for TruthGit validation module.
"""

import pytest

from truthgit.validation import (
    ValidationError,
    validate_claim_content,
    validate_confidence,
    validate_domain,
    validate_hash,
    validate_hash_prefix,
    validate_sources,
    validate_validators_list,
    validate_verifier_results,
)


class TestValidationError:
    """Tests for ValidationError exception."""

    def test_error_message(self):
        """ValidationError has correct message format."""
        error = ValidationError("field", "message")
        assert str(error) == "field: message"

    def test_error_with_value(self):
        """ValidationError stores value."""
        error = ValidationError("field", "message", value=42)
        assert error.value == 42


class TestValidateClaimContent:
    """Tests for validate_claim_content function."""

    def test_valid_content(self):
        """Valid content passes validation."""
        result = validate_claim_content("This is a valid claim")
        assert result == "This is a valid claim"

    def test_strips_whitespace(self):
        """Content is stripped of whitespace."""
        result = validate_claim_content("  Claim with spaces  ")
        assert result == "Claim with spaces"

    def test_none_raises_error(self):
        """None content raises ValidationError."""
        with pytest.raises(ValidationError) as exc:
            validate_claim_content(None)
        assert "cannot be None" in str(exc.value)

    def test_empty_raises_error(self):
        """Empty content raises ValidationError."""
        with pytest.raises(ValidationError) as exc:
            validate_claim_content("")
        assert "cannot be empty" in str(exc.value)

    def test_whitespace_only_raises_error(self):
        """Whitespace-only content raises ValidationError."""
        with pytest.raises(ValidationError) as exc:
            validate_claim_content("   ")
        assert "cannot be empty" in str(exc.value)

    def test_non_string_raises_error(self):
        """Non-string content raises ValidationError."""
        with pytest.raises(ValidationError) as exc:
            validate_claim_content(123)
        assert "must be a string" in str(exc.value)

    def test_exceeds_max_length(self):
        """Content exceeding max length raises ValidationError."""
        long_content = "x" * 10001
        with pytest.raises(ValidationError) as exc:
            validate_claim_content(long_content)
        assert "exceeds maximum length" in str(exc.value)

    def test_custom_max_length(self):
        """Custom max length is respected."""
        with pytest.raises(ValidationError):
            validate_claim_content("12345", max_length=3)


class TestValidateConfidence:
    """Tests for validate_confidence function."""

    def test_valid_confidence(self):
        """Valid confidence passes."""
        assert validate_confidence(0.5) == 0.5
        assert validate_confidence(0) == 0
        assert validate_confidence(1) == 1

    def test_clamps_high(self):
        """High values are clamped to 1."""
        assert validate_confidence(1.5) == 1.0

    def test_clamps_low(self):
        """Low values are clamped to 0."""
        assert validate_confidence(-0.5) == 0.0

    def test_converts_int(self):
        """Integer values are converted to float."""
        assert validate_confidence(1) == 1.0
        assert isinstance(validate_confidence(1), float)

    def test_none_raises_error(self):
        """None confidence raises ValidationError."""
        with pytest.raises(ValidationError):
            validate_confidence(None)

    def test_non_numeric_raises_error(self):
        """Non-numeric confidence raises ValidationError."""
        with pytest.raises(ValidationError):
            validate_confidence("high")


class TestValidateDomain:
    """Tests for validate_domain function."""

    def test_valid_domain(self):
        """Valid domain passes."""
        assert validate_domain("physics") == "physics"
        assert validate_domain("programming.python") == "programming.python"

    def test_converts_to_lowercase(self):
        """Domain is converted to lowercase."""
        assert validate_domain("PHYSICS") == "physics"

    def test_none_returns_general(self):
        """None domain returns 'general'."""
        assert validate_domain(None) == "general"

    def test_empty_returns_general(self):
        """Empty domain returns 'general'."""
        assert validate_domain("") == "general"

    def test_strips_whitespace(self):
        """Domain is stripped."""
        assert validate_domain("  physics  ") == "physics"

    def test_non_string_raises_error(self):
        """Non-string domain raises ValidationError."""
        with pytest.raises(ValidationError):
            validate_domain(123)

    def test_exceeds_max_length(self):
        """Long domain raises ValidationError."""
        with pytest.raises(ValidationError):
            validate_domain("x" * 101)

    def test_invalid_characters_raises_error(self):
        """Invalid characters raise ValidationError."""
        with pytest.raises(ValidationError):
            validate_domain("physics & math")


class TestValidateHash:
    """Tests for validate_hash function."""

    def test_valid_hash(self):
        """Valid 64-char hex hash passes."""
        valid_hash = "a" * 64
        assert validate_hash(valid_hash) == valid_hash

    def test_converts_to_lowercase(self):
        """Hash is converted to lowercase."""
        assert validate_hash("A" * 64) == "a" * 64

    def test_strips_whitespace(self):
        """Hash is stripped."""
        assert validate_hash("  " + "b" * 64 + "  ") == "b" * 64

    def test_none_raises_error(self):
        """None hash raises ValidationError."""
        with pytest.raises(ValidationError):
            validate_hash(None)

    def test_non_string_raises_error(self):
        """Non-string hash raises ValidationError."""
        with pytest.raises(ValidationError):
            validate_hash(12345)

    def test_wrong_length_raises_error(self):
        """Wrong length hash raises ValidationError."""
        with pytest.raises(ValidationError) as exc:
            validate_hash("abc")
        assert "64 characters" in str(exc.value)

    def test_non_hex_raises_error(self):
        """Non-hexadecimal hash raises ValidationError."""
        with pytest.raises(ValidationError) as exc:
            validate_hash("g" * 64)  # 'g' is not hex
        assert "hexadecimal" in str(exc.value)


class TestValidateHashPrefix:
    """Tests for validate_hash_prefix function."""

    def test_valid_prefix(self):
        """Valid prefix passes."""
        assert validate_hash_prefix("abcd") == "abcd"
        assert validate_hash_prefix("a" * 64) == "a" * 64

    def test_too_short_raises_error(self):
        """Too short prefix raises ValidationError."""
        with pytest.raises(ValidationError):
            validate_hash_prefix("abc")

    def test_custom_min_length(self):
        """Custom min length is respected."""
        assert validate_hash_prefix("ab", min_length=2) == "ab"

    def test_none_raises_error(self):
        """None prefix raises ValidationError."""
        with pytest.raises(ValidationError):
            validate_hash_prefix(None)

    def test_too_long_raises_error(self):
        """Prefix over 64 chars raises ValidationError."""
        with pytest.raises(ValidationError):
            validate_hash_prefix("a" * 65)


class TestValidateValidatorsList:
    """Tests for validate_validators_list function."""

    def test_valid_list(self):
        """Valid list passes."""
        result = validate_validators_list(["claude", "gpt"])
        assert result == ["CLAUDE", "GPT"]

    def test_converts_to_uppercase(self):
        """Names are converted to uppercase."""
        result = validate_validators_list(["Claude"])
        assert result == ["CLAUDE"]

    def test_none_raises_error(self):
        """None list raises ValidationError."""
        with pytest.raises(ValidationError):
            validate_validators_list(None)

    def test_empty_list_raises_error(self):
        """Empty list raises ValidationError with default min_count."""
        with pytest.raises(ValidationError):
            validate_validators_list([])

    def test_custom_min_count(self):
        """Custom min_count is respected."""
        result = validate_validators_list([], min_count=0)
        assert result == []

    def test_non_list_raises_error(self):
        """Non-list raises ValidationError."""
        with pytest.raises(ValidationError):
            validate_validators_list("claude")

    def test_non_string_element_raises_error(self):
        """Non-string element raises ValidationError."""
        with pytest.raises(ValidationError):
            validate_validators_list([123])


class TestValidateVerifierResults:
    """Tests for validate_verifier_results function."""

    def test_valid_results(self):
        """Valid results pass."""
        result = validate_verifier_results({"claude": (0.9, "Good")})
        assert result == {"CLAUDE": (0.9, "Good")}

    def test_none_raises_error(self):
        """None results raise ValidationError."""
        with pytest.raises(ValidationError):
            validate_verifier_results(None)

    def test_empty_raises_error(self):
        """Empty results raise ValidationError."""
        with pytest.raises(ValidationError):
            validate_verifier_results({})

    def test_non_dict_raises_error(self):
        """Non-dict results raise ValidationError."""
        with pytest.raises(ValidationError):
            validate_verifier_results([])

    def test_invalid_tuple_raises_error(self):
        """Invalid tuple format raises ValidationError."""
        with pytest.raises(ValidationError):
            validate_verifier_results({"claude": (0.9,)})  # Missing reasoning

    def test_clamps_confidence(self):
        """High confidence is clamped."""
        result = validate_verifier_results({"v": (1.5, "Over")})
        assert result["V"][0] == 1.0


class TestValidateSources:
    """Tests for validate_sources function."""

    def test_valid_sources(self):
        """Valid sources pass."""
        result = validate_sources([{"url": "https://example.com", "title": "Example"}])
        assert len(result) == 1
        assert result[0]["url"] == "https://example.com"

    def test_none_returns_empty(self):
        """None sources returns empty list."""
        assert validate_sources(None) == []

    def test_non_list_raises_error(self):
        """Non-list raises ValidationError."""
        with pytest.raises(ValidationError):
            validate_sources("source")

    def test_non_dict_element_raises_error(self):
        """Non-dict element raises ValidationError."""
        with pytest.raises(ValidationError):
            validate_sources(["not a dict"])

    def test_default_values(self):
        """Default values are applied."""
        result = validate_sources([{}])
        assert result[0]["url"] == ""
        assert result[0]["type"] == "PRIMARY"
        assert result[0]["reliability"] == 0.8
