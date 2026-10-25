"""
Simple PDF viewer widget using PyMuPDF to render pages as QPixmaps.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

try:
    import fitz
    HAS_FITZ = True
except ImportError:
    HAS_FITZ = False


class PDFViewer(QWidget):
    """Renders a PDF as a scrollable image preview."""

    def __init__(self, pdf_path: str, dpi: int = 150, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self.load_pdf(pdf_path, dpi)

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.image_label.setStyleSheet("background-color: #1a1a1a;")

        self.scroll_area.setWidget(self.image_label)
        layout.addWidget(self.scroll_area)

    def load_pdf(self, pdf_path: str, dpi: int = 150) -> None:
        """Load and render the first page of the PDF."""
        if not HAS_FITZ:
            self.image_label.setText("PyMuPDF not installed — cannot preview PDF.")
            return

        path = Path(pdf_path)
        if not path.exists():
            self.image_label.setText(f"PDF not found: {pdf_path}")
            return

        try:
            doc = fitz.open(str(path))
            if doc.page_count == 0:
                self.image_label.setText("Empty PDF.")
                return

            page = doc[0]
            mat = fitz.Matrix(dpi / 72, dpi / 72)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            doc.close()

            # Convert to QPixmap
            img = QImage(
                pix.samples,
                pix.width,
                pix.height,
                pix.stride,
                QImage.Format.Format_RGB888,
            )
            pixmap = QPixmap.fromImage(img)

            # Scale to fit reasonable width
            max_width = 800
            if pixmap.width() > max_width:
                pixmap = pixmap.scaledToWidth(
                    max_width, Qt.TransformationMode.SmoothTransformation
                )

            self.image_label.setPixmap(pixmap)
            self.image_label.setFixedSize(pixmap.size())

        except Exception as exc:
            self.image_label.setText(f"PDF render error: {exc}")
