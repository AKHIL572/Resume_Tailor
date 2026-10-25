"""
Loads and manages the rule files used as LLM system prompts.
Each rule file starts with a placeholder header and contains the user's instructions.
"""

from __future__ import annotations

import logging
from pathlib import Path

from app.core.data_dirs import data_path

logger = logging.getLogger(__name__)

RULE_FILES = {
    "source_of_truth": "01_source_of_truth.md",
    "job_analysis": "02_job_analysis.md",
    "verdict": "03_verdict.md",
    "email": "04_email.md",
    "resume_content": "05_resume_content.md",
    "layout_and_validation": "06_layout_and_validation.md",
    "final_review": "07_final_review.md",
}


def load_rule(key: str) -> str:
    """Load a rule file by its logical key. Returns empty string if missing."""
    filename = RULE_FILES.get(key)
    if not filename:
        logger.warning("Unknown rule key: %s", key)
        return ""
    path = data_path("rules", filename)
    if not path.exists():
        logger.warning("Rule file not found: %s", path)
        return ""
    return path.read_text(encoding="utf-8")


def load_all_rules() -> dict[str, str]:
    """Load all rule files. Returns dict of key -> content."""
    return {key: load_rule(key) for key in RULE_FILES}


def save_rule(key: str, content: str) -> None:
    """Persist an edited rule file."""
    filename = RULE_FILES.get(key)
    if not filename:
        raise ValueError(f"Unknown rule key: {key}")
    path = data_path("rules", filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_system_prompt(step_key: str, extra_sections: list[str] | None = None) -> str:
    """
    Assemble the system prompt for an LLM call.
    Order: 01_source_of_truth + step-specific rule + extra sections.
    """
    parts: list[str] = []

    sot = load_rule("source_of_truth")
    if sot:
        parts.append(sot)

    step_rule = load_rule(step_key)
    if step_rule:
        parts.append(step_rule)

    if extra_sections:
        parts.extend(extra_sections)

    return "\n\n---\n\n".join(p.strip() for p in parts if p.strip())
