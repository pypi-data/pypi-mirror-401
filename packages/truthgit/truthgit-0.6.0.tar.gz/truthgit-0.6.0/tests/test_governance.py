"""
Tests for Governance Layer.

Tests the governance API that transforms TruthGit from a consensus tracker
into a governance layer for autonomous agents.

Components tested:
- RiskProfile thresholds
- PolicyEngine decision logic
- GovernanceResult generation
- AuditObject creation
"""

import pytest

from truthgit.governance import (
    AuditObject,
    GovernanceAction,
    GovernanceRequest,
    GovernanceResult,
    GovernanceStatus,
    PolicyEngine,
    RiskProfile,
    evaluate_governance,
)


# =============================================================================
# RISK PROFILE TESTS
# =============================================================================


class TestRiskProfiles:
    """Test risk profile thresholds and behavior."""

    def test_low_risk_threshold(self):
        """Low risk should have threshold of 0.60."""
        engine = PolicyEngine()
        assert engine.get_threshold(RiskProfile.LOW) == 0.60

    def test_medium_risk_threshold(self):
        """Medium risk should have threshold of 0.75."""
        engine = PolicyEngine()
        assert engine.get_threshold(RiskProfile.MEDIUM) == 0.75

    def test_high_risk_threshold(self):
        """High risk should have threshold of 0.90."""
        engine = PolicyEngine()
        assert engine.get_threshold(RiskProfile.HIGH) == 0.90

    def test_medical_domain_upgrades_low_to_medium(self):
        """Medical domain should upgrade LOW risk to MEDIUM."""
        engine = PolicyEngine()
        effective = engine.get_effective_risk(RiskProfile.LOW, "medical")
        assert effective == RiskProfile.MEDIUM

    def test_financial_domain_upgrades_low_to_medium(self):
        """Financial domain should upgrade LOW risk to MEDIUM."""
        engine = PolicyEngine()
        effective = engine.get_effective_risk(RiskProfile.LOW, "financial")
        assert effective == RiskProfile.MEDIUM

    def test_general_domain_preserves_risk(self):
        """General domain should preserve original risk profile."""
        engine = PolicyEngine()
        effective = engine.get_effective_risk(RiskProfile.LOW, "general")
        assert effective == RiskProfile.LOW


# =============================================================================
# POLICY ENGINE TESTS
# =============================================================================


class TestPolicyEngine:
    """Test policy engine decision logic."""

    def test_high_confidence_low_risk_proceeds(self):
        """High confidence with low risk should proceed."""
        request = GovernanceRequest(
            claim="Water boils at 100°C at sea level",
            domain="physics",
            risk_profile=RiskProfile.LOW,
        )
        validator_results = {
            "claude": (0.95, "Scientifically established fact"),
            "gpt": (0.92, "Well-documented physical property"),
        }

        engine = PolicyEngine()
        result, audit = engine.evaluate(request, validator_results)

        assert result.status == GovernanceStatus.PASSED
        assert result.action == GovernanceAction.PROCEED
        assert result.confidence >= 0.90

    def test_high_confidence_high_risk_proceeds(self):
        """High confidence with high risk should proceed."""
        request = GovernanceRequest(
            claim="Aspirin is an anti-inflammatory",
            domain="medical",
            risk_profile=RiskProfile.HIGH,
        )
        validator_results = {
            "claude": (0.98, "Well-established pharmacological property"),
            "gpt": (0.96, "Documented medical fact"),
            "gemini": (0.95, "Standard medical knowledge"),
        }

        engine = PolicyEngine()
        result, audit = engine.evaluate(request, validator_results)

        assert result.status == GovernanceStatus.PASSED
        assert result.action == GovernanceAction.PROCEED

    def test_low_confidence_high_risk_aborts(self):
        """Low confidence with high risk should abort."""
        request = GovernanceRequest(
            claim="This treatment cures disease X",
            domain="medical",
            risk_profile=RiskProfile.HIGH,
        )
        validator_results = {
            "claude": (0.65, "Limited evidence"),
            "gpt": (0.60, "Needs more studies"),
        }

        engine = PolicyEngine()
        result, audit = engine.evaluate(request, validator_results)

        # Should abort due to low confidence in high-risk medical domain
        assert result.action in [GovernanceAction.ABORT, GovernanceAction.ESCALATE]

    def test_low_confidence_low_risk_proceeds(self):
        """Low confidence with low risk can still proceed."""
        request = GovernanceRequest(
            claim="This movie is entertaining",
            domain="general",
            risk_profile=RiskProfile.LOW,
        )
        validator_results = {
            "claude": (0.65, "Subjective assessment"),
            "gpt": (0.70, "Matter of opinion"),
        }

        engine = PolicyEngine()
        result, audit = engine.evaluate(request, validator_results)

        # Low risk allows proceeding with moderate confidence
        assert result.confidence >= 0.60
        assert result.action == GovernanceAction.PROCEED

    def test_philosophical_claim_triggers_mystery(self):
        """Philosophical claims should trigger MYSTERY status."""
        request = GovernanceRequest(
            claim="Free will exists",
            domain="philosophy",
            risk_profile=RiskProfile.MEDIUM,
        )
        validator_results = {
            "claude": (0.55, "Compatibilism suggests yes"),
            "gpt": (0.50, "Hard determinism suggests no"),
        }

        engine = PolicyEngine()
        result, audit = engine.evaluate(request, validator_results)

        # Philosophical disagreement should be preserved
        assert result.status == GovernanceStatus.MYSTERY
        assert result.action == GovernanceAction.ABORT

    def test_unfalsifiable_claim_triggers_gap(self):
        """Unfalsifiable claims should trigger GAP status."""
        request = GovernanceRequest(
            claim="Everything happens for a reason",
            domain="philosophy",
            risk_profile=RiskProfile.LOW,
        )
        validator_results = {
            "claude": (0.40, "Cannot be tested empirically"),
            "gpt": (0.35, "Unfalsifiable statement"),
        }

        engine = PolicyEngine()
        result, audit = engine.evaluate(request, validator_results)

        # Should escalate for human judgment
        assert result.status == GovernanceStatus.GAP
        assert result.action == GovernanceAction.ESCALATE


# =============================================================================
# AUDIT OBJECT TESTS
# =============================================================================


class TestAuditObject:
    """Test audit object creation and integrity."""

    def test_audit_object_created(self):
        """Audit object should be created for every decision."""
        request = GovernanceRequest(
            claim="Test claim",
            domain="general",
            risk_profile=RiskProfile.MEDIUM,
        )
        validator_results = {
            "claude": (0.85, "Reasoning A"),
            "gpt": (0.80, "Reasoning B"),
        }

        engine = PolicyEngine()
        result, audit = engine.evaluate(request, validator_results)

        assert audit is not None
        assert audit.id.startswith("audit_")
        assert audit.claim == "Test claim"
        assert audit.domain == "general"
        assert audit.risk_profile == RiskProfile.MEDIUM

    def test_audit_object_has_validators(self):
        """Audit object should include all validator records."""
        request = GovernanceRequest(
            claim="Test claim",
            domain="general",
            risk_profile=RiskProfile.MEDIUM,
        )
        validator_results = {
            "claude": (0.85, "Reasoning A"),
            "gpt": (0.80, "Reasoning B"),
        }

        engine = PolicyEngine()
        result, audit = engine.evaluate(request, validator_results)

        assert len(audit.validators) == 2
        validator_names = [v.name for v in audit.validators]
        assert "claude" in validator_names
        assert "gpt" in validator_names

    def test_audit_object_has_hash(self):
        """Audit object should have cryptographic hash."""
        request = GovernanceRequest(
            claim="Test claim",
            domain="general",
            risk_profile=RiskProfile.MEDIUM,
        )
        validator_results = {
            "claude": (0.85, "Reasoning A"),
        }

        engine = PolicyEngine()
        result, audit = engine.evaluate(request, validator_results)

        assert audit.hash is not None
        assert audit.hash.startswith("sha256:")

    def test_audit_object_serializes_to_json(self):
        """Audit object should serialize to valid JSON."""
        request = GovernanceRequest(
            claim="Test claim",
            domain="general",
            risk_profile=RiskProfile.MEDIUM,
        )
        validator_results = {
            "claude": (0.85, "Reasoning A"),
        }

        engine = PolicyEngine()
        result, audit = engine.evaluate(request, validator_results)

        json_str = audit.to_json()
        assert isinstance(json_str, str)
        assert "Test claim" in json_str
        assert "sha256:" in json_str

    def test_audit_history_links_parent_hash(self):
        """Sequential audits should link via parent hash."""
        engine = PolicyEngine()

        # First evaluation
        request1 = GovernanceRequest(claim="First claim", domain="general")
        result1, audit1 = engine.evaluate(
            request1, {"claude": (0.85, "Reasoning")}
        )

        # Second evaluation
        request2 = GovernanceRequest(claim="Second claim", domain="general")
        result2, audit2 = engine.evaluate(
            request2, {"claude": (0.90, "Reasoning")}
        )

        assert audit1.parent_hash is None
        assert audit2.parent_hash == audit1.hash


# =============================================================================
# CONVENIENCE FUNCTION TESTS
# =============================================================================


class TestEvaluateGovernance:
    """Test the convenience function."""

    def test_evaluate_governance_returns_result(self):
        """evaluate_governance should return GovernanceResult."""
        result = evaluate_governance(
            claim="The Earth is round",
            validator_results={
                "claude": (0.98, "Scientific consensus"),
                "gpt": (0.97, "Established fact"),
            },
            domain="science",
            risk_profile="low",
        )

        assert isinstance(result, GovernanceResult)
        assert result.status == GovernanceStatus.PASSED
        assert result.action == GovernanceAction.PROCEED

    def test_evaluate_governance_with_high_risk(self):
        """evaluate_governance should respect risk profile."""
        result = evaluate_governance(
            claim="Treatment X is effective",
            validator_results={
                "claude": (0.70, "Some evidence"),
                "gpt": (0.65, "Limited data"),
            },
            domain="medical",
            risk_profile="high",
        )

        # Medical domain with high risk and low confidence
        assert result.action in [GovernanceAction.ABORT, GovernanceAction.ESCALATE]


# =============================================================================
# EDGE CASE TESTS
# =============================================================================


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_validator_results(self):
        """Should handle empty validator results gracefully."""
        request = GovernanceRequest(
            claim="Test claim",
            domain="general",
            risk_profile=RiskProfile.MEDIUM,
        )

        engine = PolicyEngine()
        result, audit = engine.evaluate(request, {})

        # Empty results should not proceed
        assert result.action != GovernanceAction.PROCEED

    def test_single_validator(self):
        """Should work with single validator."""
        request = GovernanceRequest(
            claim="Test claim",
            domain="general",
            risk_profile=RiskProfile.LOW,
        )
        validator_results = {
            "claude": (0.85, "Single validator reasoning"),
        }

        engine = PolicyEngine()
        result, audit = engine.evaluate(request, validator_results)

        assert result is not None
        assert len(audit.validators) == 1

    def test_confidence_at_exact_threshold(self):
        """Confidence exactly at threshold should pass."""
        request = GovernanceRequest(
            claim="Test claim",
            domain="general",
            risk_profile=RiskProfile.MEDIUM,  # threshold = 0.75
        )
        validator_results = {
            "claude": (0.75, "Exactly at threshold"),
            "gpt": (0.75, "Exactly at threshold"),
        }

        engine = PolicyEngine()
        result, audit = engine.evaluate(request, validator_results)

        # At threshold should pass
        assert result.status == GovernanceStatus.PASSED
        assert result.action == GovernanceAction.PROCEED

    def test_result_to_dict(self):
        """GovernanceResult should convert to dict."""
        result = GovernanceResult(
            status=GovernanceStatus.PASSED,
            action=GovernanceAction.PROCEED,
            confidence=0.90,
            reason="Test reason",
            audit_ref="audit_123",
            ontological_type=None,
        )

        d = result.to_dict()
        assert d["status"] == "PASSED"
        assert d["action"] == "proceed"
        assert d["confidence"] == 0.90
        assert d["audit_ref"] == "audit_123"


# =============================================================================
# INTEGRATION TESTS
# =============================================================================


class TestIntegration:
    """Integration tests with real scenarios."""

    def test_medical_high_risk_scenario(self):
        """Medical claim with high risk should be strict."""
        result = evaluate_governance(
            claim="This drug treats cancer",
            validator_results={
                "claude": (0.75, "Some clinical evidence"),
                "gpt": (0.70, "Limited trials"),
                "gemini": (0.72, "Promising but inconclusive"),
            },
            domain="medical",
            risk_profile="high",
        )

        # High risk medical claim with ~72% confidence should not proceed
        assert result.action in [GovernanceAction.ABORT, GovernanceAction.ESCALATE]
        assert "medical" in result.reason.lower() or "risk" in result.reason.lower()

    def test_casual_claim_low_risk_scenario(self):
        """Casual claim with low risk should be permissive."""
        result = evaluate_governance(
            claim="Coffee tastes good",
            validator_results={
                "claude": (0.65, "Subjective but common opinion"),
                "gpt": (0.68, "Popular preference"),
            },
            domain="general",
            risk_profile="low",
        )

        # Low risk general claim with moderate confidence can proceed
        assert result.status == GovernanceStatus.PASSED
        assert result.action == GovernanceAction.PROCEED

    def test_financial_advice_scenario(self):
        """Financial advice should be treated carefully."""
        result = evaluate_governance(
            claim="Stock X will increase in value",
            validator_results={
                "claude": (0.55, "Cannot predict markets"),
                "gpt": (0.50, "Speculative at best"),
            },
            domain="financial",
            risk_profile="low",  # Will be upgraded to MEDIUM
        )

        # Financial domain upgrades risk, low confidence should not proceed
        assert result.action != GovernanceAction.PROCEED
