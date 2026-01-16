"""Text extractor for plain text files (.txt, .md, .rst)."""

import os
from datetime import datetime
from pathlib import Path

from semplex_cli.types import TextMetadata
from semplex_cli.utils.file_utils import get_file_owner


class TextExtractor:
    """Extract text content from plain text files."""

    SUPPORTED_EXTENSIONS = {".txt", ".md", ".rst", ".text", ".markdown"}
    ENCODINGS = ["utf-8", "utf-8-sig", "latin-1", "cp1252", "iso-8859-1"]

    def extract(self, file_path: Path) -> TextMetadata:
        """
        Extract text content from a plain text file.

        Args:
            file_path: Path to the text file

        Returns:
            TextMetadata with file content and metadata
        """
        file_path = Path(file_path)
        stat = file_path.stat()

        # Try different encodings
        content = None
        encoding_used = None

        for encoding in self.ENCODINGS:
            try:
                content = file_path.read_text(encoding=encoding)
                encoding_used = encoding
                break
            except (UnicodeDecodeError, LookupError):
                continue

        if content is None:
            # Fallback: read as bytes and decode with errors replaced
            content = file_path.read_bytes().decode("utf-8", errors="replace")
            encoding_used = "utf-8 (with replacements)"

        # Calculate metrics
        lines = content.split("\n")
        words = content.split()

        return TextMetadata(
            filename=file_path.name,
            filepath=str(file_path.absolute()),
            file_type=file_path.suffix.lower(),
            file_size=stat.st_size,
            file_owner=get_file_owner(file_path),
            modified_at=datetime.fromtimestamp(stat.st_mtime).isoformat(),
            extracted_at=datetime.now().isoformat(),
            content=content,
            char_count=len(content),
            word_count=len(words),
            line_count=len(lines),
            encoding=encoding_used,
        )
