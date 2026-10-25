"""
Job analysis step: sends the JD to the LLM and returns a structured JobAnalysis.
"""

from __future__ import annotations

import logging

from app.core.llm_client import LLMClient
from app.core.rules_loader import build_system_prompt
from app.models.schemas import JobAnalysis

logger = logging.getLogger(__name__)

JSON_SCHEMA_HINT = """
Return ONLY a JSON object with these fields:
{
  "company": "string",
  "job_title": "string",
  "location": "string",
  "employment_type": "string",
  "salary": "string",
  "experience_requirement": "string",
  "education_requirement": "string",
  "technical_requirements": ["string", ...],
  "responsibilities": ["string", ...],
  "domain_industry": "string",
  "other_requirements": ["string", ...],
  "emails_in_jd": ["string", ...],
  "requirements": {
    "must_have": ["string", ...],
    "preferred": ["string", ...],
    "responsibilities": ["string", ...],
    "domain_context": ["string", ...]
  }
}
"""


def analyze_job(client: LLMClient, jd_text: str) -> JobAnalysis:
    """
    Step 1: Parse and categorize the job description.
    Returns a validated JobAnalysis object.
    """
    logger.info("Starting job analysis")

    system_prompt = build_system_prompt("job_analysis")

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": (
                f"Analyze the following job description and return a structured JSON object.\n\n"
                f"{JSON_SCHEMA_HINT}\n\n"
                f"JOB DESCRIPTION:\n\n{jd_text}\n\n"
                "Return ONLY the JSON object, no markdown, no explanation."
            ),
        },
    ]

    result = client.chat_json("job_analysis", messages, JobAnalysis)
    result.raw_jd_snippet = jd_text[:300]
    logger.info("Job analysis complete: company=%s, title=%s", result.company, result.job_title)
    return result
