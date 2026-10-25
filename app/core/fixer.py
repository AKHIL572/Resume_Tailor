"""
Fixer (Step 12): Sends precise validation failures back to the LLM
and iterates until all checks pass or max_rounds is reached.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Callable

from app.core.llm_client import LLMClient
from app.core.latex_utils import fill_template, compile_latex
from app.core.rules_loader import build_system_prompt
from app.models.schemas import (
    ResumeContent,
    ValidationReport,
    CheckResult,
)

logger = logging.getLogger(__name__)

JSON_SCHEMA_HINT = """
Return ONLY a JSON object with the FULL updated resume content (same schema as before):
{
  "summary": "string",
  "skills_categories": [...],
  "experience_bullets": [...],
  "projects": [...],
  "leadership": [...],
  "certifications": [...],
  "role_type_flags": {...}
}
"""


def fix_loop(
    client: LLMClient,
    content: ResumeContent,
    report: ValidationReport,
    template_tex: str,
    master_profile_text: str,
    tectonic_path: str,
    output_dir: Path,
    max_rounds: int,
    progress_callback: Callable[[str], None] | None = None,
) -> tuple[ResumeContent, str, Path | None, ValidationReport]:
    """
    Iterative fix loop:
    1. Collect failures from ValidationReport.
    2. Send precise failure descriptions to the LLM.
    3. Receive updated ResumeContent.
    4. Recompile and re-validate.
    5. Repeat up to max_rounds.

    Returns (best_content, best_tex, best_pdf_path, best_report).
    """
    best_content = content
    best_tex = fill_template(template_tex, content)
    best_pdf: Path | None = None
    best_report = report

    for round_num in range(1, max_rounds + 1):
        failures = report.failures()
        warnings = report.warnings()
        all_issues = failures + warnings

        if not failures:
            logger.info("Fix loop: all errors resolved after round %d", round_num - 1)
            break

        if progress_callback:
            progress_callback(f"Fix round {round_num}/{max_rounds}: {len(failures)} error(s)")

        logger.info(
            "Fix loop round %d: %d errors, %d warnings",
            round_num, len(failures), len(warnings),
        )

        # Build precise failure descriptions
        failure_text = _format_failures(failures, warnings, content)

        # Ask LLM to fix
        system_prompt = build_system_prompt("resume_content")

        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": (
                    f"The following validation issues were found in the resume. "
                    f"Fix ONLY the issues listed below. Do NOT change other content. "
                    f"Do NOT invent facts not in the Master Profile.\n\n"
                    f"ISSUES TO FIX:\n{failure_text}\n\n"
                    f"CURRENT RESUME CONTENT:\n{content.model_dump_json(indent=2)}\n\n"
                    f"MASTER PROFILE (source of truth):\n{master_profile_text}\n\n"
                    f"{JSON_SCHEMA_HINT}\n\n"
                    "Return ONLY the JSON object with the fixed content."
                ),
            },
        ]

        try:
            new_content = client.chat_json(
                f"fix_round_{round_num}", messages, ResumeContent
            )
        except Exception as exc:
            logger.warning("Fix round %d LLM call failed: %s", round_num, exc)
            break

        # Recompile
        new_tex = fill_template(template_tex, new_content)
        success, new_pdf, compile_log = compile_latex(
            new_tex, tectonic_path=tectonic_path, output_dir=output_dir
        )

        if not success or new_pdf is None:
            logger.warning("Fix round %d compile failed: %s", round_num, compile_log)
            break

        # Re-validate
        from app.core.validator import validate
        from app.core.config import load_layout_config
        new_report = validate(
            new_pdf,
            new_content,
            template_tex,
            new_tex,
            master_profile_text,
        )
        new_report.round_number = round_num

        # Keep the best attempt (fewest errors)
        if len(new_report.failures()) <= len(best_report.failures()):
            best_content = new_content
            best_tex = new_tex
            best_pdf = new_pdf
            best_report = new_report

        content = new_content
        report = new_report

    return best_content, best_tex, best_pdf, best_report


def _format_failures(
    failures: list[CheckResult],
    warnings: list[CheckResult],
    content: ResumeContent,
) -> str:
    """Format validation failures as precise, actionable LLM instructions."""
    lines: list[str] = []

    for f in failures:
        lines.append(f"ERROR [{f.check_id}]: {f.name}")
        lines.append(f"  Detail: {f.detail}")

        # Add actionable guidance for known check types
        if "bullet_wrap" in f.check_id:
            lines.append(
                "  Fix: Shorten this bullet without changing the facts. "
                "Remove filler words, use abbreviations where natural."
            )
        elif "line_fill" in f.check_id:
            lines.append(
                "  Fix: Extend this bullet to fill the line using ONLY facts present in the profile. "
                "Add a tool, outcome, or context detail already mentioned in the profile."
            )
        elif "experience_bullet_count" in f.check_id:
            exp_count = len(content.experience_bullets)
            lines.append(
                f"  Fix: Adjust experience bullets to the required count "
                f"(currently {exp_count}). Do not invent new content."
            )
        elif "proj_bullet_count" in f.check_id:
            lines.append(
                "  Fix: Adjust the number of bullets in this project to match the required count."
            )
        elif "skills_whitelist" in f.check_id:
            lines.append(
                "  Fix: Remove any skill/tool not present in the Master Profile. "
                "Use only exact names or recognized abbreviations from the profile."
            )
        elif "truthfulness" in f.check_id:
            lines.append(
                "  Fix: Remove the metric or number that is not in the Master Profile. "
                "Rephrase the bullet without invented figures."
            )

        lines.append("")

    for w in warnings[:5]:  # Limit warnings shown
        lines.append(f"WARNING [{w.check_id}]: {w.name}")
        lines.append(f"  Detail: {w.detail}")
        lines.append("")

    return "\n".join(lines)
