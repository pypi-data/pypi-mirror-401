"""Feedback Triage Workflow for obra CLI - Simplified version.

Part of FEEDBACK-TRIAGE-001: Feedback Triage Orchestration System.

This is a simplified version for the obra SaaS CLI that loads config directly
from obra/config/defaults/. For the full tiered resolution version, see
src/workflow/feedback_triage.py.

Example:
    >>> from obra.workflow.feedback_triage import FeedbackTriageWorkflow
    >>> workflow = FeedbackTriageWorkflow()
    >>> decision = workflow.execute(feedback_item)
"""

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


# =============================================================================
# Data Classes for Triage Results
# =============================================================================


@dataclass
class ValidationResult:
    """Result of validation stage."""

    is_valid: bool
    is_spam: bool = False
    spam_reason: str | None = None
    quality_score: int = 0  # 0-100
    quality_details: dict[str, Any] = field(default_factory=dict)


@dataclass
class ClassificationResult:
    """Result of type classification stage."""

    feedback_type: str  # bug, enhancement, question
    confidence: float  # 0.0 - 1.0
    indicators_found: list[str] = field(default_factory=list)


@dataclass
class SeverityResult:
    """Result of severity assignment stage."""

    severity: str  # P0, P1, P2, P3
    keywords_matched: list[str] = field(default_factory=list)
    confidence: float = 0.0


@dataclass
class TriageDecision:
    """Final triage decision with routing information."""

    decision: str  # accept, reject, escalate
    confidence: float  # 0.0 - 1.0
    reasoning: str
    severity: str | None = None  # P0, P1, P2, P3 (for bugs)
    human_review_required: bool = False
    destination: str | None = None  # File path for routing
    metadata: dict[str, Any] = field(default_factory=dict)


# =============================================================================
# Feedback Triage Workflow
# =============================================================================


class FeedbackTriageWorkflow:
    """Multi-stage workflow for automated feedback triage.

    Simplified version for obra CLI that loads config directly from
    obra/config/defaults/feedback_classification.yaml.
    """

    def __init__(self, config_path: Path | None = None):
        """Initialize FeedbackTriageWorkflow.

        Args:
            config_path: Optional path to config file. If None, uses default.
        """
        self.config = self._load_config(config_path)
        logger.info("FeedbackTriageWorkflow initialized")

    def _load_config(self, config_path: Path | None = None) -> dict[str, Any]:
        """Load feedback_classification config.

        Args:
            config_path: Optional config path. If None, uses default.

        Returns:
            Configuration dictionary

        Raises:
            FileNotFoundError: If config file not found
            ValueError: If config is invalid
        """
        if config_path is None:
            # Default to obra/config/defaults/feedback_classification.yaml
            obra_root = Path(__file__).parent.parent  # obra/workflow -> obra/
            config_path = obra_root / "config" / "defaults" / "feedback_classification.yaml"

        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        if not config:
            raise ValueError("Config file is empty")

        return config

    def execute(self, feedback: dict[str, Any]) -> TriageDecision:
        """Execute complete triage workflow on a feedback submission.

        Args:
            feedback: Feedback submission dictionary with keys:
                - type: str (bug, enhancement, question)
                - description: str
                - metadata: dict (optional)

        Returns:
            TriageDecision with routing information and confidence scores
        """
        logger.info(f"Starting triage workflow for feedback type: {feedback.get('type', 'unknown')}")

        # Stage 1: Validate submission
        validation = self.validate_submission(feedback)
        if not validation.is_valid:
            reason = validation.spam_reason or "Quality score below threshold"
            logger.info(f"Feedback rejected: {reason}")
            return TriageDecision(
                decision="reject",
                confidence=1.0,
                reasoning=reason,
                human_review_required=False,
                metadata={"validation": validation.__dict__},
            )

        # Stage 2: Classify type
        classification = self.classify_type(feedback)

        # Stage 3: Assign severity (for bugs)
        severity_result = None
        if classification.feedback_type == "bug":
            severity_result = self.assign_severity(feedback)

        # Stage 4: Generate routing decision
        decision = self.route_decision(
            feedback=feedback,
            validation=validation,
            classification=classification,
            severity=severity_result,
        )

        logger.info(
            f"Triage complete: decision={decision.decision}, "
            f"severity={decision.severity}, confidence={decision.confidence:.2f}"
        )

        return decision

    def validate_submission(self, feedback: dict[str, Any]) -> ValidationResult:
        """Stage 1: Validate submission for spam and quality."""
        description = feedback.get("description", "")
        spam_config = self.config["spam_detection"]
        quality_config = self.config["quality_scoring"]

        # Check minimum length
        if len(description) < spam_config["min_length"]:
            return ValidationResult(
                is_valid=False,
                is_spam=True,
                spam_reason=f"Description too short (< {spam_config['min_length']} chars)",
                quality_score=0,
            )

        # Check spam patterns
        for pattern_config in spam_config["patterns"]:
            try:
                if re.match(pattern_config["regex"], description, re.IGNORECASE):
                    return ValidationResult(
                        is_valid=False,
                        is_spam=True,
                        spam_reason=pattern_config["reason"],
                        quality_score=0,
                    )
            except re.error:
                logger.warning(f"Invalid spam regex pattern: {pattern_config['regex']}")

        # Calculate quality score
        quality_score = self._calculate_quality_score(feedback, quality_config)

        # Check quality thresholds
        reject_threshold = quality_config["thresholds"]["reject"]
        is_valid = quality_score >= reject_threshold

        return ValidationResult(
            is_valid=is_valid,
            is_spam=False,
            quality_score=quality_score,
            quality_details={"threshold": reject_threshold},
        )

    def _calculate_quality_score(
        self, feedback: dict[str, Any], quality_config: dict[str, Any]
    ) -> int:
        """Calculate quality score based on weighted factors."""
        description = feedback.get("description", "")
        metadata = feedback.get("metadata", {})
        weights = quality_config["weights"]
        score = 0

        # 1. Description length
        length_score = self._get_length_score(len(description), quality_config["length_scoring"])
        score += length_score

        # 2. Has repro steps
        has_repro = any(
            keyword in description.lower()
            for keyword in ["steps to reproduce", "repro", "reproduce:", "1.", "2.", "3."]
        )
        if has_repro:
            score += weights["has_repro_steps"]

        # 3. Has error message
        has_error = any(
            keyword in description.lower()
            for keyword in ["error:", "exception:", "traceback", "stack trace", "failed with"]
        )
        if has_error:
            score += weights["has_error_message"]

        # 4. Includes context
        has_context = bool(metadata) or any(
            keyword in description.lower()
            for keyword in ["version", "environment", "os:", "browser", "session"]
        )
        if has_context:
            score += weights["includes_context"]

        # 5. Clear language
        clear_language = (
            description[0].isupper() if description else False
        ) and description.endswith((".", "!", "?"))
        if clear_language:
            score += weights["clear_language"]

        return min(score, 100)

    def _get_length_score(self, length: int, length_scoring: list[dict[str, Any]]) -> int:
        """Get score based on description length."""
        for range_config in length_scoring:
            min_len, max_len = range_config["range"]
            if min_len <= length <= max_len:
                return range_config["score"]
        return 0

    def classify_type(self, feedback: dict[str, Any]) -> ClassificationResult:
        """Stage 2: Classify feedback type with confidence."""
        description = feedback.get("description", "").lower()
        declared_type = feedback.get("type", "").lower()
        type_config = self.config["type_classification"]

        # If user declared a type, trust it unless confidence is very low
        if declared_type in self.config["feedback_types"]:
            indicators = self._find_type_indicators(description, declared_type, type_config)
            if indicators:
                return ClassificationResult(
                    feedback_type=declared_type,
                    confidence=0.9,
                    indicators_found=indicators,
                )

        # Otherwise, infer type from indicators
        type_scores: dict[str, tuple[float, list[str]]] = {}

        for feedback_type in ["bug", "enhancement", "question"]:
            indicators_key = f"{feedback_type}_indicators"
            indicators = type_config.get(indicators_key, [])
            matches = [ind for ind in indicators if ind.lower() in description]

            if matches:
                confidence = min(0.3 + (len(matches) / len(indicators)) * 0.6, 0.9)
                type_scores[feedback_type] = (confidence, matches)

        if not type_scores:
            fallback_type = declared_type if declared_type in self.config["feedback_types"] else "question"
            return ClassificationResult(
                feedback_type=fallback_type,
                confidence=0.3,
                indicators_found=[],
            )

        # Select type with highest confidence
        best_type = max(type_scores.items(), key=lambda x: x[1][0])
        return ClassificationResult(
            feedback_type=best_type[0],
            confidence=best_type[1][0],
            indicators_found=best_type[1][1],
        )

    def _find_type_indicators(
        self, description: str, feedback_type: str, type_config: dict[str, Any]
    ) -> list[str]:
        """Find type indicators in description."""
        indicators_key = f"{feedback_type}_indicators"
        indicators = type_config.get(indicators_key, [])
        return [ind for ind in indicators if ind.lower() in description]

    def assign_severity(self, feedback: dict[str, Any]) -> SeverityResult:
        """Stage 3: Assign severity level for bugs."""
        description = feedback.get("description", "").lower()
        severity_config = self.config["severity_detection"]

        # Check each severity level (highest to lowest priority)
        severity_checks = [
            ("P0", severity_config["critical_keywords"]),
            ("P1", severity_config["high_keywords"]),
            ("P2", severity_config["medium_keywords"]),
            ("P3", severity_config["low_keywords"]),
        ]

        for severity, keywords in severity_checks:
            matches = [kw for kw in keywords if kw.lower() in description]
            if matches:
                confidence = min(0.5 + (len(matches) / len(keywords)) * 0.4, 0.9)
                return SeverityResult(
                    severity=severity, keywords_matched=matches, confidence=confidence
                )

        # Default to P2 (medium) if no clear indicators
        return SeverityResult(severity="P2", keywords_matched=[], confidence=0.5)

    def route_decision(
        self,
        feedback: dict[str, Any],
        validation: ValidationResult,
        classification: ClassificationResult,
        severity: SeverityResult | None,
    ) -> TriageDecision:
        """Stage 4: Generate routing decision with confidence."""
        escalation_config = self.config["escalation"]
        routing_config = self.config["routing"]

        # Check escalation conditions
        human_review_required = False
        escalation_reasons = []

        # Check confidence threshold
        if classification.confidence < escalation_config["confidence_threshold"]:
            human_review_required = True
            escalation_reasons.append("classification_ambiguous")

        # Check quality score
        if validation.quality_score < self.config["quality_scoring"]["thresholds"]["low_quality"]:
            human_review_required = True
            escalation_reasons.append("quality_score_below_40")

        # Check severity-based escalation
        if severity and severity.severity == "P0":
            human_review_required = True
            escalation_reasons.append("severity_p0")

        # Check routing config for type-specific review requirements
        type_routing = routing_config.get(classification.feedback_type, {})
        if type_routing.get("requires_review", False):
            human_review_required = True
            escalation_reasons.append(f"{classification.feedback_type}_requires_review")

        # Determine destination
        destination = type_routing.get("destination")

        # Calculate overall confidence
        confidence_factors = [classification.confidence, validation.quality_score / 100.0]
        if severity:
            confidence_factors.append(severity.confidence)
        overall_confidence = sum(confidence_factors) / len(confidence_factors)

        # Build reasoning
        reasoning_parts = [
            f"Type: {classification.feedback_type} ({classification.confidence:.2f})",
            f"Quality: {validation.quality_score}/100",
        ]
        if severity:
            reasoning_parts.append(f"Severity: {severity.severity} ({severity.confidence:.2f})")
        if escalation_reasons:
            reasoning_parts.append(f"Escalation: {', '.join(escalation_reasons)}")

        reasoning = "; ".join(reasoning_parts)

        # Determine final decision
        if human_review_required:
            decision = "escalate"
        else:
            decision = "accept"

        return TriageDecision(
            decision=decision,
            confidence=overall_confidence,
            reasoning=reasoning,
            severity=severity.severity if severity else None,
            human_review_required=human_review_required,
            destination=destination,
            metadata={
                "validation": validation.__dict__,
                "classification": classification.__dict__,
                "severity": severity.__dict__ if severity else None,
                "escalation_reasons": escalation_reasons,
            },
        )
