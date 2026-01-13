"""Tests for intent extractor module."""

from __future__ import annotations

import pytest

from preflights.core.intent_extractor import extract_intent
from preflights.core.types import ExplicitIntent, ExtractedEntity, Intention


# =============================================================================
# FIXTURES
# =============================================================================


@pytest.fixture
def auth_vocabulary():
    """Vocabulary for authentication-related terms."""
    return (
        ("oauth", ("auth_strategy", "OAuth")),
        ("jwt", ("auth_strategy", "JWT")),
        ("clerk", ("auth_library", "Clerk")),
        ("nextauth", ("auth_library", "NextAuth.js")),
        ("next-auth", ("auth_library", "NextAuth.js")),
        ("auth0", ("auth_library", "Auth0")),
    )


@pytest.fixture
def db_vocabulary():
    """Vocabulary for database-related terms."""
    return (
        ("postgresql", ("db_type", "PostgreSQL")),
        ("postgres", ("db_type", "PostgreSQL")),
        ("mongodb", ("db_type", "MongoDB")),
        ("mongo", ("db_type", "MongoDB")),
        ("prisma", ("db_orm", "Prisma")),
        ("drizzle", ("db_orm", "Drizzle")),
    )


@pytest.fixture
def field_categories():
    """Field to category mapping."""
    return (
        ("auth_strategy", "Authentication"),
        ("auth_library", "Authentication"),
        ("db_type", "Database"),
        ("db_orm", "Database"),
    )


# =============================================================================
# BASIC EXTRACTION TESTS
# =============================================================================


class TestExtractIntentBasic:
    """Test basic intent extraction functionality."""

    def test_extract_oauth_clerk(self, auth_vocabulary, field_categories):
        """Test extraction of OAuth and Clerk from intention."""
        intention = Intention("Add OAuth auth with Clerk")
        result = extract_intent(intention, auth_vocabulary, field_categories)

        assert result.is_explicit("auth_strategy")
        assert result.get_explicit_value("auth_strategy") == "OAuth"
        assert result.is_explicit("auth_library")
        assert result.get_explicit_value("auth_library") == "Clerk"
        assert result.detected_category == "Authentication"

    def test_extract_jwt_nextauth(self, auth_vocabulary, field_categories):
        """Test extraction of JWT and NextAuth."""
        intention = Intention("Implement JWT authentication using nextauth")
        result = extract_intent(intention, auth_vocabulary, field_categories)

        assert result.get_explicit_value("auth_strategy") == "JWT"
        assert result.get_explicit_value("auth_library") == "NextAuth.js"

    def test_extract_postgres_prisma(self, db_vocabulary, field_categories):
        """Test extraction of PostgreSQL and Prisma."""
        intention = Intention("Set up PostgreSQL database with Prisma ORM")
        result = extract_intent(intention, db_vocabulary, field_categories)

        assert result.get_explicit_value("db_type") == "PostgreSQL"
        assert result.get_explicit_value("db_orm") == "Prisma"
        assert result.detected_category == "Database"

    def test_no_explicit_values(self, auth_vocabulary, field_categories):
        """Test when no explicit values are mentioned."""
        intention = Intention("Add authentication to the app")
        result = extract_intent(intention, auth_vocabulary, field_categories)

        assert not result.is_explicit("auth_strategy")
        assert not result.is_explicit("auth_library")
        assert result.get_explicit_value("auth_strategy") is None

    def test_empty_intention(self, auth_vocabulary, field_categories):
        """Test with empty intention."""
        intention = Intention("")
        result = extract_intent(intention, auth_vocabulary, field_categories)

        assert len(result.entities) == 0
        assert result.detected_category is None


# =============================================================================
# CONFIDENCE TESTS
# =============================================================================


class TestConfidence:
    """Test confidence calculation based on word boundaries."""

    def test_exact_word_boundaries_high_confidence(self, auth_vocabulary, field_categories):
        """Test that exact word boundaries give high confidence."""
        intention = Intention("Use OAuth for authentication")
        result = extract_intent(intention, auth_vocabulary, field_categories)

        oauth_entity = next(
            (e for e in result.entities if e.field_id == "auth_strategy"), None
        )
        assert oauth_entity is not None
        assert oauth_entity.confidence == 1.0

    def test_term_at_start_high_confidence(self, auth_vocabulary, field_categories):
        """Test that term at start of text gets high confidence."""
        intention = Intention("OAuth authentication")
        result = extract_intent(intention, auth_vocabulary, field_categories)

        oauth_entity = next(
            (e for e in result.entities if e.field_id == "auth_strategy"), None
        )
        assert oauth_entity is not None
        assert oauth_entity.confidence == 1.0

    def test_term_at_end_high_confidence(self, auth_vocabulary, field_categories):
        """Test that term at end of text gets high confidence."""
        intention = Intention("Add OAuth")
        result = extract_intent(intention, auth_vocabulary, field_categories)

        oauth_entity = next(
            (e for e in result.entities if e.field_id == "auth_strategy"), None
        )
        assert oauth_entity is not None
        assert oauth_entity.confidence == 1.0


# =============================================================================
# THRESHOLD TESTS
# =============================================================================


class TestThresholds:
    """Test min_confidence threshold behavior."""

    def test_default_threshold_0_9(self, auth_vocabulary, field_categories):
        """Test that default threshold is 0.9."""
        intention = Intention("Use OAuth")
        result = extract_intent(intention, auth_vocabulary, field_categories)

        # High confidence match should pass default threshold
        assert result.is_explicit("auth_strategy", min_confidence=0.9)
        assert result.get_explicit_value("auth_strategy", min_confidence=0.9) == "OAuth"

    def test_lower_threshold_includes_more(self, auth_vocabulary, field_categories):
        """Test that lower threshold includes more matches."""
        intention = Intention("Use OAuth")
        result = extract_intent(intention, auth_vocabulary, field_categories)

        # Should definitely be explicit at 0.7 threshold
        assert result.is_explicit("auth_strategy", min_confidence=0.7)


# =============================================================================
# CASE INSENSITIVITY TESTS
# =============================================================================


class TestCaseInsensitivity:
    """Test case-insensitive matching."""

    def test_uppercase_match(self, auth_vocabulary, field_categories):
        """Test that uppercase terms are matched."""
        intention = Intention("Add OAUTH authentication")
        result = extract_intent(intention, auth_vocabulary, field_categories)

        assert result.is_explicit("auth_strategy")
        assert result.get_explicit_value("auth_strategy") == "OAuth"

    def test_mixed_case_match(self, auth_vocabulary, field_categories):
        """Test that mixed case terms are matched."""
        intention = Intention("Add OAuth with CLERK")
        result = extract_intent(intention, auth_vocabulary, field_categories)

        assert result.get_explicit_value("auth_strategy") == "OAuth"
        assert result.get_explicit_value("auth_library") == "Clerk"


# =============================================================================
# OVERLAP PREVENTION TESTS
# =============================================================================


class TestOverlapPrevention:
    """Test that overlapping matches are prevented."""

    def test_longer_term_takes_precedence(self):
        """Test that longer terms match before shorter ones."""
        vocabulary = (
            ("postgresql", ("db_type", "PostgreSQL")),
            ("postgres", ("db_type", "PostgreSQL")),
        )
        intention = Intention("Use PostgreSQL")
        result = extract_intent(intention, vocabulary, None)

        # Should only have one entity (longer match)
        assert len(result.entities) == 1
        assert result.entities[0].value == "PostgreSQL"


# =============================================================================
# CATEGORY DETECTION TESTS
# =============================================================================


class TestCategoryDetection:
    """Test dominant category detection."""

    def test_detect_authentication_category(self, auth_vocabulary, field_categories):
        """Test detection of Authentication category."""
        intention = Intention("Add OAuth with Clerk")
        result = extract_intent(intention, auth_vocabulary, field_categories)

        assert result.detected_category == "Authentication"

    def test_detect_database_category(self, db_vocabulary, field_categories):
        """Test detection of Database category."""
        intention = Intention("Set up PostgreSQL with Prisma")
        result = extract_intent(intention, db_vocabulary, field_categories)

        assert result.detected_category == "Database"

    def test_no_category_without_mapping(self, auth_vocabulary):
        """Test no category when no mapping provided."""
        intention = Intention("Add OAuth")
        result = extract_intent(intention, auth_vocabulary, None)

        assert result.detected_category is None


# =============================================================================
# GET ALL EXPLICIT TESTS
# =============================================================================


class TestGetAllExplicit:
    """Test get_all_explicit method."""

    def test_get_all_explicit_pairs(self, auth_vocabulary, field_categories):
        """Test getting all explicit field-value pairs."""
        intention = Intention("Add OAuth with Clerk")
        result = extract_intent(intention, auth_vocabulary, field_categories)

        explicit_pairs = result.get_all_explicit(min_confidence=0.9)
        assert ("auth_strategy", "OAuth") in explicit_pairs
        assert ("auth_library", "Clerk") in explicit_pairs
