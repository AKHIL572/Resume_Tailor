"""Unit tests for validator content and layout rule checks."""

import pytest
from app.core.validator import (
    _check_skills_whitelist,
    _check_truthfulness,
    _check_repetition,
    _check_no_project1,
)
from app.models.schemas import (
    ResumeContent,
    SkillCategory,
    ProjectContent,
    LeadershipContent,
)


MASTER_PROFILE = """
# Skills
Python, SQL, Power BI, Streamlit, Git

# Projects
Project 2: Supermarket Sales Analysis
Project 3: House Price Prediction
Improved sales analysis by 25% and handled 1000 records.
"""


def test_validator_skills_whitelist_pass():
    content = ResumeContent(
        summary="Data Analyst",
        skills_categories=[SkillCategory(title="Languages", items=["Python", "SQL"])],
        experience_bullets=["Analysis."],
        projects=[ProjectContent(name="Supermarket Sales", bullets=["EDA."])],
    )
    results = _check_skills_whitelist(content, MASTER_PROFILE)
    assert results[0].passed is True


def test_validator_skills_whitelist_flags_unsupported():
    content = ResumeContent(
        summary="Data Analyst",
        skills_categories=[SkillCategory(title="Tools", items=["Rust", "Kubernetes"])],
        experience_bullets=["Analysis."],
        projects=[ProjectContent(name="Supermarket Sales", bullets=["EDA."])],
    )
    results = _check_skills_whitelist(content, MASTER_PROFILE)
    assert results[0].passed is False
    assert "Rust" in results[0].detail


def test_validator_truthfulness_flags_unsupported_metrics():
    # Profile has 25% and 1000 records; 98.5% is invented
    content = ResumeContent(
        summary="Data Analyst",
        skills_categories=[SkillCategory(title="Languages", items=["Python"])],
        experience_bullets=["Achieved 98.5% precision on unseen test data."],
        projects=[ProjectContent(name="Supermarket Sales", bullets=["EDA."])],
    )
    results = _check_truthfulness(content, MASTER_PROFILE)
    assert results[0].passed is False
    assert "98.5%" in results[0].detail


def test_validator_project_rules_flags_project1():
    compiled_with_p1 = r"\section{Projects} \textbf{Project 1: House Price Analysis}"
    res_fail = _check_no_project1(compiled_with_p1)
    assert res_fail.passed is False

    compiled_without_p1 = r"\section{Projects} \textbf{Project 2: Supermarket Sales}"
    res_pass = _check_no_project1(compiled_without_p1)
    assert res_pass.passed is True
