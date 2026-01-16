"""File metadata extractors."""

from pathlib import Path
from typing import Optional, Protocol, Set

from .csv_extractor import CSVExtractor
from .excel_extractor import ExcelExtractor
from .text_extractor import TextExtractor
from .code_extractor import CodeExtractor

# Optional extractors (may not be available)
try:
    from .pdf_extractor import PDFExtractor
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    PDFExtractor = None

try:
    from .docx_extractor import DocxExtractor
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False
    DocxExtractor = None

try:
    from .pptx_extractor import PptxExtractor
    PPTX_AVAILABLE = True
except ImportError:
    PPTX_AVAILABLE = False
    PptxExtractor = None


class Extractor(Protocol):
    """Protocol for file extractors."""

    def extract_header(self, file_path: Path) -> dict:
        """Extract header/metadata from file."""
        ...


class DocumentExtractor(Protocol):
    """Protocol for document extractors that return TextMetadata."""

    def extract(self, file_path: Path):
        """Extract text content from file."""
        ...


def get_extractor(file_path: Path, count_rows: bool = False) -> Optional[Extractor]:
    """Get the appropriate extractor for a tabular file.

    Args:
        file_path: Path to the file
        count_rows: Whether to count total rows (requires reading entire file)

    Returns:
        Appropriate extractor instance, or None if unsupported
    """
    suffix = file_path.suffix.lower()

    if suffix in [".xlsx", ".xls", ".xlsm"]:
        return ExcelExtractor(count_rows=count_rows)
    elif suffix in [".csv", ".tsv"]:
        return CSVExtractor(count_rows=count_rows)
    else:
        return None


def get_document_extractor(file_path: Path) -> Optional[DocumentExtractor]:
    """Get the appropriate extractor for a text document.

    Args:
        file_path: Path to the file

    Returns:
        Appropriate document extractor instance, or None if unsupported
    """
    suffix = file_path.suffix.lower()

    # Plain text files
    if suffix in TextExtractor.SUPPORTED_EXTENSIONS:
        return TextExtractor()

    # Code files
    if suffix in CodeExtractor.SUPPORTED_EXTENSIONS:
        return CodeExtractor()

    # PDF files
    if suffix == ".pdf":
        if PDF_AVAILABLE:
            return PDFExtractor()
        else:
            return None

    # Word documents
    if suffix == ".docx":
        if DOCX_AVAILABLE:
            return DocxExtractor()
        else:
            return None

    # PowerPoint presentations
    if suffix == ".pptx":
        if PPTX_AVAILABLE:
            return PptxExtractor()
        else:
            return None

    return None


def is_tabular_file(file_path: Path) -> bool:
    """Check if a file is a tabular data file (CSV, Excel)."""
    suffix = file_path.suffix.lower()
    return suffix in [".xlsx", ".xls", ".xlsm", ".csv", ".tsv"]


def is_document_file(file_path: Path) -> bool:
    """Check if a file is a text document that can be chunked."""
    suffix = file_path.suffix.lower()

    # Check supported extensions
    if suffix in TextExtractor.SUPPORTED_EXTENSIONS:
        return True
    if suffix in CodeExtractor.SUPPORTED_EXTENSIONS:
        return True
    if suffix == ".pdf" and PDF_AVAILABLE:
        return True
    if suffix == ".docx" and DOCX_AVAILABLE:
        return True
    if suffix == ".pptx" and PPTX_AVAILABLE:
        return True

    return False


def get_supported_document_extensions() -> Set[str]:
    """Get all supported document extensions."""
    extensions = set()
    extensions.update(TextExtractor.SUPPORTED_EXTENSIONS)
    extensions.update(CodeExtractor.SUPPORTED_EXTENSIONS)

    if PDF_AVAILABLE:
        extensions.add(".pdf")
    if DOCX_AVAILABLE:
        extensions.add(".docx")
    if PPTX_AVAILABLE:
        extensions.add(".pptx")

    return extensions


__all__ = [
    "Extractor",
    "DocumentExtractor",
    "get_extractor",
    "get_document_extractor",
    "is_tabular_file",
    "is_document_file",
    "get_supported_document_extensions",
    "ExcelExtractor",
    "CSVExtractor",
    "TextExtractor",
    "CodeExtractor",
    "PDFExtractor",
    "DocxExtractor",
    "PptxExtractor",
    "PDF_AVAILABLE",
    "DOCX_AVAILABLE",
    "PPTX_AVAILABLE",
]
