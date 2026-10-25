"""Unit tests for Master Profile parser, Project 1 exclusion, and internship tagging."""

import pytest
from app.core.profile_loader import parse_profile


SAMPLE_PROFILE = """# Master Profile

# Certificates
- IBM Data Science Professional Certificate
- Tata GenAI Job Simulation

# Leadership Position That I Handled
## 1. College Union (Senate) — Executive Member & Magazine Editor
Coordinated with PTA and managed magazine publication.

# Project Portfolio

# Project 1
## 1. Title
House Price Analysis & Prediction System
## 2. Overview
Used King County dataset to predict housing costs.

# Project 2
## 1. Title
Supermarket Sales Analysis
## 2. Overview
Analyzed store branch revenue.

# Project 6
## 1. Title
Credit Risk Prediction & Analysis System
## 2. Overview
Internship machine learning pipeline for risk assessment.

# Project 10: Brazilian E-Commerce
## 1. Title
Brazilian E-Commerce End-to-End Analysis
"""


def test_profile_loader_project_filtering():
    parsed = parse_profile(
        SAMPLE_PROFILE,
        project1_identifier="Project 1",
        internship_identifier="Project 6",
    )

    # Project 1 must be excluded
    assert parsed.project1_excluded is True
    assert not any("House Price Analysis" in p for p in parsed.projects)

    # Project 6 must be tagged as internship
    assert parsed.internship_project_tagged is True
    assert "Credit Risk Prediction" in parsed.internship_project_text
    assert not any("Credit Risk Prediction" in p for p in parsed.projects)

    # Project 10 must NOT be treated as Project 1
    assert any("Brazilian E-Commerce" in p for p in parsed.projects)
    assert any("Supermarket Sales Analysis" in p for p in parsed.projects)

    # Leadership and Certifications
    assert "College Union" in parsed.leadership
    assert "IBM Data Science" in parsed.certifications
