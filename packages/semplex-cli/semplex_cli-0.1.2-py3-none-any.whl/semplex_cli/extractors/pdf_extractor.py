"""PDF extractor for PDF documents."""

import os
from datetime import datetime
from pathlib import Path

from semplex_cli.types import TextMetadata
from semplex_cli.utils.file_utils import get_file_owner

# Optional dependency - will be imported at runtime
try:
    from pypdf import PdfReader
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False


class PDFExtractor:
    """Extract text content from PDF files."""

    SUPPORTED_EXTENSIONS = {".pdf"}

    def __init__(self):
        if not PYPDF_AVAILABLE:
            raise ImportError(
                "pypdf is required for PDF extraction. "
                "Install it with: pip install pypdf"
            )

    def extract(self, file_path: Path) -> TextMetadata:
        """
        Extract text content from a PDF file.

        Args:
            file_path: Path to the PDF file

        Returns:
            TextMetadata with file content and metadata
        """
        file_path = Path(file_path)
        stat = file_path.stat()

        # Read PDF
        reader = PdfReader(file_path)
        page_count = len(reader.pages)

        # Extract text from all pages
        text_parts = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)

        content = "\n\n".join(text_parts)

        # Calculate metrics
        lines = content.split("\n")
        words = content.split()

        return TextMetadata(
            filename=file_path.name,
            filepath=str(file_path.absolute()),
            file_type=".pdf",
            file_size=stat.st_size,
            file_owner=get_file_owner(file_path),
            modified_at=datetime.fromtimestamp(stat.st_mtime).isoformat(),
            extracted_at=datetime.now().isoformat(),
            content=content,
            char_count=len(content),
            word_count=len(words),
            line_count=len(lines),
            page_count=page_count,
        )
