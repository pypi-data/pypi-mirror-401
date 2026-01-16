"""Configuration management for Semplex CLI."""

import os
from pathlib import Path
from typing import List, Optional

import yaml
from pydantic import BaseModel, Field


class UserConfig(BaseModel):
    """User configuration model."""

    machine_name: Optional[str] = Field(default=None, description="Machine/cluster name being indexed")


class OrganizationConfig(BaseModel):
    """Organization configuration with associated directories."""

    handle: str = Field(..., description="Organization handle/identifier")
    directories: List[str] = Field(default_factory=list, description="Directories to watch for this organization")


class WatchConfig(BaseModel):
    """Watch configuration model."""

    directories: List[str] = Field(default_factory=list, description="Legacy: directories without org mapping")
    file_types: List[str] = Field(
        default_factory=lambda: [
            # Tabular data
            ".xlsx", ".xls", ".xlsm", ".csv", ".tsv", ".parquet",
            # Structured data
            ".json", ".jsonl", ".xml", ".yaml", ".yml", ".toml",
            # Documents
            ".txt", ".md", ".rst", ".pdf", ".docx", ".doc", ".pptx", ".rtf",
            # Code
            ".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".rs", ".java",
            ".c", ".cpp", ".h", ".hpp", ".rb", ".php", ".swift", ".kt",
            ".scala", ".r", ".sql", ".sh", ".bash", ".zsh",
            # Web
            ".html", ".htm", ".css", ".scss", ".sass", ".less",
        ],
        description="File extensions to process",
    )
    excluded_file_types: List[str] = Field(
        default_factory=list,
        description="File extensions to exclude from processing",
    )
    recursive: bool = True
    ignore_patterns: List[str] = Field(
        default_factory=lambda: [
            "*.tmp",       # Temporary files
            "~$*",         # Excel/Office temp files
            "**/.*",       # Hidden files and directories (starts with .)
            "**/temp",     # Common temp directories
            "**/tmp",      # Common temp directories
            "**/out",      # Common output directories
            "**/node_modules",  # Node.js dependencies
            "**/__pycache__",   # Python cache
            "**/venv",          # Python virtual environments
            "**/.venv",         # Python virtual environments (hidden)
            "**/.git",          # Git directory
            "**/site-packages", # Python packages
        ]
    )
    count_rows: bool = Field(
        default=False,
        description="Count total rows in files (requires reading entire file, slower for large files)",
    )
    max_workers: Optional[int] = Field(
        default=None,
        description="Max parallel workers for file processing. None = auto (CPU count / 2, min 1, max 8)",
    )

    def get_active_file_types(self) -> List[str]:
        """Get file types to process (file_types minus excluded_file_types)."""
        excluded = set(self.excluded_file_types)
        return [ft for ft in self.file_types if ft not in excluded]

    def get_effective_max_workers(self) -> int:
        """Get the effective max workers count with autoscaling."""
        if self.max_workers is not None:
            return max(1, self.max_workers)
        # Auto-scale: use half of CPU cores, min 1, max 8
        cpu_count = os.cpu_count() or 2
        return max(1, min(8, cpu_count // 2))


class APIConfig(BaseModel):
    """API configuration model."""

    url: str = "https://semplex.simage.ai/api/metadata"
    annotation_service_url: Optional[str] = Field(
        default=None,
        description="URL for annotation service (for document chunk embedding). If not set, uses url base.",
    )
    api_key: Optional[str] = Field(default=None, description="API key for authentication")
    user_email: Optional[str] = Field(default=None, description="Authenticated user email")
    default_organization: Optional[str] = Field(
        default=None,
        description="Default organization handle for file metadata",
    )
    timeout: int = 30
    retry_attempts: int = 3
    debug_mode: bool = False
    debug_output_file: Optional[str] = None

    def get_api_key(self) -> Optional[str]:
        """Get API key from config or environment variable."""
        return os.environ.get("SEMPLEX_API_KEY") or self.api_key

    def get_user_email(self) -> Optional[str]:
        """Get user email from config or environment variable."""
        return os.environ.get("SEMPLEX_USER_EMAIL") or self.user_email

    def get_organization(self) -> Optional[str]:
        """Get organization from config or environment variable."""
        return os.environ.get("SEMPLEX_ORGANIZATION") or self.default_organization

    def is_authenticated(self) -> bool:
        """Check if the CLI is authenticated with valid credentials.

        Checks both config file and environment variables.
        """
        return bool(self.get_api_key() and self.get_user_email())

    def get_annotation_service_url(self) -> str:
        """Get the annotation service URL, deriving from API URL if not set."""
        if self.annotation_service_url:
            return self.annotation_service_url
        # Derive from API URL by parsing and replacing the port
        # e.g., http://localhost:3000/api/metadata -> http://localhost:8080
        from urllib.parse import urlparse
        parsed = urlparse(self.url)
        # For localhost, use port 8080 for annotation service
        if parsed.hostname in ("localhost", "127.0.0.1"):
            return f"{parsed.scheme}://{parsed.hostname}:8080"
        # For production, assume annotation service is at same host on /api/v1 path
        # This should be explicitly configured via annotation_service_url for production
        return f"{parsed.scheme}://{parsed.hostname}:8080"


class DocumentConfig(BaseModel):
    """Configuration for document processing and chunking."""

    enabled: bool = Field(
        default=True,
        description="Enable document processing (text files, PDF, DOCX, etc.)",
    )
    file_types: List[str] = Field(
        default_factory=lambda: [
            # Text
            ".txt", ".md", ".rst",
            # Code (common)
            ".py", ".js", ".ts", ".go", ".rs", ".java",
            # Office
            ".pdf", ".docx", ".pptx",
        ],
        description="File types to process as documents",
    )
    chunk_size: int = Field(
        default=512,
        description="Target tokens per chunk",
    )
    chunk_overlap: int = Field(
        default=64,
        description="Tokens to overlap between chunks",
    )
    store_text: bool = Field(
        default=False,
        description="Store chunk text in cloud database (privacy consideration)",
    )
    max_file_size: int = Field(
        default=50_000_000,  # 50MB
        description="Maximum file size to process (bytes)",
    )


class Config(BaseModel):
    """Main configuration model."""

    user: UserConfig = Field(default_factory=UserConfig)
    watch: WatchConfig = Field(default_factory=WatchConfig)
    api: APIConfig = Field(default_factory=APIConfig)
    documents: DocumentConfig = Field(default_factory=DocumentConfig)
    organizations: List[OrganizationConfig] = Field(
        default_factory=list, description="Organization configurations with directory mappings"
    )

    @classmethod
    def get_config_path(cls) -> Path:
        """Get the configuration file path."""
        config_dir = Path.home() / ".config" / "semplex"
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / "config.yaml"

    @classmethod
    def get_pid_path(cls) -> Path:
        """Get the PID file path."""
        config_dir = Path.home() / ".config" / "semplex"
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / "watcher.pid"

    @classmethod
    def load(cls) -> "Config":
        """Load configuration from file."""
        config_path = cls.get_config_path()

        if not config_path.exists():
            return cls()

        with open(config_path, "r") as f:
            data = yaml.safe_load(f)
            return cls(**data) if data else cls()

    def save(self) -> None:
        """Save configuration to file."""
        config_path = self.get_config_path()

        with open(config_path, "w") as f:
            yaml.dump(self.model_dump(), f, default_flow_style=False, sort_keys=False)

    def is_configured(self) -> bool:
        """Check if the CLI is configured."""
        return len(self.watch.directories) > 0 or len(self.organizations) > 0

    def get_all_directories(self) -> List[str]:
        """Get all directories to watch (from both organizations and legacy config)."""
        directories = list(self.watch.directories)
        for org in self.organizations:
            directories.extend(org.directories)
        return directories

    def get_organization_for_path(self, file_path: Path) -> Optional[str]:
        """
        Get the organization handle for a given file path.

        Args:
            file_path: Path to the file

        Returns:
            Organization handle if found, None otherwise
        """
        file_path = file_path.resolve()

        # Check each organization's directories
        for org in self.organizations:
            for directory in org.directories:
                dir_path = Path(directory).expanduser().resolve()
                try:
                    # Check if file_path is relative to this directory
                    file_path.relative_to(dir_path)
                    return org.handle
                except ValueError:
                    # Not a subdirectory, continue
                    continue

        # No organization mapping found
        return None
