"""LLM adapter port."""

from __future__ import annotations

from typing import Protocol

from preflights.application.types import (
    LLMContext,
    LLMResponse,
    Question,
    SessionSnapshot,
)
from preflights.core.types import DecisionPatch, HeuristicsConfig


class LLMPort(Protocol):
    """
    Port for LLM interactions.

    Responsible for:
    - Generating clarification questions from intention
    - Extracting structured DecisionPatch from answers

    Supports multiple implementations:
    - MockLLMAdapter: Deterministic (default, fallback)
    - AnthropicLLMAdapter: Claude via tool use
    - OpenAILLMAdapter: GPT via function calling
    - OpenRouterLLMAdapter: Multiple models via OpenRouter
    """

    def generate_questions(
        self,
        intention: str,
        heuristics_config: HeuristicsConfig,
        context: LLMContext | None = None,
        session_state: SessionSnapshot | None = None,
        *,
        debug_llm: bool = False,
        repo_path: str | None = None,
    ) -> LLMResponse:
        """
        Generate clarification questions based on intention.

        Args:
            intention: User's intention text
            heuristics_config: Schema and heuristics configuration
            context: Optional filtered and redacted context
            session_state: Optional session snapshot for cross-session tracking
            debug_llm: If True, write prompt to .preflights/debug/last_llm_prompt.md
            repo_path: Repository path (required if debug_llm=True)

        Returns:
            LLMResponse with questions and semantic tracking fields
        """
        ...

    def extract_decision_patch(
        self,
        intention: str,
        answers: dict[str, str | tuple[str, ...]],
        heuristics_config: HeuristicsConfig,
        *,
        debug_llm: bool = False,
        repo_path: str | None = None,
    ) -> DecisionPatch | None:
        """
        Extract structured DecisionPatch from answers.

        Args:
            intention: User's intention text
            answers: Question ID -> answer mapping
            heuristics_config: Schema for validation
            debug_llm: If True, write prompt to .preflights/debug/last_llm_prompt.md
            repo_path: Repository path (required if debug_llm=True)

        Returns:
            DecisionPatch if extraction successful, None if failed

        Note: Returns None if LLM cannot extract valid patch.
              Application should return PATCH_EXTRACTION_FAILED error.
        """
        ...


# Legacy type alias for backward compatibility
LegacyQuestionTuple = tuple[Question, ...]
