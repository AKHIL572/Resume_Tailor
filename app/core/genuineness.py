"""
Genuineness assessment (Step 3):
Combines rule-based heuristic checks with an LLM summary.
Never claims certainty - outputs risk indicators only.
"""

from __future__ import annotations

import logging
import re
from typing import Optional

from app.core.llm_client import LLMClient
from app.core.rules_loader import build_system_prompt
from app.models.schemas import (
    GenuinenessResult,
    GenuinenessSignal,
    RiskLevel,
    EmailClassification,
    ExtractedEmail,
    JobAnalysis,
)

logger = logging.getLogger(__name__)

# Patterns that suggest scam / low-quality postings
URGENCY_PATTERNS = re.compile(
    r"\b(urgent|immediately|asap|as soon as possible|right away|"
    r"limited time|act now|apply today|don.t miss|"
    r"last chance|hurry)\b",
    re.IGNORECASE,
)
FEE_PATTERNS = re.compile(
    r"\b(registration fee|processing fee|training fee|equipment fee|"
    r"deposit|advance payment|upfront|background check fee)\b",
    re.IGNORECASE,
)
WHATSAPP_PATTERNS = re.compile(
    r"\b(whatsapp|telegram|signal|wechat)\s*(me|us|only|contact|number|chat)\b",
    re.IGNORECASE,
)
UNREALISTIC_SALARY_PATTERN = re.compile(
    r"\$\s*([0-9]{1,3}(?:,?[0-9]{3})*)\s*(?:per\s*(?:week|day|hour))?\s*"
    r"(?:/\s*(?:week|day|hour))?",
    re.IGNORECASE,
)
VAGUE_COMPANY_PATTERNS = re.compile(
    r"\b(a reputed company|leading company|confidential company|"
    r"anonymous client|name on selection|disclosed on interview)\b",
    re.IGNORECASE,
)

JSON_SCHEMA_HINT = """
Return ONLY a JSON object:
{
  "risk_level": "LOW" | "MEDIUM" | "HIGH",
  "signals": [
    {"signal": "string", "reason": "string", "severity": "low"|"medium"|"high"}
  ],
  "summary": "string"
}
"""


def assess_genuineness(
    client: LLMClient,
    jd_text: str,
    job_analysis: JobAnalysis,
    emails: list[ExtractedEmail],
) -> GenuinenessResult:
    """
    Step 3: Assess whether the job posting appears genuine.
    Combines rule-based signals with an LLM summary.
    """
    logger.info("Assessing job genuineness")

    # ── Rule-based signals ──────────────────────────────────────────────
    rule_signals: list[GenuinenessSignal] = []

    # Fee requests
    if FEE_PATTERNS.search(jd_text):
        rule_signals.append(GenuinenessSignal(
            signal="Fee request detected",
            reason="Legitimate employers do not charge fees for applications or training.",
            severity="high",
        ))

    # Free email for company contact
    free_emails = [e for e in emails if e.classification == EmailClassification.FREE_PROVIDER]
    if free_emails:
        addrs = ", ".join(e.address for e in free_emails)
        rule_signals.append(GenuinenessSignal(
            signal=f"Free email provider used: {addrs}",
            reason="A company using a free email service (Gmail, Yahoo, etc.) for official hiring communications is unusual.",
            severity="high",
        ))

    # WhatsApp/Telegram only contact
    if WHATSAPP_PATTERNS.search(jd_text):
        rule_signals.append(GenuinenessSignal(
            signal="Messaging-app-only contact method",
            reason="Genuine employers typically use professional channels; insistence on WhatsApp/Telegram can indicate a scam.",
            severity="medium",
        ))

    # Urgency pressure
    if URGENCY_PATTERNS.search(jd_text):
        rule_signals.append(GenuinenessSignal(
            signal="Urgency/pressure language detected",
            reason="High-pressure urgency wording is a common tactic in fraudulent postings.",
            severity="medium",
        ))

    # Vague company
    if VAGUE_COMPANY_PATTERNS.search(jd_text) or not job_analysis.company.strip():
        rule_signals.append(GenuinenessSignal(
            signal="Company identity unclear or withheld",
            reason="Legitimate postings typically name the employer. Anonymous companies make verification impossible.",
            severity="medium",
        ))

    # Domain mismatch (emails found but domain doesn't match company)
    company_lower = job_analysis.company.lower().replace(" ", "")
    company_emails = [e for e in emails if e.classification == EmailClassification.COMPANY]
    if company_lower and company_emails:
        for e in company_emails:
            domain_base = e.domain.split(".")[0]
            if company_lower and domain_base not in company_lower and company_lower not in domain_base:
                rule_signals.append(GenuinenessSignal(
                    signal=f"Email domain '{e.domain}' may not match company '{job_analysis.company}'",
                    reason="A mismatch between the email domain and the stated company name can indicate impersonation.",
                    severity="medium",
                ))

    # ── Optional: WHOIS domain age ──────────────────────────────────────
    _try_whois_check(company_emails, rule_signals)

    # ── LLM holistic assessment ─────────────────────────────────────────
    system_prompt = build_system_prompt("source_of_truth")
    rule_signal_text = "\n".join(
        f"- [{s.severity.upper()}] {s.signal}: {s.reason}" for s in rule_signals
    ) or "No automatic rule-based signals triggered."

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": (
                "Assess whether this job posting appears genuine. "
                "You are NOT claiming certainty - only identifying risk indicators.\n\n"
                f"Rule-based signals already detected:\n{rule_signal_text}\n\n"
                f"{JSON_SCHEMA_HINT}\n\n"
                f"JOB DESCRIPTION:\n\n{jd_text}\n\n"
                "Identify any additional risk signals not already listed. "
                "Return ONLY the JSON object."
            ),
        },
    ]

    try:
        llm_result = client.chat_json("genuineness", messages, GenuinenessResult)
        # Merge rule-based signals with LLM signals
        all_signals = rule_signals + llm_result.signals
        # Deduplicate by signal text
        seen: set[str] = set()
        deduped: list[GenuinenessSignal] = []
        for s in all_signals:
            key = s.signal.lower()[:60]
            if key not in seen:
                seen.add(key)
                deduped.append(s)

        # Compute final risk level
        final_risk = _compute_risk_level(deduped, llm_result.risk_level)

        return GenuinenessResult(
            risk_level=final_risk,
            signals=deduped,
            summary=llm_result.summary,
        )

    except Exception as exc:
        logger.warning("LLM genuineness assessment failed, using rule-based only: %s", exc)
        risk = _compute_risk_level(rule_signals, RiskLevel.LOW)
        return GenuinenessResult(
            risk_level=risk,
            signals=rule_signals,
            summary=(
                "Automated assessment based on rule-based signals only "
                "(LLM assessment unavailable)."
            ),
        )


def _compute_risk_level(
    signals: list[GenuinenessSignal],
    llm_level: RiskLevel,
) -> RiskLevel:
    """Compute final risk level from signals and LLM assessment."""
    high_count = sum(1 for s in signals if s.severity == "high")
    medium_count = sum(1 for s in signals if s.severity == "medium")

    if high_count >= 1 or llm_level == RiskLevel.HIGH:
        return RiskLevel.HIGH
    if medium_count >= 2 or llm_level == RiskLevel.MEDIUM:
        return RiskLevel.MEDIUM
    return RiskLevel.LOW


def _try_whois_check(
    company_emails: list[ExtractedEmail],
    signals: list[GenuinenessSignal],
) -> None:
    """Optional WHOIS domain-age check. Silently skips if unavailable."""
    try:
        import whois  # type: ignore
        for email in company_emails[:1]:  # Check first company domain only
            domain = email.domain
            try:
                w = whois.whois(domain)
                created = w.creation_date
                if created:
                    if isinstance(created, list):
                        created = created[0]
                    from datetime import datetime, timezone
                    age_days = (datetime.now(timezone.utc) - created.replace(tzinfo=timezone.utc)).days
                    if age_days < 180:
                        signals.append(GenuinenessSignal(
                            signal=f"Domain '{domain}' is relatively new ({age_days} days old)",
                            reason="Newly registered domains are sometimes used in fraudulent postings.",
                            severity="medium",
                        ))
            except Exception:
                pass
    except ImportError:
        pass
