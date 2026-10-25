"""Unit tests for LaTeX utilities (escaping and template substitution)."""

import pytest
from app.core.latex_utils import escape_latex, fill_template
from app.models.schemas import ResumeContent, SkillCategory, ProjectContent, LeadershipContent


def test_escape_latex_special_characters():
    raw = "Analysis & Design in C# with 100% test coverage_v2 {beta} [ok] ~5 $20 ^test"
    escaped = escape_latex(raw)
    assert r"\&" in escaped
    assert r"\%" in escaped
    assert r"\_" in escaped
    assert r"\{" in escaped
    assert r"\}" in escaped
    assert r"\$" in escaped
    assert r"\#" in escaped


def test_fill_template_replaces_placeholders():
    template = (
        r"\documentclass{article}" "\n"
        r"\begin{document}" "\n"
        r"Role: %%JOB_ROLE%%" "\n"
        r"%%SUMMARY%%" "\n"
        r"%%SKILLS%%" "\n"
        r"%%EXPERIENCE%%" "\n"
        r"%%PROJECTS%%" "\n"
        r"%%LEADERSHIP%%" "\n"
        r"%%CERTIFICATIONS%%" "\n"
        r"\end{document}"
    )
    content = ResumeContent(
        summary="Experienced Data Professional.",
        skills_categories=[SkillCategory(title="Languages", items=["Python", "SQL"])],
        experience_bullets=["Built model for fraud detection."],
        projects=[ProjectContent(name="Smart AI Assistant", bullets=["Created chatbot."])],
        leadership=[LeadershipContent(role="Lead", organization="Club", bullet="Coordinated events.")],
        certifications=["IBM Data Science Professional"],
        role_type_flags={"is_qa_role": False},
        target_role="Data Analyst",
    )
    rendered = fill_template(template, content)

    assert "Data Analyst" in rendered
    assert "Experienced Data Professional." in rendered
    assert "Languages" in rendered
    assert "Built model for fraud detection." in rendered
    assert "Smart AI Assistant" in rendered
    assert "Coordinated events." in rendered
    assert "IBM Data Science Professional" in rendered
    assert "%%SUMMARY%%" not in rendered
    assert "%%SKILLS%%" not in rendered
    assert "%%EXPERIENCE%%" not in rendered
    assert "%%PROJECTS%%" not in rendered


def test_compile_template_produces_single_page():
    from pathlib import Path
    from app.core.latex_utils import compile_latex, _find_executable
    import fitz

    # Check if a compiler is available
    tectonic_exe = _find_executable("tectonic")
    if not tectonic_exe:
        pytest.skip("No LaTeX compiler found")

    template_path = Path(__file__).parent.parent / "templates" / "resume_template.tex"
    template = template_path.read_text(encoding="utf-8")

    # 3 projects x 3 bullets — matches the real resume shown in the screenshot.
    # Bullets are kept to one line each so they don't wrap and overflow the page.
    content = ResumeContent(
        summary=(
            "Computer Science graduate with a foundation in Python, Flask, REST APIs, HTML, CSS, "
            "and databases. Eager to contribute to web application development."
        ),
        skills_categories=[
            SkillCategory(title="Languages & Web", items=["Python", "JavaScript", "HTML", "CSS"]),
            SkillCategory(title="Frameworks & APIs", items=["Flask", "Node.js", "Express.js", "JWT"]),
            SkillCategory(title="Databases & Tools", items=["SQLite", "MongoDB", "MySQL"]),
            SkillCategory(title="Testing & Tools", items=["Git", "VS Code", "Postman", "Selenium", "pytest"]),
        ],
        experience_bullets=[
            "Loaded and cleaned a 2.26 million row loan dataset using memory-safe chunked reading.",
            "Organised code into reusable Python modules for loading, preprocessing and prediction.",
            "Delivered a Streamlit app that scores one applicant or a CSV batch with trained models.",
            "Added data validation checks and saved training caps for batch and single scoring.",
        ],
        projects=[
            ProjectContent(
                name="Clinic Appointment Booking System",
                bullets=[
                    "Built a Flask booking app with patient, doctor and admin roles using SQLite and Flask Login.",
                    "Created JSON REST APIs for booking, cancellation and doctor access, tested in Postman.",
                    "Found and fixed 3 defects, then wrote a 39-test Selenium and pytest suite to catch regressions.",
                ]
            ),
            ProjectContent(
                name="Student Enrollment and Learning Management System",
                bullets=[
                    "Developed an enrollment platform using Node.js, Express, MongoDB and an Angular front end.",
                    "Secured the REST API with JWT login and role-based access for students, trainers and admins.",
                    "Tested the APIs in Postman and fixed 4 defects, including seats lost on failed payments.",
                ]
            ),
            ProjectContent(
                name="Smart AI Assistant",
                bullets=[
                    "Designed a Streamlit app with chat, food image analysis, YouTube summaries and PDF Q&A.",
                    "Connected the app to the Google Gemini API with retries so short API failures do not crash it.",
                    "Fixed a Unicode crash in PDF export and added page limits on PDF reading to protect memory.",
                ]
            ),
        ],
        leadership=[],
        certifications=[
            "IBM Data Science Professional Certificate -- IBM & Coursera",
            "Software Testing with Jira & Agile (QA Lead) -- MasterClass, Udemy",
        ],
        target_role="Python Full Stack Developer Intern",
    )

    rendered = fill_template(template, content)
    success, pdf_path, log = compile_latex(rendered, tectonic_path=tectonic_exe)
    assert success is True, f"Compilation failed: {log}"
    assert pdf_path is not None

    doc = fitz.open(str(pdf_path))
    assert doc.page_count == 1, f"Expected 1 page, got {doc.page_count}"
    doc.close()

