"""
Rules page: editable rule files with reset-to-default per file.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QSplitter,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.core.rules_loader import RULE_FILES, load_rule, save_rule
from app.core.data_dirs import data_path


class RulesPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_key: str | None = None
        self._setup_ui()
        self._load_list()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        header = QLabel("Rule Files")
        header.setObjectName("header")
        sub = QLabel(
            "These files contain the instructions injected into every LLM call. "
            "Edit them to change how JobTailor analyzes, rates, and writes content. "
            "Paste your own rules below the placeholder header line."
        )
        sub.setObjectName("subheader")
        sub.setWordWrap(True)
        layout.addWidget(header)
        layout.addWidget(sub)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        # List of rule files
        self.rule_list = QListWidget()
        self.rule_list.setFixedWidth(240)
        self.rule_list.currentRowChanged.connect(self._load_rule)
        splitter.addWidget(self.rule_list)

        # Editor area
        editor_widget = QWidget()
        editor_layout = QVBoxLayout(editor_widget)
        editor_layout.setContentsMargins(16, 0, 0, 0)
        editor_layout.setSpacing(8)

        self.file_label = QLabel("Select a rule file")
        self.file_label.setStyleSheet("color: #5b6af0; font-weight: 600;")
        editor_layout.addWidget(self.file_label)

        self.editor = QTextEdit()
        self.editor.setFont(QFont("Consolas", 10))
        editor_layout.addWidget(self.editor)

        btn_row = QHBoxLayout()
        self.save_btn = QPushButton("💾 Save Rule")
        self.reset_btn = QPushButton("↺ Reset to Default")
        self.reset_btn.setObjectName("secondary")
        btn_row.addWidget(self.save_btn)
        btn_row.addWidget(self.reset_btn)
        btn_row.addStretch()
        editor_layout.addLayout(btn_row)

        splitter.addWidget(editor_widget)
        layout.addWidget(splitter)

        self.save_btn.clicked.connect(self._save_rule)
        self.reset_btn.clicked.connect(self._reset_rule)

    def _load_list(self) -> None:
        self.rule_list.clear()
        descriptions = {
            "source_of_truth": "01 — Source of Truth (all calls)",
            "job_analysis": "02 — Job Analysis",
            "verdict": "03 — Verdict / Fit Assessment",
            "email": "04 — Email Writer",
            "resume_content": "05 — Resume Content",
            "layout_and_validation": "06 — Layout & Validation",
            "final_review": "07 — Final HR Review",
        }
        for key in RULE_FILES:
            label = descriptions.get(key, key)
            item = QListWidgetItem(label)
            item.setData(Qt.ItemDataRole.UserRole, key)
            self.rule_list.addItem(item)

        if self.rule_list.count() > 0:
            self.rule_list.setCurrentRow(0)

    def _load_rule(self, row: int) -> None:
        item = self.rule_list.item(row)
        if not item:
            return
        key = item.data(Qt.ItemDataRole.UserRole)
        self._current_key = key
        self.file_label.setText(RULE_FILES.get(key, key))
        content = load_rule(key)
        self.editor.setPlainText(content)

    def _save_rule(self) -> None:
        if not self._current_key:
            return
        save_rule(self._current_key, self.editor.toPlainText())
        QMessageBox.information(self, "Saved", f"Rule '{self._current_key}' saved.")

    def _reset_rule(self) -> None:
        if not self._current_key:
            return
        filename = RULE_FILES[self._current_key]
        default_src = Path(__file__).parent.parent.parent.parent / "prompts" / filename
        if not default_src.exists():
            QMessageBox.warning(self, "Not Found", f"Default file not found: {default_src}")
            return
        save_rule(self._current_key, default_src.read_text(encoding="utf-8"))
        self._load_rule(self.rule_list.currentRow())
        QMessageBox.information(self, "Reset", "Rule reset to default.")
