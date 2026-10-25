"""
SQLite history database.
Records each pipeline run with JD, verdict, email, tex source, PDF path, timestamp.
"""

from __future__ import annotations

import json
import logging
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

from app.core.data_dirs import data_path

logger = logging.getLogger(__name__)

DB_SCHEMA = """
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    company TEXT,
    job_title TEXT,
    verdict TEXT,
    jd_snippet TEXT,
    email_subject TEXT,
    email_body TEXT,
    resume_tex TEXT,
    pdf_path TEXT,
    output_dir TEXT,
    analysis_json TEXT,
    validation_passed INTEGER
);
"""


def _get_connection() -> sqlite3.Connection:
    db_path = data_path("history.db")
    conn = sqlite3.connect(str(db_path))
    conn.execute(DB_SCHEMA)
    conn.commit()
    return conn


def write_history_entry(result: Any, job_analysis: Any, verdict: Any) -> int:
    """
    Insert a new history record.
    Returns the inserted row ID.
    """
    conn = _get_connection()
    try:
        analysis_data = {}
        if job_analysis:
            analysis_data["job_analysis"] = job_analysis.model_dump()
        if verdict:
            analysis_data["verdict"] = verdict.model_dump()
        if result.genuineness:
            analysis_data["genuineness"] = result.genuineness.model_dump()

        email_subject = ""
        email_body = ""
        if result.email_draft:
            email_subject = result.email_draft.subject
            email_body = result.email_draft.body

        validation_passed = 0
        if result.validation_report:
            validation_passed = 1 if result.validation_report.passed else 0

        cursor = conn.execute(
            """
            INSERT INTO history
            (timestamp, company, job_title, verdict, jd_snippet, email_subject,
             email_body, resume_tex, pdf_path, output_dir, analysis_json, validation_passed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now().isoformat(),
                getattr(job_analysis, "company", ""),
                getattr(verdict, "job_role", ""),
                str(getattr(verdict, "verdict", "")),
                getattr(job_analysis, "raw_jd_snippet", "")[:500],
                email_subject,
                email_body,
                result.resume_tex or "",
                result.resume_pdf_path or "",
                result.output_dir or "",
                json.dumps(analysis_data, default=str),
                validation_passed,
            ),
        )
        conn.commit()
        row_id = cursor.lastrowid
        logger.info("History entry written: id=%s", row_id)
        return row_id
    finally:
        conn.close()


def get_history(limit: int = 100, search: str = "") -> list[dict[str, Any]]:
    """Return history records, newest first."""
    conn = _get_connection()
    try:
        if search:
            rows = conn.execute(
                """
                SELECT id, timestamp, company, job_title, verdict, jd_snippet, validation_passed, output_dir
                FROM history
                WHERE company LIKE ? OR job_title LIKE ? OR verdict LIKE ? OR jd_snippet LIKE ?
                ORDER BY id DESC LIMIT ?
                """,
                (f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%", limit),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT id, timestamp, company, job_title, verdict, jd_snippet, validation_passed, output_dir
                FROM history
                ORDER BY id DESC LIMIT ?
                """,
                (limit,),
            ).fetchall()

        keys = ["id", "timestamp", "company", "job_title", "verdict", "jd_snippet", "validation_passed", "output_dir"]
        return [dict(zip(keys, row)) for row in rows]
    finally:
        conn.close()


def get_history_entry(entry_id: int) -> dict[str, Any] | None:
    """Return a full history record by ID."""
    conn = _get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM history WHERE id = ?", (entry_id,)
        ).fetchone()
        if row is None:
            return None
        cols = [desc[0] for desc in conn.execute("SELECT * FROM history WHERE id = ?", (entry_id,)).description]
        return dict(zip(cols, row))
    finally:
        conn.close()


def delete_history_entry(entry_id: int) -> None:
    """Delete a history record by ID."""
    conn = _get_connection()
    try:
        conn.execute("DELETE FROM history WHERE id = ?", (entry_id,))
        conn.commit()
    finally:
        conn.close()
