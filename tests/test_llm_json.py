"""Unit tests for LLM client JSON extraction and repair."""

import pytest
from app.core.llm_client import _extract_json


def test_extract_json_with_code_fences():
    raw_markdown = """```json
    {
        "role": "Data Analyst",
        "verdict": "APPLY"
    }
    ```"""
    cleaned = _extract_json(raw_markdown)
    assert '"role": "Data Analyst"' in cleaned
    assert "```" not in cleaned


def test_extract_json_removes_trailing_commas():
    raw_json = '{"items": ["Python", "SQL",], "valid": true,}'
    cleaned = _extract_json(raw_json)
    assert '["Python", "SQL"]' in cleaned
    assert '"valid": true}' in cleaned
