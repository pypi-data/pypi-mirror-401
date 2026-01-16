"""CSV/TSV file header extractor."""

import csv
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from ..types import CSVMetadata
from ..utils.file_utils import get_file_owner
from .header_detector import HeaderDetector


class CSVExtractor:
    """Extract headers from CSV/TSV files."""

    def __init__(self, count_rows: bool = False):
        """Initialize CSV extractor.

        Args:
            count_rows: Whether to count total rows (uses fast system commands when available)
        """
        self.count_rows = count_rows

    @staticmethod
    def _fast_line_count(file_path: Path) -> Optional[int]:
        """Fast line counting using system tools (wc -l on Unix).

        This is orders of magnitude faster than reading the file in Python.
        Falls back to None if not available.

        Args:
            file_path: Path to the file

        Returns:
            Line count or None if fast counting not available
        """
        # Only use on Unix-like systems
        if sys.platform not in ["darwin", "linux", "linux2"]:
            return None

        try:
            # Use wc -l which is fast even for huge files
            # Note: On network mounts this might take longer, but still faster than Python parsing
            result = subprocess.run(
                ["wc", "-l", str(file_path)],
                capture_output=True,
                text=True,
                timeout=120,  # Allow up to 2 minutes for network mounts
            )

            if result.returncode == 0:
                # wc -l output format: "  12345 filename.csv"
                line_count = int(result.stdout.split()[0])
                return line_count
        except (subprocess.TimeoutExpired, ValueError, IndexError, FileNotFoundError):
            pass

        return None

    def extract_header(self, file_path: Path) -> CSVMetadata:
        """Extract header row and metadata from CSV/TSV file.

        Uses smart header detection to handle multi-line headers (metadata, column names, units).

        Args:
            file_path: Path to the CSV/TSV file

        Returns:
            CSVMetadata instance with file metadata and header information
        """
        try:
            # Determine delimiter based on file extension
            delimiter = "\t" if file_path.suffix.lower() == ".tsv" else ","

            # Get file stats
            stats = file_path.stat()

            # Get file owner
            file_owner = get_file_owner(file_path)

            # Read sample to detect dialect for CSV files
            if file_path.suffix.lower() == ".csv":
                encodings = ["utf-8-sig", "utf-8", "latin-1", "cp1252", "iso-8859-1"]
                for encoding in encodings:
                    try:
                        with open(file_path, "r", encoding=encoding) as f:
                            sample = f.read(8192)
                            try:
                                dialect = csv.Sniffer().sniff(sample)
                                delimiter = dialect.delimiter
                            except csv.Error:
                                # Fall back to comma if detection fails
                                delimiter = ","
                        break
                    except (UnicodeDecodeError, UnicodeError):
                        continue

            # Use smart header detection
            header_row, header_row_index, metadata_rows = HeaderDetector.detect_header(file_path, delimiter)

            # Count total rows only if enabled
            row_count = None
            data_row_count = None
            if self.count_rows:
                # Try fast line counting first (wc -l on Unix)
                row_count = self._fast_line_count(file_path)

                # Fall back to Python-based counting only if fast method unavailable
                if row_count is None:
                    encodings = ["utf-8-sig", "utf-8", "latin-1", "cp1252", "iso-8859-1"]
                    for encoding in encodings:
                        try:
                            with open(file_path, "r", encoding=encoding) as f:
                                reader = csv.reader(f, delimiter=delimiter)
                                row_count = sum(1 for _ in reader)
                            break
                        except (UnicodeDecodeError, UnicodeError):
                            continue

                # Calculate data row count (excluding all header/metadata rows)
                if row_count is not None:
                    data_row_count = row_count - header_row_index - 1 if header_row_index < row_count else 0

            return CSVMetadata(
                filename=file_path.name,
                filepath=str(file_path.absolute()),
                file_type=file_path.suffix.lower(),
                file_size=stats.st_size,
                file_owner=file_owner,
                modified_at=datetime.fromtimestamp(stats.st_mtime).isoformat(),
                headers=header_row,
                header_row_index=header_row_index,
                metadata_rows=metadata_rows if metadata_rows else None,
                row_count=row_count,  # Keep for backward compatibility
                total_row_count=row_count,
                data_row_count=data_row_count,
                column_count=len(header_row),
                delimiter=repr(delimiter),  # Show \t for tab
                extracted_at=datetime.now().isoformat(),
            )

        except Exception as e:
            # Return error information
            return CSVMetadata(
                filename=file_path.name,
                filepath=str(file_path.absolute()),
                file_type=file_path.suffix.lower(),
                error=str(e),
                extracted_at=datetime.now().isoformat(),
            )
