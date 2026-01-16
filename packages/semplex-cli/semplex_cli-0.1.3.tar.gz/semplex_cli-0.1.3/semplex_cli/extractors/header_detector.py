"""Smart header detection for CSV/TSV files."""

import csv
import re
from pathlib import Path
from typing import List, Optional, Tuple


class HeaderDetector:
    """Detect headers in CSV/TSV files, including multi-line headers."""

    @staticmethod
    def detect_header(file_path: Path, delimiter: str = ",", max_rows: int = 10) -> Tuple[List[str], int, List[List[str]]]:
        """Detect the header row(s) in a CSV/TSV file.

        This function analyzes the first few rows to determine:
        1. Whether there are multi-line headers (metadata, column names, units)
        2. Which row contains the actual column names

        Args:
            file_path: Path to the CSV/TSV file
            delimiter: Field delimiter
            max_rows: Maximum number of rows to analyze

        Returns:
            Tuple of (header_list, header_row_index, metadata_rows)
            - header_list: The actual column names
            - header_row_index: 0-based index of the header row
            - metadata_rows: All rows above the header (useful context like units, descriptions)
        """
        # Try multiple encodings
        encodings = ["utf-8-sig", "utf-8", "latin-1", "cp1252", "iso-8859-1"]
        rows = []

        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as f:
                    reader = csv.reader(f, delimiter=delimiter)

                    # Read first few rows
                    for i, row in enumerate(reader):
                        if i >= max_rows:
                            break
                        rows.append(row)

                    if not rows:
                        return [], 0

                    # Successfully read file, break out of encoding loop
                    break
            except (UnicodeDecodeError, UnicodeError):
                # Try next encoding
                rows = []
                continue

        if not rows:
            # If all encodings failed, return empty
            return [], 0, []

        # Analyze rows to find the header
        header_idx = HeaderDetector._find_header_row(rows)

        # Extract metadata rows (all rows before the header)
        metadata_rows = rows[:header_idx] if header_idx > 0 else []

        return rows[header_idx] if header_idx < len(rows) else rows[0], header_idx, metadata_rows

    @staticmethod
    def _find_header_row(rows: List[List[str]]) -> int:
        """Find which row is the actual header.

        Strategy:
        1. Check if first row has mostly empty cells or is a title/metadata row
        2. Check if there's a row that looks like column names followed by a row with units
        3. Look for rows with parentheses (units) or special patterns
        4. Default to first non-empty row

        Args:
            rows: List of rows from CSV file

        Returns:
            0-based index of the header row
        """
        if not rows or len(rows) < 2:
            return 0

        scores = []
        for idx, row in enumerate(rows[:5]):  # Only check first 5 rows
            score = HeaderDetector._score_as_header(row, idx, rows)
            scores.append((idx, score))

        # Return the row with the highest score
        best_idx = max(scores, key=lambda x: x[1])[0]
        return best_idx

    @staticmethod
    def _score_as_header(row: List[str], row_idx: int, all_rows: List[List[str]]) -> float:
        """Score a row based on how likely it is to be the header.

        Args:
            row: The row to score
            row_idx: Index of this row
            all_rows: All rows for context

        Returns:
            Score (higher = more likely to be header)
        """
        if not row:
            return 0.0

        score = 0.0
        non_empty_count = sum(1 for cell in row if cell and cell.strip())

        # Penalize rows with too few non-empty cells
        if non_empty_count < len(row) * 0.3:
            score -= 10.0

        # Check if this is the first row
        if row_idx == 0:
            # First row gets a bonus, but check if it looks like metadata
            if HeaderDetector._looks_like_metadata_row(row):
                score -= 5.0  # Penalize metadata rows
            else:
                score += 2.0  # Bonus for being first row

        # Check if next row looks like units (has parentheses)
        if row_idx + 1 < len(all_rows):
            next_row = all_rows[row_idx + 1]
            if HeaderDetector._looks_like_units_row(next_row):
                score += 10.0  # Strong indicator this is the column names row

        # Check if this row itself looks like units
        if HeaderDetector._looks_like_units_row(row):
            score -= 15.0  # Units row is not the header we want

        # Check if row has mostly text (good for headers)
        text_count = sum(1 for cell in row if cell and not HeaderDetector._is_numeric(cell.strip()))
        if non_empty_count > 0:
            text_ratio = text_count / non_empty_count
            score += text_ratio * 5.0

        # Check if the row after this one looks like data
        if row_idx + 1 < len(all_rows):
            next_row = all_rows[row_idx + 1]
            if not HeaderDetector._looks_like_units_row(next_row):
                # Check if next row has more numeric values (data row)
                next_numeric = sum(1 for cell in next_row if cell and HeaderDetector._is_numeric(cell.strip()))
                if len(next_row) > 0 and next_numeric / len(next_row) > 0.5:
                    score += 5.0

        # Penalize rows that look like pure data (mostly numbers)
        numeric_count = sum(1 for cell in row if cell and HeaderDetector._is_numeric(cell.strip()))
        if non_empty_count > 0 and numeric_count / non_empty_count > 0.7:
            score -= 8.0

        # Check for common header patterns (case-insensitive)
        header_keywords = ['date', 'time', 'id', 'name', 'value', 'type', 'status', 'temperature', 'pressure', 'latitude', 'longitude']
        for cell in row:
            if cell and any(keyword in cell.lower() for keyword in header_keywords):
                score += 3.0
                break

        return score

    @staticmethod
    def _looks_like_metadata_row(row: List[str]) -> bool:
        """Check if row looks like a metadata/title row.

        Metadata rows typically have:
        - A title in the first cell
        - Mostly empty cells after that
        - No structured column-like data

        Args:
            row: The row to check

        Returns:
            True if row looks like metadata
        """
        if not row:
            return False

        non_empty = [cell for cell in row if cell and cell.strip()]

        # If mostly empty except for first few cells
        if len(non_empty) <= 2 and len(row) > 3:
            return True

        # If first cell is long text and rest are empty
        if len(row) > 2 and row[0] and len(row[0]) > 10:
            if sum(1 for cell in row[1:] if not cell or not cell.strip()) > len(row) * 0.7:
                return True

        return False

    @staticmethod
    def _looks_like_units_row(row: List[str]) -> bool:
        """Check if row looks like a units row.

        Units rows typically have:
        - Parentheses: (°C), (mm), (Degrees)
        - Short text
        - Similar pattern across columns

        Args:
            row: The row to check

        Returns:
            True if row looks like units
        """
        if not row:
            return False

        parentheses_count = sum(1 for cell in row if cell and '(' in cell and ')' in cell)
        non_empty = sum(1 for cell in row if cell and cell.strip())

        # If more than 30% of non-empty cells have parentheses
        if non_empty > 0 and parentheses_count / non_empty > 0.3:
            return True

        return False

    @staticmethod
    def _is_numeric(value: str) -> bool:
        """Check if a string value is numeric.

        Args:
            value: String to check

        Returns:
            True if value is numeric
        """
        if not value:
            return False

        # Remove common numeric formatting
        clean_value = value.replace(',', '').replace(' ', '').strip()

        try:
            float(clean_value)
            return True
        except ValueError:
            # Check for date patterns
            if re.match(r'\d{4}-\d{2}-\d{2}', clean_value):
                return True
            if re.match(r'\d{2}/\d{2}/\d{2,4}', clean_value):
                return True
            return False
