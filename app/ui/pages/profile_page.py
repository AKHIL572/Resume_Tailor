"""
Master Profile page: editor for master_profile.md + parse check.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSplitter,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.core.profile_loader import load_profile, save_profile, parse_profile
from app.core.data_dirs import data_path


class ProfilePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._load()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        header = QLabel("Master Profile")
        header.setObjectName("header")
        sub = QLabel("This is the single source of truth for all resume and email generation.")
        sub.setObjectName("subheader")
        layout.addWidget(header)
        layout.addWidget(sub)

        # Toolbar
        btn_row = QHBoxLayout()
        self.import_btn = QPushButton("📂 Import from File")
        self.import_btn.setObjectName("secondary")
        self.save_btn = QPushButton("💾 Save Profile")
        self.parse_btn = QPushButton("🔍 Parse Check")
        self.parse_btn.setObjectName("secondary")

        btn_row.addWidget(self.import_btn)
        btn_row.addWidget(self.save_btn)
        btn_row.addWidget(self.parse_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        # Splitter: editor | parse report
        splitter = QSplitter(Qt.Orientation.Horizontal)

        self.editor = QTextEdit()
        self.editor.setFont(QFont("Consolas", 10))
        self.editor.setPlaceholderText("Paste or type your master profile in Markdown format…")
        splitter.addWidget(self.editor)

        # Parse report panel
        report_widget = QWidget()
        report_layout = QVBoxLayout(report_widget)
        report_layout.setContentsMargins(16, 0, 0, 0)
        report_lbl = QLabel("Parse Report")
        report_lbl.setStyleSheet("color: #8b90a0; font-weight: 600; font-size: 11px; text-transform: uppercase;")
        self.parse_view = QTextEdit()
        self.parse_view.setReadOnly(True)
        self.parse_view.setFont(QFont("Consolas", 9))
        report_layout.addWidget(report_lbl)
        report_layout.addWidget(self.parse_view)
        splitter.addWidget(report_widget)
        splitter.setSizes([700, 400])

        layout.addWidget(splitter)

        # Contact JSON editor
        contact_lbl = QLabel("Contact Info (JSON)")
        contact_lbl.setObjectName("subheader")
        layout.addWidget(contact_lbl)

        self.contact_editor = QTextEdit()
        self.contact_editor.setMaximumHeight(120)
        self.contact_editor.setFont(QFont("Consolas", 10))
        layout.addWidget(self.contact_editor)

        self.save_contact_btn = QPushButton("💾 Save Contact")
        self.save_contact_btn.setObjectName("secondary")
        layout.addWidget(self.save_contact_btn)

        # Connect signals
        self.import_btn.clicked.connect(self._import_file)
        self.save_btn.clicked.connect(self._save)
        self.parse_btn.clicked.connect(self._parse_check)
        self.save_contact_btn.clicked.connect(self._save_contact)

    def _load(self) -> None:
        self.editor.setPlainText(load_profile())

        contact_path = data_path("profile", "contact.json")
        if contact_path.exists():
            self.contact_editor.setPlainText(
                contact_path.read_text(encoding="utf-8")
            )

    def _import_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Import Profile", "", "Markdown Files (*.md);;Text Files (*.txt);;All Files (*)"
        )
        if path:
            text = Path(path).read_text(encoding="utf-8", errors="replace")
            self.editor.setPlainText(text)

    def _save(self) -> None:
        save_profile(self.editor.toPlainText())
        QMessageBox.information(self, "Saved", "Master Profile saved successfully.")

    def _save_contact(self) -> None:
        import json
        try:
            data = json.loads(self.contact_editor.toPlainText())
            from app.core.profile_loader import save_contact
            save_contact(data)
            QMessageBox.information(self, "Saved", "Contact info saved.")
        except Exception as exc:
            QMessageBox.critical(self, "Error", f"Invalid JSON: {exc}")

    def _parse_check(self) -> None:
        raw = self.editor.toPlainText()
        parsed = parse_profile(raw)

        lines = [
            "=== PARSE REPORT ===\n",
            f"Education:      {'✓' if parsed.education else '✗ Not found'}",
            f"Skills:         {'✓' if parsed.skills else '✗ Not found'}",
            f"Experience:     {'✓' if parsed.experience else '✗ Not found'}",
            f"Leadership:     {'✓' if parsed.leadership else '✗ Not found'}",
            f"Certifications: {'✓' if parsed.certifications else '✗ Not found'}",
            f"\nProjects ({len(parsed.projects)} included):",
        ]
        for proj in parsed.projects:
            lines.append(f"  ✓ {proj[:60]}")

        if parsed.project1_excluded:
            lines.append("\n⚠ Project 1 detected and EXCLUDED (correct)")
        if parsed.internship_project_tagged:
            lines.append("⚠ Internship project tagged for experience-only (correct)")

        if parsed.warnings:
            lines.append("\nWarnings:")
            for w in parsed.warnings:
                lines.append(f"  ⚠ {w}")

        self.parse_view.setPlainText("\n".join(lines))
