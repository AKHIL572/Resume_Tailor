"""
LaTeX utilities:
- Text escaping for LaTeX special characters
- Template placeholder filling
- PDF compilation via Tectonic or pdflatex
"""

from __future__ import annotations

import logging
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from app.models.schemas import ResumeContent

logger = logging.getLogger(__name__)

# LaTeX special characters that must be escaped
_LATEX_SPECIALS = {
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
    "\\": r"\textbackslash{}",
}

# Unicode characters that cause LaTeX compile issues unless mapped
_UNICODE_REPLACEMENTS = {
    "\u2018": "'",    # Left single quote ‘
    "\u2019": "'",    # Right single quote ’
    "\u201c": '"',    # Left double quote “
    "\u201d": '"',    # Right double quote ”
    "\u2013": "--",   # En dash –
    "\u2014": "---",  # Em dash —
    "\u20b9": "INR ", # Indian Rupee ₹
    "\u2026": "...",  # Ellipsis …
    "\u00a0": " ",    # Non-breaking space
    "\u2022": "*",    # Bullet •
    "\u2192": r"$\rightarrow$", # Arrow →
}


def escape_latex(text: str) -> str:
    """
    Escape LaTeX special characters in plain text.
    Safe to call on text that will be inserted into a .tex file.
    This does NOT escape text that's already inside LaTeX commands.
    """
    if not text:
        return ""

    # First sanitize unicode characters that can break LaTeX engines
    for u_char, repl in _UNICODE_REPLACEMENTS.items():
        text = text.replace(u_char, repl)

    result = []
    i = 0
    while i < len(text):
        ch = text[i]
        # Check if it's a backslash followed by a known LaTeX command
        if ch == "\\" and i + 1 < len(text):
            # Preserve existing LaTeX commands
            result.append(ch)
            i += 1
            continue
        if ch in _LATEX_SPECIALS:
            result.append(_LATEX_SPECIALS[ch])
        else:
            result.append(ch)
        i += 1
    return "".join(result)


def fill_template(template_tex: str, content: ResumeContent) -> str:
    """
    Fill all %%PLACEHOLDER%% slots in the template with generated content.
    Preserves everything else (preamble, structure, education, etc.).
    """
    tex = template_tex

    # ── Role & Portfolio ───────────────────────────────────────────────
    is_qa_or_dev = False
    if hasattr(content, "role_type_flags") and content.role_type_flags:
        is_qa_or_dev = bool(content.role_type_flags.get("is_qa_role", False))
    portfolio_url = (
        "https://akhil-tv-qa-portfolio.vercel.app/"
        if is_qa_or_dev
        else "https://akhil-tv-portfolio.vercel.app/"
    )
    tex = tex.replace("%%PORTFOLIO_URL%%", portfolio_url)
    role_name = getattr(content, "target_role", "") or "Software / Data Professional"
    tex = tex.replace("%%JOB_ROLE%%", escape_latex(role_name))

    # ── Summary ────────────────────────────────────────────────────────
    summary_tex = escape_latex(content.summary)
    tex = tex.replace("%%SUMMARY%%", summary_tex)

    # ── Skills ─────────────────────────────────────────────────────────
    skills_lines: list[str] = []
    for cat in content.skills_categories:
        title_esc = escape_latex(cat.title)
        items_esc = ", ".join(escape_latex(item) for item in cat.items)
        skills_lines.append(rf"\textbf{{{title_esc}}}: {items_esc}")
    # Join with line breaks but ensure no trailing \\ on the last item
    tex = tex.replace("%%SKILLS%%", " \\\\[2pt]\n".join(skills_lines))

    # ── Experience ─────────────────────────────────────────────────────
    exp_lines: list[str] = [r"\begin{itemize}"]
    for bullet in content.experience_bullets:
        exp_lines.append(rf"    \resumeItem{{{escape_latex(bullet)}}}")
    exp_lines.append(r"\end{itemize}")
    exp_block = "\n".join(exp_lines)
    tex = tex.replace("%%EXPERIENCE%%", exp_block)
    tex = tex.replace("%%EXPERIENCE_BULLETS%%", exp_block)

    # ── Projects ───────────────────────────────────────────────────────
    proj_blocks: list[str] = []
    for idx, proj in enumerate(content.projects):
        name_esc = escape_latex(proj.name)
        tech_esc = escape_latex(getattr(proj, "technologies", "") or "Python, SQL, Analytics")
        github_url = getattr(proj, "github_url", "")
        demo_url = getattr(proj, "demo_url", "")
        
        links = []
        if github_url:
            links.append(rf"\href{{{github_url}}}{{GitHub}}")
        if demo_url:
            links.append(rf"\href{{{demo_url}}}{{Live Demo}}")
        links_str = r" \,|\, ".join(links) if links else ""

        proj_blocks.append(
            rf"\resumeProjectHeading" "\n"
            rf"{{{name_esc}}}" "\n"
            rf"{{{links_str}}}" "\n"
            rf"{{{tech_esc}}}"
        )
        proj_blocks.append(r"\begin{itemize}")
        for b in proj.bullets:
            proj_blocks.append(rf"    \resumeItem{{{escape_latex(b)}}}")
        proj_blocks.append(r"\end{itemize}")
        proj_blocks.append(r"\resumeProjectEnd")
        if idx < len(content.projects) - 1:
            proj_blocks.append(r"\vspace{0.10cm}")

    tex = tex.replace("%%PROJECTS%%", "\n".join(proj_blocks))

    # ── Leadership ─────────────────────────────────────────────────────
    if content.leadership:
        lead_lines: list[str] = [
            r"\section*{Leadership}",
            r"\vspace{0.04cm}",
            r"\begin{itemize}",
        ]
        for pos in content.leadership:
            role_esc = escape_latex(pos.role)
            org_esc = escape_latex(pos.organization)
            header_part = rf"\textbf{{{role_esc}}}" + (f", {org_esc}" if org_esc else "")
            bullet_part = f": {escape_latex(pos.bullet)}" if pos.bullet else ""
            lead_lines.append(rf"    \resumeItem{{{header_part}{bullet_part}}}")
        lead_lines.append(r"\end{itemize}")
        tex = tex.replace("%%LEADERSHIP%%", "\n".join(lead_lines))
    else:
        tex = tex.replace("%%LEADERSHIP%%", "")

    # ── Certifications ─────────────────────────────────────────────────
    if content.certifications:
        cert_lines: list[str] = [
            r"\section*{Certifications}",
            r"\vspace{0.04cm}",
            r"\begin{itemize}",
        ]
        for cert in content.certifications:
            cert_lines.append(rf"    \resumeItem{{{escape_latex(cert)}}}")
        cert_lines.append(r"\end{itemize}")
        tex = tex.replace("%%CERTIFICATIONS%%", "\n".join(cert_lines))
    else:
        tex = tex.replace("%%CERTIFICATIONS%%", "")

    return tex


def compile_latex(
    tex_source: str,
    tectonic_path: str = "tectonic",
    output_dir: Path | None = None,
) -> tuple[bool, Path | None, str]:
    """
    Compile a LaTeX string to PDF.
    Returns (success, pdf_path, log_output).

    Tries Tectonic first, then falls back to pdflatex.
    Compiles in a temp directory to avoid polluting the workspace.
    Never allows shell-escape.
    """
    with tempfile.TemporaryDirectory(prefix="jobtailor_tex_") as tmpdir:
        tmp = Path(tmpdir)
        tex_file = tmp / "resume.tex"
        tex_file.write_text(tex_source, encoding="utf-8")

        log_output = ""
        pdf_path: Path | None = None

        # Try Tectonic
        tectonic_exe = _find_executable(tectonic_path)
        if tectonic_exe:
            success, log_output = _run_tectonic(tectonic_exe, tex_file, tmp)
        else:
            # Fall back to pdflatex
            pdflatex = _find_executable("pdflatex")
            if pdflatex:
                success, log_output = _run_pdflatex(pdflatex, tex_file, tmp)
            else:
                return (
                    False,
                    None,
                    "Neither Tectonic nor pdflatex found. "
                    "Install Tectonic (https://tectonic-typesetting.github.io) or a TeX distribution.",
                )

        if success:
            pdf_src = tmp / "resume.pdf"
            if pdf_src.exists():
                if output_dir:
                    output_dir.mkdir(parents=True, exist_ok=True)
                    dst = output_dir / "resume.pdf"
                    shutil.copy2(pdf_src, dst)
                    pdf_path = dst
                else:
                    # Move to a stable temp location
                    import tempfile as tf
                    stable = tf.mktemp(suffix=".pdf", prefix="jobtailor_")
                    shutil.copy2(pdf_src, stable)
                    pdf_path = Path(stable)
            else:
                success = False
                log_output += "\nPDF output file not found after compilation."

        return success, pdf_path, log_output


def _find_executable(name: str) -> str | None:
    """Find an executable on PATH, direct file path, or project bin/ directory."""
    if not name:
        name = "tectonic"

    # Check if exact path or relative path exists
    if os.path.isfile(name):
        return str(Path(name).resolve())

    # Check project bin directory (e.g. <project_root>/bin/tectonic.exe)
    project_root = Path(__file__).resolve().parent.parent.parent
    for candidate in [name, f"{name}.exe", "tectonic.exe"]:
        bin_path = project_root / "bin" / candidate
        if bin_path.is_file():
            return str(bin_path.resolve())

    # Check user data bin directory
    try:
        from app.core.data_dirs import data_path
        user_bin = data_path("bin", f"{name}.exe" if not name.endswith(".exe") else name)
        if user_bin.is_file():
            return str(user_bin.resolve())
    except Exception:
        pass

    # Check on system PATH
    found = shutil.which(name)
    if found:
        return found
    if not name.endswith(".exe"):
        found = shutil.which(f"{name}.exe")
        if found:
            return found

    return None


def _run_tectonic(
    tectonic_exe: str,
    tex_file: Path,
    work_dir: Path,
) -> tuple[bool, str]:
    """Run Tectonic to compile a .tex file."""
    cmd = [
        tectonic_exe,
        "--outdir", str(work_dir),
        "--keep-logs",
        str(tex_file),
    ]
    return _run_compile(cmd, work_dir)


def _run_pdflatex(
    pdflatex_exe: str,
    tex_file: Path,
    work_dir: Path,
) -> tuple[bool, str]:
    """Run pdflatex to compile a .tex file (no shell-escape)."""
    cmd = [
        pdflatex_exe,
        "-interaction=nonstopmode",
        "-no-shell-escape",
        "-output-directory", str(work_dir),
        str(tex_file),
    ]
    return _run_compile(cmd, work_dir)


def _run_compile(cmd: list[str], work_dir: Path) -> tuple[bool, str]:
    """Execute a compile command and capture output."""
    try:
        result = subprocess.run(
            cmd,
            cwd=str(work_dir),
            capture_output=True,
            text=True,
            timeout=180,
        )
        log = result.stdout + result.stderr
        success = result.returncode == 0
        if not success:
            # Extract relevant error lines
            error_lines = [
                line for line in log.splitlines()
                if line.startswith("!") or "error" in line.lower()
            ][:20]
            log = "\n".join(error_lines) or log[:2000]
        return success, log
    except subprocess.TimeoutExpired:
        return False, "LaTeX compilation timed out after 120 seconds."
    except FileNotFoundError as exc:
        return False, f"Executable not found: {exc}"
    except Exception as exc:
        return False, f"Compilation error: {exc}"


def extract_fixed_education_text(template_tex: str) -> str:
    """
    Extract the education section text from the template for diff checking.
    Returns the text between \\section*{Education} and the next section or end.
    """
    pattern = re.compile(
        r"\\section\*\{Education\}(.*?)(?=\\section\*\{|\\end\{document\})",
        re.DOTALL,
    )
    match = pattern.search(template_tex)
    if match:
        return match.group(1).strip()
    return ""
