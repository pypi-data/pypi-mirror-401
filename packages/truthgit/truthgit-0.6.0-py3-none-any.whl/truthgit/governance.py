"""
TruthGit - Governance Layer

Transforms TruthGit from a consensus tracker into a governance layer
for autonomous agents. Answers: "Should the agent act?" not "Is this
objectively true?"

Core components:
- RiskProfile: low|medium|high thresholds
- PolicyEngine: status + risk → action mapping
- AuditObject: Immutable decision record
"""

import hashlib
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from .ontological_classifier import (
    ConsensusStatus,
    DisagreementType,
    OntologicalConsensus,
    calculate_ontological_consensus,
)


# === Enums ===


class RiskProfile(str, Enum):
    """Risk tolerance level affecting thresholds and actions."""

    LOW = "low"
    """Permissive: allows action with moderate confidence."""

    MEDIUM = "medium"
    """Balanced: standard threshold, escalates on uncertainty."""

    HIGH = "high"
    """Strict: requires high confidence, aborts on any doubt."""


class GovernanceAction(str, Enum):
    """The action an agent should take based on governance decision."""

    PROCEED = "proceed"
    """Safe to act - consensus achieved at acceptable confidence."""

    ABORT = "abort"
    """Do not act - insufficient confidence or critical uncertainty."""

    ESCALATE = "escalate"
    """Requires human decision - GAP or ambiguous situation."""

    REVISE = "revise"
    """Claim needs reformulation - error detected in input."""


class GovernanceStatus(str, Enum):
    """Governance layer status (maps from ontological consensus)."""

    PASSED = "PASSED"
    """Consensus above threshold for risk profile."""

    MYSTERY = "MYSTERY"
    """Legitimate philosophical disagreement - unknowable."""

    GAP = "GAP"
    """Knowledge gap - requires external info or human judgment."""

    ERROR = "ERROR"
    """Logical error detected or invalid input."""


# === Data Classes ===


@dataclass
class ValidatorRecord:
    """Record of a single validator's assessment."""

    name: str
    confidence: float
    reasoning: str


@dataclass
class ConsensusRecord:
    """Summary of consensus calculation."""

    status: GovernanceStatus
    action: GovernanceAction
    confidence: float
    consensus_type: str  # UNANIMOUS, SUPERMAJORITY, MAJORITY, DISPUTED


@dataclass
class ReasoningRecord:
    """Detailed reasoning for the governance decision."""

    ontological_classification: str | None = None
    gap_type: str | None = None
    fallacies_detected: list[str] = field(default_factory=list)
    hypothesis_status: str | None = None
    threshold_used: float = 0.0
    risk_profile: str = "medium"


@dataclass
class GovernanceRequest:
    """Input request for governance verification."""

    claim: str
    domain: str = "general"
    context: str = ""
    risk_profile: RiskProfile = RiskProfile.MEDIUM


@dataclass
class GovernanceResult:
    """Output of governance verification."""

    status: GovernanceStatus
    action: GovernanceAction
    confidence: float
    reason: str
    audit_ref: str
    ontological_type: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "status": self.status.value,
            "action": self.action.value,
            "confidence": self.confidence,
            "reason": self.reason,
            "audit_ref": self.audit_ref,
            "ontological_type": self.ontological_type,
        }


@dataclass
class AuditObject:
    """
    Immutable audit record of a governance decision.

    This is the audit trail that makes decisions traceable
    and reviewable. Linked via hashes for integrity.
    """

    id: str
    timestamp: str
    claim: str
    domain: str
    risk_profile: RiskProfile
    validators: list[ValidatorRecord]
    consensus: ConsensusRecord
    reasoning: ReasoningRecord
    hash: str
    parent_hash: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "claim": self.claim,
            "domain": self.domain,
            "risk_profile": self.risk_profile.value,
            "validators": [
                {"name": v.name, "confidence": v.confidence, "reasoning": v.reasoning}
                for v in self.validators
            ],
            "consensus": {
                "status": self.consensus.status.value,
                "action": self.consensus.action.value,
                "confidence": self.consensus.confidence,
                "type": self.consensus.consensus_type,
            },
            "reasoning": {
                "ontological_classification": self.reasoning.ontological_classification,
                "gap_type": self.reasoning.gap_type,
                "fallacies_detected": self.reasoning.fallacies_detected,
                "hypothesis_status": self.reasoning.hypothesis_status,
                "threshold_used": self.reasoning.threshold_used,
                "risk_profile": self.reasoning.risk_profile,
            },
            "hash": self.hash,
            "parent_hash": self.parent_hash,
        }

    def to_json(self) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


# === Policy Engine ===


class PolicyEngine:
    """
    Maps verification status + risk profile → governance action.

    The core decision engine that transforms ontological consensus
    into actionable guidance for agents.
    """

    # Confidence thresholds by risk profile
    THRESHOLDS: dict[RiskProfile, float] = {
        RiskProfile.LOW: 0.60,
        RiskProfile.MEDIUM: 0.75,
        RiskProfile.HIGH: 0.90,
    }

    # Domains that default to HIGH risk
    HIGH_RISK_DOMAINS: set[str] = {"medical", "financial", "legal", "safety"}

    def __init__(self) -> None:
        self._audit_history: list[AuditObject] = []

    def get_threshold(self, risk_profile: RiskProfile) -> float:
        """Get confidence threshold for risk profile."""
        return self.THRESHOLDS[risk_profile]

    def get_effective_risk(self, risk_profile: RiskProfile, domain: str) -> RiskProfile:
        """Get effective risk profile considering domain."""
        if domain.lower() in self.HIGH_RISK_DOMAINS:
            # High-risk domains upgrade LOW to MEDIUM
            if risk_profile == RiskProfile.LOW:
                return RiskProfile.MEDIUM
        return risk_profile

    def _map_consensus_to_status(
        self, consensus: OntologicalConsensus
    ) -> GovernanceStatus:
        """Map ontological consensus status to governance status."""
        if consensus.status == ConsensusStatus.PASSED:
            return GovernanceStatus.PASSED
        elif consensus.status == ConsensusStatus.UNRESOLVABLE:
            return GovernanceStatus.MYSTERY
        elif consensus.status == ConsensusStatus.PENDING_MEDIATION:
            return GovernanceStatus.GAP
        else:
            # FAILED or unknown
            return GovernanceStatus.ERROR

    def _determine_action(
        self,
        status: GovernanceStatus,
        confidence: float,
        risk_profile: RiskProfile,
    ) -> GovernanceAction:
        """
        Determine governance action based on status, confidence, and risk.

        Decision matrix:
        | Status  | Low Risk  | Medium Risk | High Risk |
        |---------|-----------|-------------|-----------|
        | PASSED  | proceed   | proceed     | proceed   |
        | MYSTERY | escalate  | abort       | abort     |
        | GAP     | escalate  | escalate    | abort     |
        | ERROR   | revise    | revise      | abort     |

        Additionally, if confidence is below threshold for risk level,
        PASSED becomes escalate (medium) or abort (high).
        """
        threshold = self.get_threshold(risk_profile)

        if status == GovernanceStatus.PASSED:
            if confidence >= threshold:
                return GovernanceAction.PROCEED
            else:
                # Below threshold for this risk profile
                if risk_profile == RiskProfile.HIGH:
                    return GovernanceAction.ABORT
                elif risk_profile == RiskProfile.MEDIUM:
                    return GovernanceAction.ESCALATE
                else:
                    return GovernanceAction.PROCEED  # LOW allows it

        elif status == GovernanceStatus.MYSTERY:
            # Philosophical uncertainty - respect it
            if risk_profile == RiskProfile.LOW:
                return GovernanceAction.ESCALATE
            else:
                return GovernanceAction.ABORT

        elif status == GovernanceStatus.GAP:
            # Knowledge gap - needs human input
            if risk_profile == RiskProfile.HIGH:
                return GovernanceAction.ABORT
            else:
                return GovernanceAction.ESCALATE

        elif status == GovernanceStatus.ERROR:
            # Error detected
            if risk_profile == RiskProfile.HIGH:
                return GovernanceAction.ABORT
            else:
                return GovernanceAction.REVISE

        # Fallback
        return GovernanceAction.ABORT

    def _generate_reason(
        self,
        status: GovernanceStatus,
        action: GovernanceAction,
        confidence: float,
        risk_profile: RiskProfile,
        domain: str,
        disagreement_type: DisagreementType | None,
    ) -> str:
        """Generate human-readable reason for the decision."""
        threshold = self.get_threshold(risk_profile)

        if action == GovernanceAction.PROCEED:
            return (
                f"Consensus achieved ({confidence:.0%}) above {risk_profile.value} "
                f"risk threshold ({threshold:.0%})"
            )

        elif action == GovernanceAction.ABORT:
            if status == GovernanceStatus.MYSTERY:
                return (
                    f"Philosophical uncertainty detected - cannot resolve algorithmically "
                    f"({risk_profile.value} risk profile requires certainty)"
                )
            elif status == GovernanceStatus.GAP:
                return (
                    f"Knowledge gap detected - insufficient evidence for {risk_profile.value} "
                    f"risk {domain} claim"
                )
            else:
                return (
                    f"Confidence ({confidence:.0%}) below {risk_profile.value} risk "
                    f"threshold ({threshold:.0%})"
                )

        elif action == GovernanceAction.ESCALATE:
            if status == GovernanceStatus.GAP:
                return "Requires human judgment - knowledge gap detected"
            elif status == GovernanceStatus.MYSTERY:
                return "Requires human judgment - legitimate philosophical disagreement"
            else:
                return (
                    f"Confidence ({confidence:.0%}) below threshold - escalating for review"
                )

        elif action == GovernanceAction.REVISE:
            return "Logical error or invalid input detected - claim needs reformulation"

        return "Unknown decision state"

    def _compute_audit_hash(self, audit_data: dict[str, Any]) -> str:
        """Compute SHA-256 hash for audit object."""
        canonical = json.dumps(audit_data, sort_keys=True, ensure_ascii=False)
        return f"sha256:{hashlib.sha256(canonical.encode()).hexdigest()}"

    def create_audit_object(
        self,
        request: GovernanceRequest,
        result: GovernanceResult,
        validator_results: dict[str, tuple[float, str]],
        ontological_consensus: OntologicalConsensus,
    ) -> AuditObject:
        """Create immutable audit record for a governance decision."""
        audit_id = f"audit_{uuid.uuid4().hex[:12]}"
        timestamp = datetime.now(timezone.utc).isoformat()

        validators = [
            ValidatorRecord(name=name, confidence=conf, reasoning=reasoning)
            for name, (conf, reasoning) in validator_results.items()
        ]

        consensus = ConsensusRecord(
            status=result.status,
            action=result.action,
            confidence=result.confidence,
            consensus_type=self._get_consensus_type(result.confidence),
        )

        reasoning = ReasoningRecord(
            ontological_classification=(
                ontological_consensus.disagreement_type.value
                if ontological_consensus.disagreement_type
                else None
            ),
            gap_type=(
                "insufficient_evidence"
                if result.status == GovernanceStatus.GAP
                else None
            ),
            fallacies_detected=[],
            hypothesis_status=None,
            threshold_used=self.get_threshold(request.risk_profile),
            risk_profile=request.risk_profile.value,
        )

        # Compute hash
        hash_data = {
            "claim": request.claim,
            "domain": request.domain,
            "risk_profile": request.risk_profile.value,
            "status": result.status.value,
            "action": result.action.value,
            "confidence": result.confidence,
            "timestamp": timestamp,
        }
        audit_hash = self._compute_audit_hash(hash_data)

        # Get parent hash if available
        parent_hash = (
            self._audit_history[-1].hash if self._audit_history else None
        )

        audit = AuditObject(
            id=audit_id,
            timestamp=timestamp,
            claim=request.claim,
            domain=request.domain,
            risk_profile=request.risk_profile,
            validators=validators,
            consensus=consensus,
            reasoning=reasoning,
            hash=audit_hash,
            parent_hash=parent_hash,
        )

        self._audit_history.append(audit)
        return audit

    def _get_consensus_type(self, confidence: float) -> str:
        """Determine consensus type from confidence level."""
        if confidence >= 1.0:
            return "UNANIMOUS"
        elif confidence >= 0.75:
            return "SUPERMAJORITY"
        elif confidence >= 0.66:
            return "MAJORITY"
        else:
            return "DISPUTED"

    def evaluate(
        self,
        request: GovernanceRequest,
        validator_results: dict[str, tuple[float, str]],
    ) -> tuple[GovernanceResult, AuditObject]:
        """
        Evaluate a governance request and return decision with audit trail.

        This is the main entry point for the governance layer.

        Args:
            request: GovernanceRequest with claim, domain, context, risk_profile
            validator_results: Dict mapping validator name to (confidence, reasoning)

        Returns:
            Tuple of (GovernanceResult, AuditObject)
        """
        # Get effective risk profile (domain may upgrade it)
        effective_risk = self.get_effective_risk(request.risk_profile, request.domain)
        threshold = self.get_threshold(effective_risk)

        # Calculate ontological consensus
        ontological_consensus = calculate_ontological_consensus(
            claim=request.claim,
            validator_results=validator_results,
            threshold=threshold,
            domain=request.domain,
        )

        # Map to governance status
        status = self._map_consensus_to_status(ontological_consensus)

        # Determine action
        action = self._determine_action(
            status=status,
            confidence=ontological_consensus.value,
            risk_profile=effective_risk,
        )

        # Generate reason
        reason = self._generate_reason(
            status=status,
            action=action,
            confidence=ontological_consensus.value,
            risk_profile=effective_risk,
            domain=request.domain,
            disagreement_type=ontological_consensus.disagreement_type,
        )

        # Create result (audit_ref will be filled after audit creation)
        result = GovernanceResult(
            status=status,
            action=action,
            confidence=ontological_consensus.value,
            reason=reason,
            audit_ref="",  # Temporary
            ontological_type=(
                ontological_consensus.disagreement_type.value
                if ontological_consensus.disagreement_type
                else None
            ),
        )

        # Create audit object
        audit = self.create_audit_object(
            request=request,
            result=result,
            validator_results=validator_results,
            ontological_consensus=ontological_consensus,
        )

        # Update result with audit reference
        result.audit_ref = audit.id

        return result, audit


# === Convenience Functions ===


def evaluate_governance(
    claim: str,
    validator_results: dict[str, tuple[float, str]],
    domain: str = "general",
    context: str = "",
    risk_profile: str = "medium",
) -> GovernanceResult:
    """
    Convenience function for quick governance evaluation.

    Args:
        claim: The claim to verify
        validator_results: Dict mapping validator name to (confidence, reasoning)
        domain: Knowledge domain
        context: Additional context
        risk_profile: "low", "medium", or "high"

    Returns:
        GovernanceResult with status, action, confidence, reason, audit_ref
    """
    request = GovernanceRequest(
        claim=claim,
        domain=domain,
        context=context,
        risk_profile=RiskProfile(risk_profile),
    )

    engine = PolicyEngine()
    result, _ = engine.evaluate(request, validator_results)
    return result
