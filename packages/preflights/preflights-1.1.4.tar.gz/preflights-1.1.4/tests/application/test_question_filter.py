"""Tests for question filter module."""

from __future__ import annotations

import pytest

from preflights.application.question_filter import (
    FilterResult,
    filter_questions,
    merge_answers,
)
from preflights.application.types import Question
from preflights.core.types import ExplicitIntent, ExtractedEntity


# =============================================================================
# FIXTURES
# =============================================================================


@pytest.fixture
def auth_questions():
    """Sample authentication questions."""
    return (
        Question(
            id="auth_strategy",
            type="single_choice",
            question="Which authentication strategy?",
            options=("OAuth", "Email/Password", "Magic Links", "SAML"),
        ),
        Question(
            id="auth_library",
            type="single_choice",
            question="Which authentication library?",
            options=("NextAuth.js", "Clerk", "Auth0", "Custom"),
        ),
        Question(
            id="oauth_providers",
            type="multi_choice",
            question="Which OAuth providers to support?",
            options=("Google", "GitHub", "Microsoft", "Facebook"),
            optional=True,
        ),
    )


@pytest.fixture
def oauth_clerk_explicit():
    """ExplicitIntent with OAuth and Clerk detected."""
    return ExplicitIntent(
        raw_text="Add OAuth auth with Clerk",
        entities=(
            ExtractedEntity(
                field_id="auth_strategy",
                value="OAuth",
                confidence=1.0,
                source_span=(4, 9),
            ),
            ExtractedEntity(
                field_id="auth_library",
                value="Clerk",
                confidence=1.0,
                source_span=(20, 25),
            ),
        ),
        detected_category="Authentication",
    )


@pytest.fixture
def low_confidence_explicit():
    """ExplicitIntent with low confidence matches."""
    return ExplicitIntent(
        raw_text="Maybe use jwt",
        entities=(
            ExtractedEntity(
                field_id="auth_strategy",
                value="JWT",
                confidence=0.7,  # Below skip threshold
                source_span=(10, 13),
            ),
        ),
        detected_category="Authentication",
    )


@pytest.fixture
def empty_explicit():
    """ExplicitIntent with no entities."""
    return ExplicitIntent(
        raw_text="Add authentication",
        entities=(),
        detected_category=None,
    )


# =============================================================================
# FILTER QUESTIONS TESTS
# =============================================================================


class TestFilterQuestionsSkipsExplicit:
    """Test that filter_questions skips explicitly answered questions."""

    def test_skips_explicit_questions(self, auth_questions, oauth_clerk_explicit):
        """Test that questions with explicit answers are skipped."""
        result = filter_questions(
            questions=auth_questions,
            explicit_intent=oauth_clerk_explicit,
            skip_threshold=0.9,
        )

        # Only oauth_providers should remain
        assert len(result.remaining_questions) == 1
        assert result.remaining_questions[0].id == "oauth_providers"

    def test_prefills_explicit_answers(self, auth_questions, oauth_clerk_explicit):
        """Test that explicit values are prefilled."""
        result = filter_questions(
            questions=auth_questions,
            explicit_intent=oauth_clerk_explicit,
            skip_threshold=0.9,
        )

        # auth_strategy and auth_library should be prefilled
        assert "auth_strategy" in result.prefilled_answers
        assert result.prefilled_answers["auth_strategy"] == "OAuth"
        assert "auth_library" in result.prefilled_answers
        assert result.prefilled_answers["auth_library"] == "Clerk"

    def test_generates_detected_pairs_for_ux(self, auth_questions, oauth_clerk_explicit):
        """Test that detected pairs are generated for UX display."""
        result = filter_questions(
            questions=auth_questions,
            explicit_intent=oauth_clerk_explicit,
            skip_threshold=0.9,
        )

        # Should have 2 detected pairs
        assert len(result.detected_pairs) == 2
        # Labels should be human-readable (from question text)
        labels = [pair[0] for pair in result.detected_pairs]
        values = [pair[1] for pair in result.detected_pairs]
        assert "OAuth" in values
        assert "Clerk" in values


class TestFilterQuestionsLowConfidence:
    """Test behavior with low confidence matches."""

    def test_does_not_skip_low_confidence(self, auth_questions, low_confidence_explicit):
        """Test that low confidence matches don't skip questions."""
        result = filter_questions(
            questions=auth_questions,
            explicit_intent=low_confidence_explicit,
            skip_threshold=0.9,
        )

        # All questions should remain (low confidence doesn't skip)
        assert len(result.remaining_questions) == 3
        assert len(result.prefilled_answers) == 0

    def test_lower_threshold_skips_more(self, auth_questions, low_confidence_explicit):
        """Test that lower threshold skips more questions."""
        result = filter_questions(
            questions=auth_questions,
            explicit_intent=low_confidence_explicit,
            skip_threshold=0.6,  # Lower threshold
        )

        # Now the low confidence match should be skipped
        assert len(result.remaining_questions) == 2
        assert "auth_strategy" in result.prefilled_answers


class TestFilterQuestionsNoExplicit:
    """Test behavior when nothing is explicit."""

    def test_no_filtering_when_nothing_explicit(self, auth_questions, empty_explicit):
        """Test that all questions remain when nothing explicit."""
        result = filter_questions(
            questions=auth_questions,
            explicit_intent=empty_explicit,
            skip_threshold=0.9,
        )

        # All questions should remain
        assert len(result.remaining_questions) == 3
        assert len(result.prefilled_answers) == 0
        assert len(result.detected_pairs) == 0


# =============================================================================
# MERGE ANSWERS TESTS
# =============================================================================


class TestMergeAnswers:
    """Test merge_answers function."""

    def test_user_answer_overrides_prefill(self):
        """Test that user answers override prefilled values."""
        prefilled = {
            "auth_strategy": "OAuth",
            "auth_library": "Clerk",
        }
        user_answers = {
            "auth_library": "Auth0",  # Override Clerk
            "oauth_providers": ("Google", "GitHub"),
        }

        merged = merge_answers(prefilled, user_answers)

        # User answer should override
        assert merged["auth_library"] == "Auth0"
        # Prefilled should remain
        assert merged["auth_strategy"] == "OAuth"
        # New user answer should be included
        assert merged["oauth_providers"] == ("Google", "GitHub")

    def test_prefill_preserved_when_no_override(self):
        """Test that prefilled values are preserved when not overridden."""
        prefilled = {
            "auth_strategy": "OAuth",
            "auth_library": "Clerk",
        }
        user_answers = {
            "oauth_providers": ("Google",),
        }

        merged = merge_answers(prefilled, user_answers)

        # All prefilled should remain
        assert merged["auth_strategy"] == "OAuth"
        assert merged["auth_library"] == "Clerk"
        assert merged["oauth_providers"] == ("Google",)

    def test_empty_prefill(self):
        """Test merge with empty prefilled."""
        prefilled: dict[str, str | tuple[str, ...]] = {}
        user_answers = {
            "auth_strategy": "JWT",
        }

        merged = merge_answers(prefilled, user_answers)

        assert merged["auth_strategy"] == "JWT"
        assert len(merged) == 1

    def test_empty_user_answers(self):
        """Test merge with empty user answers."""
        prefilled = {
            "auth_strategy": "OAuth",
        }
        user_answers: dict[str, str | tuple[str, ...]] = {}

        merged = merge_answers(prefilled, user_answers)

        assert merged["auth_strategy"] == "OAuth"
        assert len(merged) == 1
