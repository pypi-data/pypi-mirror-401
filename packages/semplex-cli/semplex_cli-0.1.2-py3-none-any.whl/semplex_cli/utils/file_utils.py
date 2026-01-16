"""File utility functions."""

import sys
from pathlib import Path
from typing import Optional


def get_file_owner(file_path: Path) -> Optional[str]:
    """Get the owner of a file.

    Args:
        file_path: Path to the file

    Returns:
        Username of the file owner, or None if unable to determine
    """
    try:
        # Get file stats
        stats = file_path.stat()

        # On Unix-like systems (Linux, macOS)
        if sys.platform != "win32":
            import pwd

            try:
                owner_info = pwd.getpwuid(stats.st_uid)
                return owner_info.pw_name
            except (KeyError, ImportError):
                # If we can't resolve the UID to a username, return the UID as a string
                return str(stats.st_uid)
        else:
            # On Windows, we need to use different APIs
            try:
                import win32security

                # Get file security descriptor
                sd = win32security.GetFileSecurity(
                    str(file_path), win32security.OWNER_SECURITY_INFORMATION
                )
                owner_sid = sd.GetSecurityDescriptorOwner()
                name, domain, _ = win32security.LookupAccountSid(None, owner_sid)
                return f"{domain}\\{name}" if domain else name
            except (ImportError, Exception):
                # If win32security is not available or fails, return None
                return None

    except (OSError, IOError):
        return None
