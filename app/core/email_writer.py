"""
Email writer (Step 7):
Generates a tailored application email only when a legitimate email address is present.
"""

from __future__ import annotations

import logging

from app.core.llm_client import LLMClient
from app.core.rules_loader import build_system_prompt
from app.core.profile_loader import ParsedProfile, load_contact
from app.models.schemas import EmailDraft, ExtractedEmail, VerdictResult

logger = logging.getLogger(__name__)

JSON_SCHEMA_HINT = """
Return ONLY a JSON object:
{
  "subject": "string",
  "body": "string",
  "recipient": "string"
}
"""


def write_email(
    client: LLMClient,
    jd_text: str,
    verdict: VerdictResult,
    emails: list[ExtractedEmail],
    parsed_profile: ParsedProfile,
) -> EmailDraft | None:
    """
    Step 7: Generate a tailored application email.
    Returns None if no legitimate email address is available.
    """
    legitimate_emails = [e for e in emails if e.is_legitimate]

    if not legitimate_emails:
        logger.info("No legitimate email found - skipping email generation")
        return None

    recipient = legitimate_emails[0].address
    contact = parsed_profile.contact or load_contact()

    logger.info("Writing application email to: %s", recipient)

    system_prompt = build_system_prompt("email")

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": (
                f"Write a tailored application email for the following job.\n\n"
                f"{JSON_SCHEMA_HINT}\n\n"
                f"Job Role: {verdict.job_role}\n"
                f"Company: (from JD)\n"
                f"Recipient email: {recipient}\n\n"
                f"Candidate strengths for this role:\n"
                + "\n".join(f"- {s}" for s in verdict.strengths) + "\n\n"
                f"MASTER PROFILE (for context - do not invent details):\n"
                f"Contact: {contact}\n\n"
                f"JOB DESCRIPTION:\n\n{jd_text}\n\n"
                "Return ONLY the JSON object."
            ),
        },
    ]

    draft = client.chat_json("email_writer", messages, EmailDraft)
    draft.recipient = recipient
    logger.info("Email draft generated, subject: %s", draft.subject)
    return draft
