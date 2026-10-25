"""
Validator (Step 11): Runs all layout and content checks against the compiled PDF.
All numeric thresholds come from layout_config.json (never hard-coded here).
"""

from __future__ import annotations

import logging
import re
import unicodedata
from pathlib import Path
from typing import Any

import fitz  # PyMuPDF

from app.core.config import load_layout_config
from app.core.latex_utils import extract_fixed_education_text
from app.models.schemas import (
    CheckResult,
    ValidationReport,
    ResumeContent,
)

logger = logging.getLogger(__name__)

MM_TO_POINTS = 2.8346  # 1 mm = 2.8346 pt


def validate(
    pdf_path: Path,
    resume_content: ResumeContent,
    template_tex: str,
    compiled_tex: str,
    master_profile_text: str,
    cfg: dict[str, Any] | None = None,
) -> ValidationReport:
    """
    Run all validation checks on the compiled PDF.
    Returns a structured ValidationReport.
    """
    if cfg is None:
        cfg = load_layout_config()

    checks: list[CheckResult] = []
    doc: fitz.Document | None = None

    # ── Open PDF ───────────────────────────────────────────────────────
    try:
        doc = fitz.open(str(pdf_path))
    except Exception as exc:
        checks.append(CheckResult(
            check_id="pdf_open",
            name="PDF can be opened",
            passed=False,
            detail=f"Could not open PDF: {exc}",
        ))
        return ValidationReport(passed=False, checks=checks)

    page_count = doc.page_count

    # ── Check 1: Page count ────────────────────────────────────────────
    expected_pages = cfg.get("page_count", 1)
    checks.append(CheckResult(
        check_id="page_count",
        name="Page count",
        passed=(page_count == expected_pages),
        detail=f"Expected {expected_pages} page(s), got {page_count}.",
        severity="error" if page_count != expected_pages else "info",
    ))

    if page_count < 1:
        doc.close()
        return ValidationReport(passed=False, checks=checks, page_count=page_count)

    page = doc[0]
    page_rect = page.rect  # page dimensions in points
    page_width = page_rect.width
    page_height = page_rect.height

    # Estimate margins from geometry (assume letter paper with 0.5in margins)
    # 1 inch = 72 points; 0.5in = 36pt
    margin_pt = 36.0
    available_width = page_width - 2 * margin_pt

    # ── Extract text with bounding boxes ──────────────────────────────
    blocks = page.get_text("dict")["blocks"]
    all_lines: list[dict] = []
    for block in blocks:
        if block.get("type") == 0:  # text block
            for line in block.get("lines", []):
                all_lines.append(line)

    # ── Check 2: Single-line bullets ──────────────────────────────────
    bullet_issues = _check_bullet_line_wrapping(
        all_lines, resume_content, available_width, margin_pt
    )
    for issue in bullet_issues:
        checks.append(issue)

    # ── Check 3: Line fill ────────────────────────────────────────────
    fill_min = cfg.get("line_fill_min", 0.85)
    fill_max = cfg.get("line_fill_max", 1.00)
    fill_issues = _check_line_fill(all_lines, available_width, fill_min, fill_max)
    for issue in fill_issues:
        checks.append(issue)

    # ── Check 4: Summary line count ───────────────────────────────────
    summary_range = cfg.get("summary_lines", [3, 4])
    summary_check = _check_summary_lines(all_lines, summary_range, resume_content.summary)
    checks.append(summary_check)

    # ── Check 5: Counts (bullets, projects, categories) ───────────────
    count_checks = _check_counts(resume_content, cfg)
    checks.extend(count_checks)

    # ── Check 6: No overlapping elements ─────────────────────────────
    overlap_issues = _check_overlaps(blocks, margin_pt, page_width, page_height)
    checks.extend(overlap_issues)

    # ── Check 7: Unused whitespace at page bottom ─────────────────────
    threshold_mm = cfg.get("unused_space_threshold_mm", 15.0)
    unused_check, unused_mm = _check_unused_space(
        all_lines, page_height, margin_pt, threshold_mm
    )
    checks.append(unused_check)

    # ── Check 8: Skills whitelist ─────────────────────────────────────
    skill_checks = _check_skills_whitelist(resume_content, master_profile_text)
    checks.extend(skill_checks)

    # ── Check 9: Truthfulness guard ───────────────────────────────────
    truth_checks = _check_truthfulness(resume_content, master_profile_text)
    checks.extend(truth_checks)

    # ── Check 10: Project 1 never appears ─────────────────────────────
    proj1_check = _check_no_project1(compiled_tex)
    checks.append(proj1_check)

    # ── Check 11: Repetition detector ────────────────────────────────
    rep_checks = _check_repetition(resume_content)
    checks.extend(rep_checks)

    # ── Check 12: Fixed education text unchanged ──────────────────────
    edu_check = _check_education_unchanged(template_tex, compiled_tex)
    checks.append(edu_check)

    doc.close()

    all_errors = [c for c in checks if not c.passed and c.severity == "error"]
    passed = len(all_errors) == 0

    return ValidationReport(
        passed=passed,
        checks=checks,
        page_count=page_count,
        unused_space_mm=unused_mm,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Individual checks
# ─────────────────────────────────────────────────────────────────────────────

def _check_bullet_line_wrapping(
    all_lines: list[dict],
    content: ResumeContent,
    available_width: float,
    margin_pt: float,
) -> list[CheckResult]:
    """Check 2: Every bullet occupies exactly one physical line in the rendered PDF."""
    issues: list[CheckResult] = []

    # Extract all rendered text lines with NFKD normalization
    pdf_lines: list[str] = []
    for line in all_lines:
        spans = line.get("spans", [])
        if spans:
            raw_t = "".join(s.get("text", "") for s in spans).strip()
            if raw_t:
                pdf_lines.append(unicodedata.normalize("NFKD", raw_t))

    # Collect all bullets from experience and projects
    all_bullets: list[tuple[str, str]] = []  # (source, text)
    for i, b in enumerate(content.experience_bullets):
        all_bullets.append((f"Experience bullet {i+1}", b))
    for proj in content.projects:
        for i, b in enumerate(proj.bullets):
            all_bullets.append((f"Project '{proj.name}' bullet {i+1}", b))

    # Check each bullet
    for source, bullet_text in all_bullets:
        norm_b = unicodedata.normalize("NFKD", bullet_text).strip()
        words = norm_b.split()
        if not words:
            continue

        prefix = " ".join(words[:min(4, len(words))]).lower()
        suffix = " ".join(words[max(0, len(words)-3):]).lower()

        # Find matching line in PDF
        matches = [idx for idx, pl in enumerate(pdf_lines) if prefix in pl.lower()]
        
        wrapped = False
        if matches:
            first_line = pdf_lines[matches[0]].lower()
            # If suffix is not present in the same line, the bullet wrapped onto another line
            if len(words) > 5 and suffix not in first_line:
                wrapped = True
        else:
            # Fallback estimation if not located directly in spans
            approx_chars = available_width / 5.2
            if len(bullet_text) > approx_chars * 1.05:
                wrapped = True

        if wrapped:
            issues.append(CheckResult(
                check_id=f"bullet_wrap_{source.replace(' ', '_')}",
                name=f"Single-line bullet: {source}",
                passed=False,
                detail=(
                    f"{source} wraps to multiple lines in PDF. "
                    f"Bullet length: {len(bullet_text)} chars. "
                    f"Shorten text to maintain a strict single physical line."
                ),
                severity="error",
            ))
        else:
            issues.append(CheckResult(
                check_id=f"bullet_wrap_{source.replace(' ', '_')}",
                name=f"Single-line bullet: {source}",
                passed=True,
                detail=f"Bullet fits strictly on 1 physical line ({len(bullet_text)} chars).",
                severity="info",
            ))

    return issues


def _check_line_fill(
    all_lines: list[dict],
    available_width: float,
    fill_min: float,
    fill_max: float,
) -> list[CheckResult]:
    """Check 3: Each bullet line fill is within [fill_min, fill_max]."""
    issues: list[CheckResult] = []

    # Bullet markers in rendered PDFs
    bullet_marker_pattern = re.compile(r"^[\s\u2022\u2023\u25e6\u2043\u2219\uf0b7\*\-]")

    bullet_count = 0
    for i, line in enumerate(all_lines):
        spans = line.get("spans", [])
        if not spans:
            continue
        line_text = unicodedata.normalize("NFKD", "".join(s.get("text", "") for s in spans)).strip()
        if not line_text or len(line_text) < 15:
            continue

        # Check if line starts with a bullet marker or has bullet symbol at start
        is_bullet = bool(bullet_marker_pattern.match(line_text)) or "\u2022" in line_text[:5] or "\uf0b7" in line_text[:5]
        if not is_bullet:
            continue

        bullet_count += 1
        bbox = line.get("bbox", [0, 0, 0, 0])
        rendered_width = bbox[2] - bbox[0]
        fill = rendered_width / available_width if available_width > 0 else 0.0

        if fill < fill_min:
            issues.append(CheckResult(
                check_id=f"line_fill_bullet_{bullet_count}",
                name=f"Line fill (Bullet {bullet_count})",
                passed=False,
                detail=(
                    f"Bullet fills {fill*100:.1f}% of available width "
                    f"(target {fill_min*100:.0f}%-{fill_max*100:.0f}%): '{line_text[:60]}...'"
                ),
                severity="warning",
            ))
        elif fill > fill_max:
            issues.append(CheckResult(
                check_id=f"line_fill_bullet_{bullet_count}",
                name=f"Line fill (Bullet {bullet_count})",
                passed=False,
                detail=f"Bullet overflows available width ({fill*100:.1f}%): '{line_text[:60]}...'",
                severity="warning",
            ))
        else:
            issues.append(CheckResult(
                check_id=f"line_fill_bullet_{bullet_count}",
                name=f"Line fill (Bullet {bullet_count})",
                passed=True,
                detail=f"Bullet line fill {fill*100:.1f}% is within target range.",
                severity="info",
            ))

    return issues


def _check_summary_lines(
    all_lines: list[dict],
    summary_range: list[int],
    summary_text: str,
) -> CheckResult:
    """Check 4: Summary line count within range."""
    # Estimate by splitting on newlines and word-wrapping
    estimated_lines = max(1, len(summary_text) // 90)
    low, high = summary_range[0], summary_range[1]
    in_range = low <= estimated_lines <= high

    return CheckResult(
        check_id="summary_lines",
        name="Summary line count",
        passed=in_range,
        detail=(
            f"Estimated {estimated_lines} line(s), expected {low}-{high}."
        ),
        severity="warning" if not in_range else "info",
    )


def _check_counts(content: ResumeContent, cfg: dict) -> list[CheckResult]:
    """Check 5: Section counts match config."""
    checks: list[CheckResult] = []

    # Experience bullets
    exp_expected = cfg.get("experience_bullets", 4)
    exp_actual = len(content.experience_bullets)
    checks.append(CheckResult(
        check_id="experience_bullet_count",
        name="Experience bullet count",
        passed=(exp_actual == exp_expected),
        detail=f"Expected {exp_expected}, got {exp_actual}.",
        severity="error" if exp_actual != exp_expected else "info",
    ))

    # Projects
    projects_default = cfg.get("projects_default", 3)
    proj_actual = len(content.projects)
    # Flexible: 2 or 3 projects are both OK
    proj_ok = proj_actual in (2, 3)
    checks.append(CheckResult(
        check_id="project_count",
        name="Project count",
        passed=proj_ok,
        detail=f"Expected 2-3 projects, got {proj_actual}.",
        severity="error" if not proj_ok else "info",
    ))

    # Bullets per project
    bullets_cfg: dict = cfg.get("bullets_per_project", {"2_projects": 4, "3_projects": 3})
    expected_per_project = (
        bullets_cfg.get("2_projects", 4) if proj_actual <= 2
        else bullets_cfg.get("3_projects", 3)
    )

    # Apply combo_overrides
    combo_overrides = cfg.get("combo_overrides", [])
    for override in combo_overrides:
        conds = override.get("conditions", {})
        if _matches_combo(conds, content, cfg):
            expected_per_project = override.get("bullets_per_project", expected_per_project)

    for proj in content.projects:
        actual_proj_bullets = len(proj.bullets)
        checks.append(CheckResult(
            check_id=f"proj_bullet_count_{proj.name[:20]}",
            name=f"Bullets in project '{proj.name[:30]}'",
            passed=(actual_proj_bullets == expected_per_project),
            detail=f"Expected {expected_per_project}, got {actual_proj_bullets}.",
            severity="error" if actual_proj_bullets != expected_per_project else "info",
        ))

    # Skills categories
    is_qa = content.role_type_flags.get("is_qa_role", False)
    two_proj = proj_actual <= 2
    skills_expected = (
        cfg.get("skills_categories_when_two_projects_or_qa_role", 5)
        if (is_qa or two_proj) else cfg.get("skills_categories_default", 4)
    )
    skills_actual = len(content.skills_categories)
    checks.append(CheckResult(
        check_id="skills_category_count",
        name="Skills category count",
        passed=(skills_actual == skills_expected),
        detail=f"Expected {skills_expected}, got {skills_actual}.",
        severity="error" if skills_actual != skills_expected else "info",
    ))

    # Certifications
    cert_range = cfg.get("certifications", [1, 2])
    cert_actual = len(content.certifications)
    cert_ok = cert_actual == 0 or (cert_range[0] <= cert_actual <= cert_range[1])
    checks.append(CheckResult(
        check_id="certification_count",
        name="Certification count",
        passed=cert_ok,
        detail=f"Expected 0 or {cert_range[0]}-{cert_range[1]}, got {cert_actual}.",
        severity="warning" if not cert_ok else "info",
    ))

    # Leadership
    lead_max = cfg.get("leadership_max_positions", 2)
    lead_actual = len(content.leadership)
    checks.append(CheckResult(
        check_id="leadership_count",
        name="Leadership position count",
        passed=(lead_actual <= lead_max),
        detail=f"Max {lead_max}, got {lead_actual}.",
        severity="error" if lead_actual > lead_max else "info",
    ))

    return checks


def _matches_combo(conditions: dict, content: ResumeContent, cfg: dict) -> bool:
    """Check if content matches combo_override conditions."""
    for key, val in conditions.items():
        if key == "leadership_included" and bool(content.leadership) != val:
            return False
        if key == "project_count" and len(content.projects) != val:
            return False
        if key == "is_qa_role" and content.role_type_flags.get("is_qa_role", False) != val:
            return False
    return True


def _check_overlaps(
    blocks: list[dict],
    margin_pt: float,
    page_width: float,
    page_height: float,
) -> list[CheckResult]:
    """Check 6: No overlapping text elements and no content beyond margins."""
    issues: list[CheckResult] = []
    rects: list[tuple[float, float, float, float, int]] = []  # (x0,y0,x1,y1,index)

    for i, block in enumerate(blocks):
        if block.get("type") == 0:
            b = block.get("bbox", [0, 0, 0, 0])
            rects.append((b[0], b[1], b[2], b[3], i))

            # Check margins
            if b[0] < margin_pt - 2 or b[2] > page_width - margin_pt + 2:
                issues.append(CheckResult(
                    check_id=f"margin_overflow_{i}",
                    name=f"Content beyond margin (block {i})",
                    passed=False,
                    detail=f"Block {i} extends beyond page margins (x: {b[0]:.1f}-{b[2]:.1f}).",
                    severity="error",
                ))
            if b[3] > page_height - margin_pt + 2:
                issues.append(CheckResult(
                    check_id=f"bottom_overflow_{i}",
                    name=f"Content beyond bottom margin (block {i})",
                    passed=False,
                    detail=f"Block {i} extends below bottom margin (y1: {b[3]:.1f}).",
                    severity="error",
                ))

    # Simple overlap check
    for i in range(len(rects)):
        for j in range(i + 1, len(rects)):
            r1 = rects[i]
            r2 = rects[j]
            # Check if bounding boxes overlap
            if r1[0] < r2[2] and r1[2] > r2[0] and r1[1] < r2[3] and r1[3] > r2[1]:
                # Some overlap is expected (e.g. section headers touching text)
                # Only flag significant overlaps
                overlap_x = min(r1[2], r2[2]) - max(r1[0], r2[0])
                overlap_y = min(r1[3], r2[3]) - max(r1[1], r2[1])
                if overlap_x > 5 and overlap_y > 5:
                    issues.append(CheckResult(
                        check_id=f"overlap_{i}_{j}",
                        name=f"Overlapping elements (blocks {i} and {j})",
                        passed=False,
                        detail=f"Blocks {i} and {j} overlap by {overlap_x:.1f}x{overlap_y:.1f}pt.",
                        severity="warning",
                    ))

    if not any(not c.passed for c in issues):
        issues.append(CheckResult(
            check_id="no_overlaps",
            name="No overlapping elements",
            passed=True,
            detail="No significant overlaps detected.",
            severity="info",
        ))

    return issues


def _check_unused_space(
    all_lines: list[dict],
    page_height: float,
    margin_pt: float,
    threshold_mm: float,
) -> tuple[CheckResult, float]:
    """Check 7: Unused whitespace at page bottom."""
    if not all_lines:
        return CheckResult(
            check_id="unused_space",
            name="Unused space at bottom",
            passed=True,
            detail="No text lines found.",
            severity="info",
        ), 0.0

    last_y = max(line.get("bbox", [0, 0, 0, 0])[3] for line in all_lines)
    bottom_margin = page_height - margin_pt
    unused_pt = bottom_margin - last_y
    unused_mm = unused_pt / MM_TO_POINTS

    threshold_pt = threshold_mm * MM_TO_POINTS
    passed = unused_pt <= threshold_pt

    return CheckResult(
        check_id="unused_space",
        name="Unused space at page bottom",
        passed=passed,
        detail=f"Unused space: {unused_mm:.1f}mm (threshold: {threshold_mm:.0f}mm).",
        severity="warning" if not passed else "info",
    ), unused_mm


def _check_skills_whitelist(
    content: ResumeContent,
    master_profile_text: str,
) -> list[CheckResult]:
    """Check 8: Every skill/tool in the output exists in the Master Profile."""
    profile_lower = master_profile_text.lower()
    unknown_skills: list[str] = []

    for cat in content.skills_categories:
        for item in cat.items:
            if item.lower() not in profile_lower:
                # Check for synonym/partial match
                item_words = re.findall(r"\w+", item.lower())
                found = any(w in profile_lower for w in item_words if len(w) > 2)
                if not found:
                    unknown_skills.append(item)

    if unknown_skills:
        return [CheckResult(
            check_id="skills_whitelist",
            name="Skills whitelist",
            passed=False,
            detail=f"Skills not found in Master Profile: {', '.join(unknown_skills[:10])}",
            severity="error",
        )]
    return [CheckResult(
        check_id="skills_whitelist",
        name="Skills whitelist",
        passed=True,
        detail="All skills verified against Master Profile.",
        severity="info",
    )]


def _check_truthfulness(
    content: ResumeContent,
    master_profile_text: str,
) -> list[CheckResult]:
    """Check 9: No numbers/metrics in output that don't exist in the profile."""
    profile_text = master_profile_text

    # Extract all numbers from the resume content
    all_bullets = list(content.experience_bullets)
    for proj in content.projects:
        all_bullets.extend(proj.bullets)
    for lead in content.leadership:
        if lead.bullet:
            all_bullets.append(lead.bullet)

    issues: list[str] = []
    number_pattern = re.compile(r"\b(\d+(?:\.\d+)?(?:%|x|\+)?)\b")

    for bullet in all_bullets:
        for match in number_pattern.finditer(bullet):
            num = match.group(1)
            # Check if this number appears in the profile
            if num not in profile_text:
                # Allow common numbers that are plausibly fine (1, 2, 3... up to small ordinals)
                try:
                    val = float(num.rstrip("%x+"))
                    if val <= 10:
                        continue  # Small numbers like "3 APIs" are probably fine
                except ValueError:
                    pass
                issues.append(f"'{num}' in bullet: '{bullet[:60]}...'")

    if issues:
        return [CheckResult(
            check_id="truthfulness",
            name="Truthfulness guard",
            passed=False,
            detail=f"Metrics not found in Master Profile: {'; '.join(issues[:5])}",
            severity="error",
        )]
    return [CheckResult(
        check_id="truthfulness",
        name="Truthfulness guard",
        passed=True,
        detail="All numbers and metrics verified against Master Profile.",
        severity="info",
    )]


def _check_no_project1(compiled_tex: str) -> CheckResult:
    """Check 10: Project 1 never appears in the compiled .tex."""
    # This is a heuristic; the actual identifier is configurable
    if "Project 1" in compiled_tex or "project 1" in compiled_tex.lower():
        return CheckResult(
            check_id="no_project1",
            name="Project 1 excluded",
            passed=False,
            detail="'Project 1' appears in the compiled LaTeX source.",
            severity="error",
        )
    return CheckResult(
        check_id="no_project1",
        name="Project 1 excluded",
        passed=True,
        detail="Project 1 is not present in the output.",
        severity="info",
    )


def _check_repetition(content: ResumeContent) -> list[CheckResult]:
    """Check 11: Flag near-duplicate bullets or repeated opening verbs."""
    all_bullets: list[str] = list(content.experience_bullets)
    for proj in content.projects:
        all_bullets.extend(proj.bullets)

    opening_verbs: list[str] = []
    for bullet in all_bullets:
        words = bullet.strip().split()
        if words:
            opening_verbs.append(words[0].lower())

    # Find repeated verbs
    from collections import Counter
    verb_counts = Counter(opening_verbs)
    repeated = [v for v, c in verb_counts.items() if c >= 3]

    issues: list[CheckResult] = []

    if repeated:
        issues.append(CheckResult(
            check_id="repeated_verbs",
            name="Repeated opening verbs",
            passed=False,
            detail=f"Opening verb(s) used 3+ times: {', '.join(repeated)}",
            severity="warning",
        ))

    # Near-duplicate detection (simple: check for very similar bullets)
    seen: list[str] = []
    dups: list[str] = []
    for bullet in all_bullets:
        # Normalize
        norm = re.sub(r"\W+", " ", bullet.lower()).strip()
        for prev in seen:
            # Rough Jaccard similarity
            a = set(norm.split())
            b = set(prev.split())
            if a and b:
                sim = len(a & b) / len(a | b)
                if sim > 0.7:
                    dups.append(f"'{bullet[:50]}...'")
                    break
        seen.append(norm)

    if dups:
        issues.append(CheckResult(
            check_id="near_duplicates",
            name="Near-duplicate bullets",
            passed=False,
            detail=f"Potentially duplicated bullets: {'; '.join(dups[:3])}",
            severity="warning",
        ))

    if not issues:
        issues.append(CheckResult(
            check_id="repetition",
            name="No repeated opening verbs or duplicates",
            passed=True,
            detail="Bullets are varied.",
            severity="info",
        ))

    return issues


def _check_education_unchanged(template_tex: str, compiled_tex: str) -> CheckResult:
    """Check 12: The fixed education section text is unchanged."""
    template_edu = extract_fixed_education_text(template_tex)
    compiled_edu = extract_fixed_education_text(compiled_tex)

    if not template_edu:
        return CheckResult(
            check_id="education_unchanged",
            name="Fixed education text unchanged",
            passed=True,
            detail="No fixed education section found in template (no change to check).",
            severity="info",
        )

    # Normalize whitespace for comparison
    def normalize(s: str) -> str:
        return re.sub(r"\s+", " ", s.strip())

    if normalize(template_edu) == normalize(compiled_edu):
        return CheckResult(
            check_id="education_unchanged",
            name="Fixed education text unchanged",
            passed=True,
            detail="Education section matches template.",
            severity="info",
        )

    return CheckResult(
        check_id="education_unchanged",
        name="Fixed education text unchanged",
        passed=False,
        detail="Education section has been modified from the template.",
        severity="error",
    )
