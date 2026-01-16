"""Tests for metadata extractors."""

import csv
from pathlib import Path

import openpyxl
import pytest

from semplex_cli.extractors import get_extractor
from semplex_cli.extractors.csv_extractor import CSVExtractor
from semplex_cli.extractors.excel_extractor import ExcelExtractor


@pytest.fixture
def temp_csv_file(tmp_path):
    """Create a temporary CSV file for testing."""
    csv_file = tmp_path / "test.csv"
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Age", "Email"])
        writer.writerow(["Alice", "30", "alice@example.com"])
        writer.writerow(["Bob", "25", "bob@example.com"])
    return csv_file


@pytest.fixture
def temp_excel_file(tmp_path):
    """Create a temporary Excel file for testing."""
    excel_file = tmp_path / "test.xlsx"
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(["Name", "Age", "Email"])
    sheet.append(["Alice", 30, "alice@example.com"])
    sheet.append(["Bob", 25, "bob@example.com"])
    workbook.save(excel_file)
    return excel_file


def test_csv_extractor(temp_csv_file):
    """Test CSV metadata extraction."""
    extractor = CSVExtractor()
    metadata = extractor.extract_header(temp_csv_file)

    assert metadata["filename"] == "test.csv"
    assert metadata["file_type"] == ".csv"
    assert metadata["headers"] == ["Name", "Age", "Email"]
    assert metadata["row_count"] == 3
    assert metadata["column_count"] == 3
    assert "error" not in metadata


def test_excel_extractor(temp_excel_file):
    """Test Excel metadata extraction."""
    extractor = ExcelExtractor()
    metadata = extractor.extract_header(temp_excel_file)

    assert metadata["filename"] == "test.xlsx"
    assert metadata["file_type"] == ".xlsx"
    assert metadata["headers"] == ["Name", "Age", "Email"]
    assert metadata["row_count"] == 3
    assert metadata["column_count"] == 3
    assert "error" not in metadata


def test_get_extractor_csv(temp_csv_file):
    """Test getting CSV extractor."""
    extractor = get_extractor(temp_csv_file)
    assert isinstance(extractor, CSVExtractor)


def test_get_extractor_excel(temp_excel_file):
    """Test getting Excel extractor."""
    extractor = get_extractor(temp_excel_file)
    assert isinstance(extractor, ExcelExtractor)


def test_get_extractor_unsupported():
    """Test getting extractor for unsupported file type."""
    with pytest.raises(ValueError, match="Unsupported file type"):
        get_extractor(Path("test.txt"))


def test_csv_extractor_nonexistent_file():
    """Test CSV extractor with nonexistent file."""
    extractor = CSVExtractor()
    metadata = extractor.extract_header(Path("nonexistent.csv"))

    assert "error" in metadata
    assert metadata["filename"] == "nonexistent.csv"


def test_excel_extractor_nonexistent_file():
    """Test Excel extractor with nonexistent file."""
    extractor = ExcelExtractor()
    metadata = extractor.extract_header(Path("nonexistent.xlsx"))

    assert "error" in metadata
    assert metadata["filename"] == "nonexistent.xlsx"
