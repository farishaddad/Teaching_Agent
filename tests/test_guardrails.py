"""Tests for the Guardrails module — violation handling, rate limiting, friendly messages."""

import asyncio
import time
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from backend.guardrails.config import POLICY, GuardrailPolicy
from backend.guardrails.violation_handler import (
    FRIENDLY_MESSAGES,
    RATE_LIMIT_THRESHOLD,
    RATE_LIMIT_WINDOW_SECONDS,
    _violation_counts,
    check_rate_limit,
    classify_violation,
    get_friendly_message,
    is_rate_limited,
    log_violation,
    record_violation_for_rate_limit,
)


# ─── Friendly Message Tests ──────────────────────────────────────────


class TestFriendlyMessages:
    """Ensure students never see technical guardrail details."""

    def test_topic_denial_message_is_helpful(self):
        msg = get_friendly_message("topic_denial")
        assert "Agentic AI" in msg
        assert "policy" not in msg.lower()
        assert "guardrail" not in msg.lower()

    def test_content_filter_message_is_safe(self):
        msg = get_friendly_message("content_filter")
        assert "learning" in msg.lower() or "focused" in msg.lower()
        assert "HATE" not in msg
        assert "filter" not in msg.lower()

    def test_pii_blocked_message_is_helpful(self):
        msg = get_friendly_message("pii_blocked")
        assert "privacy" in msg.lower() or "sensitive" in msg.lower()
        assert "anonymize" not in msg.lower()

    def test_grounding_failed_message(self):
        msg = get_friendly_message("grounding_failed")
        assert "course materials" in msg.lower()
        assert "grounding" not in msg.lower()

    def test_unknown_violation_has_fallback(self):
        msg = get_friendly_message("something_weird")
        assert len(msg) > 20  # Not empty
        assert "Agentic AI" in msg or "rephras" in msg.lower()

    def test_all_messages_are_nonempty(self):
        for vtype, msg in FRIENDLY_MESSAGES.items():
            assert len(msg) > 30, f"Message for {vtype} is too short"

    def test_no_message_exposes_internals(self):
        """No friendly message should contain technical guardrail terms."""
        forbidden_terms = [
            "guardrail", "policy", "CfnGuardrail", "bedrock",
            "inputAssessment", "outputAssessment", "BLOCKED",
            "HIGH", "MEDIUM", "topicPolicy",
        ]
        for vtype, msg in FRIENDLY_MESSAGES.items():
            for term in forbidden_terms:
                assert term not in msg, f"Message for {vtype} contains '{term}'"


# ─── Violation Classification Tests ──────────────────────────────────


class TestClassifyViolation:
    """Test parsing of Bedrock Guardrail trace structures."""

    def test_topic_denial_detected(self):
        trace = {
            "inputAssessment": {
                "topicPolicy": {
                    "topics": [
                        {"name": "Politics", "type": "DENY", "action": "BLOCKED"}
                    ]
                }
            }
        }
        result = classify_violation(trace)
        assert result["violation_type"] == "topic_denial"
        assert result["policy_name"] == "Politics"

    def test_content_filter_detected(self):
        trace = {
            "inputAssessment": {
                "contentPolicy": {
                    "filters": [
                        {"type": "HATE", "confidence": "HIGH", "action": "BLOCKED"}
                    ]
                }
            }
        }
        result = classify_violation(trace)
        assert result["violation_type"] == "content_filter"
        assert "HATE" in result["details"]

    def test_pii_blocked_detected(self):
        trace = {
            "inputAssessment": {
                "sensitiveInformationPolicy": {
                    "piiEntities": [
                        {"type": "AWS_ACCESS_KEY", "action": "BLOCKED"}
                    ]
                }
            }
        }
        result = classify_violation(trace)
        assert result["violation_type"] == "pii_blocked"
        assert result["pii_detected"] is True
        # Must NOT contain the actual PII value
        assert "AKIA" not in result["details"]

    def test_pii_anonymized_detected(self):
        trace = {
            "inputAssessment": {
                "sensitiveInformationPolicy": {
                    "piiEntities": [
                        {"type": "EMAIL", "action": "ANONYMIZED"}
                    ]
                }
            }
        }
        result = classify_violation(trace)
        assert result["violation_type"] == "pii_anonymized"
        assert result["pii_detected"] is True

    def test_word_policy_detected(self):
        trace = {
            "inputAssessment": {
                "wordPolicy": {
                    "customWords": [{"match": "ignore previous instructions"}]
                }
            }
        }
        result = classify_violation(trace)
        assert result["violation_type"] == "word_policy"

    def test_grounding_failed_detected(self):
        trace = {
            "outputAssessment": {
                "contextualGroundingPolicy": {
                    "filters": [
                        {"type": "GROUNDING", "score": 0.45, "threshold": 0.7, "action": "BLOCKED"}
                    ]
                }
            }
        }
        result = classify_violation(trace)
        assert result["violation_type"] == "grounding_failed"
        assert "0.45" in result["details"]

    def test_empty_trace_returns_unknown(self):
        result = classify_violation({})
        assert result["violation_type"] == "unknown"

    def test_output_assessment_fallback(self):
        """If inputAssessment is empty, check outputAssessment."""
        trace = {
            "inputAssessment": {},
            "outputAssessment": {
                "topicPolicy": {
                    "topics": [{"name": "Religion", "type": "DENY", "action": "BLOCKED"}]
                }
            }
        }
        result = classify_violation(trace)
        assert result["violation_type"] == "topic_denial"
        assert result["policy_name"] == "Religion"


# ─── Rate Limiting Tests ─────────────────────────────────────────────


class TestRateLimiting:
    """Test abuse detection via violation rate limiting."""

    def setup_method(self):
        """Clear rate limit state before each test."""
        _violation_counts.clear()

    def test_under_threshold_not_limited(self):
        student = "test-student-1"
        for _ in range(RATE_LIMIT_THRESHOLD - 1):
            record_violation_for_rate_limit(student)
        assert not is_rate_limited(student)

    def test_at_threshold_is_limited(self):
        student = "test-student-2"
        for _ in range(RATE_LIMIT_THRESHOLD):
            record_violation_for_rate_limit(student)
        assert is_rate_limited(student)

    def test_old_violations_expire(self):
        student = "test-student-3"
        # Add violations from "11 minutes ago" (outside window)
        old_time = time.time() - RATE_LIMIT_WINDOW_SECONDS - 60
        _violation_counts[student] = [old_time] * RATE_LIMIT_THRESHOLD
        # Should NOT be rate limited (old entries)
        assert not is_rate_limited(student)

    def test_different_students_independent(self):
        for _ in range(RATE_LIMIT_THRESHOLD):
            record_violation_for_rate_limit("student-a")
        assert is_rate_limited("student-a")
        assert not is_rate_limited("student-b")


# ─── Violation Logging Tests ─────────────────────────────────────────


class TestViolationLogging:
    """Test DynamoDB violation logging."""

    @patch("backend.guardrails.violation_handler.table")
    def test_log_violation_writes_to_dynamodb(self, mock_table):
        mock_table.put_item = MagicMock()
        asyncio.run(log_violation(
            student_id="stu-123",
            violation_type="topic_denial",
            query_summary="Who should I vote for?",
            details="topic_count=1",
        ))
        mock_table.put_item.assert_called_once()
        item = mock_table.put_item.call_args[1]["Item"]
        assert item["PK"] == "STU#stu-123"
        assert item["SK"].startswith("VIO#")
        assert item["violation_type"] == "topic_denial"

    @patch("backend.guardrails.violation_handler.table")
    def test_pii_violation_redacts_query(self, mock_table):
        """PII violations must NOT log the actual query content."""
        mock_table.put_item = MagicMock()
        asyncio.run(log_violation(
            student_id="stu-456",
            violation_type="pii_blocked",
            query_summary="My AWS key is AKIAIOSFODNN7EXAMPLE",
            details="pii_types_blocked=1",
        ))
        item = mock_table.put_item.call_args[1]["Item"]
        assert "AKIA" not in item["query_summary"]
        assert "REDACTED" in item["query_summary"]

    @patch("backend.guardrails.violation_handler.table")
    def test_log_failure_does_not_raise(self, mock_table):
        """Logging failures are swallowed — never crash the request."""
        mock_table.put_item = MagicMock(side_effect=Exception("DynamoDB unavailable"))
        # Should not raise
        asyncio.run(log_violation(
            student_id="stu-789",
            violation_type="content_filter",
            query_summary="test",
        ))


# ─── Policy Config Tests ─────────────────────────────────────────────


class TestGuardrailPolicy:
    """Test the policy configuration dataclass."""

    def test_default_policy_has_allowed_topics(self):
        assert len(POLICY.allowed_topics) > 5

    def test_default_policy_has_denied_topics(self):
        assert len(POLICY.denied_topics) > 3

    def test_grounding_threshold_is_sensible(self):
        assert 0.5 <= POLICY.grounding_threshold <= 0.9

    def test_denial_message_mentions_course(self):
        assert "course" in POLICY.denial_message.lower() or "Agentic AI" in POLICY.denial_message

    def test_content_filters_cover_key_categories(self):
        required = {"HATE", "SEXUAL", "VIOLENCE"}
        assert required.issubset(set(POLICY.content_filters.keys()))

    def test_pii_actions_include_aws_keys(self):
        assert "AWS_ACCESS_KEY" in POLICY.pii_actions
        assert POLICY.pii_actions["AWS_ACCESS_KEY"] == "BLOCK"
