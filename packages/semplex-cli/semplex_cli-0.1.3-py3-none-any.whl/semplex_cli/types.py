"""Shared type definitions for Good Head CLI and services.

This module defines Pydantic models for metadata extraction and processing.
These models ensure type safety across CLI, MongoDB storage, and backend services.
"""

from datetime import datetime
from typing import Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field, field_validator


# ============================================================================
# File Metadata Models
# ============================================================================


class BaseFileMetadata(BaseModel):
    """Base metadata common to all file types."""

    filename: str = Field(description="Name of the file")
    filepath: str = Field(description="Absolute path to the file")
    file_type: str = Field(description="File extension (e.g., .csv, .xlsx)")
    file_size: Optional[int] = Field(None, description="File size in bytes")
    file_owner: Optional[str] = Field(None, description="Owner of the file (username)")
    modified_at: Optional[str] = Field(None, description="ISO timestamp of last modification")
    extracted_at: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="ISO timestamp when metadata was extracted",
    )
    error: Optional[str] = Field(None, description="Error message if extraction failed")

    @field_validator("file_type")
    @classmethod
    def normalize_file_type(cls, v: str) -> str:
        """Ensure file type starts with a dot and is lowercase."""
        if not v.startswith("."):
            v = f".{v}"
        return v.lower()


class CSVMetadata(BaseFileMetadata):
    """Metadata extracted from CSV/TSV files."""

    headers: List[str] = Field(
        default_factory=list, description="Column headers from the detected header row"
    )
    header_row_index: int = Field(
        default=0, description="0-based index of the row containing column headers"
    )
    metadata_rows: Optional[List[List[str]]] = Field(
        None, description="Rows above the header (metadata, units, descriptions)"
    )
    row_count: Optional[int] = Field(
        None, description="Total number of rows including header (deprecated, use total_row_count)"
    )
    total_row_count: Optional[int] = Field(None, description="Total number of rows in the file")
    data_row_count: Optional[int] = Field(
        None, description="Number of data rows (excluding headers/metadata)"
    )
    column_count: Optional[int] = Field(None, description="Number of columns")
    delimiter: Optional[str] = Field(None, description="Delimiter used (e.g., ',', '\\t')")

    @field_validator("file_type")
    @classmethod
    def validate_csv_type(cls, v: str) -> str:
        """Ensure file type is CSV or TSV."""
        if v not in [".csv", ".tsv"]:
            raise ValueError(f"Invalid file type for CSV metadata: {v}")
        return v


class ExcelMetadata(BaseFileMetadata):
    """Metadata extracted from Excel files."""

    headers: List[str] = Field(
        default_factory=list, description="Column headers from the first row"
    )
    row_count: Optional[int] = Field(None, description="Total number of rows")
    column_count: Optional[int] = Field(None, description="Number of columns")
    sheet_name: Optional[str] = Field(None, description="Name of the active/processed sheet")
    sheet_names: List[str] = Field(
        default_factory=list, description="Names of all sheets in the workbook"
    )

    @field_validator("file_type")
    @classmethod
    def validate_excel_type(cls, v: str) -> str:
        """Ensure file type is Excel."""
        if v not in [".xlsx", ".xls", ".xlsm"]:
            raise ValueError(f"Invalid file type for Excel metadata: {v}")
        return v


class JSONMetadata(BaseFileMetadata):
    """Metadata extracted from JSON files."""

    headers: List[str] = Field(
        default_factory=list,
        description="Top-level keys if JSON is an object, or inferred from array items",
    )
    row_count: Optional[int] = Field(
        None, description="Number of items if JSON is an array"
    )
    column_count: Optional[int] = Field(
        None, description="Number of top-level keys or inferred columns"
    )
    is_array: Optional[bool] = Field(None, description="Whether the root element is an array")
    depth: Optional[int] = Field(None, description="Maximum nesting depth")

    @field_validator("file_type")
    @classmethod
    def validate_json_type(cls, v: str) -> str:
        """Ensure file type is JSON."""
        if v not in [".json", ".jsonl"]:
            raise ValueError(f"Invalid file type for JSON metadata: {v}")
        return v


class TextMetadata(BaseFileMetadata):
    """Metadata extracted from text-based documents (txt, md, pdf, docx, code files)."""

    content: str = Field(description="Full text content of the document")
    char_count: Optional[int] = Field(None, description="Number of characters")
    word_count: Optional[int] = Field(None, description="Approximate word count")
    line_count: Optional[int] = Field(None, description="Number of lines")
    encoding: Optional[str] = Field(None, description="Text encoding (e.g., utf-8)")
    language: Optional[str] = Field(None, description="Detected or inferred language")

    # For documents with structure
    page_count: Optional[int] = Field(None, description="Number of pages (for PDF, PPTX)")
    section_count: Optional[int] = Field(None, description="Number of sections/slides")


# Union type for all file metadata
FileMetadata = Union[CSVMetadata, ExcelMetadata, JSONMetadata, TextMetadata, BaseFileMetadata]


# ============================================================================
# Annotation Service Models
# ============================================================================


class AnnotationRequest(BaseModel):
    """Request to annotate a file with LinkML schema."""

    request_id: str = Field(description="Unique identifier for the metadata record in MongoDB")
    mode: Literal["sync", "async"] = Field(
        default="async",
        description="Sync returns result immediately, async queues for processing",
    )
    owner: Optional[str] = Field(None, description="Owner/user who submitted the request")
    priority: int = Field(
        default=1, ge=1, le=10, description="Processing priority (1=low, 10=high)"
    )


class SemanticQualityCheck(BaseModel):
    """Result of semantic quality check on file headers."""

    has_semantic_info: bool = Field(
        description="Whether headers contain meaningful semantic information"
    )
    reason: str = Field(description="Explanation of the quality assessment")
    confidence: float = Field(
        ge=0.0, le=1.0, description="Confidence in the quality assessment"
    )


class ColumnAnalysis(BaseModel):
    """Analysis of a single column/slot."""

    name: str = Field(description="Column name from header")
    inferred_type: Optional[str] = Field(
        None,
        description="Inferred data type (string, integer, date, boolean, identifier, etc.)",
    )
    description: Optional[str] = Field(None, description="Generated description of the column")
    ontology_hints: List[str] = Field(
        default_factory=list, description="Potential ontology mappings (URIs)"
    )
    confidence: float = Field(
        ge=0.0, le=1.0, description="Confidence in the column analysis"
    )
    is_uncertain: bool = Field(
        default=False, description="Whether this column has unclear semantics"
    )
    uncertainty_reason: Optional[str] = Field(
        None, description="Reason for uncertainty if applicable"
    )


class LinkMLAnnotationResponse(BaseModel):
    """Structured response from LinkML generation agent.

    This is the primary output from the annotation service.
    """

    # Status of annotation attempt
    status: Literal["success", "low_confidence", "no_semantic_info", "error"] = Field(
        description=(
            "Overall status:\n"
            "- success: LinkML generated successfully\n"
            "- low_confidence: Generated but low confidence\n"
            "- no_semantic_info: Headers are nonsensical/random\n"
            "- error: Processing error occurred"
        )
    )

    # Confidence metrics
    confidence: float = Field(
        ge=0.0, le=1.0, description="Overall confidence in generated LinkML model (0-1)"
    )

    # LinkML model output
    linkml_model: Optional[str] = Field(
        None, description="Generated LinkML model as YAML string"
    )
    linkml_version: str = Field(
        default="1.7.0", description="LinkML specification version"
    )
    class_name: Optional[str] = Field(None, description="Name of the generated LinkML class")
    slot_count: Optional[int] = Field(
        None, description="Number of slots/columns in the model"
    )

    # Uncertainty tracking
    uncertain_columns: Optional[List[str]] = Field(
        None, description="Column names where semantic meaning was unclear"
    )
    uncertain_column_details: Optional[Dict[str, str]] = Field(
        None, description="Map of column name to uncertainty reason"
    )

    # Ontology mappings
    ontology_mappings: Optional[Dict[str, List[str]]] = Field(
        None,
        description="Map of column/slot name to ontology URIs (e.g., schema.org, NCIT)",
    )

    # Quality indicators
    warnings: Optional[List[str]] = Field(
        None, description="Non-critical warnings during generation"
    )
    rationale: Optional[str] = Field(
        None, description="Natural language explanation of decisions made"
    )

    # Metadata
    processing_time_seconds: Optional[float] = Field(
        None, description="Time taken to generate the LinkML model"
    )
    token_usage: Optional[Dict[str, int]] = Field(
        None, description="LLM token usage (prompt_tokens, completion_tokens, total_tokens)"
    )


class AnnotationResult(BaseModel):
    """Complete annotation result stored in PostgreSQL."""

    id: Optional[str] = Field(None, description="UUID primary key")
    request_id: str = Field(description="Original request ID from MongoDB")

    # Original file metadata
    filename: str
    filepath: str
    owner: Optional[str] = None
    file_type: str
    file_size: Optional[int] = None
    modified_at: Optional[str] = None
    row_count: Optional[int] = None
    column_count: Optional[int] = None

    # Header data
    raw_headers: List[str] = Field(
        default_factory=list, description="Original column headers"
    )

    # LinkML model
    linkml_model: Optional[str] = Field(None, description="Generated LinkML YAML")
    linkml_version: Optional[str] = None
    class_name: Optional[str] = None

    # Annotation metadata
    status: str = Field(description="Status from LinkMLAnnotationResponse")
    confidence: float = Field(description="Confidence score")
    uncertain_columns: Optional[List[str]] = None
    ontology_mappings: Optional[Dict[str, List[str]]] = None
    warnings: Optional[List[str]] = None

    # Vector embedding
    embedding: Optional[List[float]] = Field(
        None, description="Vector embedding of the LinkML model"
    )

    # Timestamps
    created_at: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="When the record was created",
    )
    processed_at: Optional[str] = Field(None, description="When annotation completed")


# ============================================================================
# API Response Models
# ============================================================================


class HealthResponse(BaseModel):
    """Health check response."""

    status: Literal["healthy", "unhealthy"]
    service: str = "annotation-service"
    version: str = "0.1.0"
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


class ReadinessResponse(BaseModel):
    """Readiness check response with dependency status."""

    ready: bool
    dependencies: Dict[str, bool] = Field(
        description="Status of each dependency (mongodb, postgres, redis, etc.)"
    )
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


class ErrorResponse(BaseModel):
    """Standard error response."""

    error: str = Field(description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    request_id: Optional[str] = Field(None, description="Request ID if applicable")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
