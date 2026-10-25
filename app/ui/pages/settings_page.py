"""
Settings page: LLM provider, API key, Tectonic path, theme, etc.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from PySide6.QtCore import Qt, QThread, QObject, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.core.config import load_config, save_config
from app.core.data_dirs import data_path, get_data_root
from app.core.llm_client import set_api_key, get_api_key, delete_api_key


class ConnectionTester(QObject):
    result = Signal(bool, str)

    def __init__(self, config: dict, api_key: str):
        super().__init__()
        self._config = config
        self._api_key = api_key

    def run(self) -> None:
        from app.core.llm_client import LLMClient
        client = LLMClient(
            provider=self._config.get("provider", "ollama"),
            base_url=self._config.get("base_url", "http://localhost:11434/v1"),
            model=self._config.get("model", "llama3.1:8b"),
            api_key=self._api_key,
            temperature=0.0,
        )
        ok, msg = client.test_connection()
        self.result.emit(ok, msg)


class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._thread: QThread | None = None
        self._setup_ui()
        self._load()

    def _setup_ui(self) -> None:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)

        content = QWidget()
        scroll.setWidget(content)
        layout = QVBoxLayout(content)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        header = QLabel("Settings")
        header.setObjectName("header")
        layout.addWidget(header)

        # ── Privacy note ───────────────────────────────────────────────
        privacy = QLabel(
            "🔒 Privacy: Everything runs locally except the LLM and search API calls you configure below. "
            "Cloud providers (Groq, Together, OpenRouter) receive your job description and master profile."
        )
        privacy.setWordWrap(True)
        privacy.setStyleSheet(
            "background: #1e2235; color: #8b90a0; border-radius: 8px; padding: 12px; font-size: 12px;"
        )
        layout.addWidget(privacy)

        # ── LLM Provider ───────────────────────────────────────────────
        llm_group = QGroupBox("LLM Provider")
        llm_form = QFormLayout(llm_group)

        self.provider_combo = QComboBox()
        self.provider_combo.addItems(["ollama", "groq", "together", "openrouter", "custom"])
        self.provider_combo.currentTextChanged.connect(self._on_provider_changed)
        llm_form.addRow("Provider:", self.provider_combo)

        self.base_url_edit = QLineEdit()
        self.base_url_edit.setPlaceholderText("http://localhost:11434/v1")
        llm_form.addRow("Base URL:", self.base_url_edit)

        self.model_edit = QLineEdit()
        self.model_edit.setPlaceholderText("llama3.1:8b")
        llm_form.addRow("Model:", self.model_edit)

        self.api_key_edit = QLineEdit()
        self.api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_edit.setPlaceholderText("(stored securely in system keyring)")
        llm_form.addRow("API Key:", self.api_key_edit)

        self.temp_spin = QDoubleSpinBox()
        self.temp_spin.setRange(0.0, 2.0)
        self.temp_spin.setSingleStep(0.1)
        self.temp_spin.setValue(0.3)
        llm_form.addRow("Temperature:", self.temp_spin)

        self.retry_spin = QSpinBox()
        self.retry_spin.setRange(1, 10)
        self.retry_spin.setValue(3)
        llm_form.addRow("Max Retries:", self.retry_spin)

        # Test connection button
        test_row = QHBoxLayout()
        self.test_btn = QPushButton("🔌 Test Connection")
        self.test_btn.setObjectName("secondary")
        self.test_result_lbl = QLabel("")
        test_row.addWidget(self.test_btn)
        test_row.addWidget(self.test_result_lbl)
        test_row.addStretch()
        llm_form.addRow("", test_row)

        layout.addWidget(llm_group)

        # ── Tavily Search ──────────────────────────────────────────────
        tavily_group = QGroupBox("Tavily Web Search (Optional)")
        tavily_form = QFormLayout(tavily_group)
        self.tavily_enabled = QCheckBox("Enable Tavily search for application links")
        self.tavily_key_edit = QLineEdit()
        self.tavily_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.tavily_key_edit.setPlaceholderText("tvly-...")
        tavily_form.addRow("", self.tavily_enabled)
        tavily_form.addRow("Tavily API Key:", self.tavily_key_edit)
        layout.addWidget(tavily_group)

        # ── LaTeX / Tectonic ───────────────────────────────────────────
        tex_group = QGroupBox("LaTeX Compiler")
        tex_form = QFormLayout(tex_group)
        tex_row = QHBoxLayout()
        self.tectonic_edit = QLineEdit()
        self.tectonic_edit.setPlaceholderText("tectonic  (or full path)")
        self.tectonic_browse_btn = QPushButton("Browse…")
        self.tectonic_browse_btn.setObjectName("secondary")
        self.tectonic_browse_btn.clicked.connect(self._browse_tectonic)
        self.tectonic_test_btn = QPushButton("Test Compiler")
        self.tectonic_test_btn.setObjectName("secondary")
        self.tectonic_test_btn.clicked.connect(self._test_compiler)
        tex_row.addWidget(self.tectonic_edit)
        tex_row.addWidget(self.tectonic_browse_btn)
        tex_row.addWidget(self.tectonic_test_btn)
        tex_form.addRow("Tectonic path:", tex_row)

        self.compiler_status_lbl = QLabel("")
        self.compiler_status_lbl.setStyleSheet("font-size: 11px;")
        tex_form.addRow("Compiler status:", self.compiler_status_lbl)

        self.fix_rounds_spin = QSpinBox()
        self.fix_rounds_spin.setRange(0, 20)
        self.fix_rounds_spin.setValue(5)
        tex_form.addRow("Max fix rounds:", self.fix_rounds_spin)
        layout.addWidget(tex_group)

        # ── Theme ──────────────────────────────────────────────────────
        theme_group = QGroupBox("Appearance")
        theme_form = QFormLayout(theme_group)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["dark", "light"])
        theme_form.addRow("Theme:", self.theme_combo)
        layout.addWidget(theme_group)

        # ── Profile identifiers ────────────────────────────────────────
        ident_group = QGroupBox("Profile Identifiers")
        ident_form = QFormLayout(ident_group)
        self.proj1_edit = QLineEdit()
        self.proj1_edit.setPlaceholderText("Project 1")
        self.intern_edit = QLineEdit()
        self.intern_edit.setPlaceholderText("Project 6")
        ident_form.addRow("Project 1 identifier:", self.proj1_edit)
        ident_form.addRow("Internship project identifier:", self.intern_edit)
        layout.addWidget(ident_group)

        # ── Data folder buttons ────────────────────────────────────────
        data_group = QGroupBox("Data Management")
        data_layout = QHBoxLayout(data_group)
        open_data_btn = QPushButton("📁 Open Data Folder")
        open_data_btn.setObjectName("secondary")
        reset_rules_btn = QPushButton("↺ Reset Rules to Default")
        reset_rules_btn.setObjectName("secondary")
        export_btn = QPushButton("📦 Export All Settings")
        export_btn.setObjectName("secondary")
        import_btn = QPushButton("📂 Import Settings")
        import_btn.setObjectName("secondary")
        for btn in [open_data_btn, reset_rules_btn, export_btn, import_btn]:
            data_layout.addWidget(btn)
        data_layout.addStretch()
        layout.addWidget(data_group)

        open_data_btn.clicked.connect(self._open_data_folder)
        reset_rules_btn.clicked.connect(self._reset_rules)
        export_btn.clicked.connect(self._export_settings)
        import_btn.clicked.connect(self._import_settings)

        # ── Save button ────────────────────────────────────────────────
        save_btn = QPushButton("💾 Save Settings")
        save_btn.setMinimumHeight(40)
        layout.addWidget(save_btn)
        layout.addStretch()

        # Connect
        self.test_btn.clicked.connect(self._test_connection)
        save_btn.clicked.connect(self._save)

        # Provider presets
        self._provider_presets = {
            "ollama": ("http://localhost:11434/v1", "llama3.1:8b"),
            "groq": ("https://api.groq.com/openai/v1", "llama3-8b-8192"),
            "together": ("https://api.together.xyz/v1", "meta-llama/Llama-3.1-8B-Instruct-Turbo"),
            "openrouter": ("https://openrouter.ai/api/v1", "meta-llama/llama-3.1-8b-instruct"),
            "custom": ("", ""),
        }

    def _load(self) -> None:
        cfg = load_config()
        provider = cfg.get("provider", "ollama")
        idx = self.provider_combo.findText(provider)
        if idx >= 0:
            self.provider_combo.setCurrentIndex(idx)
        self.base_url_edit.setText(cfg.get("base_url", "http://localhost:11434/v1"))
        self.model_edit.setText(cfg.get("model", "llama3.1:8b"))
        self.temp_spin.setValue(float(cfg.get("temperature", 0.3)))
        self.retry_spin.setValue(int(cfg.get("max_retries", 3)))
        self.tectonic_edit.setText(cfg.get("tectonic_path", "tectonic"))
        self.fix_rounds_spin.setValue(int(cfg.get("max_fix_rounds", 5)))
        theme_idx = self.theme_combo.findText(cfg.get("theme", "dark"))
        if theme_idx >= 0:
            self.theme_combo.setCurrentIndex(theme_idx)
        self.proj1_edit.setText(cfg.get("project1_identifier", "Project 1"))
        self.intern_edit.setText(cfg.get("internship_project_identifier", "Project 6"))
        self.tavily_enabled.setChecked(cfg.get("tavily_enabled", False))

        # Load API key from keyring (masked)
        key = get_api_key(provider)
        if key and provider != "ollama":
            self.api_key_edit.setPlaceholderText("(key stored — enter new key to replace)")

        # Tavily key
        tav_key = get_api_key("tavily")
        if tav_key:
            self.tavily_key_edit.setPlaceholderText("(key stored)")

        # Verify compiler on page load
        self._test_compiler()

    def _on_provider_changed(self, provider: str) -> None:
        if provider in self._provider_presets:
            url, model = self._provider_presets[provider]
            if url:
                self.base_url_edit.setText(url)
            if model:
                self.model_edit.setText(model)

    def _save(self) -> None:
        provider = self.provider_combo.currentText()
        cfg = {
            "provider": provider,
            "base_url": self.base_url_edit.text().strip(),
            "model": self.model_edit.text().strip(),
            "temperature": self.temp_spin.value(),
            "max_retries": self.retry_spin.value(),
            "tectonic_path": self.tectonic_edit.text().strip() or "tectonic",
            "max_fix_rounds": self.fix_rounds_spin.value(),
            "theme": self.theme_combo.currentText(),
            "project1_identifier": self.proj1_edit.text().strip() or "Project 1",
            "internship_project_identifier": self.intern_edit.text().strip() or "Project 6",
            "tavily_enabled": self.tavily_enabled.isChecked(),
        }
        save_config(cfg)

        # Store API key in keyring
        api_key = self.api_key_edit.text().strip()
        if api_key:
            set_api_key(provider, api_key)
            self.api_key_edit.clear()

        # Tavily key
        tavily_key = self.tavily_key_edit.text().strip()
        if tavily_key:
            set_api_key("tavily", tavily_key)
            self.tavily_key_edit.clear()

        # Apply theme immediately
        from app.ui.theme import apply_theme
        from PySide6.QtWidgets import QApplication
        apply_theme(QApplication.instance(), cfg["theme"])

        # Reload config in main window
        parent = self.parent()
        if parent and hasattr(parent, "parent") and hasattr(parent.parent(), "reload_config"):
            parent.parent().reload_config()

        QMessageBox.information(self, "Saved", "Settings saved.")

    def _test_connection(self) -> None:
        if self._thread and self._thread.isRunning():
            return

        provider = self.provider_combo.currentText()
        api_key = self.api_key_edit.text().strip() or get_api_key(provider)

        cfg = {
            "provider": provider,
            "base_url": self.base_url_edit.text().strip(),
            "model": self.model_edit.text().strip(),
            "temperature": 0.0,
        }

        self.test_result_lbl.setText("Testing…")
        self.test_btn.setEnabled(False)

        worker = ConnectionTester(cfg, api_key)
        self._thread = QThread()
        worker.moveToThread(self._thread)
        self._thread.started.connect(worker.run)
        worker.result.connect(self._on_test_result)
        worker.result.connect(self._thread.quit)
        self._thread.finished.connect(lambda: self.test_btn.setEnabled(True))
        self._thread.start()

    def _on_test_result(self, ok: bool, msg: str) -> None:
        if ok:
            self.test_result_lbl.setStyleSheet("color: #10b981;")
            self.test_result_lbl.setText(f"✓ {msg}")
        else:
            self.test_result_lbl.setStyleSheet("color: #f87171;")
            self.test_result_lbl.setText(f"✗ {msg}")

    def _browse_tectonic(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Find Tectonic Executable", "",
            "Executables (*.exe);;All Files (*)" if sys.platform == "win32" else "All Files (*)"
        )
        if path:
            self.tectonic_edit.setText(path)
            self._test_compiler()

    def _test_compiler(self) -> None:
        path = self.tectonic_edit.text().strip() or "tectonic"
        from app.core.latex_utils import _find_executable
        exe = _find_executable(path)
        if not exe:
            exe = _find_executable("pdflatex")
        if not exe:
            self.compiler_status_lbl.setStyleSheet("color: #f87171;")
            self.compiler_status_lbl.setText("✗ Compiler not detected. Specify path or check bin/tectonic.exe")
            return

        try:
            flag = "--version" if "tectonic" in exe.lower() else "-v"
            res = subprocess.run([exe, flag], capture_output=True, text=True, timeout=5)
            first_line = (res.stdout.splitlines() or ["OK"])[0].strip()
            self.compiler_status_lbl.setStyleSheet("color: #10b981;")
            self.compiler_status_lbl.setText(f"✓ {first_line} ({exe})")
        except Exception as exc:
            self.compiler_status_lbl.setStyleSheet("color: #f59e0b;")
            self.compiler_status_lbl.setText(f"⚠ Found at {exe}, but run error: {exc}")

    def _open_data_folder(self) -> None:
        path = str(get_data_root())
        if sys.platform == "win32":
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.run(["open", path])
        else:
            subprocess.run(["xdg-open", path])

    def _reset_rules(self) -> None:
        reply = QMessageBox.question(
            self, "Reset Rules",
            "Reset all rule files to their defaults? Your custom rules will be overwritten.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            from app.core.data_dirs import _seed_defaults
            # Force re-copy by temporarily removing existing rule files
            rules_dir = data_path("rules")
            for f in rules_dir.glob("*.md"):
                f.unlink()
            _seed_defaults()
            QMessageBox.information(self, "Done", "Rules reset to defaults.")

    def _export_settings(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self, "Export Settings", "jobtailor_settings.json", "JSON Files (*.json)"
        )
        if not path:
            return
        cfg = load_config()
        # Don't export secrets
        cfg.pop("api_key", None)
        Path(path).write_text(json.dumps(cfg, indent=2), encoding="utf-8")
        QMessageBox.information(self, "Exported", f"Settings exported to {path}")

    def _import_settings(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Import Settings", "", "JSON Files (*.json)"
        )
        if not path:
            return
        try:
            data = json.loads(Path(path).read_text(encoding="utf-8"))
            save_config(data)
            self._load()
            QMessageBox.information(self, "Imported", "Settings imported.")
        except Exception as exc:
            QMessageBox.critical(self, "Error", f"Failed to import settings: {exc}")
