"""
Intent Extractor - Semantic parsing of user intention.

PURE MODULE - No I/O, deterministic, vocabulary injected.

Responsibility: Extract named entities from intention text
and map them to schema fields with confidence scores.
"""

from __future__ import annotations

from preflights.core.types import ExplicitIntent, ExtractedEntity, Intention

# Type alias for vocabulary: term -> (field_id, normalized_value)
EntityVocabulary = tuple[tuple[str, tuple[str, str]], ...]

# Type alias for category mapping: field_id -> category
FieldCategoryMapping = tuple[tuple[str, str], ...]


def extract_intent(
    intention: Intention,
    vocabulary: EntityVocabulary,
    field_categories: FieldCategoryMapping | None = None,
) -> ExplicitIntent:
    """
    Extract explicit entities from user intention.

    Algorithm:
    1. Normalize text (lowercase)
    2. Match terms from vocabulary (longest first to handle compound terms)
    3. Compute confidence based on word boundaries
    4. Detect dominant category from extracted entities

    Args:
        intention: User intention to parse
        vocabulary: Injected vocabulary mapping terms to (field_id, normalized_value)
        field_categories: Optional mapping of field_id to category name

    Returns:
        ExplicitIntent with all extracted entities and confidence scores

    Example:
        >>> vocab = (("oauth", ("auth_strategy", "OAuth")), ("clerk", ("auth_library", "Clerk")))
        >>> intent = Intention("Add OAuth auth with Clerk")
        >>> result = extract_intent(intent, vocab)
        >>> result.get_explicit_value("auth_strategy")
        'OAuth'
    """
    text = intention.text
    text_lower = text.lower()

    entities: list[ExtractedEntity] = []

    # Sort vocabulary by term length (descending) to match compound terms first
    sorted_vocab = sorted(vocabulary, key=lambda x: len(x[0]), reverse=True)

    matched_spans: list[tuple[int, int]] = []

    for term, (field_id, normalized_value) in sorted_vocab:
        term_lower = term.lower()
        start = 0

        while True:
            pos = text_lower.find(term_lower, start)
            if pos == -1:
                break

            end = pos + len(term_lower)

            # Skip if overlaps with already matched span
            if not _overlaps_existing(pos, end, matched_spans):
                confidence = _compute_confidence(text_lower, pos, end)

                if confidence >= 0.7:  # Minimum threshold to consider
                    entities.append(
                        ExtractedEntity(
                            field_id=field_id,
                            value=normalized_value,
                            confidence=confidence,
                            source_span=(pos, end),
                        )
                    )
                    matched_spans.append((pos, end))

            start = end

    # Detect dominant category
    detected_category = _detect_dominant_category(entities, field_categories)

    return ExplicitIntent(
        raw_text=text,
        entities=tuple(entities),
        detected_category=detected_category,
    )


def _overlaps_existing(start: int, end: int, spans: list[tuple[int, int]]) -> bool:
    """Check if span overlaps with any existing span."""
    for s, e in spans:
        if not (end <= s or start >= e):
            return True
    return False


def _compute_confidence(text: str, start: int, end: int) -> float:
    """
    Compute match confidence based on word boundaries.

    - Exact word boundaries (space, punctuation, start/end) = 1.0
    - Partial boundaries = 0.85
    - No clear boundaries = 0.7
    """
    word_boundary_chars = frozenset(
        " ,.:;!?()[]{}\"'`\n\t-_/"
    )

    has_left_boundary = start == 0 or text[start - 1] in word_boundary_chars
    has_right_boundary = end == len(text) or text[end] in word_boundary_chars

    if has_left_boundary and has_right_boundary:
        return 1.0
    elif has_left_boundary or has_right_boundary:
        return 0.85
    else:
        return 0.7


def _detect_dominant_category(
    entities: list[ExtractedEntity],
    field_categories: FieldCategoryMapping | None,
) -> str | None:
    """
    Detect dominant category based on extracted entities.

    Returns the category with most entity matches.
    """
    if not field_categories or not entities:
        return None

    # Build lookup dict
    field_to_category = dict(field_categories)

    category_counts: dict[str, int] = {}
    for entity in entities:
        cat = field_to_category.get(entity.field_id)
        if cat:
            category_counts[cat] = category_counts.get(cat, 0) + 1

    if not category_counts:
        return None

    return max(category_counts, key=lambda k: category_counts[k])
