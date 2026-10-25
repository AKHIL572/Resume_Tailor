"""
History page: searchable list of past job analyses.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtGui import QDesktopServices, QFont
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSplitter,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.core.history import get_history, get_history_entry, delete_history_entry


class HistoryPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._entries: list[dict] = []
        self._setup_ui()
        self._load_history()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        header = QLabel("History")
        header.setObjectName("header")
        layout.addWidget(header)

        # Search bar
        search_row = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search by company, role, or verdict…")
        refresh_btn = QPushButton("↺ Refresh")
        refresh_btn.setObjectName("secondary")
        search_row.addWidget(self.search_box)
        search_row.addWidget(refresh_btn)
        layout.addLayout(search_row)

        self.search_box.textChanged.connect(self._search)
        refresh_btn.clicked.connect(self._load_history)

        # Splitter: list | detail
        splitter = QSplitter(Qt.Orientation.Horizontal)

        self.list_widget = QListWidget()
        self.list_widget.currentRowChanged.connect(self._show_detail)
        splitter.addWidget(self.list_widget)

        # Detail panel
        detail_widget = QWidget()
        detail_layout = QVBoxLayout(detail_widget)
        detail_layout.setContentsMargins(16, 0, 0, 0)
        detail_layout.setSpacing(10)

        self.detail_view = QTextEdit()
        self.detail_view.setReadOnly(True)
        self.detail_view.setFont(QFont("Consolas", 10))
        detail_layout.addWidget(self.detail_view)

        # Action buttons
        btn_row = QHBoxLayout()
        self.open_dir_btn = QPushButton("📁 Open Output Folder")
        self.open_dir_btn.setObjectName("secondary")
        self.open_pdf_btn = QPushButton("🔍 Open PDF")
        self.open_pdf_btn.setObjectName("secondary")
        self.delete_btn = QPushButton("🗑 Delete")
        self.delete_btn.setObjectName("secondary")
        btn_row.addWidget(self.open_dir_btn)
        btn_row.addWidget(self.open_pdf_btn)
        btn_row.addWidget(self.delete_btn)
        btn_row.addStretch()
        detail_layout.addLayout(btn_row)

        self.open_dir_btn.clicked.connect(self._open_dir)
        self.open_pdf_btn.clicked.connect(self._open_pdf)
        self.delete_btn.clicked.connect(self._delete_entry)

        splitter.addWidget(detail_widget)
        splitter.setSizes([300, 700])

        layout.addWidget(splitter)

    def _load_history(self) -> None:
        query = self.search_box.text().strip()
        self._entries = get_history(search=query)
        self.list_widget.clear()
        for entry in self._entries:
            text = (
                f"{entry['timestamp'][:16]}  "
                f"{entry['company'] or '?'} — {entry['job_title'] or '?'}  "
                f"[{entry['verdict']}]"
            )
            item = QListWidgetItem(text)
            verdict = entry.get("verdict", "")
            if "STRONGLY APPLY" == verdict:
                item.setForeground(Qt.GlobalColor.green)
            elif "DON'T APPLY" in verdict or "STRONGLY DON'T" in verdict:
                item.setForeground(Qt.GlobalColor.red)
            self.list_widget.addItem(item)

    def _search(self) -> None:
        QTimer.singleShot(400, self._load_history)

    def _show_detail(self, row: int) -> None:
        if row < 0 or row >= len(self._entries):
            self.detail_view.clear()
            return
        entry = self._entries[row]
        full = get_history_entry(entry["id"]) or {}

        text_parts = [
            f"ID: {full.get('id')}",
            f"Timestamp: {full.get('timestamp')}",
            f"Company: {full.get('company')}",
            f"Job Title: {full.get('job_title')}",
            f"Verdict: {full.get('verdict')}",
            f"Validation Passed: {'Yes' if full.get('validation_passed') else 'No'}",
            "",
            "=== Email Subject ===",
            full.get("email_subject", ""),
            "",
            "=== JD Snippet ===",
            full.get("jd_snippet", ""),
        ]
        self.detail_view.setPlainText("\n".join(str(p) for p in text_parts))

    def _current_entry(self) -> dict | None:
        row = self.list_widget.currentRow()
        if 0 <= row < len(self._entries):
            return self._entries[row]
        return None

    def _open_dir(self) -> None:
        entry = self._current_entry()
        if entry and entry.get("output_dir"):
            path = entry["output_dir"]
            if os.path.isdir(path):
                if sys.platform == "win32":
                    os.startfile(path)
                elif sys.platform == "darwin":
                    subprocess.run(["open", path])
                else:
                    subprocess.run(["xdg-open", path])

    def _open_pdf(self) -> None:
        row = self.list_widget.currentRow()
        if row < 0:
            return
        full = get_history_entry(self._entries[row]["id"]) or {}
        pdf = full.get("pdf_path", "")
        if pdf and Path(pdf).exists():
            QDesktopServices.openUrl(QUrl.fromLocalFile(pdf))

    def _delete_entry(self) -> None:
        entry = self._current_entry()
        if entry:
            delete_history_entry(entry["id"])
            self._load_history()
