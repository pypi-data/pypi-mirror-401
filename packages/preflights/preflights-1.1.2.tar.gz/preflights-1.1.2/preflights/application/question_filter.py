"""
Question Filter - Filter questions based on explicit intent extraction.

Removes questions where the user has explicitly mentioned the answer
in their intention text. Produces pre-filled answers for skipped questions.
"""

from __future__ import annotations

from dataclasses import dataclass

from preflights.application.types import Question
from preflights.core.types import ExplicitIntent


@dataclass(frozen=True)
class FilterResult:
    """Result of filtering questions against explicit intent."""

    remaining_questions: tuple[Question, ...]
    prefilled_answers: dict[str, str | tuple[str, ...]]  # Aligned with Session.answers
    detected_pairs: tuple[tuple[str, str], ...]  # (label, value) for UX display


def filter_questions(
    questions: tuple[Question, ...],
    explicit_intent: ExplicitIntent,
    skip_threshold: float = 0.9,
) -> FilterResult:
    """
    Filter questions based on explicit intent extraction.

    Policy V1.1 (2 levels):
    - confidence >= skip_threshold: prefill answer + skip question
    - confidence < skip_threshold: ask question normally

    Args:
        questions: Questions to filter
        explicit_intent: Extracted explicit intent from user
        skip_threshold: Minimum confidence to skip a question (default 0.9)

    Returns:
        FilterResult with:
        - remaining_questions: Questions to ask the user
        - prefilled_answers: Answers extracted from intent (dict format, aligned with Session.answers)
        - detected_pairs: Human-readable (label, value) pairs for UX feedback

    Example:
        >>> # User said "Add OAuth auth with Clerk"
        >>> # explicit_intent has auth_strategy=OAuth (1.0), auth_library=Clerk (1.0)
        >>> # questions: auth_strategy, auth_library, oauth_providers
        >>> result = filter_questions(questions, explicit_intent)
        >>> len(result.remaining_questions)  # Only oauth_providers
        1
        >>> len(result.prefilled_answers)  # auth_strategy + auth_library
        2
    """
    remaining: list[Question] = []
    prefilled: dict[str, str | tuple[str, ...]] = {}
    detected: list[tuple[str, str]] = []

    for question in questions:
        explicit_value = explicit_intent.get_explicit_value(
            question.id, min_confidence=skip_threshold
        )

        if explicit_value is not None:
            # Value explicitly mentioned with high confidence -> prefill + skip
            prefilled[question.id] = explicit_value
            # Use question text as label (human-readable)
            label = _extract_label_from_question(question)
            detected.append((label, explicit_value))
        else:
            # No explicit value or low confidence -> ask the question
            remaining.append(question)

    return FilterResult(
        remaining_questions=tuple(remaining),
        prefilled_answers=prefilled,
        detected_pairs=tuple(detected),
    )


def merge_answers(
    prefilled: dict[str, str | tuple[str, ...]],
    user_answers: dict[str, str | tuple[str, ...]],
) -> dict[str, str | tuple[str, ...]]:
    """
    Merge prefilled answers with user answers.

    Priority: user_answers > prefilled (user can always override extraction).

    Args:
        prefilled: Answers pre-filled from intent extraction
        user_answers: Answers provided by user

    Returns:
        Merged answers dict with user answers taking precedence
    """
    merged = dict(prefilled)
    merged.update(user_answers)
    return merged


def _extract_label_from_question(question: Question) -> str:
    """
    Extract a short label from question for UX display.

    Uses the question text, cleaned up for display.
    Example: "Which authentication strategy?" -> "Authentication strategy"
    """
    text = question.question

    # Remove common prefixes
    prefixes = ("Which ", "What ", "Select ", "Choose ")
    for prefix in prefixes:
        if text.startswith(prefix):
            text = text[len(prefix) :]
            break

    # Remove trailing question mark and clean up
    text = text.rstrip("?").strip()

    # Capitalize first letter
    if text:
        text = text[0].upper() + text[1:]

    return text
