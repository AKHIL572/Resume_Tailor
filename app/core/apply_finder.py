"""
Email extraction (Step 2):
- Regex extraction from JD text
- Classification: company domain vs free provider vs unknown
- Merges with any emails found by the LLM in job analysis
"""

from __future__ import annotations

import logging
import re

from app.models.schemas import ExtractedEmail, EmailClassification

logger = logging.getLogger(__name__)

# Common free email providers
FREE_PROVIDERS = {
    "gmail.com", "yahoo.com", "yahoo.co.uk", "yahoo.in",
    "outlook.com", "hotmail.com", "hotmail.co.uk",
    "live.com", "live.co.uk", "icloud.com", "me.com",
    "aol.com", "protonmail.com", "proton.me",
    "zoho.com", "yandex.com", "yandex.ru",
    "mail.com", "gmx.com", "gmx.net",
    "inbox.com", "rediffmail.com", "rocketmail.com",
}

# Regex to find email addresses
EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b"
)


def extract_emails(
    jd_text: str,
    llm_emails: list[str] | None = None,
    company_name: str = "",
) -> list[ExtractedEmail]:
    """
    Extract and classify email addresses from job description text.

    Args:
        jd_text: Full job description
        llm_emails: Emails already found by the LLM in job analysis
        company_name: Company name to help guess if a domain is company-owned

    Returns:
        Deduplicated list of ExtractedEmail objects
    """
    found_addresses: set[str] = set()

    # Regex extraction
    for match in EMAIL_PATTERN.finditer(jd_text):
        found_addresses.add(match.group().lower())

    # Merge LLM-found emails
    if llm_emails:
        for addr in llm_emails:
            if addr and EMAIL_PATTERN.match(addr.strip()):
                found_addresses.add(addr.strip().lower())

    results: list[ExtractedEmail] = []
    for addr in sorted(found_addresses):
        classified = _classify_email(addr, company_name)
        results.append(classified)

    logger.debug("Extracted %d email(s) from JD", len(results))
    return results


def _classify_email(address: str, company_name: str = "") -> ExtractedEmail:
    """Classify a single email address."""
    parts = address.split("@", 1)
    if len(parts) != 2:
        return ExtractedEmail(
            address=address,
            classification=EmailClassification.UNKNOWN,
            domain="",
            is_legitimate=False,
        )

    domain = parts[1].lower()

    is_free = (
        domain in FREE_PROVIDERS
        or any(domain.startswith(p) for p in ("yahoo.", "gmail.", "hotmail.", "outlook.", "proton.", "zoho."))
    )
    if is_free:
        classification = EmailClassification.FREE_PROVIDER
        # A company using a free email for hiring is a risk signal
        is_legitimate = False
    else:
        classification = EmailClassification.COMPANY
        is_legitimate = True

    return ExtractedEmail(
        address=address,
        classification=classification,
        domain=domain,
        is_legitimate=is_legitimate,
    )


def get_legitimate_emails(emails: list[ExtractedEmail]) -> list[ExtractedEmail]:
    """Return only emails classified as company (legitimate) addresses."""
    return [e for e in emails if e.is_legitimate and e.classification == EmailClassification.COMPANY]
