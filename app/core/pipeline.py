"""
Main pipeline orchestrator (Steps 1-14).
Runs in a background thread; emits progress signals to the UI.
"""

from __future__ import annotations

import json
import logging
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Callable

from app.core.apply_finder import extract_emails, get_legitimate_emails
from app.core.config import load_config, load_layout_config
from app.core.data_dirs import data_path
from app.core.email_writer import write_email
from app.core.fixer import fix_loop
from app.core.genuineness import assess_genuineness
from app.core.job_analyzer import analyze_job
from app.core.latex_utils import compile_latex, fill_template
from app.core.llm_client import LLMClient, get_api_key
from app.core.profile_loader import (
    load_profile,
    parse_profile,
    filter_profile_for_llm,
    load_contact,
)
from app.core.resume_builder import generate_resume_content
from app.core.rules_loader import build_system_prompt
from app.core.validator import validate
from app.core.verdict import assess_verdict, should_stop
from app.models.schemas import (
    HowToApply,
    PipelineResult,
    ResumeContent,
    ValidationReport,
    EmailDraft,
)

logger = logging.getLogger(__name__)

# Tavily search (optional)
try:
    from tavily import TavilyClient  # type: ignore
    HAS_TAVILY = True
except ImportError:
    HAS_TAVILY = False


class Pipeline:
    """
    Orchestrates the full JobTailor pipeline.
    Accepts a progress callback for live step updates.
    Cancelled via the cancel_flag callable.
    """

    def __init__(
        self,
        jd_text: str,
        progress_callback: Callable[[str], None] | None = None,
        cancel_flag: Callable[[], bool] | None = None,
    ):
        self.jd_text = jd_text
        self.progress = progress_callback or (lambda msg: None)
        self.is_cancelled = cancel_flag or (lambda: False)
        self.config = load_config()
        self.layout_cfg = load_layout_config()

        # Build LLM client from config
        provider = self.config.get("provider", "ollama")
        api_key = get_api_key(provider) if provider != "ollama" else "ollama"
        self.client = LLMClient(
            provider=provider,
            base_url=self.config.get("base_url", "http://localhost:11434/v1"),
            model=self.config.get("model", "llama3.1:8b"),
            api_key=api_key,
            temperature=float(self.config.get("temperature", 0.3)),
            max_retries=int(self.config.get("max_retries", 3)),
        )

    # ------------------------------------------------------------------

    def run(self) -> PipelineResult:
        """Execute the full pipeline. Returns PipelineResult."""
        result = PipelineResult()

        # ── Load master profile ───────────────────────────────────────
        self._step("Loading Master Profile")
        raw_profile = load_profile()
        if not raw_profile.strip():
            raise RuntimeError(
                "Master Profile is empty. Please import your profile in the "
                "Master Profile tab before running the pipeline."
            )

        p1_id = self.config.get("project1_identifier", "Project 1")
        intern_id = self.config.get("internship_project_identifier", "Project 6")
        parsed_profile = parse_profile(raw_profile, p1_id, intern_id)

        # ── Load template ─────────────────────────────────────────────
        template_path = data_path("templates", "resume_template.tex")
        if not template_path.exists():
            raise RuntimeError(
                "No LaTeX template found. Please import your template in the Template tab."
            )
        template_tex = template_path.read_text(encoding="utf-8")

        if self.is_cancelled():
            raise InterruptedError("Cancelled by user")

        # ── Step 1: Job analysis ──────────────────────────────────────
        self._step("Analyzing job description")
        job_analysis = analyze_job(self.client, self.jd_text)
        result.job_analysis = job_analysis

        if self.is_cancelled():
            raise InterruptedError("Cancelled by user")

        # ── Step 2: Email extraction ──────────────────────────────────
        self._step("Extracting contact emails")
        emails = extract_emails(
            self.jd_text,
            llm_emails=job_analysis.emails_in_jd,
            company_name=job_analysis.company,
        )

        # ── Step 3: Genuineness ───────────────────────────────────────
        self._step("Assessing job genuineness")
        genuineness = assess_genuineness(self.client, self.jd_text, job_analysis, emails)
        result.genuineness = genuineness

        if self.is_cancelled():
            raise InterruptedError("Cancelled by user")

        # ── Step 4: Verdict ───────────────────────────────────────────
        self._step("Assessing fit & generating verdict")
        verdict = assess_verdict(self.client, self.jd_text, job_analysis, parsed_profile)
        result.verdict = verdict

        # ── Step 5: Stop check ────────────────────────────────────────
        if should_stop(verdict):
            logger.info("Verdict %s: stopping pipeline early", verdict.verdict)
            result.stopped_early = True
            self._save_output(result, job_analysis.company, verdict.job_role)
            return result

        # ── Step 6: How to apply ──────────────────────────────────────
        self._step("Finding application details")
        how_to_apply = self._find_how_to_apply(job_analysis, emails)
        result.how_to_apply = how_to_apply

        if self.is_cancelled():
            raise InterruptedError("Cancelled by user")

        # ── Step 7: Email ─────────────────────────────────────────────
        self._step("Writing application email")
        email_draft = write_email(
            self.client, self.jd_text, verdict, emails, parsed_profile
        )
        result.email_draft = email_draft

        if self.is_cancelled():
            raise InterruptedError("Cancelled by user")

        # ── Step 8: Resume content ────────────────────────────────────
        self._step("Generating resume content")
        resume_content = generate_resume_content(
            self.client, self.jd_text, job_analysis, verdict, parsed_profile
        )
        result.resume_content = resume_content

        if self.is_cancelled():
            raise InterruptedError("Cancelled by user")

        # ── Step 9: Build LaTeX ───────────────────────────────────────
        self._step("Building LaTeX")
        filled_tex = fill_template(template_tex, resume_content)

        # ── Step 10: Compile ──────────────────────────────────────────
        self._step("Compiling PDF")
        output_dir = self._make_output_dir(job_analysis.company, verdict.job_role)
        tectonic_path = self.config.get("tectonic_path", "tectonic")

        success, pdf_path, compile_log = compile_latex(
            filled_tex, tectonic_path=tectonic_path, output_dir=output_dir
        )

        if not success or pdf_path is None:
            raise RuntimeError(
                f"LaTeX compilation failed.\n\nCompiler output:\n{compile_log}"
            )

        result.resume_tex = filled_tex
        result.resume_pdf_path = str(pdf_path)

        if self.is_cancelled():
            raise InterruptedError("Cancelled by user")

        # ── Step 11: Validate ─────────────────────────────────────────
        self._step("Validating PDF layout")
        report = validate(
            pdf_path,
            resume_content,
            template_tex,
            filled_tex,
            raw_profile,
            self.layout_cfg,
        )

        if self.is_cancelled():
            raise InterruptedError("Cancelled by user")

        # ── Step 12: Fix loop ─────────────────────────────────────────
        max_rounds = int(self.layout_cfg.get("max_fix_rounds", 5))
        if not report.passed and max_rounds > 0:
            self._step("Running fix loop")
            resume_content, filled_tex, new_pdf, report = fix_loop(
                client=self.client,
                content=resume_content,
                report=report,
                template_tex=template_tex,
                master_profile_text=raw_profile,
                tectonic_path=tectonic_path,
                output_dir=output_dir,
                max_rounds=max_rounds,
                progress_callback=self.progress,
            )
            if new_pdf:
                pdf_path = new_pdf
                result.resume_pdf_path = str(pdf_path)
            result.resume_tex = filled_tex
            result.resume_content = resume_content

        if self.is_cancelled():
            raise InterruptedError("Cancelled by user")

        # ── Step 13: Final review ─────────────────────────────────────
        self._step("Final HR review pass")
        try:
            resume_content, filled_tex, report = self._final_review(
                resume_content, filled_tex, template_tex, raw_profile,
                pdf_path, output_dir, tectonic_path, report
            )
            result.resume_tex = filled_tex
            result.resume_content = resume_content
            if pdf_path:
                result.resume_pdf_path = str(pdf_path)
        except Exception as exc:
            logger.warning("Final review pass failed (non-fatal): %s", exc)

        result.validation_report = report

        # ── Step 14: Save outputs ─────────────────────────────────────
        self._step("Saving outputs")
        self._save_output(result, job_analysis.company, verdict.job_role, output_dir)

        # Write to history DB
        self._write_history(result, job_analysis, verdict)

        self._step("Done ✓")
        return result

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _step(self, msg: str) -> None:
        logger.info("Pipeline step: %s", msg)
        self.progress(msg)

    def _find_how_to_apply(self, job_analysis, emails) -> HowToApply:
        """Step 6: Find application method."""
        legitimate = get_legitimate_emails(emails)
        application_link = ""
        search_notes = ""

        # Try Tavily if no emails found
        if not legitimate and self.config.get("tavily_enabled", False) and HAS_TAVILY:
            try:
                from app.core.llm_client import get_api_key as gak
                tavily_key = gak("tavily")
                if tavily_key:
                    tc = TavilyClient(api_key=tavily_key)
                    query = f"{job_analysis.company} {job_analysis.job_title} job application"
                    resp = tc.search(query, max_results=3)
                    urls = [r.get("url", "") for r in resp.get("results", []) if r.get("url")]
                    if urls:
                        application_link = urls[0]
                        search_notes = f"Web search found: {', '.join(urls[:3])}"
            except Exception as exc:
                logger.warning("Tavily search failed: %s", exc)
                search_notes = f"Web search failed: {exc}"
        elif not legitimate:
            search_notes = (
                "No application email found in the JD. "
                "Check the official company website or job board posting directly."
            )

        instruction = _build_application_instruction(job_analysis, legitimate)

        return HowToApply(
            emails=emails,
            application_link=application_link,
            search_notes=search_notes,
            instruction=instruction,
        )

    def _final_review(
        self,
        content: ResumeContent,
        tex: str,
        template_tex: str,
        raw_profile: str,
        pdf_path: Path,
        output_dir: Path,
        tectonic_path: str,
        report: ValidationReport,
    ) -> tuple[ResumeContent, str, ValidationReport]:
        """Step 13: Second LLM pass as HR reviewer."""
        system_prompt = build_system_prompt("final_review")
        all_bullets = list(content.experience_bullets)
        for proj in content.projects:
            all_bullets.extend(proj.bullets)

        bullets_text = "\n".join(f"- {b}" for b in all_bullets)

        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": (
                    "You are an experienced HR reviewer. Review the following resume bullets "
                    "for: unsupported claims, invented metrics, repeated wording, and generic phrases.\n\n"
                    "For each bullet that fails, provide the bullet index (0-based) and the issue.\n\n"
                    f"RESUME BULLETS:\n{bullets_text}\n\n"
                    f"MASTER PROFILE (source of truth):\n{raw_profile[:3000]}\n\n"
                    "Return a JSON object:\n"
                    '{"issues": [{"index": 0, "bullet": "...", "issue": "...", "fix": "..."}]}\n'
                    "If no issues, return: {\"issues\": []}"
                ),
            },
        ]

        from pydantic import BaseModel

        class IssueItem(BaseModel):
            index: int
            bullet: str = ""
            issue: str
            fix: str = ""

        class ReviewResult(BaseModel):
            issues: list[IssueItem] = []

        review = self.client.chat_json("final_review", messages, ReviewResult)

        if not review.issues:
            logger.info("Final review: no issues found")
            return content, tex, report

        # Apply fixes
        logger.info("Final review: %d issue(s) to fix", len(review.issues))
        exp_count = len(content.experience_bullets)
        for issue in review.issues:
            idx = issue.index
            fix_text = issue.fix.strip()
            if not fix_text:
                continue
            if idx < exp_count:
                content.experience_bullets[idx] = fix_text
            else:
                proj_idx = idx - exp_count
                for proj in content.projects:
                    if proj_idx < len(proj.bullets):
                        proj.bullets[proj_idx] = fix_text
                        break
                    proj_idx -= len(proj.bullets)

        # Recompile after fixes
        new_tex = fill_template(template_tex, content)
        success, new_pdf, _ = compile_latex(
            new_tex, tectonic_path=tectonic_path, output_dir=output_dir
        )
        if success and new_pdf:
            new_report = validate(new_pdf, content, template_tex, new_tex, raw_profile)
            return content, new_tex, new_report

        return content, tex, report

    def _make_output_dir(self, company: str, role: str) -> Path:
        """Create a timestamped output directory."""
        safe_company = re.sub(r"[^\w\-]", "_", company)[:30]
        safe_role = re.sub(r"[^\w\-]", "_", role)[:30]
        date_str = datetime.now().strftime("%Y%m%d_%H%M")
        folder_name = f"{date_str}_{safe_company}_{safe_role}"
        out_dir = data_path("output", folder_name)
        out_dir.mkdir(parents=True, exist_ok=True)
        return out_dir

    def _save_output(
        self,
        result: PipelineResult,
        company: str,
        role: str,
        output_dir: Path | None = None,
    ) -> None:
        """Write output files to the output directory."""
        if output_dir is None:
            output_dir = self._make_output_dir(company, role)
        result.output_dir = str(output_dir)

        # Save analysis JSON
        analysis_data = {}
        if result.job_analysis:
            analysis_data["job_analysis"] = result.job_analysis.model_dump()
        if result.genuineness:
            analysis_data["genuineness"] = result.genuineness.model_dump()
        if result.verdict:
            analysis_data["verdict"] = result.verdict.model_dump()

        (output_dir / "analysis.json").write_text(
            json.dumps(analysis_data, indent=2, default=str), encoding="utf-8"
        )

        # Save email
        if result.email_draft:
            email_text = (
                f"To: {result.email_draft.recipient}\n"
                f"Subject: {result.email_draft.subject}\n\n"
                f"{result.email_draft.body}"
            )
            (output_dir / "email.txt").write_text(email_text, encoding="utf-8")

        # Save resume.tex
        if result.resume_tex:
            (output_dir / "resume.tex").write_text(result.resume_tex, encoding="utf-8")

        # PDF is already saved by compile_latex

        # Save LLM log
        log_text = "\n".join(r.to_log_text() for r in self.client.log_records)
        (output_dir / "llm_log.txt").write_text(log_text, encoding="utf-8")

    def _write_history(self, result: PipelineResult, job_analysis, verdict) -> None:
        """Write a record to the history SQLite database."""
        try:
            from app.core.history import write_history_entry
            write_history_entry(result, job_analysis, verdict)
        except Exception as exc:
            logger.warning("Failed to write history entry: %s", exc)


def _build_application_instruction(job_analysis, legitimate_emails) -> str:
    """Build a human-readable application instruction."""
    if legitimate_emails:
        addrs = ", ".join(e.address for e in legitimate_emails)
        return f"Apply by email to: {addrs}"
    if job_analysis.company:
        return f"Visit {job_analysis.company}'s official website or careers page to apply."
    return "Check the original job posting source for application instructions."
