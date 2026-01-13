"""
LLM Debug - Write LLM prompts to debug file.

Writes the exact prompt sent to LLM for debugging and tuning.
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path


DEBUG_DIR = ".preflights/debug"
DEBUG_FILE = "last_llm_prompt.md"


def write_llm_debug(
    repo_path: str,
    operation: str,  # "generate_questions" or "extract_decision_patch"
    system_prompt: str,
    user_message: str,
    tools: list[dict],
    model: str,
    provider: str,
    cli_command: str | None = None,
) -> str:
    """
    Write LLM prompt to debug file.

    Args:
        repo_path: Repository root path
        operation: "generate_questions" or "extract_decision_patch"
        system_prompt: System prompt sent to LLM
        user_message: User message sent to LLM
        tools: Tool schemas sent to LLM
        model: Model name/ID
        provider: Provider name (anthropic, openai, etc.)
        cli_command: Optional CLI command that triggered this

    Returns:
        Path to debug file (relative to repo_path)
    """
    debug_dir = Path(repo_path) / DEBUG_DIR
    debug_file = debug_dir / DEBUG_FILE

    # Create debug directory if needed
    debug_dir.mkdir(parents=True, exist_ok=True)

    # Ensure .gitignore exists
    _ensure_gitignore(Path(repo_path))

    # Build content
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    # Check if file exists and has content (append mode)
    append_mode = debug_file.exists() and debug_file.stat().st_size > 0

    content_parts = []

    if not append_mode:
        # Header (only on first write)
        content_parts.append("# LLM Debug - Preflights")
        content_parts.append("")
        content_parts.append(f"**Timestamp:** {timestamp}")
        content_parts.append(f"**Repository:** {repo_path}")
        if cli_command:
            content_parts.append(f"**CLI Command:** `{cli_command}`")
        content_parts.append(f"**Provider:** {provider}")
        content_parts.append(f"**Model:** {model}")
        content_parts.append("")
        content_parts.append("---")
        content_parts.append("")

    # Section for this operation
    op_title = "Question Generation" if operation == "generate_questions" else "Decision Extraction"
    content_parts.append(f"## {op_title}")
    content_parts.append("")
    content_parts.append(f"**Timestamp:** {timestamp}")
    content_parts.append("")

    # System prompt
    content_parts.append("### System Prompt")
    content_parts.append("")
    content_parts.append("```")
    content_parts.append(system_prompt)
    content_parts.append("```")
    content_parts.append("")

    # User message
    content_parts.append("### User Message")
    content_parts.append("")
    content_parts.append("```")
    content_parts.append(user_message)
    content_parts.append("```")
    content_parts.append("")

    # Tools schema
    content_parts.append("### Tools Schema")
    content_parts.append("")
    content_parts.append("```json")
    import json
    content_parts.append(json.dumps(tools, indent=2))
    content_parts.append("```")
    content_parts.append("")
    content_parts.append("---")
    content_parts.append("")

    content = "\n".join(content_parts)

    # Write or append
    if append_mode:
        with open(debug_file, "a") as f:
            f.write(content)
    else:
        with open(debug_file, "w") as f:
            f.write(content)

    return f"{DEBUG_DIR}/{DEBUG_FILE}"


def _ensure_gitignore(repo_path: Path) -> None:
    """Ensure debug/ is in .preflights/.gitignore."""
    preflights_dir = repo_path / ".preflights"
    gitignore_path = preflights_dir / ".gitignore"

    # Create .preflights if needed
    preflights_dir.mkdir(parents=True, exist_ok=True)

    # Check if gitignore exists and contains debug/
    if gitignore_path.exists():
        content = gitignore_path.read_text()
        if "debug/" not in content:
            with open(gitignore_path, "a") as f:
                if not content.endswith("\n"):
                    f.write("\n")
                f.write("debug/\n")
    else:
        gitignore_path.write_text("debug/\n")


def clear_debug_file(repo_path: str) -> None:
    """Clear debug file for a new session."""
    debug_file = Path(repo_path) / DEBUG_DIR / DEBUG_FILE
    if debug_file.exists():
        debug_file.unlink()
