"""
JobTailor - Entry point.
Run with: python -m app.main
"""

import sys
import os

# Ensure the project root is on the path when run as a module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from app.core.data_dirs import ensure_data_dirs, data_path
from app.core.config import load_config
from app.ui.main_window import MainWindow
from app.core.logging_setup import setup_logging


def main() -> None:
    """Application entry point."""
    # High-DPI support
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    app.setApplicationName("JobTailor")
    app.setOrganizationName("JobTailor")
    app.setApplicationDisplayName("JobTailor")

    # Set app icon
    icon_path = os.path.join(os.path.dirname(__file__), "..", "assets", "icon.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    # Ensure user data directories exist
    ensure_data_dirs()

    # Set up rotating log file
    setup_logging()

    # Load config (sets theme etc.)
    config = load_config()

    # Apply stylesheet
    from app.ui.theme import apply_theme
    apply_theme(app, config.get("theme", "dark"))

    # Launch main window
    window = MainWindow(config)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
