"""
Verdict / fit analysis (Step 4):
Compares the job description against the Master Profile and returns a verdict.
"""

from __future__ import annotations

import logging

from app.core.llm_client import LLMClient
from app.core.rules_loader import build_system_prompt
from app.core.profile_loader import ParsedProfile, filter_profile_for_llm
from app.models.schemas import VerdictResult, VerdictLevel, JobAnalysis

logger = logging.getLogger(__name__)

JSON_SCHEMA_HINT = """
Return ONLY a JSON object:
{
  "verdict": "STRONGLY APPLY" | "APPLY" | "APPLY WITH CAUTION" | "DON'T APPLY" | "STRONGLY DON'T APPLY",
  "job_role": "string",
  "location": "string",
  "concise_reason": "string (1-2 sentences)",
  "strengths": ["string", ...],
  "gaps": ["string", ...],
  "eligibility_notes": ["string", ...],
  "dimensions": [
    {
      "dimension": "string",
      "assessment": "string",
      "evidence": ["string", ...]
    }
  ]
}

Dimensions to evaluate (A-E):
A. keyword_technology_match - Does the candidate have the required technologies/tools?
B. real_evidence - Are there concrete projects/experience demonstrating the skills?
C. responsibility_match - Can the candidate perform the stated responsibilities?
D. domain_relevance - Is the candidate's background relevant to this industry/domain?
E. eligibility - Education, experience level, location, employment type fit?

IMPORTANT: Base verdict on evidence-based comparison, NOT keyword percentages.
"""

STOP_VERDICTS = {VerdictLevel.DONT_APPLY, VerdictLevel.STRONGLY_DONT_APPLY}


def assess_verdict(
    client: LLMClient,
    jd_text: str,
    job_analysis: JobAnalysis,
    parsed_profile: ParsedProfile,
) -> VerdictResult:
    """
    Step 4: Assess fit and return ONE of five verdict levels.
    """
    logger.info("Assessing fit verdict")

    filtered_profile = filter_profile_for_llm(parsed_profile)
    system_prompt = build_system_prompt("verdict")

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": (
                "Compare the following job description against the candidate's Master Profile "
                "and return a structured fit assessment.\n\n"
                f"{JSON_SCHEMA_HINT}\n\n"
                f"JOB DESCRIPTION:\n\n{jd_text}\n\n"
                f"MASTER PROFILE:\n\n{filtered_profile}\n\n"
                "Return ONLY the JSON object."
            ),
        },
    ]

    result = client.chat_json("verdict", messages, VerdictResult)

    # Override job_role from analysis if LLM left it blank
    if not result.job_role and job_analysis.job_title:
        result.job_role = job_analysis.job_title
    if not result.location and job_analysis.location:
        result.location = job_analysis.location

    logger.info("Verdict: %s", result.verdict)
    return result


def should_stop(verdict: VerdictResult) -> bool:
    """Return True if the pipeline should stop (not generate email/resume)."""
    return verdict.verdict in STOP_VERDICTS
