"""
Main application window with left sidebar navigation.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QFont
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QSplitter,
    QStackedWidget,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from app.core.data_dirs import data_path, get_data_root
from app.ui.pages.new_job_page import NewJobPage
from app.ui.pages.history_page import HistoryPage
from app.ui.pages.profile_page import ProfilePage
from app.ui.pages.template_page import TemplatePage
from app.ui.pages.rules_page import RulesPage
from app.ui.pages.settings_page import SettingsPage


NAV_ITEMS = [
    ("✦  New Job", "new_job"),
    ("⏱  History", "history"),
    ("👤  Master Profile", "profile"),
    ("📄  Template", "template"),
    ("⚙  Rules", "rules"),
    ("🔧  Settings", "settings"),
]


class MainWindow(QMainWindow):
    """
    The application's main window.
    Left sidebar for navigation; right area shows the active page.
    """

    def __init__(self, config: dict[str, Any]):
        super().__init__()
        self.config = config
        self._setup_window()
        self._build_ui()
        self._connect_signals()

    # ------------------------------------------------------------------

    def _setup_window(self) -> None:
        self.setWindowTitle("JobTailor")
        self.setMinimumSize(1200, 780)
        self.resize(1400, 900)

        # Center on screen
        screen = QApplication.primaryScreen()
        if screen:
            geo = screen.availableGeometry()
            self.move(
                (geo.width() - self.width()) // 2,
                (geo.height() - self.height()) // 2,
            )

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # ── Sidebar ────────────────────────────────────────────────────
        sidebar_container = QWidget()
        sidebar_container.setFixedWidth(200)
        sidebar_layout = QVBoxLayout(sidebar_container)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        # App logo / title
        logo_widget = QWidget()
        logo_widget.setFixedHeight(70)
        logo_layout = QVBoxLayout(logo_widget)
        logo_layout.setContentsMargins(20, 16, 20, 8)
        title_label = QLabel("JobTailor")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #5b6af0; font-size: 18px; font-weight: 700;")
        subtitle_label = QLabel("AI Resume & Email")
        subtitle_label.setStyleSheet("color: #555870; font-size: 10px;")
        logo_layout.addWidget(title_label)
        logo_layout.addWidget(subtitle_label)

        self.sidebar = QListWidget()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.sidebar.setSpacing(2)

        for label, _ in NAV_ITEMS:
            item = QListWidgetItem(label)
            item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.sidebar.addItem(item)

        sidebar_layout.addWidget(logo_widget)
        sidebar_layout.addWidget(self.sidebar)
        sidebar_layout.addStretch()

        # Data folder shortcut at bottom
        data_label = QLabel(f"Data: {str(get_data_root())[:25]}…")
        data_label.setStyleSheet("color: #404358; font-size: 9px; padding: 8px 16px;")
        data_label.setWordWrap(True)
        sidebar_layout.addWidget(data_label)

        # ── Page stack ─────────────────────────────────────────────────
        self.page_stack = QStackedWidget()

        self.pages: dict[str, QWidget] = {}

        self.new_job_page = NewJobPage(self)
        self.history_page = HistoryPage(self)
        self.profile_page = ProfilePage(self)
        self.template_page = TemplatePage(self)
        self.rules_page = RulesPage(self)
        self.settings_page = SettingsPage(self)

        for page in [
            self.new_job_page,
            self.history_page,
            self.profile_page,
            self.template_page,
            self.rules_page,
            self.settings_page,
        ]:
            self.page_stack.addWidget(page)

        root_layout.addWidget(sidebar_container)
        root_layout.addWidget(self.page_stack)

        # ── Status bar ─────────────────────────────────────────────────
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        # Select first item
        self.sidebar.setCurrentRow(0)

    def _connect_signals(self) -> None:
        self.sidebar.currentRowChanged.connect(self._navigate)
        self.new_job_page.status_update.connect(self.status_bar.showMessage)

    def _navigate(self, index: int) -> None:
        """Switch to the selected page."""
        self.page_stack.setCurrentIndex(index)

    def navigate_to(self, page_name: str) -> None:
        """Navigate programmatically by page key."""
        for i, (_, key) in enumerate(NAV_ITEMS):
            if key == page_name:
                self.sidebar.setCurrentRow(i)
                break

    def reload_config(self) -> None:
        """Reload config after settings change."""
        from app.core.config import load_config
        self.config = load_config()
