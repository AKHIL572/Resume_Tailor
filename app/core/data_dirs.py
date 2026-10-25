"""
Data directory management using platformdirs.
Creates all required user-data folders on first run.
"""

import os
import json
import shutil
from pathlib import Path
from platformdirs import user_data_dir

APP_NAME = "JobTailor"
APP_AUTHOR = "JobTailor"

_DATA_ROOT: Path | None = None


def get_data_root() -> Path:
    """Return the root user-data directory for JobTailor."""
    global _DATA_ROOT
    if _DATA_ROOT is None:
        _DATA_ROOT = Path(user_data_dir(APP_NAME, APP_AUTHOR))
    return _DATA_ROOT


def data_path(*parts: str) -> Path:
    """Return an absolute path inside the user-data directory."""
    return get_data_root().joinpath(*parts)


def ensure_data_dirs() -> None:
    """Create all required subdirectories and seed default files."""
    root = get_data_root()
    dirs = [
        root / "profile",
        root / "templates",
        root / "rules",
        root / "config",
        root / "output",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    _seed_defaults()


def _seed_defaults() -> None:
    """Copy default files from prompts/ if user files don't yet exist."""
    prompts_dir = Path(__file__).parent.parent.parent / "prompts"

    # Seed rule files
    rules_dir = data_path("rules")
    if prompts_dir.exists():
        for src in prompts_dir.glob("*.md"):
            dst = rules_dir / src.name
            if not dst.exists():
                shutil.copy2(src, dst)

    # Seed layout config
    layout_cfg = data_path("config", "layout_config.json")
    if not layout_cfg.exists():
        default_layout = {
            "page_count": 1,
            "summary_lines": [3, 4],
            "experience_bullets": 4,
            "skills_categories_default": 4,
            "skills_categories_when_two_projects_or_qa_role": 5,
            "projects_default": 3,
            "bullets_per_project": {"2_projects": 4, "3_projects": 3},
            "leadership_max_positions": 2,
            "leadership_bullets_per_position": 1,
            "certifications": [1, 2],
            "line_fill_min": 0.85,
            "line_fill_max": 1.00,
            "max_fix_rounds": 5,
            "unused_space_threshold_mm": 15.0,
            "combo_overrides": []
        }
        layout_cfg.write_text(json.dumps(default_layout, indent=2))

    project_root = Path(__file__).parent.parent.parent

    # Seed settings
    settings_cfg = data_path("config", "settings.json")
    if not settings_cfg.exists():
        tectonic_default = "tectonic"
        if (project_root / "bin" / "tectonic.exe").exists():
            tectonic_default = str((project_root / "bin" / "tectonic.exe").resolve())

        default_settings = {
            "provider": "ollama",
            "base_url": "http://localhost:11434/v1",
            "model": "llama3.1:8b",
            "temperature": 0.3,
            "theme": "dark",
            "tectonic_path": tectonic_default,
            "max_retries": 3,
            "max_fix_rounds": 5,
            "project1_identifier": "Project 1",
            "internship_project_identifier": "Project 6",
            "tavily_enabled": False
        }
        settings_cfg.write_text(json.dumps(default_settings, indent=2))

    # Seed contact
    contact_file = data_path("profile", "contact.json")
    if not contact_file.exists():
        contact_file.write_text(json.dumps({
            "name": "AKHIL T V",
            "phone": "+91 7510114772",
            "email": "akhilthottekkat135@gmail.com",
            "linkedin": "https://www.linkedin.com/in/akhil-t-v",
            "github": "https://github.com/akhil-t-v",
            "website": "https://akhil-tv-portfolio.vercel.app/"
        }, indent=2))

    # Seed master profile
    profile_file = data_path("profile", "master_profile.md")
    root_profile = project_root / "master_profile.md"
    if not profile_file.exists():
        if root_profile.exists():
            shutil.copy2(root_profile, profile_file)
        else:
            profile_file.write_text(
                "# Master Profile\n\n"
                "<!-- Paste your full master profile here. -->\n"
                "<!-- The app uses this as the single source of truth. -->\n"
            )

    # Seed template
    template_file = data_path("templates", "resume_template.tex")
    root_template = project_root / "templates" / "resume_template.tex"
    if not template_file.exists():
        if root_template.exists():
            shutil.copy2(root_template, template_file)
        else:
            _write_sample_template(template_file)


def _write_sample_template(path: Path) -> None:
    """Write a minimal sample LaTeX resume template."""
    sample = r"""\documentclass[10pt,letterpaper]{article}
\usepackage[margin=0.5in]{geometry}
\usepackage{enumitem}
\usepackage{hyperref}
\usepackage{fontawesome5}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\pagestyle{empty}

\begin{document}

% ===== HEADER =====
\begin{center}
    {\Huge \textbf{YOUR NAME}} \\[4pt]
    City, State $\cdot$ phone $\cdot$ \href{mailto:email}{email} $\cdot$
    \href{https://linkedin.com/in/yourprofile}{LinkedIn} $\cdot$
    \href{https://github.com/yourgithub}{GitHub}
\end{center}

% ===== SUMMARY =====
\section*{Summary}
%%SUMMARY%%

% ===== SKILLS =====
\section*{Technical Skills}
%%SKILLS%%

% ===== EXPERIENCE =====
\section*{Experience}
%%EXPERIENCE%%

% ===== PROJECTS =====
\section*{Projects}
%%PROJECTS%%

% ===== EDUCATION (fixed - do not change) =====
\section*{Education}
\textbf{University Name} \hfill City, State \\
Bachelor of Science in Computer Science \hfill Graduated: Month Year \\
GPA: X.XX/4.00

% ===== LEADERSHIP =====
%%LEADERSHIP%%

% ===== CERTIFICATIONS =====
%%CERTIFICATIONS%%

\end{document}
"""
    path.write_text(sample)
