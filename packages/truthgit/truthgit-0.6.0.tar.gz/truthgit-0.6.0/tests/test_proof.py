"""
Comprehensive tests for TruthGit Proof module.
Tests cryptographic proof generation and verification.
"""

import base64
import json
import tempfile
from pathlib import Path

import pytest

from truthgit.proof import ProofCertificate, ProofManager, verify_proof_standalone


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def proof_manager(temp_dir):
    """Create a ProofManager with generated keys."""
    manager = ProofManager(temp_dir)
    manager.generate_keypair()
    return manager


@pytest.fixture
def sample_certificate_data():
    """Sample data for creating a certificate."""
    return {
        "claim_hash": "a" * 64,
        "claim_content": "Water boils at 100 degrees Celsius",
        "claim_domain": "physics",
        "verification_hash": "b" * 64,
        "consensus_value": 0.92,
        "consensus_passed": True,
        "validators": ["CLAUDE", "GPT", "GEMINI"],
        "timestamp": "2026-01-13T10:00:00Z",
    }


# =============================================================================
# ProofCertificate Tests
# =============================================================================


class TestProofCertificate:
    """Tests for ProofCertificate dataclass."""

    def test_to_dict_structure(self):
        """to_dict returns correctly structured dictionary."""
        cert = ProofCertificate(
            version="1.0",
            claim_hash="abc123",
            claim_content="Test claim",
            claim_domain="test",
            verification_hash="def456",
            consensus_value=0.85,
            consensus_passed=True,
            validators=["V1", "V2"],
            timestamp="2026-01-13T00:00:00Z",
            signature="sig123",
            public_key="pub456",
            repo_id="repo789",
        )

        result = cert.to_dict()

        assert "version" in result
        assert "claim" in result
        assert "verification" in result
        assert "proof" in result
        assert result["claim"]["hash"] == "abc123"
        assert result["verification"]["consensus"] == 0.85
        assert result["proof"]["signature"] == "sig123"

    def test_to_json_returns_valid_json(self):
        """to_json returns valid JSON string."""
        cert = ProofCertificate(
            version="1.0",
            claim_hash="abc",
            claim_content="Test",
            claim_domain="test",
            verification_hash="def",
            consensus_value=0.9,
            consensus_passed=True,
            validators=["V1"],
            timestamp="2026-01-13T00:00:00Z",
            signature="sig",
            public_key="pub",
        )

        json_str = cert.to_json()
        parsed = json.loads(json_str)

        assert parsed["version"] == "1.0"
        assert parsed["claim"]["content"] == "Test"

    def test_to_compact_returns_base64(self):
        """to_compact returns valid base64 string."""
        cert = ProofCertificate(
            version="1.0",
            claim_hash="abc",
            claim_content="Test",
            claim_domain="test",
            verification_hash="def",
            consensus_value=0.9,
            consensus_passed=True,
            validators=["V1"],
            timestamp="2026-01-13T00:00:00Z",
            signature="sig",
            public_key="pub",
        )

        compact = cert.to_compact()

        # Should be valid base64
        decoded = base64.urlsafe_b64decode(compact.encode())
        parsed = json.loads(decoded.decode())
        assert parsed["version"] == "1.0"

    def test_from_dict_reconstructs_certificate(self):
        """from_dict correctly reconstructs a certificate."""
        original_data = {
            "version": "1.0",
            "claim": {
                "hash": "abc123",
                "content": "Test claim",
                "domain": "test",
            },
            "verification": {
                "hash": "def456",
                "consensus": 0.87,
                "passed": True,
                "validators": ["V1", "V2"],
                "timestamp": "2026-01-13T00:00:00Z",
            },
            "proof": {
                "signature": "sig789",
                "public_key": "pub000",
                "repo_id": "repo111",
            },
        }

        cert = ProofCertificate.from_dict(original_data)

        assert cert.version == "1.0"
        assert cert.claim_hash == "abc123"
        assert cert.consensus_value == 0.87
        assert cert.validators == ["V1", "V2"]

    def test_from_json_parses_json_string(self):
        """from_json correctly parses JSON string."""
        json_str = json.dumps(
            {
                "version": "1.0",
                "claim": {"hash": "a", "content": "C", "domain": "d"},
                "verification": {
                    "hash": "b",
                    "consensus": 0.75,
                    "passed": True,
                    "validators": ["V"],
                    "timestamp": "2026-01-13T00:00:00Z",
                },
                "proof": {"signature": "s", "public_key": "p"},
            }
        )

        cert = ProofCertificate.from_json(json_str)

        assert cert.claim_hash == "a"
        assert cert.consensus_value == 0.75

    def test_from_compact_decodes_base64(self):
        """from_compact correctly decodes base64 certificate."""
        data = {
            "version": "1.0",
            "claim": {"hash": "h", "content": "Compact", "domain": "d"},
            "verification": {
                "hash": "v",
                "consensus": 0.8,
                "passed": True,
                "validators": ["V"],
                "timestamp": "2026-01-13T00:00:00Z",
            },
            "proof": {"signature": "s", "public_key": "p"},
        }
        compact = base64.urlsafe_b64encode(json.dumps(data).encode()).decode()

        cert = ProofCertificate.from_compact(compact)

        assert cert.claim_content == "Compact"
        assert cert.consensus_value == 0.8

    def test_roundtrip_json(self):
        """Certificate survives JSON roundtrip."""
        original = ProofCertificate(
            version="1.0",
            claim_hash="abc",
            claim_content="Roundtrip test",
            claim_domain="test",
            verification_hash="def",
            consensus_value=0.95,
            consensus_passed=True,
            validators=["V1", "V2", "V3"],
            timestamp="2026-01-13T12:00:00Z",
            signature="signature",
            public_key="public_key",
            repo_id="repo_id",
        )

        json_str = original.to_json()
        restored = ProofCertificate.from_json(json_str)

        assert restored.claim_hash == original.claim_hash
        assert restored.claim_content == original.claim_content
        assert restored.consensus_value == original.consensus_value
        assert restored.validators == original.validators

    def test_roundtrip_compact(self):
        """Certificate survives compact roundtrip."""
        original = ProofCertificate(
            version="1.0",
            claim_hash="xyz",
            claim_content="Compact roundtrip",
            claim_domain="test",
            verification_hash="uvw",
            consensus_value=0.88,
            consensus_passed=True,
            validators=["A", "B"],
            timestamp="2026-01-13T15:00:00Z",
            signature="sig",
            public_key="pub",
        )

        compact = original.to_compact()
        restored = ProofCertificate.from_compact(compact)

        assert restored.claim_content == original.claim_content
        assert restored.consensus_value == original.consensus_value


# =============================================================================
# ProofManager Tests
# =============================================================================


class TestProofManager:
    """Tests for ProofManager class."""

    def test_init_sets_repo_path(self, temp_dir):
        """__init__ sets repository path."""
        manager = ProofManager(temp_dir)
        assert manager.repo_path == temp_dir

    def test_keys_exist_false_initially(self, temp_dir):
        """keys_exist is False before generation."""
        manager = ProofManager(temp_dir)
        assert manager.keys_exist is False

    def test_keys_exist_true_after_generation(self, proof_manager):
        """keys_exist is True after key generation."""
        assert proof_manager.keys_exist is True

    def test_generate_keypair_creates_files(self, temp_dir):
        """generate_keypair creates key files."""
        manager = ProofManager(temp_dir)
        private_path, public_path = manager.generate_keypair()

        assert Path(private_path).exists()
        assert Path(public_path).exists()
        assert (temp_dir / "proof.key").exists()
        assert (temp_dir / "proof.pub").exists()

    def test_generate_keypair_raises_if_exists(self, proof_manager):
        """generate_keypair raises if keys exist and force=False."""
        with pytest.raises(FileExistsError):
            proof_manager.generate_keypair(force=False)

    def test_generate_keypair_with_force(self, proof_manager, temp_dir):
        """generate_keypair with force=True regenerates keys."""
        # Get original public key
        original_pub = proof_manager.get_public_key_b64()

        # Regenerate
        proof_manager.generate_keypair(force=True)
        new_pub = proof_manager.get_public_key_b64()

        # Keys should be different
        assert original_pub != new_pub

    def test_load_keys_raises_if_missing(self, temp_dir):
        """load_keys raises if no keys exist."""
        manager = ProofManager(temp_dir)

        with pytest.raises(FileNotFoundError):
            manager.load_keys()

    def test_load_keys_loads_existing(self, proof_manager, temp_dir):
        """load_keys loads existing keys."""
        # Get public key before
        pub_before = proof_manager.get_public_key_b64()

        # Create new manager and load
        new_manager = ProofManager(temp_dir)
        new_manager.load_keys()
        pub_after = new_manager.get_public_key_b64()

        assert pub_before == pub_after

    def test_get_public_key_b64_returns_base64(self, proof_manager):
        """get_public_key_b64 returns valid base64 string."""
        pub_key = proof_manager.get_public_key_b64()

        # Should be valid base64
        decoded = base64.urlsafe_b64decode(pub_key.encode())
        assert len(decoded) == 32  # Ed25519 public key is 32 bytes

    def test_get_repo_id_returns_hex_string(self, proof_manager):
        """get_repo_id returns short hex identifier."""
        repo_id = proof_manager.get_repo_id()

        assert len(repo_id) == 16
        # Should be hexadecimal
        int(repo_id, 16)

    def test_sign_returns_base64_signature(self, proof_manager):
        """sign returns base64 encoded signature."""
        data = "Test data to sign"
        signature = proof_manager.sign(data)

        # Should be valid base64
        decoded = base64.urlsafe_b64decode(signature.encode())
        assert len(decoded) == 64  # Ed25519 signature is 64 bytes

    def test_verify_signature_valid(self, proof_manager):
        """verify_signature returns True for valid signature."""
        data = "Data to verify"
        signature = proof_manager.sign(data)
        public_key = proof_manager.get_public_key_b64()

        result = proof_manager.verify_signature(data, signature, public_key)

        assert result is True

    def test_verify_signature_invalid_data(self, proof_manager):
        """verify_signature returns False for tampered data."""
        data = "Original data"
        signature = proof_manager.sign(data)
        public_key = proof_manager.get_public_key_b64()

        result = proof_manager.verify_signature("Tampered data", signature, public_key)

        assert result is False

    def test_verify_signature_invalid_signature(self, proof_manager):
        """verify_signature returns False for invalid signature."""
        data = "Test data"
        public_key = proof_manager.get_public_key_b64()
        bad_signature = base64.urlsafe_b64encode(b"x" * 64).decode()

        result = proof_manager.verify_signature(data, bad_signature, public_key)

        assert result is False


# =============================================================================
# Proof Creation and Verification Tests
# =============================================================================


class TestProofCreationAndVerification:
    """Tests for proof creation and verification workflow."""

    def test_create_proof_returns_certificate(self, proof_manager, sample_certificate_data):
        """create_proof returns a ProofCertificate."""
        cert = proof_manager.create_proof(**sample_certificate_data)

        assert isinstance(cert, ProofCertificate)
        assert cert.claim_hash == sample_certificate_data["claim_hash"]
        assert cert.claim_content == sample_certificate_data["claim_content"]
        assert cert.consensus_value == sample_certificate_data["consensus_value"]

    def test_create_proof_includes_signature(self, proof_manager, sample_certificate_data):
        """create_proof includes a valid signature."""
        cert = proof_manager.create_proof(**sample_certificate_data)

        assert cert.signature is not None
        assert len(cert.signature) > 0
        # Should be valid base64
        base64.urlsafe_b64decode(cert.signature.encode())

    def test_create_proof_includes_public_key(self, proof_manager, sample_certificate_data):
        """create_proof includes the public key."""
        cert = proof_manager.create_proof(**sample_certificate_data)

        assert cert.public_key == proof_manager.get_public_key_b64()

    def test_create_proof_includes_repo_id(self, proof_manager, sample_certificate_data):
        """create_proof includes the repository ID."""
        cert = proof_manager.create_proof(**sample_certificate_data)

        assert cert.repo_id == proof_manager.get_repo_id()

    def test_create_proof_uses_provided_timestamp(self, proof_manager, sample_certificate_data):
        """create_proof uses provided timestamp."""
        cert = proof_manager.create_proof(**sample_certificate_data)

        assert cert.timestamp == sample_certificate_data["timestamp"]

    def test_create_proof_generates_timestamp_if_none(self, proof_manager):
        """create_proof generates timestamp if not provided."""
        cert = proof_manager.create_proof(
            claim_hash="h",
            claim_content="c",
            claim_domain="d",
            verification_hash="v",
            consensus_value=0.9,
            consensus_passed=True,
            validators=["V"],
        )

        assert cert.timestamp is not None
        assert cert.timestamp.endswith("Z")

    def test_verify_proof_valid(self, proof_manager, sample_certificate_data):
        """verify_proof returns True for valid certificate."""
        cert = proof_manager.create_proof(**sample_certificate_data)

        is_valid, message = proof_manager.verify_proof(cert)

        assert is_valid is True
        assert "Valid proof" in message

    def test_verify_proof_includes_consensus_info(self, proof_manager, sample_certificate_data):
        """verify_proof message includes consensus information."""
        cert = proof_manager.create_proof(**sample_certificate_data)

        is_valid, message = proof_manager.verify_proof(cert)

        assert "92%" in message
        assert "3 validators" in message

    def test_verify_proof_failed_consensus(self, proof_manager):
        """verify_proof handles failed consensus."""
        cert = proof_manager.create_proof(
            claim_hash="h",
            claim_content="c",
            claim_domain="d",
            verification_hash="v",
            consensus_value=0.4,
            consensus_passed=False,
            validators=["V"],
            timestamp="2026-01-13T00:00:00Z",
        )

        is_valid, message = proof_manager.verify_proof(cert)

        assert is_valid is True  # Signature is valid
        assert "did NOT pass" in message

    def test_verify_proof_invalid_signature(self, proof_manager, sample_certificate_data):
        """verify_proof returns False for tampered certificate."""
        cert = proof_manager.create_proof(**sample_certificate_data)

        # Tamper with the certificate
        tampered_cert = ProofCertificate(
            version=cert.version,
            claim_hash=cert.claim_hash,
            claim_content="TAMPERED CONTENT",  # Changed
            claim_domain=cert.claim_domain,
            verification_hash=cert.verification_hash,
            consensus_value=cert.consensus_value,
            consensus_passed=cert.consensus_passed,
            validators=cert.validators,
            timestamp=cert.timestamp,
            signature=cert.signature,  # Original signature
            public_key=cert.public_key,
        )

        is_valid, message = proof_manager.verify_proof(tampered_cert)

        assert is_valid is False
        assert "Invalid signature" in message


# =============================================================================
# Standalone Verification Tests
# =============================================================================


class TestStandaloneVerification:
    """Tests for verify_proof_standalone function."""

    def test_verify_standalone_with_dict(self, proof_manager, sample_certificate_data):
        """verify_proof_standalone works with dict input."""
        cert = proof_manager.create_proof(**sample_certificate_data)
        cert_dict = cert.to_dict()

        is_valid, message, parsed_cert = verify_proof_standalone(cert_dict)

        assert is_valid is True
        assert parsed_cert is not None
        assert parsed_cert.claim_hash == cert.claim_hash

    def test_verify_standalone_with_json(self, proof_manager, sample_certificate_data):
        """verify_proof_standalone works with JSON string."""
        cert = proof_manager.create_proof(**sample_certificate_data)
        json_str = cert.to_json()

        is_valid, message, parsed_cert = verify_proof_standalone(json_str)

        assert is_valid is True
        assert parsed_cert.claim_content == sample_certificate_data["claim_content"]

    def test_verify_standalone_with_compact(self, proof_manager, sample_certificate_data):
        """verify_proof_standalone works with compact base64."""
        cert = proof_manager.create_proof(**sample_certificate_data)
        compact = cert.to_compact()

        is_valid, message, parsed_cert = verify_proof_standalone(compact)

        assert is_valid is True
        assert parsed_cert.consensus_value == sample_certificate_data["consensus_value"]

    def test_verify_standalone_invalid_json(self):
        """verify_proof_standalone handles invalid JSON."""
        is_valid, message, cert = verify_proof_standalone("not valid json")

        assert is_valid is False
        assert "Failed to parse" in message
        assert cert is None

    def test_verify_standalone_invalid_base64(self):
        """verify_proof_standalone handles invalid base64."""
        is_valid, message, cert = verify_proof_standalone("!!!not-base64!!!")

        assert is_valid is False
        assert "Failed to parse" in message
        assert cert is None

    def test_verify_standalone_missing_fields(self):
        """verify_proof_standalone handles missing fields."""
        incomplete = json.dumps({"version": "1.0"})

        is_valid, message, cert = verify_proof_standalone(incomplete)

        assert is_valid is False
        assert cert is None


# =============================================================================
# Edge Cases
# =============================================================================


class TestEdgeCases:
    """Edge case tests."""

    def test_unicode_claim_content(self, proof_manager):
        """Proof handles unicode claim content."""
        cert = proof_manager.create_proof(
            claim_hash="h",
            claim_content="Cafe con leche es delicioso",
            claim_domain="food",
            verification_hash="v",
            consensus_value=0.9,
            consensus_passed=True,
            validators=["V"],
            timestamp="2026-01-13T00:00:00Z",
        )

        is_valid, _ = proof_manager.verify_proof(cert)

        assert is_valid is True
        assert cert.claim_content == "Cafe con leche es delicioso"

    def test_empty_validators_list(self, proof_manager):
        """Proof handles empty validators list."""
        cert = proof_manager.create_proof(
            claim_hash="h",
            claim_content="c",
            claim_domain="d",
            verification_hash="v",
            consensus_value=0.0,
            consensus_passed=False,
            validators=[],
            timestamp="2026-01-13T00:00:00Z",
        )

        is_valid, message = proof_manager.verify_proof(cert)

        assert is_valid is True
        assert "did NOT pass" in message

    def test_very_long_claim_content(self, proof_manager):
        """Proof handles very long claim content."""
        long_content = "This is a very long claim. " * 1000
        cert = proof_manager.create_proof(
            claim_hash="h",
            claim_content=long_content,
            claim_domain="d",
            verification_hash="v",
            consensus_value=0.9,
            consensus_passed=True,
            validators=["V"],
            timestamp="2026-01-13T00:00:00Z",
        )

        is_valid, _ = proof_manager.verify_proof(cert)

        assert is_valid is True
        assert cert.claim_content == long_content

    def test_many_validators(self, proof_manager):
        """Proof handles many validators."""
        validators = [f"VALIDATOR_{i}" for i in range(100)]
        cert = proof_manager.create_proof(
            claim_hash="h",
            claim_content="c",
            claim_domain="d",
            verification_hash="v",
            consensus_value=0.95,
            consensus_passed=True,
            validators=validators,
            timestamp="2026-01-13T00:00:00Z",
        )

        is_valid, message = proof_manager.verify_proof(cert)

        assert is_valid is True
        assert "100 validators" in message

    def test_special_characters_in_content(self, proof_manager):
        """Proof handles special characters."""
        special_content = 'Claim with "quotes", newlines\n, and <html>'
        cert = proof_manager.create_proof(
            claim_hash="h",
            claim_content=special_content,
            claim_domain="d",
            verification_hash="v",
            consensus_value=0.9,
            consensus_passed=True,
            validators=["V"],
            timestamp="2026-01-13T00:00:00Z",
        )

        is_valid, _ = proof_manager.verify_proof(cert)

        assert is_valid is True

        # Also verify roundtrip
        json_str = cert.to_json()
        restored = ProofCertificate.from_json(json_str)
        assert restored.claim_content == special_content

    def test_consensus_edge_values(self, proof_manager):
        """Proof handles edge consensus values."""
        for value in [0.0, 0.001, 0.5, 0.999, 1.0]:
            cert = proof_manager.create_proof(
                claim_hash="h",
                claim_content="c",
                claim_domain="d",
                verification_hash="v",
                consensus_value=value,
                consensus_passed=value >= 0.66,
                validators=["V"],
                timestamp="2026-01-13T00:00:00Z",
            )

            is_valid, _ = proof_manager.verify_proof(cert)
            assert is_valid is True
            assert cert.consensus_value == value
