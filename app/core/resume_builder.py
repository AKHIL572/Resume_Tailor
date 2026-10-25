"""
Resume content generation (Step 8):
Generates tailored resume content from the Master Profile and JD.
"""

from __future__ import annotations

import logging

from app.core.llm_client import LLMClient
from app.core.rules_loader import build_system_prompt
from app.core.profile_loader import ParsedProfile, filter_profile_for_llm
from app.models.schemas import ResumeContent, JobAnalysis, VerdictResult

logger = logging.getLogger(__name__)

JSON_SCHEMA_HINT = """
Return ONLY a JSON object:
{
  "summary": "string (3-4 lines, NO bullet points, professional prose)",
  "skills_categories": [
    {"title": "string", "items": ["string", ...]}
  ],
  "experience_bullets": ["string", ...],
  "projects": [
    {"name": "string", "bullets": ["string", ...]}
  ],
  "leadership": [
    {"role": "string", "organization": "string", "bullet": "string"}
  ],
  "certifications": ["string", ...],
  "role_type_flags": {
    "is_qa_role": false,
    "two_projects": false,
    "three_projects": true
  }
}

CRITICAL RULES:
- Every bullet MUST start with a strong action verb.
- Every claim MUST be directly supported by something in the Master Profile.
- Do NOT invent metrics, numbers, or technologies not in the profile.
- Bullets must be written to fit on ONE line (approximately 90-100 characters max).
- The internship project appears ONLY in experience_bullets, NOT in projects.
- Project 1 must NEVER appear anywhere in the output.
"""


def generate_resume_content(
    client: LLMClient,
    jd_text: str,
    job_analysis: JobAnalysis,
    verdict: VerdictResult,
    parsed_profile: ParsedProfile,
) -> ResumeContent:
    """
    Step 8: Generate tailored resume content from the Master Profile.
    """
    logger.info("Generating tailored resume content")

    filtered_profile = filter_profile_for_llm(parsed_profile)
    system_prompt = build_system_prompt("resume_content")

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": (
                "Generate tailored resume content for this job application.\n\n"
                f"{JSON_SCHEMA_HINT}\n\n"
                f"Target Role: {verdict.job_role}\n"
                f"Candidate Strengths: {', '.join(verdict.strengths)}\n"
                f"Gaps to be aware of: {', '.join(verdict.gaps)}\n\n"
                f"JOB DESCRIPTION:\n\n{jd_text}\n\n"
                f"MASTER PROFILE (use ONLY information from here):\n\n{filtered_profile}\n\n"
                "Return ONLY the JSON object."
            ),
        },
    ]

    result = client.chat_json("resume_content", messages, ResumeContent)
    logger.info(
        "Resume content generated: %d skills categories, %d experience bullets, %d projects",
        len(result.skills_categories),
        len(result.experience_bullets),
        len(result.projects),
    )
    return result
