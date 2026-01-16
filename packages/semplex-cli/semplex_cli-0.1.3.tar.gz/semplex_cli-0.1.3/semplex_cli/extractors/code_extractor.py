"""Code extractor for source code files."""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from semplex_cli.types import TextMetadata
from semplex_cli.utils.file_utils import get_file_owner


class CodeExtractor:
    """Extract text content from source code files."""

    SUPPORTED_EXTENSIONS = {
        # Python
        ".py", ".pyi", ".pyx",
        # JavaScript/TypeScript
        ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs",
        # Web
        ".html", ".htm", ".css", ".scss", ".sass", ".less",
        # Systems
        ".c", ".cpp", ".cc", ".cxx", ".h", ".hpp", ".hxx",
        # JVM
        ".java", ".kt", ".kts", ".scala", ".groovy",
        # Go/Rust
        ".go", ".rs",
        # Ruby/PHP/Perl
        ".rb", ".php", ".pl", ".pm",
        # Shell
        ".sh", ".bash", ".zsh", ".fish",
        # Swift/Objective-C
        ".swift", ".m", ".mm",
        # Config/Data
        ".json", ".yaml", ".yml", ".toml", ".xml", ".ini", ".cfg",
        # SQL
        ".sql",
        # Other
        ".lua", ".r", ".R", ".jl", ".dart", ".ex", ".exs",
        ".hs", ".ml", ".mli", ".fs", ".fsx", ".clj", ".cljs",
    }

    ENCODINGS = ["utf-8", "utf-8-sig", "latin-1", "cp1252"]

    def extract(self, file_path: Path) -> TextMetadata:
        """
        Extract text content from a source code file.

        Args:
            file_path: Path to the code file

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
            content = file_path.read_bytes().decode("utf-8", errors="replace")
            encoding_used = "utf-8 (with replacements)"

        # Calculate metrics
        lines = content.split("\n")
        words = content.split()

        # Detect language from extension
        language = self._detect_language(file_path.suffix.lower())

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
            language=language,
        )

    def _detect_language(self, suffix: str) -> Optional[str]:
        """Detect programming language from file extension."""
        language_map = {
            ".py": "python", ".pyi": "python", ".pyx": "python",
            ".js": "javascript", ".jsx": "javascript",
            ".ts": "typescript", ".tsx": "typescript",
            ".java": "java", ".kt": "kotlin", ".scala": "scala",
            ".go": "go", ".rs": "rust",
            ".c": "c", ".cpp": "cpp", ".cc": "cpp", ".h": "c",
            ".rb": "ruby", ".php": "php", ".pl": "perl",
            ".sh": "shell", ".bash": "shell",
            ".swift": "swift", ".m": "objective-c",
            ".sql": "sql",
            ".html": "html", ".css": "css",
            ".json": "json", ".yaml": "yaml", ".yml": "yaml",
            ".r": "r", ".R": "r",
        }
        return language_map.get(suffix)
