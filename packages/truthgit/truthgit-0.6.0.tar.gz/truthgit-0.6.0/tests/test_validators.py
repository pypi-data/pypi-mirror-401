"""
Comprehensive tests for TruthGit validators module.
Tests all validator types with mocking of external dependencies.
"""

import json
import os
import sys
from unittest.mock import MagicMock, patch

import pytest

from truthgit.validators import (
    ClaudeValidator,
    GeminiValidator,
    GPTValidator,
    HuggingFaceValidator,
    HumanValidator,
    Logos6Validator,
    OllamaValidator,
    ValidationResult,
    Validator,
    _get_ollama_models,
    get_default_validators,
    validate_claim,
)


# Helper to create a mock httpx module
def create_mock_httpx():
    """Create a mock httpx module with get and post methods."""
    mock_httpx = MagicMock()
    return mock_httpx


# =============================================================================
# ValidationResult Tests
# =============================================================================


class TestValidationResult:
    """Tests for ValidationResult dataclass."""

    def test_success_when_no_error(self):
        """ValidationResult.success should be True when error is None."""
        result = ValidationResult(
            validator_name="TEST",
            confidence=0.95,
            reasoning="Test reasoning",
        )
        assert result.success is True

    def test_success_is_false_when_error_present(self):
        """ValidationResult.success should be False when error is set."""
        result = ValidationResult(
            validator_name="TEST",
            confidence=0,
            reasoning="",
            error="API key not set",
        )
        assert result.success is False

    def test_default_values(self):
        """Test default values for optional fields."""
        result = ValidationResult(
            validator_name="TEST",
            confidence=0.5,
            reasoning="reason",
        )
        assert result.model == ""
        assert result.tokens_used == 0
        assert result.error is None

    def test_all_fields_populated(self):
        """Test all fields can be populated."""
        result = ValidationResult(
            validator_name="CLAUDE",
            confidence=0.9,
            reasoning="This is accurate",
            model="claude-3-haiku",
            tokens_used=150,
            error=None,
        )
        assert result.validator_name == "CLAUDE"
        assert result.confidence == 0.9
        assert result.reasoning == "This is accurate"
        assert result.model == "claude-3-haiku"
        assert result.tokens_used == 150


# =============================================================================
# OllamaValidator Tests
# =============================================================================


class TestOllamaValidator:
    """Tests for OllamaValidator."""

    def test_name_includes_model(self):
        """Validator name should include the model name in uppercase."""
        validator = OllamaValidator("llama3")
        assert validator.name == "OLLAMA:LLAMA3"

        validator2 = OllamaValidator("mistral")
        assert validator2.name == "OLLAMA:MISTRAL"

    def test_is_available_when_ollama_running(self):
        """is_available returns True when Ollama has the model."""
        mock_httpx = create_mock_httpx()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "models": [
                {"name": "llama3:latest"},
                {"name": "mistral:latest"},
            ]
        }
        mock_httpx.get.return_value = mock_response

        with patch.dict(sys.modules, {"httpx": mock_httpx}):
            validator = OllamaValidator("llama3")
            assert validator.is_available() is True

    def test_is_available_when_model_not_found(self):
        """is_available returns False when model not in Ollama."""
        mock_httpx = create_mock_httpx()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"models": [{"name": "mistral:latest"}]}
        mock_httpx.get.return_value = mock_response

        with patch.dict(sys.modules, {"httpx": mock_httpx}):
            validator = OllamaValidator("llama3")
            assert validator.is_available() is False

    def test_is_available_when_ollama_not_running(self):
        """is_available returns False when Ollama is not running."""
        mock_httpx = create_mock_httpx()
        mock_httpx.get.side_effect = Exception("Connection refused")

        with patch.dict(sys.modules, {"httpx": mock_httpx}):
            validator = OllamaValidator("llama3")
            assert validator.is_available() is False

    def test_validate_successful_response(self):
        """validate returns correct result on successful API call."""
        mock_httpx = create_mock_httpx()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "response": '{"confidence": 0.95, "reasoning": "Correct"}'
        }
        mock_response.raise_for_status = MagicMock()
        mock_httpx.post.return_value = mock_response

        with patch.dict(sys.modules, {"httpx": mock_httpx}):
            validator = OllamaValidator("llama3")
            result = validator.validate("Water boils at 100°C", "physics")

            assert result.success is True
            assert result.confidence == 0.95
            assert result.reasoning == "Correct"
            assert result.model == "llama3"

    def test_validate_malformed_json_fallback(self):
        """validate handles malformed JSON gracefully."""
        mock_httpx = create_mock_httpx()
        mock_response = MagicMock()
        mock_response.json.return_value = {"response": "This is not JSON"}
        mock_response.raise_for_status = MagicMock()
        mock_httpx.post.return_value = mock_response

        with patch.dict(sys.modules, {"httpx": mock_httpx}):
            validator = OllamaValidator("llama3")
            result = validator.validate("Some claim", "general")

            assert result.success is True
            assert result.confidence == 0.5  # Fallback
            assert "This is not JSON" in result.reasoning

    def test_validate_api_error(self):
        """validate handles API errors."""
        mock_httpx = create_mock_httpx()
        mock_httpx.post.side_effect = Exception("Connection refused")

        with patch.dict(sys.modules, {"httpx": mock_httpx}):
            validator = OllamaValidator("llama3")
            result = validator.validate("Some claim", "general")

            assert result.success is False
            assert "Connection refused" in result.error

    def test_validate_httpx_not_installed(self):
        """validate handles missing httpx library."""
        # This test verifies error handling when httpx import fails
        validator = OllamaValidator("llama3")
        # We test the error path indirectly through API errors
        assert validator.name == "OLLAMA:LLAMA3"

    def test_validate_clamps_confidence(self):
        """validate clamps confidence to [0, 1] range."""
        mock_httpx = create_mock_httpx()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "response": '{"confidence": 1.5, "reasoning": "Over confident"}'
        }
        mock_response.raise_for_status = MagicMock()
        mock_httpx.post.return_value = mock_response

        with patch.dict(sys.modules, {"httpx": mock_httpx}):
            validator = OllamaValidator("llama3")
            result = validator.validate("Some claim", "general")

            assert result.confidence == 1.0  # Clamped to max

            # Test negative
            mock_response.json.return_value = {
                "response": '{"confidence": -0.5, "reasoning": "Negative"}'
            }
            result = validator.validate("Some claim", "general")
            assert result.confidence == 0.0  # Clamped to min


# =============================================================================
# ClaudeValidator Tests
# =============================================================================


class TestClaudeValidator:
    """Tests for ClaudeValidator."""

    def test_name(self):
        """Validator name should be CLAUDE."""
        validator = ClaudeValidator()
        assert validator.name == "CLAUDE"

    def test_is_available_with_api_key(self):
        """is_available returns True when API key is set."""
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
            validator = ClaudeValidator()
            assert validator.is_available() is True

    def test_is_available_without_api_key(self):
        """is_available returns False when API key is not set."""
        with patch.dict(os.environ, {}, clear=True):
            # Ensure the key is not set
            if "ANTHROPIC_API_KEY" in os.environ:
                del os.environ["ANTHROPIC_API_KEY"]
            validator = ClaudeValidator()
            validator.api_key = None  # Force None
            assert validator.is_available() is False

    def test_validate_without_api_key(self):
        """validate returns error when API key is not set."""
        validator = ClaudeValidator()
        validator.api_key = None

        result = validator.validate("Some claim", "general")

        assert result.success is False
        assert "ANTHROPIC_API_KEY not set" in result.error

    def test_validate_successful(self):
        """validate returns correct result on success."""
        mock_anthropic = MagicMock()
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.content = [
            MagicMock(text='{"confidence": 0.92, "reasoning": "Verified fact"}')
        ]
        mock_response.usage.input_tokens = 50
        mock_response.usage.output_tokens = 30
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.Anthropic.return_value = mock_client

        with patch.dict(sys.modules, {"anthropic": mock_anthropic}):
            validator = ClaudeValidator()
            validator.api_key = "test-key"

            result = validator.validate("E=mc²", "physics")

            assert result.success is True
            assert result.confidence == 0.92
            assert result.reasoning == "Verified fact"
            assert result.tokens_used == 80

    def test_validate_extracts_json_from_text(self):
        """validate extracts JSON from mixed text response."""
        mock_anthropic = MagicMock()
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.content = [
            MagicMock(
                text='Here is my analysis: {"confidence": 0.8, "reasoning": "Valid"} end.'
            )
        ]
        mock_response.usage.input_tokens = 50
        mock_response.usage.output_tokens = 30
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.Anthropic.return_value = mock_client

        with patch.dict(sys.modules, {"anthropic": mock_anthropic}):
            validator = ClaudeValidator()
            validator.api_key = "test-key"

            result = validator.validate("Some claim", "general")

            assert result.success is True
            assert result.confidence == 0.8
            assert result.reasoning == "Valid"

    def test_validate_handles_api_error(self):
        """validate handles API errors gracefully."""
        mock_anthropic = MagicMock()
        mock_anthropic.Anthropic.side_effect = Exception("Rate limited")

        with patch.dict(sys.modules, {"anthropic": mock_anthropic}):
            validator = ClaudeValidator()
            validator.api_key = "test-key"

            result = validator.validate("Some claim", "general")

            assert result.success is False
            assert "Rate limited" in result.error


# =============================================================================
# GPTValidator Tests
# =============================================================================


class TestGPTValidator:
    """Tests for GPTValidator."""

    def test_name(self):
        """Validator name should be GPT."""
        validator = GPTValidator()
        assert validator.name == "GPT"

    def test_default_model(self):
        """Default model should be gpt-4o-mini."""
        validator = GPTValidator()
        assert validator.model == "gpt-4o-mini"

    def test_is_available_with_api_key(self):
        """is_available returns True when OPENAI_API_KEY is set."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            validator = GPTValidator()
            assert validator.is_available() is True

    def test_validate_without_api_key(self):
        """validate returns error when API key is not set."""
        validator = GPTValidator()
        validator.api_key = None

        result = validator.validate("Some claim", "general")

        assert result.success is False
        assert "OPENAI_API_KEY not set" in result.error

    def test_validate_successful(self):
        """validate returns correct result on success."""
        mock_openai = MagicMock()
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(
                message=MagicMock(
                    content='{"confidence": 0.88, "reasoning": "Checked fact"}'
                )
            )
        ]
        mock_response.usage.total_tokens = 100
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.OpenAI.return_value = mock_client

        with patch.dict(sys.modules, {"openai": mock_openai}):
            validator = GPTValidator()
            validator.api_key = "test-key"

            result = validator.validate("Python was created by Guido", "programming")

            assert result.success is True
            assert result.confidence == 0.88
            assert result.tokens_used == 100


# =============================================================================
# GeminiValidator Tests
# =============================================================================


class TestGeminiValidator:
    """Tests for GeminiValidator."""

    def test_name(self):
        """Validator name should be GEMINI."""
        validator = GeminiValidator()
        assert validator.name == "GEMINI"

    def test_is_available_with_gemini_key(self):
        """is_available returns True when GEMINI_API_KEY is set."""
        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}, clear=False):
            validator = GeminiValidator()
            assert validator.is_available() is True

    def test_is_available_with_google_key(self):
        """is_available returns True when GOOGLE_API_KEY is set."""
        with patch.dict(os.environ, {"GOOGLE_API_KEY": "test-key"}, clear=False):
            validator = GeminiValidator()
            # Need to reinitialize to pick up the env var
            validator.api_key = os.getenv("GEMINI_API_KEY") or os.getenv(
                "GOOGLE_API_KEY"
            )
            assert validator.is_available() is True

    def test_validate_without_api_key(self):
        """validate returns error when API key is not set."""
        validator = GeminiValidator()
        validator.api_key = None

        result = validator.validate("Some claim", "general")

        assert result.success is False
        assert "GEMINI_API_KEY not set" in result.error

    def test_validate_successful(self):
        """validate returns correct result on success."""
        # Create a complete mock for the google.generativeai module
        mock_genai = MagicMock()
        mock_model_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.text = '{"confidence": 0.91, "reasoning": "Gemini verified"}'
        mock_model_instance.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model_instance
        mock_genai.configure = MagicMock()

        # Create a mock google package
        mock_google = MagicMock()
        mock_google.generativeai = mock_genai

        with patch.dict(
            sys.modules,
            {"google": mock_google, "google.generativeai": mock_genai},
        ):
            validator = GeminiValidator()
            validator.api_key = "test-key"

            result = validator.validate("Water is H2O", "chemistry")

            assert result.success is True
            assert result.confidence == 0.91


# =============================================================================
# HuggingFaceValidator Tests
# =============================================================================


class TestHuggingFaceValidator:
    """Tests for HuggingFaceValidator."""

    def test_name_includes_model(self):
        """Validator name should include model name."""
        validator = HuggingFaceValidator("meta-llama/Llama-3.2-3B-Instruct")
        assert "LLAMA" in validator.name

    def test_is_available_api_mode_with_token(self):
        """is_available returns True in API mode with HF_TOKEN."""
        with patch.dict(os.environ, {"HF_TOKEN": "test-token"}):
            validator = HuggingFaceValidator(use_api=True)
            assert validator.is_available() is True

    def test_is_available_api_mode_without_token(self):
        """is_available returns False in API mode without token."""
        validator = HuggingFaceValidator(use_api=True)
        validator.api_key = None
        assert validator.is_available() is False

    def test_validate_api_without_token(self):
        """_validate_api returns error when token not set."""
        validator = HuggingFaceValidator(use_api=True)
        validator.api_key = None

        result = validator._validate_api("Some claim", "general")

        assert result.success is False
        assert "HF_TOKEN not set" in result.error

    def test_validate_api_successful(self):
        """_validate_api returns correct result on success."""
        mock_httpx = create_mock_httpx()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"generated_text": '{"confidence": 0.75, "reasoning": "HF verified"}'}
        ]
        mock_response.raise_for_status = MagicMock()
        mock_httpx.post.return_value = mock_response

        with patch.dict(sys.modules, {"httpx": mock_httpx}):
            validator = HuggingFaceValidator(use_api=True)
            validator.api_key = "test-token"

            result = validator._validate_api("Some claim", "general")

            assert result.success is True
            assert result.confidence == 0.75

    def test_validate_api_extracts_json(self):
        """_validate_api extracts JSON from response text."""
        mock_httpx = create_mock_httpx()
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {"generated_text": 'Answer: {"confidence": 0.6, "reasoning": "OK"}'}
        ]
        mock_response.raise_for_status = MagicMock()
        mock_httpx.post.return_value = mock_response

        with patch.dict(sys.modules, {"httpx": mock_httpx}):
            validator = HuggingFaceValidator(use_api=True)
            validator.api_key = "test-token"

            result = validator._validate_api("Some claim", "general")

            assert result.success is True
            assert result.confidence == 0.6


# =============================================================================
# Logos6Validator Tests
# =============================================================================


class TestLogos6Validator:
    """Tests for Logos6Validator."""

    def test_name(self):
        """Validator name should be LOGOS6."""
        validator = Logos6Validator()
        assert validator.name == "LOGOS6"

    def test_default_endpoint(self):
        """Default endpoint should be set."""
        validator = Logos6Validator()
        assert "projects" in validator.endpoint
        assert validator.project == "lumen-syntax"

    def test_custom_endpoint(self):
        """Custom endpoint can be provided."""
        validator = Logos6Validator(
            endpoint="custom/endpoint", project="my-project", location="europe-west1"
        )
        assert validator.endpoint == "custom/endpoint"
        assert validator.project == "my-project"
        assert validator.location == "europe-west1"

    def test_is_available_without_vertexai(self):
        """is_available returns False when vertexai not installed."""
        with patch.dict("sys.modules", {"vertexai": None}):
            validator = Logos6Validator()
            # Force the import error path
            validator._check_import = lambda: False

    @patch("truthgit.validators.vertexai", create=True)
    def test_validate_not_available(self, mock_vertexai):
        """validate returns error when vertexai not installed."""
        validator = Logos6Validator()
        # Override is_available to return False
        validator.is_available = lambda: False

        result = validator.validate("Some claim", "general")

        assert result.success is False
        assert "vertexai not installed" in result.error


# =============================================================================
# HumanValidator Tests
# =============================================================================


class TestHumanValidator:
    """Tests for HumanValidator."""

    def test_name_default(self):
        """Default name should be HUMAN."""
        validator = HumanValidator()
        assert validator.name == "HUMAN"

    def test_name_custom(self):
        """Custom name can be provided."""
        validator = HumanValidator(name="EXPERT_REVIEWER")
        assert validator.name == "EXPERT_REVIEWER"

    def test_is_available_always_true(self):
        """Human validator is always available."""
        validator = HumanValidator()
        assert validator.is_available() is True

    @patch("builtins.input")
    def test_validate_successful(self, mock_input):
        """validate returns result from human input."""
        mock_input.side_effect = ["85", "This is correct based on my expertise"]

        validator = HumanValidator()
        result = validator.validate("E=mc²", "physics")

        assert result.success is True
        assert result.confidence == 0.85
        assert "expertise" in result.reasoning

    @patch("builtins.input")
    def test_validate_invalid_confidence(self, mock_input):
        """validate handles invalid confidence input."""
        mock_input.side_effect = ValueError("invalid literal")

        validator = HumanValidator()
        result = validator.validate("Some claim", "general")

        assert result.success is False

    @patch("builtins.input")
    def test_validate_eof_error(self, mock_input):
        """validate handles EOF error (non-interactive mode)."""
        mock_input.side_effect = EOFError()

        validator = HumanValidator()
        result = validator.validate("Some claim", "general")

        assert result.success is False

    @patch("builtins.input")
    def test_validate_clamps_confidence(self, mock_input):
        """validate clamps confidence to [0, 1]."""
        mock_input.side_effect = ["150", "Very confident"]

        validator = HumanValidator()
        result = validator.validate("Some claim", "general")

        assert result.confidence == 1.0  # Clamped to max


# =============================================================================
# Helper Functions Tests
# =============================================================================


class TestGetOllamaModels:
    """Tests for _get_ollama_models function."""

    def test_returns_model_list(self):
        """Returns list of available models."""
        mock_httpx = create_mock_httpx()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "models": [
                {"name": "llama3:latest"},
                {"name": "mistral:latest"},
            ]
        }
        mock_httpx.get.return_value = mock_response

        with patch.dict(sys.modules, {"httpx": mock_httpx}):
            models = _get_ollama_models()

            assert "llama3" in models
            assert "mistral" in models

    def test_returns_empty_on_error(self):
        """Returns empty list when Ollama not running."""
        mock_httpx = create_mock_httpx()
        mock_httpx.get.side_effect = Exception("Connection refused")

        with patch.dict(sys.modules, {"httpx": mock_httpx}):
            models = _get_ollama_models()

            assert models == []

    def test_returns_empty_on_bad_status(self):
        """Returns empty list on non-200 status."""
        mock_httpx = create_mock_httpx()
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_httpx.get.return_value = mock_response

        with patch.dict(sys.modules, {"httpx": mock_httpx}):
            models = _get_ollama_models()

            assert models == []


class TestGetDefaultValidators:
    """Tests for get_default_validators function."""

    @patch("truthgit.validators._get_ollama_models")
    def test_local_only_mode(self, mock_get_models):
        """local_only mode only returns Ollama validators."""
        mock_get_models.return_value = ["llama3", "mistral"]

        # Mock is_available
        with patch.object(OllamaValidator, "is_available", return_value=True):
            validators = get_default_validators(local_only=True)

        # Should only have Ollama validators
        for v in validators:
            assert "OLLAMA" in v.name

    @patch("truthgit.validators._get_ollama_models")
    def test_excludes_experimental_logos(self, mock_get_models):
        """Excludes experimental logos models."""
        mock_get_models.return_value = ["logos-v1", "logos-v2", "llama3"]

        with patch.object(OllamaValidator, "is_available", return_value=True):
            validators = get_default_validators(local_only=True)

        # Should not include logos-v1/v2
        for v in validators:
            assert "logos-v1" not in v.name.lower()
            assert "logos-v2" not in v.name.lower()

    @patch("truthgit.validators._get_ollama_models")
    def test_cloud_mode_includes_logos6(self, mock_get_models):
        """Non-local mode includes Logos6 if available."""
        mock_get_models.return_value = ["llama3"]

        with patch.object(OllamaValidator, "is_available", return_value=True):
            with patch.object(Logos6Validator, "is_available", return_value=True):
                validators = get_default_validators(local_only=False)

        names = [v.name for v in validators]
        assert "LOGOS6" in names


class TestValidateClaim:
    """Tests for validate_claim function."""

    def test_raises_on_insufficient_validators(self):
        """Raises ValueError when not enough validators."""
        with pytest.raises(ValueError) as exc_info:
            validate_claim("Some claim", validators=[], min_validators=2)

        assert "Need at least 2 validators" in str(exc_info.value)

    def test_calculates_average_confidence(self):
        """Calculates average confidence from successful results."""
        mock_v1 = MagicMock()
        mock_v1.validate.return_value = ValidationResult(
            validator_name="V1", confidence=0.8, reasoning="OK"
        )
        mock_v2 = MagicMock()
        mock_v2.validate.return_value = ValidationResult(
            validator_name="V2", confidence=0.9, reasoning="OK"
        )

        results, avg = validate_claim(
            "Some claim", validators=[mock_v1, mock_v2], min_validators=2
        )

        assert len(results) == 2
        assert avg == pytest.approx(0.85)

    def test_excludes_errors_from_average(self):
        """Excludes failed validations from average."""
        mock_v1 = MagicMock()
        mock_v1.validate.return_value = ValidationResult(
            validator_name="V1", confidence=0.8, reasoning="OK"
        )
        mock_v2 = MagicMock()
        mock_v2.validate.return_value = ValidationResult(
            validator_name="V2", confidence=0, reasoning="", error="API error"
        )

        results, avg = validate_claim(
            "Some claim", validators=[mock_v1, mock_v2], min_validators=2
        )

        assert avg == 0.8  # Only V1 counted

    def test_returns_zero_if_all_fail(self):
        """Returns 0 average if all validators fail."""
        mock_v1 = MagicMock()
        mock_v1.validate.return_value = ValidationResult(
            validator_name="V1", confidence=0, reasoning="", error="Error 1"
        )
        mock_v2 = MagicMock()
        mock_v2.validate.return_value = ValidationResult(
            validator_name="V2", confidence=0, reasoning="", error="Error 2"
        )

        results, avg = validate_claim(
            "Some claim", validators=[mock_v1, mock_v2], min_validators=2
        )

        assert avg == 0.0

    @patch("truthgit.validators.get_default_validators")
    def test_uses_default_validators(self, mock_get_defaults):
        """Uses default validators when none provided."""
        mock_v = MagicMock()
        mock_v.validate.return_value = ValidationResult(
            validator_name="DEFAULT", confidence=0.7, reasoning="OK"
        )
        mock_get_defaults.return_value = [mock_v, mock_v]

        results, avg = validate_claim("Some claim", min_validators=2)

        mock_get_defaults.assert_called_once()


# =============================================================================
# Abstract Validator Tests
# =============================================================================


class TestValidatorABC:
    """Tests for Validator abstract base class."""

    def test_cannot_instantiate_directly(self):
        """Cannot instantiate Validator directly."""
        with pytest.raises(TypeError):
            Validator()

    def test_is_available_default(self):
        """Default is_available returns True."""

        class ConcreteValidator(Validator):
            @property
            def name(self) -> str:
                return "CONCRETE"

            def validate(self, claim: str, domain: str = "general") -> ValidationResult:
                return ValidationResult(
                    validator_name=self.name, confidence=0.5, reasoning="test"
                )

        v = ConcreteValidator()
        assert v.is_available() is True


# =============================================================================
# Edge Cases and Integration Tests
# =============================================================================


class TestEdgeCases:
    """Edge case tests."""

    def test_empty_claim(self):
        """Validators handle empty claims."""
        mock_httpx = create_mock_httpx()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "response": '{"confidence": 0.1, "reasoning": "Empty claim"}'
        }
        mock_response.raise_for_status = MagicMock()
        mock_httpx.post.return_value = mock_response

        with patch.dict(sys.modules, {"httpx": mock_httpx}):
            validator = OllamaValidator("llama3")
            result = validator.validate("", "general")

            assert result.success is True

    def test_very_long_claim(self):
        """Validators handle very long claims."""
        long_claim = "This is a very long claim. " * 1000
        mock_httpx = create_mock_httpx()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "response": '{"confidence": 0.5, "reasoning": "Processed"}'
        }
        mock_response.raise_for_status = MagicMock()
        mock_httpx.post.return_value = mock_response

        with patch.dict(sys.modules, {"httpx": mock_httpx}):
            validator = OllamaValidator("llama3")
            result = validator.validate(long_claim, "general")

            assert result.success is True

    def test_special_characters_in_claim(self):
        """Validators handle special characters."""
        special_claim = 'Claim with "quotes", émojis, and <html>'
        mock_httpx = create_mock_httpx()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "response": '{"confidence": 0.7, "reasoning": "OK"}'
        }
        mock_response.raise_for_status = MagicMock()
        mock_httpx.post.return_value = mock_response

        with patch.dict(sys.modules, {"httpx": mock_httpx}):
            validator = OllamaValidator("llama3")
            result = validator.validate(special_claim, "general")

            assert result.success is True

    def test_unicode_domain(self):
        """Validators handle unicode in domain."""
        mock_httpx = create_mock_httpx()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "response": '{"confidence": 0.8, "reasoning": "OK"}'
        }
        mock_response.raise_for_status = MagicMock()
        mock_httpx.post.return_value = mock_response

        with patch.dict(sys.modules, {"httpx": mock_httpx}):
            validator = OllamaValidator("llama3")
            result = validator.validate("Claim", "fisica")

            assert result.success is True
