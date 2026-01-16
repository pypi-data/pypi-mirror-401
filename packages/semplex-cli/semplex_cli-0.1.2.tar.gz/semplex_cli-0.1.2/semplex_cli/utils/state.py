"""State management for tracking processed files."""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional


class StateManager:
    """Manages the state of processed files."""

    def __init__(self, state_file: Optional[Path] = None):
        """Initialize state manager.

        Args:
            state_file: Path to state file. If None, uses default config location.
        """
        if state_file is None:
            from .config import Config
            config_dir = Path.home() / ".config" / "semplex"
            config_dir.mkdir(parents=True, exist_ok=True)
            state_file = config_dir / "state.json"

        self.state_file = state_file
        self._state: Dict[str, dict] = self._load_state()

    def _load_state(self) -> Dict[str, dict]:
        """Load state from file."""
        if not self.state_file.exists():
            return {}

        try:
            with open(self.state_file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def _save_state(self) -> None:
        """Save state to file."""
        try:
            with open(self.state_file, "w") as f:
                json.dump(self._state, f, indent=2)
        except IOError as e:
            # Log error but don't crash
            print(f"Warning: Failed to save state: {e}")

    def is_processed(self, file_path: Path, retry_failed: bool = True) -> bool:
        """Check if a file has been processed.

        Args:
            file_path: Path to the file
            retry_failed: If True, files that failed will be considered not processed

        Returns:
            True if file has been successfully processed and hasn't changed since
        """
        file_key = str(file_path.absolute())

        if file_key not in self._state:
            return False

        file_info = self._state[file_key]

        # If retry_failed is True and the file previously failed, return False to retry
        if retry_failed and not file_info.get("success", True):
            return False

        # Check if file has been modified since last processing
        try:
            current_mtime = file_path.stat().st_mtime
            last_mtime = file_info.get("mtime", 0)
            current_size = file_path.stat().st_size
            last_size = file_info.get("size", 0)

            # File is considered processed if mtime and size match
            return current_mtime == last_mtime and current_size == last_size
        except (OSError, IOError):
            # If we can't stat the file, consider it not processed
            return False

    def mark_processed(self, file_path: Path, success: bool = True, error: Optional[str] = None) -> None:
        """Mark a file as processed.

        Args:
            file_path: Path to the file
            success: Whether processing was successful
            error: Error message if processing failed
        """
        file_key = str(file_path.absolute())

        try:
            stats = file_path.stat()
            self._state[file_key] = {
                "filename": file_path.name,
                "mtime": stats.st_mtime,
                "size": stats.st_size,
                "processed_at": datetime.now().isoformat(),
                "success": success,
                "error": error,
            }
            self._save_state()
        except (OSError, IOError) as e:
            print(f"Warning: Failed to mark file as processed: {e}")

    def get_file_info(self, file_path: Path) -> Optional[dict]:
        """Get processing info for a file.

        Args:
            file_path: Path to the file

        Returns:
            Dictionary with processing info, or None if not found
        """
        file_key = str(file_path.absolute())
        return self._state.get(file_key)

    def clear_file(self, file_path: Path) -> None:
        """Remove a file from the state.

        Args:
            file_path: Path to the file
        """
        file_key = str(file_path.absolute())
        if file_key in self._state:
            del self._state[file_key]
            self._save_state()

    def clear_all(self) -> None:
        """Clear all state."""
        self._state = {}
        self._save_state()

    def get_stats(self) -> dict:
        """Get statistics about processed files.

        Returns:
            Dictionary with statistics
        """
        total = len(self._state)
        successful = sum(1 for v in self._state.values() if v.get("success", False))
        failed = total - successful

        return {
            "total": total,
            "successful": successful,
            "failed": failed,
        }
