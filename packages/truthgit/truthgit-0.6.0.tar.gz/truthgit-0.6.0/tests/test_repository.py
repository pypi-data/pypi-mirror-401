"""
Comprehensive tests for TruthGit TruthRepository.
Tests all repository operations with temporary directories.
"""

import json
import tempfile
import zlib
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from truthgit.objects import (
    Axiom,
    AxiomType,
    Claim,
    ClaimCategory,
    Context,
    ObjectType,
    Source,
    Verification,
)
from truthgit.repository import TruthRepository


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def repo(temp_dir):
    """Create an initialized repository."""
    repo = TruthRepository(str(temp_dir / ".truth"))
    repo.init()
    return repo


@pytest.fixture
def uninitialized_repo(temp_dir):
    """Create an uninitialized repository."""
    return TruthRepository(str(temp_dir / ".truth"))


# =============================================================================
# Initialization Tests
# =============================================================================


class TestRepositoryInit:
    """Tests for repository initialization."""

    def test_init_creates_directory_structure(self, temp_dir):
        """init creates required directory structure."""
        repo = TruthRepository(str(temp_dir / ".truth"))
        repo.init()

        assert repo.root.exists()
        assert repo.objects_dir.exists()
        assert (repo.objects_dir / "ax").exists()
        assert (repo.objects_dir / "cl").exists()
        assert (repo.objects_dir / "ct").exists()
        assert (repo.objects_dir / "vf").exists()
        assert repo.refs_dir.exists()
        assert (repo.refs_dir / "perspectives").exists()
        assert (repo.refs_dir / "consensus").exists()
        assert (repo.refs_dir / "anchors").exists()

    def test_init_creates_head_file(self, temp_dir):
        """init creates HEAD file with default ref."""
        repo = TruthRepository(str(temp_dir / ".truth"))
        repo.init()

        assert repo.head_file.exists()
        content = repo.head_file.read_text()
        assert content.startswith("ref: ")

    def test_init_creates_config_file(self, temp_dir):
        """init creates config file with default settings."""
        repo = TruthRepository(str(temp_dir / ".truth"))
        repo.init()

        assert repo.config_file.exists()
        config = json.loads(repo.config_file.read_text())
        assert "version" in config
        assert "consensus_threshold" in config
        assert config["consensus_threshold"] == 0.66

    def test_init_creates_index_file(self, temp_dir):
        """init creates empty index file."""
        repo = TruthRepository(str(temp_dir / ".truth"))
        repo.init()

        assert repo.index_file.exists()
        index = json.loads(repo.index_file.read_text())
        assert index["staged"] == []

    def test_init_raises_if_exists_without_force(self, repo):
        """init raises error if repo exists and force=False."""
        with pytest.raises(FileExistsError):
            repo.init(force=False)

    def test_init_with_force_recreates_repo(self, repo, temp_dir):
        """init with force=True recreates repository."""
        # Store something first
        claim = Claim(
            content="Test claim",
            confidence=0.8,
            category=ClaimCategory.FACTUAL,
            domain="test",
        )
        repo.store(claim)

        # Reinit with force
        repo.init(force=True)

        # Should be empty now
        assert repo.is_initialized()
        assert repo.count_objects()[ObjectType.CLAIM.value] == 0

    def test_is_initialized_true_after_init(self, repo):
        """is_initialized returns True after init."""
        assert repo.is_initialized() is True

    def test_is_initialized_false_before_init(self, uninitialized_repo):
        """is_initialized returns False before init."""
        assert uninitialized_repo.is_initialized() is False


# =============================================================================
# Object Storage Tests
# =============================================================================


class TestObjectStorage:
    """Tests for object storage operations."""

    def test_store_claim(self, repo):
        """store saves a Claim object."""
        claim = Claim(
            content="Python was created by Guido",
            confidence=0.9,
            category=ClaimCategory.FACTUAL,
            domain="programming",
        )

        obj_hash = repo.store(claim)

        assert obj_hash is not None
        assert len(obj_hash) == 64  # SHA-256

    def test_load_claim(self, repo):
        """load retrieves a stored Claim."""
        claim = Claim(
            content="Test claim",
            confidence=0.8,
            category=ClaimCategory.FACTUAL,
            domain="test",
        )
        obj_hash = repo.store(claim)

        loaded = repo.load(ObjectType.CLAIM, obj_hash)

        assert loaded is not None
        assert loaded.content == claim.content
        assert loaded.confidence == claim.confidence

    def test_load_nonexistent_returns_none(self, repo):
        """load returns None for nonexistent object."""
        result = repo.load(ObjectType.CLAIM, "nonexistent" * 8)
        assert result is None

    def test_exists_returns_true_for_stored(self, repo):
        """exists returns True for stored objects."""
        claim = Claim(
            content="Test", confidence=0.5, category=ClaimCategory.FACTUAL, domain="test"
        )
        obj_hash = repo.store(claim)

        assert repo.exists(ObjectType.CLAIM, obj_hash) is True

    def test_exists_returns_false_for_missing(self, repo):
        """exists returns False for missing objects."""
        assert repo.exists(ObjectType.CLAIM, "missing" * 8) is False

    def test_delete_removes_object(self, repo):
        """delete removes an object from storage."""
        claim = Claim(
            content="To delete", confidence=0.5, category=ClaimCategory.FACTUAL, domain="test"
        )
        obj_hash = repo.store(claim)

        result = repo.delete(ObjectType.CLAIM, obj_hash)

        assert result is True
        assert repo.exists(ObjectType.CLAIM, obj_hash) is False

    def test_delete_nonexistent_returns_false(self, repo):
        """delete returns False for nonexistent object."""
        result = repo.delete(ObjectType.CLAIM, "nonexistent" * 8)
        assert result is False

    def test_store_compresses_data(self, repo):
        """store compresses object data with zlib."""
        claim = Claim(
            content="Test compression with a longer string " * 10,
            confidence=0.5,
            category=ClaimCategory.FACTUAL,
            domain="test",
        )
        obj_hash = repo.store(claim)

        # Read raw bytes
        obj_path = repo._object_path(ObjectType.CLAIM, obj_hash)
        compressed = obj_path.read_bytes()

        # Verify it's compressed
        decompressed = zlib.decompress(compressed)
        assert len(compressed) < len(decompressed)

    def test_store_axiom(self, repo):
        """store saves an Axiom object."""
        axiom = Axiom(
            content="All bachelors are unmarried",
            axiom_type=AxiomType.LINGUISTIC_DEFINITION,
            domain="philosophy",
            authority_source="Logical definition",
        )

        obj_hash = repo.store(axiom)
        loaded = repo.load(ObjectType.AXIOM, obj_hash)

        assert loaded is not None
        assert loaded.content == axiom.content


# =============================================================================
# Staging Tests
# =============================================================================


class TestStaging:
    """Tests for staging area operations."""

    def test_stage_adds_to_index(self, repo):
        """stage adds object to index."""
        claim = Claim(
            content="Staged claim",
            confidence=0.7,
            category=ClaimCategory.FACTUAL,
            domain="test",
        )

        obj_hash = repo.stage(claim)
        staged = repo.get_staged()

        assert len(staged) == 1
        assert staged[0]["hash"] == obj_hash
        assert staged[0]["type"] == ObjectType.CLAIM.value

    def test_stage_prevents_duplicates(self, repo):
        """stage does not add same object twice."""
        claim = Claim(
            content="Duplicate test",
            confidence=0.6,
            category=ClaimCategory.FACTUAL,
            domain="test",
        )

        repo.stage(claim)
        repo.stage(claim)  # Stage again
        staged = repo.get_staged()

        assert len(staged) == 1

    def test_unstage_removes_from_index(self, repo):
        """unstage removes object from index."""
        claim = Claim(
            content="To unstage",
            confidence=0.5,
            category=ClaimCategory.FACTUAL,
            domain="test",
        )
        obj_hash = repo.stage(claim)

        result = repo.unstage(obj_hash)

        assert result is True
        assert len(repo.get_staged()) == 0

    def test_unstage_nonexistent_returns_false(self, repo):
        """unstage returns False for non-staged object."""
        result = repo.unstage("nonexistent" * 8)
        assert result is False

    def test_get_staged_returns_empty_initially(self, repo):
        """get_staged returns empty list initially."""
        staged = repo.get_staged()
        assert staged == []

    def test_clear_staging_removes_all(self, repo):
        """clear_staging removes all staged items."""
        claim1 = Claim(
            content="Claim 1", confidence=0.5, category=ClaimCategory.FACTUAL, domain="test"
        )
        claim2 = Claim(
            content="Claim 2", confidence=0.6, category=ClaimCategory.FACTUAL, domain="test"
        )
        repo.stage(claim1)
        repo.stage(claim2)

        repo.clear_staging()

        assert len(repo.get_staged()) == 0


# =============================================================================
# Reference Tests
# =============================================================================


class TestReferences:
    """Tests for reference operations."""

    def test_set_ref_creates_file(self, repo):
        """set_ref creates reference file."""
        test_hash = "a" * 64
        repo.set_ref("test/ref", test_hash)

        ref_path = repo.refs_dir / "test" / "ref"
        assert ref_path.exists()
        assert ref_path.read_text().strip() == test_hash

    def test_get_ref_returns_hash(self, repo):
        """get_ref returns stored hash."""
        test_hash = "b" * 64
        repo.set_ref("myref", test_hash)

        result = repo.get_ref("myref")

        assert result == test_hash

    def test_get_ref_nonexistent_returns_none(self, repo):
        """get_ref returns None for nonexistent ref."""
        result = repo.get_ref("nonexistent/ref")
        assert result is None

    def test_delete_ref_removes_file(self, repo):
        """delete_ref removes reference file."""
        test_hash = "c" * 64
        repo.set_ref("to_delete", test_hash)

        result = repo.delete_ref("to_delete")

        assert result is True
        assert repo.get_ref("to_delete") is None

    def test_delete_ref_nonexistent_returns_false(self, repo):
        """delete_ref returns False for nonexistent ref."""
        result = repo.delete_ref("nonexistent")
        assert result is False

    def test_list_refs_returns_all(self, repo):
        """list_refs returns all references."""
        repo.set_ref("ref1", "a" * 64)
        repo.set_ref("ref2", "b" * 64)
        repo.set_ref("nested/ref3", "c" * 64)

        refs = repo.list_refs()

        # Convert to dict for easier checking
        refs_dict = dict(refs)
        assert "ref1" in refs_dict
        assert "ref2" in refs_dict
        assert "nested/ref3" in refs_dict

    def test_list_refs_with_prefix(self, repo):
        """list_refs filters by prefix."""
        repo.set_ref("perspectives/CLAUDE", "a" * 64)
        repo.set_ref("perspectives/GPT", "b" * 64)
        repo.set_ref("consensus/main", "c" * 64)

        refs = repo.list_refs("perspectives")

        assert len(refs) == 2
        names = [r[0] for r in refs]
        assert all("perspectives" in name for name in names)


# =============================================================================
# HEAD Tests
# =============================================================================


class TestHead:
    """Tests for HEAD operations."""

    def test_get_head_initial(self, repo):
        """get_head returns None when no commits."""
        result = repo.get_head()
        # HEAD points to consensus/main which is empty
        assert result is None

    def test_set_head_symbolic(self, repo):
        """set_head creates symbolic reference."""
        repo.set_ref("test/branch", "d" * 64)
        repo.set_head("test/branch", symbolic=True)

        content = repo.head_file.read_text()
        assert content.startswith("ref: ")

        # get_head should follow the ref
        assert repo.get_head() == "d" * 64

    def test_set_head_direct(self, repo):
        """set_head with symbolic=False sets direct hash."""
        test_hash = "e" * 64
        repo.set_head(test_hash, symbolic=False)

        content = repo.head_file.read_text().strip()
        assert content == test_hash
        assert repo.get_head() == test_hash


# =============================================================================
# High-Level Operation Tests
# =============================================================================


class TestHighLevelOps:
    """Tests for high-level operations (claim, axiom, verify)."""

    def test_claim_creates_and_stages(self, repo):
        """claim method creates and stages a claim."""
        claim = repo.claim(
            content="Test claim",
            sources=[{"url": "https://example.com", "title": "Example"}],
            confidence=0.9,
            domain="test",
        )

        assert claim is not None
        staged = repo.get_staged()
        assert len(staged) == 1
        assert staged[0]["type"] == ObjectType.CLAIM.value

    def test_claim_with_sources(self, repo):
        """claim stores source information."""
        claim = repo.claim(
            content="Python is popular",
            sources=[
                {"url": "https://python.org", "title": "Python.org", "reliability": 0.95}
            ],
            confidence=0.8,
            domain="programming",
        )

        assert len(claim.sources) == 1
        assert claim.sources[0].url == "https://python.org"

    def test_axiom_creates_and_stages(self, repo):
        """axiom method creates and stages an axiom."""
        axiom = repo.axiom(
            content="A equals A",
            axiom_type="logical_tautology",
            domain="logic",
            authority_source="Law of identity",
        )

        assert axiom is not None
        staged = repo.get_staged()
        assert len(staged) == 1
        assert staged[0]["type"] == ObjectType.AXIOM.value

    def test_verify_returns_none_if_nothing_staged(self, repo):
        """verify returns None when nothing is staged."""
        result = repo.verify(
            verifier_results={"CLAUDE": (0.9, "Test")},
            trigger="test",
        )

        assert result is None

    def test_verify_creates_verification(self, repo):
        """verify creates a Verification object."""
        repo.claim(content="Test claim", confidence=0.8, domain="test")

        verification = repo.verify(
            verifier_results={
                "CLAUDE": (0.9, "Verified"),
                "GPT": (0.85, "Also verified"),
            },
            trigger="test",
            use_ontological=False,
        )

        assert verification is not None
        assert verification.consensus.passed is True

    def test_verify_clears_staging(self, repo):
        """verify clears staging area after success."""
        repo.claim(content="To verify", confidence=0.7, domain="test")

        repo.verify(
            verifier_results={"CLAUDE": (0.9, "OK")},
            trigger="test",
            use_ontological=False,
        )

        assert len(repo.get_staged()) == 0

    def test_verify_updates_consensus_ref(self, repo):
        """verify updates consensus/main reference."""
        repo.claim(content="Consensus test", confidence=0.8, domain="test")

        verification = repo.verify(
            verifier_results={"CLAUDE": (0.9, "OK"), "GPT": (0.85, "OK")},
            trigger="test",
            use_ontological=False,
        )

        consensus_hash = repo.get_ref("consensus/main")
        assert consensus_hash is not None
        assert consensus_hash == verification.hash

    def test_verify_updates_perspective_refs(self, repo):
        """verify updates perspective references for each verifier."""
        repo.claim(content="Perspective test", confidence=0.8, domain="test")

        verification = repo.verify(
            verifier_results={
                "CLAUDE": (0.9, "Verified by Claude"),
                "GPT": (0.85, "Verified by GPT"),
            },
            trigger="test",
            use_ontological=False,
        )

        claude_ref = repo.get_ref("perspectives/CLAUDE")
        gpt_ref = repo.get_ref("perspectives/GPT")

        assert claude_ref == verification.hash
        assert gpt_ref == verification.hash


# =============================================================================
# History and Status Tests
# =============================================================================


class TestHistoryAndStatus:
    """Tests for history and status operations."""

    def test_history_returns_verifications(self, repo):
        """history returns list of verifications."""
        repo.claim(content="First claim", confidence=0.8, domain="test")
        repo.verify(
            verifier_results={"CLAUDE": (0.9, "OK")},
            trigger="test",
            use_ontological=False,
        )

        repo.claim(content="Second claim", confidence=0.7, domain="test")
        repo.verify(
            verifier_results={"CLAUDE": (0.85, "OK")},
            trigger="test",
            use_ontological=False,
        )

        history = repo.history(limit=10)

        assert len(history) == 2

    def test_history_respects_limit(self, repo):
        """history respects limit parameter."""
        for i in range(5):
            repo.claim(content=f"Claim {i}", confidence=0.8, domain="test")
            repo.verify(
                verifier_results={"CLAUDE": (0.9, "OK")},
                trigger="test",
                use_ontological=False,
            )

        history = repo.history(limit=3)

        assert len(history) == 3

    def test_history_empty_initially(self, repo):
        """history returns empty list when no verifications."""
        history = repo.history()
        assert history == []

    def test_status_returns_dict(self, repo):
        """status returns dictionary with expected keys."""
        status = repo.status()

        assert "initialized" in status
        assert "staged_count" in status
        assert "staged" in status
        assert "head" in status
        assert "perspectives" in status
        assert "consensus" in status

    def test_status_reflects_staged_count(self, repo):
        """status reflects number of staged items."""
        repo.claim(content="Staged 1", confidence=0.8, domain="test")
        repo.claim(content="Staged 2", confidence=0.7, domain="test")

        status = repo.status()

        assert status["staged_count"] == 2


# =============================================================================
# Iteration Tests
# =============================================================================


class TestIteration:
    """Tests for object iteration."""

    def test_iter_objects_yields_all(self, repo):
        """iter_objects yields all objects of type."""
        claim1 = Claim(
            content="Claim A", confidence=0.5, category=ClaimCategory.FACTUAL, domain="test"
        )
        claim2 = Claim(
            content="Claim B", confidence=0.6, category=ClaimCategory.FACTUAL, domain="test"
        )
        repo.store(claim1)
        repo.store(claim2)

        claims = list(repo.iter_objects(ObjectType.CLAIM))

        assert len(claims) == 2

    def test_iter_objects_empty_type(self, repo):
        """iter_objects yields nothing for empty type."""
        axioms = list(repo.iter_objects(ObjectType.AXIOM))
        assert axioms == []

    def test_count_objects_returns_dict(self, repo):
        """count_objects returns counts per type."""
        claim = Claim(
            content="Test", confidence=0.5, category=ClaimCategory.FACTUAL, domain="test"
        )
        repo.store(claim)

        counts = repo.count_objects()

        assert counts[ObjectType.CLAIM.value] == 1
        assert counts[ObjectType.AXIOM.value] == 0


# =============================================================================
# Lookup Helper Tests
# =============================================================================


class TestLookupHelpers:
    """Tests for lookup helper methods."""

    def test_get_object_returns_dict(self, repo):
        """get_object returns object as dictionary."""
        claim = Claim(
            content="Lookup test",
            confidence=0.8,
            category=ClaimCategory.FACTUAL,
            domain="test",
        )
        obj_hash = repo.store(claim)

        result = repo.get_object(ObjectType.CLAIM, obj_hash)

        assert result is not None
        assert result["content"] == "Lookup test"
        assert "$hash" in result

    def test_get_object_nonexistent_returns_none(self, repo):
        """get_object returns None for nonexistent object."""
        result = repo.get_object(ObjectType.CLAIM, "x" * 64)
        assert result is None

    def test_get_object_by_prefix_finds_match(self, repo):
        """get_object_by_prefix finds object by hash prefix."""
        claim = Claim(
            content="Prefix test",
            confidence=0.7,
            category=ClaimCategory.FACTUAL,
            domain="test",
        )
        obj_hash = repo.store(claim)
        prefix = obj_hash[:8]

        result = repo.get_object_by_prefix(prefix)

        assert result is not None
        obj_type, obj_data = result
        assert obj_type == ObjectType.CLAIM
        assert obj_data["content"] == "Prefix test"

    def test_get_object_by_prefix_nonexistent_returns_none(self, repo):
        """get_object_by_prefix returns None for no match."""
        result = repo.get_object_by_prefix("zzzzzzz")
        assert result is None

    def test_find_verifications_for_claim(self, repo):
        """find_verifications_for_claim finds related verifications."""
        claim = repo.claim(content="Find me", confidence=0.8, domain="test")
        claim_hash = claim.hash

        repo.verify(
            verifier_results={"CLAUDE": (0.9, "Found")},
            trigger="test",
            use_ontological=False,
        )

        results = repo.find_verifications_for_claim(claim_hash)

        assert len(results) == 1

    def test_find_verifications_for_claim_no_match(self, repo):
        """find_verifications_for_claim returns empty for no match."""
        results = repo.find_verifications_for_claim("nonexistent" * 8)
        assert results == []


# =============================================================================
# Edge Cases
# =============================================================================


class TestEdgeCases:
    """Edge case tests."""

    def test_unicode_content(self, repo):
        """Repository handles unicode content."""
        claim = Claim(
            content="Contenido en espanol con acentos: cafe, nino",
            confidence=0.8,
            category=ClaimCategory.FACTUAL,
            domain="test",
        )
        obj_hash = repo.store(claim)
        loaded = repo.load(ObjectType.CLAIM, obj_hash)

        assert loaded.content == claim.content

    def test_very_long_content(self, repo):
        """Repository handles very long content."""
        long_content = "This is a very long claim. " * 1000
        claim = Claim(
            content=long_content,
            confidence=0.5,
            category=ClaimCategory.FACTUAL,
            domain="test",
        )
        obj_hash = repo.store(claim)
        loaded = repo.load(ObjectType.CLAIM, obj_hash)

        assert loaded.content == long_content

    def test_multiple_verifications_chain(self, repo):
        """Multiple verifications form a chain via parent_hash."""
        # First verification
        repo.claim(content="First", confidence=0.8, domain="test")
        v1 = repo.verify(
            verifier_results={"CLAUDE": (0.9, "OK")},
            trigger="test",
            use_ontological=False,
        )

        # Second verification
        repo.claim(content="Second", confidence=0.8, domain="test")
        v2 = repo.verify(
            verifier_results={"CLAUDE": (0.9, "OK")},
            trigger="test",
            use_ontological=False,
        )

        # v2 should have v1 as parent
        assert v2.parent_hash == v1.hash

    def test_read_config(self, repo):
        """_read_config returns config dictionary."""
        config = repo._read_config()

        assert "version" in config
        assert "consensus_threshold" in config

    def test_read_config_missing_file(self, temp_dir):
        """_read_config returns empty dict for missing file."""
        repo = TruthRepository(str(temp_dir / ".truth"))
        # Don't init - no config file
        repo.root.mkdir(parents=True)

        config = repo._read_config()

        assert config == {}


# =============================================================================
# Integration Tests
# =============================================================================


class TestIntegration:
    """Integration tests for complete workflows."""

    def test_full_verification_workflow(self, repo):
        """Test complete claim -> verify -> history workflow."""
        # Create and stage a claim
        claim = repo.claim(
            content="Python was created by Guido van Rossum",
            sources=[{"url": "https://python.org", "title": "Python"}],
            confidence=0.95,
            domain="programming.history",
        )

        # Verify with multiple validators
        verification = repo.verify(
            verifier_results={
                "CLAUDE": (0.92, "Verified from python.org"),
                "GPT": (0.88, "Cross-referenced with Wikipedia"),
            },
            trigger="test",
            use_ontological=False,
        )

        # Check verification
        assert verification is not None
        assert verification.consensus.passed is True
        assert verification.consensus.value > 0.8

        # Check history
        history = repo.history()
        assert len(history) == 1
        assert history[0].hash == verification.hash

        # Check status
        status = repo.status()
        assert status["staged_count"] == 0
        assert status["consensus"] == verification.hash

    def test_multiple_claims_single_verification(self, repo):
        """Test verifying multiple claims at once."""
        repo.claim(content="Claim 1", confidence=0.8, domain="test")
        repo.claim(content="Claim 2", confidence=0.7, domain="test")
        repo.claim(content="Claim 3", confidence=0.9, domain="test")

        verification = repo.verify(
            verifier_results={"CLAUDE": (0.85, "All verified")},
            trigger="batch",
            use_ontological=False,
        )

        assert verification is not None
        # All claims should be cleared from staging
        assert len(repo.get_staged()) == 0
