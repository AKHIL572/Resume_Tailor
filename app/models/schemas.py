"""
Pydantic v2 data models for JobTailor.
All LLM outputs are validated against these schemas.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


# ───────────────────────────────────────────────
# Enums
# ───────────────────────────────────────────────

class VerdictLevel(str, Enum):
    STRONGLY_APPLY = "STRONGLY APPLY"
    APPLY = "APPLY"
    APPLY_WITH_CAUTION = "APPLY WITH CAUTION"
    DONT_APPLY = "DON'T APPLY"
    STRONGLY_DONT_APPLY = "STRONGLY DON'T APPLY"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class EmailClassification(str, Enum):
    COMPANY = "company"          # matches company domain
    FREE_PROVIDER = "free"       # gmail, yahoo, outlook, hotmail, etc.
    UNKNOWN = "unknown"


# ───────────────────────────────────────────────
# Step 1: Job Analysis
# ───────────────────────────────────────────────

class RequirementGroup(BaseModel):
    must_have: list[str] = Field(default_factory=list)
    preferred: list[str] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)
    domain_context: list[str] = Field(default_factory=list)


class JobAnalysis(BaseModel):
    company: str = ""
    job_title: str = ""
    location: str = ""
    employment_type: str = ""
    salary: str = ""
    experience_requirement: str = ""
    education_requirement: str = ""
    technical_requirements: list[str] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)
    domain_industry: str = ""
    other_requirements: list[str] = Field(default_factory=list)
    emails_in_jd: list[str] = Field(default_factory=list)
    requirements: RequirementGroup = Field(default_factory=RequirementGroup)
    raw_jd_snippet: str = ""  # first 300 chars for display


# ───────────────────────────────────────────────
# Step 2: Email Extraction
# ───────────────────────────────────────────────

class ExtractedEmail(BaseModel):
    address: str
    classification: EmailClassification = EmailClassification.UNKNOWN
    domain: str = ""
    is_legitimate: bool = True


# ───────────────────────────────────────────────
# Step 3: Genuineness
# ───────────────────────────────────────────────

class GenuinenessSignal(BaseModel):
    signal: str
    reason: str
    severity: str = "medium"  # low / medium / high


class GenuinenessResult(BaseModel):
    risk_level: RiskLevel = RiskLevel.LOW
    signals: list[GenuinenessSignal] = Field(default_factory=list)
    summary: str = ""
    disclaimer: str = (
        "These are potential risk indicators only, not proof of fraud. "
        "Always verify independently before sharing personal information."
    )


# ───────────────────────────────────────────────
# Step 4: Verdict / Fit Analysis
# ───────────────────────────────────────────────

class FitDimension(BaseModel):
    dimension: str  # e.g. "keyword_match", "responsibility_match"
    assessment: str
    evidence: list[str] = Field(default_factory=list)


class VerdictResult(BaseModel):
    verdict: VerdictLevel
    job_role: str
    location: str = ""
    concise_reason: str
    strengths: list[str] = Field(default_factory=list)
    gaps: list[str] = Field(default_factory=list)
    eligibility_notes: list[str] = Field(default_factory=list)
    dimensions: list[FitDimension] = Field(default_factory=list)


# ───────────────────────────────────────────────
# Step 6: How to Apply
# ───────────────────────────────────────────────

class HowToApply(BaseModel):
    emails: list[ExtractedEmail] = Field(default_factory=list)
    application_link: str = ""
    search_notes: str = ""
    instruction: str = ""


# ───────────────────────────────────────────────
# Step 7: Email Draft
# ───────────────────────────────────────────────

class EmailDraft(BaseModel):
    subject: str
    body: str
    recipient: str = ""


# ───────────────────────────────────────────────
# Step 8: Resume Content
# ───────────────────────────────────────────────

class SkillCategory(BaseModel):
    title: str
    items: list[str] = Field(default_factory=list)


class ProjectContent(BaseModel):
    name: str
    bullets: list[str] = Field(default_factory=list)


class LeadershipContent(BaseModel):
    role: str
    organization: str = ""
    bullet: str = ""


class ResumeContent(BaseModel):
    summary: str = ""
    skills_categories: list[SkillCategory] = Field(default_factory=list)
    experience_bullets: list[str] = Field(default_factory=list)
    projects: list[ProjectContent] = Field(default_factory=list)
    leadership: list[LeadershipContent] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    role_type_flags: dict[str, bool] = Field(default_factory=dict)
    target_role: str = ""


# ───────────────────────────────────────────────
# Validation Report
# ───────────────────────────────────────────────

class CheckResult(BaseModel):
    check_id: str
    name: str
    passed: bool
    detail: str = ""
    severity: str = "error"  # "error" | "warning" | "info"


class ValidationReport(BaseModel):
    passed: bool
    checks: list[CheckResult] = Field(default_factory=list)
    page_count: int = 0
    unused_space_mm: float = 0.0
    round_number: int = 0

    def failures(self) -> list[CheckResult]:
        return [c for c in self.checks if not c.passed and c.severity == "error"]

    def warnings(self) -> list[CheckResult]:
        return [c for c in self.checks if not c.passed and c.severity == "warning"]


# ───────────────────────────────────────────────
# Final aggregated pipeline result
# ───────────────────────────────────────────────

class PipelineResult(BaseModel):
    job_analysis: Optional[JobAnalysis] = None
    genuineness: Optional[GenuinenessResult] = None
    verdict: Optional[VerdictResult] = None
    how_to_apply: Optional[HowToApply] = None
    email_draft: Optional[EmailDraft] = None
    resume_content: Optional[ResumeContent] = None
    resume_tex: str = ""
    resume_pdf_path: str = ""
    validation_report: Optional[ValidationReport] = None
    output_dir: str = ""
    stopped_early: bool = False  # True if DON'T APPLY / STRONGLY DON'T APPLY
