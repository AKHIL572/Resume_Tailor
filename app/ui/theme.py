"""
Theme / stylesheet for JobTailor.
Supports "dark" and "light" modes.
Uses a modern, premium design with Inter-inspired styling.
"""

from __future__ import annotations

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont


DARK_STYLESHEET = """
/* ─────── Global ─────── */
QWidget {
    background-color: #0f1117;
    color: #e8eaf0;
    font-family: 'Segoe UI', 'Inter', 'SF Pro Display', sans-serif;
    font-size: 13px;
}

/* ─────── Main Window ─────── */
QMainWindow {
    background-color: #0f1117;
}

/* ─────── Sidebar ─────── */
QListWidget#sidebar {
    background-color: #141720;
    border: none;
    border-right: 1px solid #1e2235;
    padding: 8px 0px;
    font-size: 13px;
    outline: none;
}
QListWidget#sidebar::item {
    padding: 12px 20px;
    border-radius: 8px;
    margin: 2px 8px;
    color: #8b90a0;
}
QListWidget#sidebar::item:selected {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #5b6af0, stop:1 #7c3aed);
    color: #ffffff;
    font-weight: 600;
}
QListWidget#sidebar::item:hover:!selected {
    background-color: #1e2235;
    color: #c8cad8;
}

/* ─────── Buttons ─────── */
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #5b6af0, stop:1 #7c3aed);
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 8px 20px;
    font-weight: 600;
    font-size: 13px;
    min-height: 32px;
}
QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #6b7af8, stop:1 #8c4aff);
}
QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #4b5ae0, stop:1 #6c2add);
}
QPushButton:disabled {
    background-color: #2a2d3e;
    color: #555870;
}
QPushButton#secondary {
    background: #1e2235;
    color: #8b90a0;
    border: 1px solid #2a2d3e;
}
QPushButton#secondary:hover {
    background: #262a40;
    color: #c8cad8;
}
QPushButton#danger {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #dc2626, stop:1 #b91c1c);
    color: #fff;
}
QPushButton#success {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #059669, stop:1 #047857);
    color: #fff;
}

/* ─────── Text areas & inputs ─────── */
QTextEdit, QPlainTextEdit {
    background-color: #141720;
    color: #e8eaf0;
    border: 1px solid #1e2235;
    border-radius: 8px;
    padding: 10px;
    font-size: 13px;
    selection-background-color: #5b6af0;
}
QTextEdit:focus, QPlainTextEdit:focus {
    border: 1px solid #5b6af0;
}
QLineEdit {
    background-color: #141720;
    color: #e8eaf0;
    border: 1px solid #1e2235;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 13px;
    selection-background-color: #5b6af0;
}
QLineEdit:focus {
    border: 1px solid #5b6af0;
}

/* ─────── Tab widget ─────── */
QTabWidget::pane {
    background-color: #141720;
    border: 1px solid #1e2235;
    border-radius: 8px;
}
QTabBar::tab {
    background-color: #0f1117;
    color: #8b90a0;
    padding: 8px 16px;
    margin-right: 2px;
    border-radius: 6px 6px 0 0;
    font-size: 12px;
}
QTabBar::tab:selected {
    background-color: #141720;
    color: #e8eaf0;
    font-weight: 600;
    border-top: 2px solid #5b6af0;
}
QTabBar::tab:hover:!selected {
    background-color: #1a1d2e;
    color: #c8cad8;
}

/* ─────── Labels ─────── */
QLabel {
    color: #e8eaf0;
}
QLabel#header {
    font-size: 22px;
    font-weight: 700;
    color: #ffffff;
}
QLabel#subheader {
    font-size: 14px;
    color: #8b90a0;
}
QLabel#verdict_strongly_apply {
    color: #10b981;
    font-size: 20px;
    font-weight: 700;
}
QLabel#verdict_apply {
    color: #34d399;
    font-size: 20px;
    font-weight: 700;
}
QLabel#verdict_caution {
    color: #f59e0b;
    font-size: 20px;
    font-weight: 700;
}
QLabel#verdict_dont {
    color: #f87171;
    font-size: 20px;
    font-weight: 700;
}
QLabel#verdict_strongly_dont {
    color: #dc2626;
    font-size: 20px;
    font-weight: 700;
}

/* ─────── Progress bar ─────── */
QProgressBar {
    background-color: #1e2235;
    border-radius: 4px;
    height: 6px;
    text-align: center;
    color: transparent;
}
QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #5b6af0, stop:1 #7c3aed);
    border-radius: 4px;
}

/* ─────── Combo box ─────── */
QComboBox {
    background-color: #141720;
    color: #e8eaf0;
    border: 1px solid #1e2235;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 13px;
    min-height: 28px;
}
QComboBox::drop-down {
    border: none;
    width: 20px;
}
QComboBox QAbstractItemView {
    background-color: #141720;
    color: #e8eaf0;
    border: 1px solid #2a2d3e;
    selection-background-color: #5b6af0;
}

/* ─────── Scroll bars ─────── */
QScrollBar:vertical {
    background: #0f1117;
    width: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #2a2d3e;
    border-radius: 4px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background: #5b6af0;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal {
    background: #0f1117;
    height: 8px;
    border-radius: 4px;
}
QScrollBar::handle:horizontal {
    background: #2a2d3e;
    border-radius: 4px;
    min-width: 30px;
}
QScrollBar::handle:horizontal:hover { background: #5b6af0; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }

/* ─────── Group boxes ─────── */
QGroupBox {
    border: 1px solid #1e2235;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 8px;
    color: #8b90a0;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
}

/* ─────── Table / List ─────── */
QTableWidget, QListWidget {
    background-color: #141720;
    alternate-background-color: #191c2a;
    gridline-color: #1e2235;
    border: 1px solid #1e2235;
    border-radius: 8px;
}
QTableWidget::item, QListWidget::item {
    padding: 6px 10px;
}
QTableWidget::item:selected, QListWidget::item:selected {
    background-color: #5b6af0;
    color: #fff;
}
QHeaderView::section {
    background-color: #1a1d2e;
    color: #8b90a0;
    padding: 6px 10px;
    border: none;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
}

/* ─────── Check box ─────── */
QCheckBox {
    spacing: 8px;
    color: #e8eaf0;
}
QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border-radius: 4px;
    border: 1px solid #2a2d3e;
    background: #141720;
}
QCheckBox::indicator:checked {
    background: #5b6af0;
    border-color: #5b6af0;
}

/* ─────── Splitter ─────── */
QSplitter::handle {
    background-color: #1e2235;
}
QSplitter::handle:horizontal { width: 1px; }
QSplitter::handle:vertical { height: 1px; }

/* ─────── Status bar ─────── */
QStatusBar {
    background-color: #0a0c12;
    color: #8b90a0;
    font-size: 11px;
    border-top: 1px solid #1e2235;
}

/* ─────── Tooltip ─────── */
QToolTip {
    background-color: #1e2235;
    color: #e8eaf0;
    border: 1px solid #2a2d3e;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
}

/* ─────── Spin box ─────── */
QSpinBox, QDoubleSpinBox {
    background-color: #141720;
    color: #e8eaf0;
    border: 1px solid #1e2235;
    border-radius: 6px;
    padding: 4px 8px;
}
"""

LIGHT_STYLESHEET = """
QWidget {
    background-color: #f8f9fc;
    color: #1a1d2e;
    font-family: 'Segoe UI', 'Inter', sans-serif;
    font-size: 13px;
}
QMainWindow { background-color: #f0f2f8; }
QListWidget#sidebar {
    background-color: #ffffff;
    border: none;
    border-right: 1px solid #e2e5f0;
    padding: 8px 0px;
}
QListWidget#sidebar::item {
    padding: 12px 20px;
    border-radius: 8px;
    margin: 2px 8px;
    color: #6b7080;
}
QListWidget#sidebar::item:selected {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #5b6af0, stop:1 #7c3aed);
    color: #ffffff;
    font-weight: 600;
}
QListWidget#sidebar::item:hover:!selected {
    background-color: #f0f2fa;
    color: #1a1d2e;
}
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #5b6af0, stop:1 #7c3aed);
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 8px 20px;
    font-weight: 600;
}
QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #6b7af8, stop:1 #8c4aff);
}
QPushButton#secondary {
    background: #eef0fa;
    color: #4b5af0;
    border: 1px solid #d0d4f0;
}
QTextEdit, QPlainTextEdit {
    background-color: #ffffff;
    color: #1a1d2e;
    border: 1px solid #e2e5f0;
    border-radius: 8px;
    padding: 10px;
}
QTextEdit:focus, QPlainTextEdit:focus { border: 1px solid #5b6af0; }
QLineEdit {
    background-color: #ffffff;
    color: #1a1d2e;
    border: 1px solid #e2e5f0;
    border-radius: 6px;
    padding: 6px 10px;
}
QLineEdit:focus { border: 1px solid #5b6af0; }
QTabWidget::pane {
    background-color: #ffffff;
    border: 1px solid #e2e5f0;
    border-radius: 8px;
}
QTabBar::tab {
    background-color: #f8f9fc;
    color: #6b7080;
    padding: 8px 16px;
    border-radius: 6px 6px 0 0;
}
QTabBar::tab:selected {
    background-color: #ffffff;
    color: #1a1d2e;
    font-weight: 600;
    border-top: 2px solid #5b6af0;
}
QGroupBox {
    border: 1px solid #e2e5f0;
    border-radius: 8px;
    margin-top: 12px;
    color: #6b7080;
    font-size: 11px;
    font-weight: 600;
}
QScrollBar:vertical { background: #f0f2f8; width: 8px; border-radius: 4px; }
QScrollBar::handle:vertical { background: #c8cce0; border-radius: 4px; min-height: 30px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QProgressBar { background-color: #e2e5f0; border-radius: 4px; height: 6px; color: transparent; }
QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #5b6af0, stop:1 #7c3aed);
    border-radius: 4px;
}
QStatusBar { background-color: #eef0fa; color: #6b7080; font-size: 11px; }
QLabel#header { font-size: 22px; font-weight: 700; color: #1a1d2e; }
QLabel#subheader { font-size: 14px; color: #6b7080; }
"""


def apply_theme(app: QApplication, theme: str) -> None:
    """Apply the chosen theme stylesheet to the application."""
    if theme == "light":
        app.setStyleSheet(LIGHT_STYLESHEET)
    else:
        app.setStyleSheet(DARK_STYLESHEET)

    # Set default font
    font = QFont("Segoe UI", 10)
    font.setHintingPreference(QFont.HintingPreference.PreferFullHinting)
    app.setFont(font)
