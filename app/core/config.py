"""
Config loader - reads/writes config/settings.json.
API keys are stored in keyring, never in the JSON file.
"""

import json
from pathlib import Path
from typing import Any

from app.core.data_dirs import data_path


def _settings_path() -> Path:
    return data_path("config", "settings.json")


def load_config() -> dict[str, Any]:
    """Load settings from disk. Returns defaults if file missing."""
    p = _settings_path()
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_config(cfg: dict[str, Any]) -> None:
    """Persist settings (without secrets) to disk."""
    p = _settings_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(cfg, indent=2), encoding="utf-8")


def load_layout_config() -> dict[str, Any]:
    """Load layout_config.json with fallback defaults."""
    p = data_path("config", "layout_config.json")
    defaults = {
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
    if not p.exists():
        return defaults
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        defaults.update(data)
        return defaults
    except Exception:
        return defaults


def save_layout_config(cfg: dict[str, Any]) -> None:
    """Persist layout config to disk."""
    p = data_path("config", "layout_config.json")
    p.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
