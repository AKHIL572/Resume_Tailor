"""
Template page: editor for resume_template.tex + placeholder wizard + test compile.
"""

from __future__ import annotations

import re
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
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

from app.core.data_dirs import data_path
from app.core.latex_utils import compile_latex

PLACEHOLDERS = [
    ("%%SUMMARY%%", "Summary paragraph (3-4 lines)"),
    ("%%SKILLS%%", "Technical skills categories"),
    ("%%EXPERIENCE%%", "Experience / internship bullets"),
    ("%%EXPERIENCE_BULLETS%%", "Experience bullets (alias for %%EXPERIENCE%%)"),
    ("%%PROJECTS%%", "Projects section (2-3 projects)"),
    ("%%LEADERSHIP%%", "Leadership & activities section"),
    ("%%CERTIFICATIONS%%", "Certifications section"),
]


class TemplatePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._load()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        header = QLabel("LaTeX Resume Template")
        header.setObjectName("header")
        sub = QLabel(
            "Edit your LaTeX template. Use placeholders like %%SUMMARY%%, %%SKILLS%%, etc. "
            "The app fills these in; everything else stays exactly as written."
        )
        sub.setObjectName("subheader")
        sub.setWordWrap(True)
        layout.addWidget(header)
        layout.addWidget(sub)

        # Toolbar
        btn_row = QHBoxLayout()
        self.import_btn = QPushButton("📂 Import .tex File")
        self.import_btn.setObjectName("secondary")
        self.save_btn = QPushButton("💾 Save Template")
        self.wizard_btn = QPushButton("🪄 Placeholder Wizard")
        self.wizard_btn.setObjectName("secondary")
        self.compile_btn = QPushButton("⚙ Test Compile")
        self.compile_btn.setObjectName("secondary")

        for btn in [self.import_btn, self.save_btn, self.wizard_btn, self.compile_btn]:
            btn_row.addWidget(btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        # Splitter: editor | placeholder guide
        splitter = QSplitter(Qt.Orientation.Horizontal)

        self.editor = QTextEdit()
        self.editor.setFont(QFont("Consolas", 10))
        self.editor.setStyleSheet("background-color: #0a0c12; color: #a8c7fa;")
        splitter.addWidget(self.editor)

        # Placeholder guide
        guide_widget = QWidget()
        guide_layout = QVBoxLayout(guide_widget)
        guide_layout.setContentsMargins(16, 0, 0, 0)

        guide_lbl = QLabel("Available Placeholders")
        guide_lbl.setStyleSheet("color: #8b90a0; font-weight: 600;")
        guide_layout.addWidget(guide_lbl)

        for ph, desc in PLACEHOLDERS:
            row = QHBoxLayout()
            ph_lbl = QLabel(ph)
            ph_lbl.setFont(QFont("Consolas", 9))
            ph_lbl.setStyleSheet("color: #5b6af0;")
            ph_lbl.setFixedWidth(180)
            desc_lbl = QLabel(desc)
            desc_lbl.setStyleSheet("color: #8b90a0; font-size: 11px;")
            desc_lbl.setWordWrap(True)
            row.addWidget(ph_lbl)
            row.addWidget(desc_lbl)
            guide_layout.addLayout(row)

        guide_layout.addStretch()

        # Detected placeholders list
        det_lbl = QLabel("Detected in Template")
        det_lbl.setStyleSheet("color: #8b90a0; font-weight: 600; margin-top: 12px;")
        self.detected_list = QListWidget()
        guide_layout.addWidget(det_lbl)
        guide_layout.addWidget(self.detected_list)

        splitter.addWidget(guide_widget)
        splitter.setSizes([700, 300])
        layout.addWidget(splitter)

        # Compile output
        self.compile_output = QTextEdit()
        self.compile_output.setReadOnly(True)
        self.compile_output.setMaximumHeight(100)
        self.compile_output.setFont(QFont("Consolas", 9))
        self.compile_output.setVisible(False)
        layout.addWidget(self.compile_output)

        # Connect
        self.import_btn.clicked.connect(self._import_file)
        self.save_btn.clicked.connect(self._save)
        self.wizard_btn.clicked.connect(self._wizard)
        self.compile_btn.clicked.connect(self._test_compile)
        self.editor.textChanged.connect(self._update_detected)

    def _load(self) -> None:
        path = data_path("templates", "resume_template.tex")
        if path.exists():
            self.editor.setPlainText(path.read_text(encoding="utf-8"))
        self._update_detected()

    def _import_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Import LaTeX Template", "", "LaTeX Files (*.tex);;All Files (*)"
        )
        if path:
            self.editor.setPlainText(Path(path).read_text(encoding="utf-8", errors="replace"))

    def _save(self) -> None:
        path = data_path("templates", "resume_template.tex")
        path.write_text(self.editor.toPlainText(), encoding="utf-8")
        QMessageBox.information(self, "Saved", "Template saved.")

    def _update_detected(self) -> None:
        text = self.editor.toPlainText()
        detected = re.findall(r"%%\w+%%", text)
        unique = sorted(set(detected))
        self.detected_list.clear()
        for ph in unique:
            item = QListWidgetItem(ph)
            known = {p for p, _ in PLACEHOLDERS}
            if ph in known:
                item.setForeground(Qt.GlobalColor.green)
            else:
                item.setForeground(Qt.GlobalColor.yellow)
            self.detected_list.addItem(item)

    def _wizard(self) -> None:
        dlg = PlaceholderWizard(self.editor.toPlainText(), self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self.editor.setPlainText(dlg.get_result())

    def _test_compile(self) -> None:
        from app.core.config import load_config
        cfg = load_config()
        tectonic = cfg.get("tectonic_path", "tectonic")

        # Fill with placeholder content for testing
        from app.models.schemas import ResumeContent, SkillCategory, ProjectContent
        test_content = ResumeContent(
            summary="Test summary for template compile check.",
            skills_categories=[SkillCategory(title="Languages", items=["Python", "Java"])],
            experience_bullets=["Developed test features using Python."] * 4,
            projects=[ProjectContent(name="Test Project", bullets=["Built a test application."] * 3)],
        )
        from app.core.latex_utils import fill_template
        try:
            filled = fill_template(self.editor.toPlainText(), test_content)
        except Exception as exc:
            self.compile_output.setVisible(True)
            self.compile_output.setPlainText(f"Template fill error: {exc}")
            return

        success, pdf, log = compile_latex(filled, tectonic_path=tectonic)
        self.compile_output.setVisible(True)
        if success:
            self.compile_output.setStyleSheet("color: #10b981;")
            self.compile_output.setPlainText(f"✓ Compile succeeded! PDF at: {pdf}")
        else:
            self.compile_output.setStyleSheet("color: #f87171;")
            self.compile_output.setPlainText(f"✗ Compile failed:\n{log}")


class PlaceholderWizard(QDialog):
    """Simple wizard to help insert placeholders into the template."""

    def __init__(self, template_text: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Placeholder Wizard")
        self.setMinimumSize(600, 400)
        self._result = template_text

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Click a placeholder to insert it at the cursor position, or verify all are present:"))

        self.preview = QTextEdit()
        self.preview.setPlainText(template_text)
        self.preview.setFont(QFont("Consolas", 10))
        layout.addWidget(self.preview)

        ph_row = QHBoxLayout()
        for ph, _ in PLACEHOLDERS:
            btn = QPushButton(ph)
            btn.setObjectName("secondary")
            btn.clicked.connect(lambda checked, p=ph: self.preview.insertPlainText(p))
            ph_row.addWidget(btn)
        layout.addLayout(ph_row)

        btns = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

    def get_result(self) -> str:
        return self.preview.toPlainText()
