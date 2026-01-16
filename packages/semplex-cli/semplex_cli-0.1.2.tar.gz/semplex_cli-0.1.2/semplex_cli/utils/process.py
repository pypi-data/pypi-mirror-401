"""Process management utilities."""

import os
import signal
from pathlib import Path
from typing import Optional

import psutil


def save_pid(pid_path: Path) -> None:
    """Save the current process ID to file."""
    with open(pid_path, "w") as f:
        f.write(str(os.getpid()))


def read_pid(pid_path: Path) -> Optional[int]:
    """Read the process ID from file."""
    if not pid_path.exists():
        return None

    try:
        with open(pid_path, "r") as f:
            return int(f.read().strip())
    except (ValueError, IOError):
        return None


def is_process_running(pid: int) -> bool:
    """Check if a process with given PID is running."""
    try:
        process = psutil.Process(pid)
        return process.is_running()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return False


def stop_process(pid: int, timeout: int = 5) -> bool:
    """Stop a process with given PID."""
    try:
        process = psutil.Process(pid)

        # Try graceful termination first
        process.terminate()

        try:
            process.wait(timeout=timeout)
            return True
        except psutil.TimeoutExpired:
            # Force kill if graceful termination fails
            process.kill()
            process.wait(timeout=2)
            return True

    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return False


def cleanup_pid_file(pid_path: Path) -> None:
    """Remove the PID file."""
    if pid_path.exists():
        pid_path.unlink()
