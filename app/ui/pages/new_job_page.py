"""
New Job page: paste JD, run pipeline, show results in tabs.
"""

from __future__ import annotations

import os
import subprocess
import sys
import urllib.parse
from pathlib import Path
from typing import Any

from PySide6.QtCore import (
    Qt,
    QThread,
    QObject,
    Signal,
    QUrl,
)
from PySide6.QtGui import QDesktopServices, QFont
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QSplitter,
    QStackedWidget,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QScrollArea,
    QFrame,
    QSizePolicy,
)

from app.models.schemas import (
    PipelineResult,
    VerdictLevel,
    RiskLevel,
)


# ─────────────────────────────────────────────────────────────────────────────
# Background worker
# ─────────────────────────────────────────────────────────────────────────────

class PipelineWorker(QObject):
    """Runs the pipeline in a background thread."""
    progress = Signal(str)
    finished = Signal(object)   # PipelineResult
    error = Signal(str)

    def __init__(self, jd_text: str):
        super().__init__()
        self.jd_text = jd_text
        self._cancel = False

    def cancel(self) -> None:
        self._cancel = True

    def run(self) -> None:
        try:
            from app.core.pipeline import Pipeline
            pipeline = Pipeline(
                self.jd_text,
                progress_callback=lambda m: self.progress.emit(m),
                cancel_flag=lambda: self._cancel,
            )
            result = pipeline.run()
            if not self._cancel:
                self.finished.emit(result)
        except InterruptedError:
            self.error.emit("Cancelled by user.")
        except Exception as exc:
            import traceback
            self.error.emit(f"{exc}\n\n{traceback.format_exc()}")


# ─────────────────────────────────────────────────────────────────────────────
# New Job page
# ─────────────────────────────────────────────────────────────────────────────

class NewJobPage(QWidget):
    """Main page for analyzing job descriptions."""
    status_update = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._worker: PipelineWorker | None = None
        self._thread: QThread | None = None
        self._result: PipelineResult | None = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)

        # ── Header ────────────────────────────────────────────────────
        header = QLabel("New Job Analysis")
        header.setObjectName("header")
        sub = QLabel("Paste a job description below, then click Analyze & Tailor.")
        sub.setObjectName("subheader")
        main_layout.addWidget(header)
        main_layout.addWidget(sub)

        # ── Main splitter: input (top) | results (bottom) ──────────────
        self.splitter = QSplitter(Qt.Orientation.Vertical)

        # Input area
        input_widget = self._build_input_area()
        self.splitter.addWidget(input_widget)

        # Results area (hidden initially)
        self.results_widget = self._build_results_area()
        self.results_widget.setVisible(False)
        self.splitter.addWidget(self.results_widget)
        self.splitter.setSizes([300, 600])

        main_layout.addWidget(self.splitter)

        # ── Progress bar ───────────────────────────────────────────────
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Indeterminate
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

        # ── Step label ─────────────────────────────────────────────────
        self.step_label = QLabel("")
        self.step_label.setStyleSheet("color: #8b90a0; font-size: 12px;")
        self.step_label.setVisible(False)
        main_layout.addWidget(self.step_label)

    def _build_input_area(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.jd_input = QTextEdit()
        self.jd_input.setPlaceholderText(
            "Paste the full job description here…\n\n"
            "Include the company name, job title, responsibilities, requirements, "
            "salary (if shown), and any contact emails."
        )
        self.jd_input.setMinimumHeight(200)
        layout.addWidget(self.jd_input)

        # Buttons row
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        self.analyze_btn = QPushButton("✦  Analyze & Tailor")
        self.analyze_btn.setObjectName("analyze_btn")
        self.analyze_btn.setMinimumHeight(40)
        self.analyze_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))

        self.cancel_btn = QPushButton("✕  Cancel")
        self.cancel_btn.setObjectName("secondary")
        self.cancel_btn.setMinimumHeight(40)
        self.cancel_btn.setVisible(False)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setObjectName("secondary")
        self.clear_btn.setMinimumHeight(40)

        btn_row.addWidget(self.analyze_btn, stretch=3)
        btn_row.addWidget(self.cancel_btn)
        btn_row.addWidget(self.clear_btn)
        layout.addLayout(btn_row)

        self.analyze_btn.clicked.connect(self._start_analysis)
        self.cancel_btn.clicked.connect(self._cancel_analysis)
        self.clear_btn.clicked.connect(self._clear)

        return w

    def _build_results_area(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Regenerate buttons
        regen_row = QHBoxLayout()
        self.regen_resume_btn = QPushButton("↺  Regenerate Resume")
        self.regen_resume_btn.setObjectName("secondary")
        self.regen_email_btn = QPushButton("↺  Regenerate Email")
        self.regen_email_btn.setObjectName("secondary")
        regen_row.addWidget(self.regen_resume_btn)
        regen_row.addWidget(self.regen_email_btn)
        regen_row.addStretch()
        layout.addLayout(regen_row)

        # Tab widget for results
        self.result_tabs = QTabWidget()
        layout.addWidget(self.result_tabs)

        self.regen_resume_btn.clicked.connect(self._start_analysis)
        self.regen_email_btn.clicked.connect(self._start_analysis)

        return w

    # ------------------------------------------------------------------
    # Pipeline execution
    # ------------------------------------------------------------------

    def _start_analysis(self) -> None:
        jd = self.jd_input.toPlainText().strip()
        if not jd:
            QMessageBox.warning(self, "Empty Input", "Please paste a job description first.")
            return

        # Clean up previous thread
        if self._thread and self._thread.isRunning():
            return

        self._set_running(True)
        self.results_widget.setVisible(False)

        self._worker = PipelineWorker(jd)
        self._thread = QThread()
        self._worker.moveToThread(self._thread)

        self._thread.started.connect(self._worker.run)
        self._worker.progress.connect(self._on_progress)
        self._worker.finished.connect(self._on_finished)
        self._worker.error.connect(self._on_error)
        self._worker.finished.connect(self._thread.quit)
        self._worker.error.connect(self._thread.quit)
        self._thread.finished.connect(lambda: self._set_running(False))

        self._thread.start()

    def _cancel_analysis(self) -> None:
        if self._worker:
            self._worker.cancel()
        self.status_update.emit("Cancelling…")

    def _clear(self) -> None:
        self.jd_input.clear()
        self.results_widget.setVisible(False)

    def _set_running(self, running: bool) -> None:
        self.analyze_btn.setEnabled(not running)
        self.cancel_btn.setVisible(running)
        self.progress_bar.setVisible(running)
        self.step_label.setVisible(running)
        if not running:
            self.step_label.setText("")

    def _on_progress(self, msg: str) -> None:
        self.step_label.setText(f"⟳  {msg}")
        self.status_update.emit(msg)

    def _on_finished(self, result: PipelineResult) -> None:
        self._result = result
        self._populate_results(result)
        self.results_widget.setVisible(True)
        self.status_update.emit("Analysis complete ✓")

    def _on_error(self, msg: str) -> None:
        QMessageBox.critical(self, "Pipeline Error", msg)
        self.status_update.emit("Error occurred")

    # ------------------------------------------------------------------
    # Result population
    # ------------------------------------------------------------------

    def _populate_results(self, result: PipelineResult) -> None:
        """Build result tabs from the pipeline result."""
        tabs = self.result_tabs
        tabs.clear()

        if result.stopped_early:
            # Only show Verdict and Job Role tabs
            tabs.addTab(self._build_verdict_tab(result), "Verdict")
            if result.job_analysis:
                tabs.addTab(self._build_job_details_tab(result), "Job Details")
            if result.genuineness:
                tabs.addTab(self._build_genuineness_tab(result), "Genuineness")
            return

        # Full result tabs
        tabs.addTab(self._build_verdict_tab(result), "Verdict")
        tabs.addTab(self._build_job_details_tab(result), "Job Details")
        tabs.addTab(self._build_genuineness_tab(result), "Genuineness")
        tabs.addTab(self._build_how_to_apply_tab(result), "How to Apply")

        if result.email_draft:
            tabs.addTab(self._build_email_tab(result), "Email")

        tabs.addTab(self._build_resume_tab(result), "Resume")
        tabs.addTab(self._build_latex_tab(result), "LaTeX")
        tabs.addTab(self._build_log_tab(result), "Log")

    # ─── Tab builders ──────────────────────────────────────────────────

    def _build_verdict_tab(self, result: PipelineResult) -> QWidget:
        w = QScrollArea()
        w.setWidgetResizable(True)
        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        v = result.verdict
        if not v:
            layout.addWidget(QLabel("No verdict available."))
            w.setWidget(inner)
            return w

        # Verdict badge
        verdict_str = v.verdict.value
        verdict_label = QLabel(verdict_str)
        verdict_label.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        verdict_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Color by verdict
        color_map = {
            VerdictLevel.STRONGLY_APPLY: "#10b981",
            VerdictLevel.APPLY: "#34d399",
            VerdictLevel.APPLY_WITH_CAUTION: "#f59e0b",
            VerdictLevel.DONT_APPLY: "#f87171",
            VerdictLevel.STRONGLY_DONT_APPLY: "#dc2626",
        }
        bg_map = {
            VerdictLevel.STRONGLY_APPLY: "#052e16",
            VerdictLevel.APPLY: "#052e16",
            VerdictLevel.APPLY_WITH_CAUTION: "#451a03",
            VerdictLevel.DONT_APPLY: "#450a0a",
            VerdictLevel.STRONGLY_DONT_APPLY: "#450a0a",
        }
        color = color_map.get(v.verdict, "#e8eaf0")
        bg = bg_map.get(v.verdict, "#1e2235")
        verdict_label.setStyleSheet(
            f"color: {color}; background-color: {bg}; "
            f"border-radius: 12px; padding: 16px 32px;"
        )
        layout.addWidget(verdict_label)

        # Role
        role_label = QLabel(f"Role: {v.job_role}" + (f"  |  {v.location}" if v.location else ""))
        role_label.setStyleSheet("color: #8b90a0; font-size: 14px;")
        role_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(role_label)

        # Reason
        reason_box = QTextEdit()
        reason_box.setReadOnly(True)
        reason_box.setMaximumHeight(80)
        reason_box.setPlainText(v.concise_reason)
        layout.addWidget(QLabel("Reason:"))
        layout.addWidget(reason_box)

        if not result.stopped_early:
            # Strengths
            if v.strengths:
                layout.addWidget(self._section_header("✓ Strengths"))
                for s in v.strengths:
                    lbl = QLabel(f"  • {s}")
                    lbl.setStyleSheet("color: #34d399;")
                    lbl.setWordWrap(True)
                    layout.addWidget(lbl)

            # Gaps
            if v.gaps:
                layout.addWidget(self._section_header("✗ Gaps / Missing"))
                for g in v.gaps:
                    lbl = QLabel(f"  • {g}")
                    lbl.setStyleSheet("color: #f87171;")
                    lbl.setWordWrap(True)
                    layout.addWidget(lbl)

            # Eligibility notes
            if v.eligibility_notes:
                layout.addWidget(self._section_header("ℹ Eligibility Notes"))
                for e in v.eligibility_notes:
                    lbl = QLabel(f"  • {e}")
                    lbl.setWordWrap(True)
                    layout.addWidget(lbl)

        layout.addStretch()
        w.setWidget(inner)
        return w

    def _build_job_details_tab(self, result: PipelineResult) -> QWidget:
        w = QScrollArea()
        w.setWidgetResizable(True)
        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        ja = result.job_analysis
        if not ja:
            layout.addWidget(QLabel("No job details available."))
            w.setWidget(inner)
            return w

        fields = [
            ("Company", ja.company),
            ("Job Title", ja.job_title),
            ("Location", ja.location),
            ("Employment Type", ja.employment_type),
            ("Salary", ja.salary),
            ("Experience Requirement", ja.experience_requirement),
            ("Education Requirement", ja.education_requirement),
            ("Domain / Industry", ja.domain_industry),
        ]
        for label, value in fields:
            row = QHBoxLayout()
            key_lbl = QLabel(f"{label}:")
            key_lbl.setFixedWidth(200)
            key_lbl.setStyleSheet("color: #8b90a0; font-weight: 600;")
            val_lbl = QLabel(value or "—")
            val_lbl.setWordWrap(True)
            row.addWidget(key_lbl)
            row.addWidget(val_lbl)
            row.addStretch()
            layout.addLayout(row)

        # Requirements groups
        req = ja.requirements
        if req.must_have:
            layout.addWidget(self._section_header("Must-Have Requirements"))
            for r in req.must_have:
                layout.addWidget(QLabel(f"  • {r}"))

        if req.preferred:
            layout.addWidget(self._section_header("Preferred / Nice-to-Have"))
            for r in req.preferred:
                layout.addWidget(QLabel(f"  • {r}"))

        if req.responsibilities:
            layout.addWidget(self._section_header("Responsibilities"))
            for r in req.responsibilities:
                layout.addWidget(QLabel(f"  • {r}"))

        if req.domain_context:
            layout.addWidget(self._section_header("Domain Context"))
            for r in req.domain_context:
                layout.addWidget(QLabel(f"  • {r}"))

        layout.addStretch()
        w.setWidget(inner)
        return w

    def _build_genuineness_tab(self, result: PipelineResult) -> QWidget:
        w = QScrollArea()
        w.setWidgetResizable(True)
        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        g = result.genuineness
        if not g:
            layout.addWidget(QLabel("Genuineness data unavailable."))
            w.setWidget(inner)
            return w

        # Disclaimer
        disc = QLabel(g.disclaimer)
        disc.setWordWrap(True)
        disc.setStyleSheet(
            "background-color: #451a03; color: #f59e0b; "
            "border-radius: 8px; padding: 12px; font-size: 12px;"
        )
        layout.addWidget(disc)

        # Risk level
        risk_colors = {
            RiskLevel.LOW: ("#10b981", "#052e16"),
            RiskLevel.MEDIUM: ("#f59e0b", "#451a03"),
            RiskLevel.HIGH: ("#dc2626", "#450a0a"),
        }
        fg, bg = risk_colors.get(g.risk_level, ("#e8eaf0", "#1e2235"))
        risk_lbl = QLabel(f"Risk Level: {g.risk_level.value}")
        risk_lbl.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        risk_lbl.setStyleSheet(f"color: {fg}; background-color: {bg}; border-radius: 8px; padding: 12px;")
        risk_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(risk_lbl)

        # Summary
        if g.summary:
            layout.addWidget(self._section_header("Assessment Summary"))
            sum_lbl = QLabel(g.summary)
            sum_lbl.setWordWrap(True)
            layout.addWidget(sum_lbl)

        # Signals
        if g.signals:
            layout.addWidget(self._section_header("Risk Signals Detected"))
            sev_colors = {"high": "#dc2626", "medium": "#f59e0b", "low": "#10b981"}
            for sig in g.signals:
                frame = QFrame()
                frame.setStyleSheet("background-color: #1e2235; border-radius: 8px; padding: 8px;")
                f_layout = QVBoxLayout(frame)
                sig_color = sev_colors.get(sig.severity, "#e8eaf0")
                sig_lbl = QLabel(f"[{sig.severity.upper()}] {sig.signal}")
                sig_lbl.setStyleSheet(f"color: {sig_color}; font-weight: 600;")
                sig_lbl.setWordWrap(True)
                reason_lbl = QLabel(sig.reason)
                reason_lbl.setWordWrap(True)
                reason_lbl.setStyleSheet("color: #8b90a0;")
                f_layout.addWidget(sig_lbl)
                f_layout.addWidget(reason_lbl)
                layout.addWidget(frame)
        else:
            layout.addWidget(QLabel("No risk signals detected."))

        layout.addStretch()
        w.setWidget(inner)
        return w

    def _build_how_to_apply_tab(self, result: PipelineResult) -> QWidget:
        w = QScrollArea()
        w.setWidgetResizable(True)
        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        hta = result.how_to_apply
        if not hta:
            layout.addWidget(QLabel("No application details available."))
            w.setWidget(inner)
            return w

        # Instruction
        inst_lbl = QLabel(hta.instruction or "Check the job posting for application details.")
        inst_lbl.setWordWrap(True)
        inst_lbl.setStyleSheet(
            "background-color: #1e2235; border-radius: 8px; padding: 12px; font-size: 13px;"
        )
        layout.addWidget(inst_lbl)

        # Emails
        if hta.emails:
            layout.addWidget(self._section_header("Emails Found in JD"))
            for email in hta.emails:
                row = QHBoxLayout()
                addr_lbl = QLabel(email.address)
                addr_lbl.setStyleSheet("font-family: monospace; color: #5b6af0;")
                class_lbl = QLabel(f"[{email.classification.value}]")
                class_color = "#10b981" if email.is_legitimate else "#f87171"
                class_lbl.setStyleSheet(f"color: {class_color}; font-size: 11px;")
                row.addWidget(addr_lbl)
                row.addWidget(class_lbl)
                row.addStretch()
                layout.addLayout(row)

        # Application link
        if hta.application_link:
            layout.addWidget(self._section_header("Application Link"))
            link_lbl = QLabel(f'<a href="{hta.application_link}">{hta.application_link}</a>')
            link_lbl.setOpenExternalLinks(True)
            link_lbl.setStyleSheet("color: #5b6af0;")
            layout.addWidget(link_lbl)

        # Search notes
        if hta.search_notes:
            layout.addWidget(self._section_header("Search Notes"))
            notes_lbl = QLabel(hta.search_notes)
            notes_lbl.setWordWrap(True)
            notes_lbl.setStyleSheet("color: #8b90a0;")
            layout.addWidget(notes_lbl)

        layout.addStretch()
        w.setWidget(inner)
        return w

    def _build_email_tab(self, result: PipelineResult) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        e = result.email_draft
        if not e:
            layout.addWidget(QLabel("No email generated."))
            return w

        # Header row
        header_row = QHBoxLayout()
        to_lbl = QLabel(f"To: {e.recipient}")
        to_lbl.setStyleSheet("color: #8b90a0;")
        subj_lbl = QLabel(f"Subject: {e.subject}")
        subj_lbl.setStyleSheet("font-weight: 600;")
        header_row.addWidget(to_lbl)
        header_row.addWidget(subj_lbl)
        header_row.addStretch()
        layout.addLayout(header_row)

        # Email body editor
        self.email_editor = QTextEdit()
        self.email_editor.setPlainText(e.body)
        layout.addWidget(self.email_editor)

        # Buttons
        btn_row = QHBoxLayout()
        copy_btn = QPushButton("📋  Copy to Clipboard")
        copy_btn.setObjectName("secondary")
        mail_btn = QPushButton("✉  Open in Mail Client")
        mail_btn.setObjectName("secondary")
        btn_row.addWidget(copy_btn)
        btn_row.addWidget(mail_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        def copy_email():
            QApplication.clipboard().setText(self.email_editor.toPlainText())

        def open_mail():
            body_enc = urllib.parse.quote(self.email_editor.toPlainText())
            subj_enc = urllib.parse.quote(e.subject)
            mailto = f"mailto:{e.recipient}?subject={subj_enc}&body={body_enc}"
            QDesktopServices.openUrl(QUrl(mailto))

        copy_btn.clicked.connect(copy_email)
        mail_btn.clicked.connect(open_mail)

        return w

    def _build_resume_tab(self, result: PipelineResult) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Validation report summary
        report = result.validation_report
        if report:
            passed_str = "✓ PASSED" if report.passed else "✗ ISSUES FOUND"
            pass_color = "#10b981" if report.passed else "#dc2626"
            status_lbl = QLabel(f"Validation: {passed_str}")
            status_lbl.setStyleSheet(
                f"color: {pass_color}; font-weight: 700; font-size: 14px; "
                f"background: {'#052e16' if report.passed else '#450a0a'}; "
                f"border-radius: 6px; padding: 8px 16px;"
            )
            layout.addWidget(status_lbl)

            # Show failures
            failures = report.failures()
            if failures:
                fail_text = QTextEdit()
                fail_text.setReadOnly(True)
                fail_text.setMaximumHeight(120)
                fail_lines = [f"✗ {f.check_id}: {f.detail}" for f in failures]
                fail_text.setPlainText("\n".join(fail_lines))
                fail_text.setStyleSheet("color: #f87171; background-color: #1a0a0a;")
                layout.addWidget(fail_text)

        # PDF preview
        if result.resume_pdf_path and Path(result.resume_pdf_path).exists():
            try:
                from app.ui.widgets.pdf_viewer import PDFViewer
                viewer = PDFViewer(result.resume_pdf_path)
                layout.addWidget(viewer, stretch=1)
            except Exception as exc:
                layout.addWidget(QLabel(f"PDF preview unavailable: {exc}"))
                # Fallback: open button
                open_btn = QPushButton("Open PDF")
                open_btn.clicked.connect(
                    lambda: QDesktopServices.openUrl(
                        QUrl.fromLocalFile(result.resume_pdf_path)
                    )
                )
                layout.addWidget(open_btn)
        else:
            layout.addWidget(QLabel("No PDF generated."))

        # Open PDF button
        if result.resume_pdf_path:
            open_btn = QPushButton("🔍  Open PDF in System Viewer")
            open_btn.setObjectName("secondary")
            open_btn.clicked.connect(
                lambda: QDesktopServices.openUrl(
                    QUrl.fromLocalFile(result.resume_pdf_path)
                )
            )
            layout.addWidget(open_btn)

        return w

    def _build_latex_tab(self, result: PipelineResult) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # LaTeX source viewer
        self.latex_viewer = QTextEdit()
        self.latex_viewer.setPlainText(result.resume_tex or "No LaTeX generated.")
        self.latex_viewer.setFont(QFont("Consolas", 10))
        self.latex_viewer.setStyleSheet(
            "background-color: #0a0c12; color: #a8c7fa; font-family: Consolas, monospace;"
        )
        layout.addWidget(self.latex_viewer)

        btn_row = QHBoxLayout()
        copy_btn = QPushButton("📋  Copy LaTeX")
        copy_btn.setObjectName("secondary")
        save_tex_btn = QPushButton("💾  Save .tex")
        save_tex_btn.setObjectName("secondary")
        save_pdf_btn = QPushButton("💾  Save PDF")
        save_pdf_btn.setObjectName("secondary")

        def copy_latex():
            QApplication.clipboard().setText(self.latex_viewer.toPlainText())

        def save_tex():
            path, _ = QFileDialog.getSaveFileName(
                self, "Save LaTeX File", "resume.tex", "LaTeX Files (*.tex)"
            )
            if path:
                Path(path).write_text(self.latex_viewer.toPlainText(), encoding="utf-8")

        def save_pdf():
            if not result.resume_pdf_path:
                return
            path, _ = QFileDialog.getSaveFileName(
                self, "Save PDF", "resume.pdf", "PDF Files (*.pdf)"
            )
            if path:
                import shutil
                shutil.copy2(result.resume_pdf_path, path)

        copy_btn.clicked.connect(copy_latex)
        save_tex_btn.clicked.connect(save_tex)
        save_pdf_btn.clicked.connect(save_pdf)

        btn_row.addWidget(copy_btn)
        btn_row.addWidget(save_tex_btn)
        btn_row.addWidget(save_pdf_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        return w

    def _build_log_tab(self, result: PipelineResult) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(20, 20, 20, 20)

        log_view = QTextEdit()
        log_view.setReadOnly(True)
        log_view.setFont(QFont("Consolas", 9))
        log_view.setStyleSheet(
            "background-color: #0a0c12; color: #6b7280; font-family: Consolas, monospace;"
        )

        # Build log from output dir
        if result.output_dir:
            log_file = Path(result.output_dir) / "llm_log.txt"
            if log_file.exists():
                log_view.setPlainText(log_file.read_text(encoding="utf-8", errors="replace"))
            else:
                log_view.setPlainText("Log file not found.")
        else:
            log_view.setPlainText("No log available.")

        layout.addWidget(log_view)
        return w

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _section_header(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setStyleSheet(
            "color: #5b6af0; font-weight: 700; font-size: 12px; "
            "text-transform: uppercase; letter-spacing: 1px; "
            "padding-top: 8px;"
        )
        return lbl
