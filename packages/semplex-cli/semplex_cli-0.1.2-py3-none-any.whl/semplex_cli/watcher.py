"""File watcher implementation."""

import asyncio
import hashlib
import json
import os
import signal
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import httpx
import pathspec
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver

from .chunker import DocumentChunker, chunk_document
from .extractors import get_extractor, get_document_extractor, is_tabular_file, is_document_file
from .utils.config import Config
from .utils.process import cleanup_pid_file, save_pid
from .utils.state import StateManager

console = Console()

# Thread-local storage for event loops
_thread_local = threading.local()


class FileChangeHandler(FileSystemEventHandler):
    """Handle file system events."""

    def __init__(
        self,
        file_types: List[str],
        ignore_patterns: List[str],
        api_url: str,
        state_manager: StateManager,
        config: Config,
        count_rows: bool = False,
        debug_mode: bool = False,
        debug_output_file: Optional[str] = None,
    ):
        self.file_types = [ft.lower() for ft in file_types]
        self.ignore_patterns = ignore_patterns
        self.api_url = api_url
        self.debug_mode = debug_mode
        self.debug_output_file = debug_output_file
        self.state_manager = state_manager
        self.config = config
        self.count_rows = count_rows
        self.processed_files: Set[Tuple[str, float]] = set()
        self._processed_files_lock = threading.Lock()

        # Document processing config
        self.document_config = config.documents
        self.document_file_types = [ft.lower() for ft in self.document_config.file_types] if self.document_config.enabled else []

        # Chunker for document processing
        self.chunker = DocumentChunker(
            chunk_size=self.document_config.chunk_size,
            chunk_overlap=self.document_config.chunk_overlap,
        ) if self.document_config.enabled else None

        # Create gitignore-style pattern matcher
        self.ignore_spec = pathspec.PathSpec.from_lines(
            pathspec.patterns.GitWildMatchPattern, ignore_patterns
        )

    def _get_event_loop(self) -> asyncio.AbstractEventLoop:
        """Get or create an event loop for the current thread."""
        if not hasattr(_thread_local, 'loop') or _thread_local.loop is None or _thread_local.loop.is_closed():
            _thread_local.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(_thread_local.loop)
        return _thread_local.loop

    def get_all_file_types(self) -> List[str]:
        """Get all file types to watch (tabular + documents)."""
        all_types = list(self.file_types)
        # Add document types, avoiding duplicates
        for ft in self.document_file_types:
            if ft not in all_types:
                all_types.append(ft)
        return all_types

    def should_process(self, file_path: Path) -> bool:
        """Check if file should be processed."""
        # Check file type (both tabular and document types)
        suffix = file_path.suffix.lower()
        all_types = self.get_all_file_types()
        if suffix not in all_types:
            return False

        # Check file size for documents
        if suffix in self.document_file_types:
            try:
                file_size = file_path.stat().st_size
                if file_size > self.document_config.max_file_size:
                    return False
            except OSError:
                pass

        # Check ignore patterns using gitignore-style matching
        # Convert to relative path for pattern matching
        try:
            # For watching directories, we need to check the full path
            # against patterns using POSIX-style paths
            path_str = str(file_path.as_posix())
            if self.ignore_spec.match_file(path_str):
                return False
        except Exception:
            # Fallback to simple name matching if pathspec fails
            if self.ignore_spec.match_file(file_path.name):
                return False

        # Check if file has already been processed (using state manager)
        if self.state_manager.is_processed(file_path):
            return False

        # In-memory debounce check (to avoid processing the same file multiple times in quick succession)
        try:
            file_stat = file_path.stat()
            file_key = (str(file_path), file_stat.st_mtime)

            with self._processed_files_lock:
                if file_key in self.processed_files:
                    return False

                self.processed_files.add(file_key)

                # Clean up old entries (keep only last 1000)
                if len(self.processed_files) > 1000:
                    self.processed_files = set(list(self.processed_files)[-1000:])
        except OSError:
            # If we can't stat the file, skip it
            return False

        return True

    def on_modified(self, event: FileSystemEvent) -> None:
        """Handle file modification events."""
        if event.is_directory:
            return

        self.process_file(event.src_path)

    def on_created(self, event: FileSystemEvent) -> None:
        """Handle file creation events."""
        if event.is_directory:
            return

        self.process_file(event.src_path)

    def process_file(self, file_path_str: str, silent: bool = False) -> bool:
        """Process a file and extract headers or content.

        Args:
            file_path_str: Path to the file to process
            silent: If True, suppress console output (for parallel processing)

        Returns:
            True if file was processed successfully, False otherwise
        """
        file_path = Path(file_path_str)

        if not file_path.exists() or not self.should_process(file_path):
            return False

        suffix = file_path.suffix.lower()

        # Route to appropriate processor based on file type
        if is_tabular_file(file_path):
            return self._process_tabular_file(file_path, silent)
        elif is_document_file(file_path) and self.document_config.enabled:
            return self._process_document_file(file_path, silent)
        else:
            return False

    def _process_tabular_file(self, file_path: Path, silent: bool = False) -> bool:
        """Process a tabular file (CSV, Excel) and send metadata.

        Args:
            file_path: Path to the file
            silent: If True, suppress console output

        Returns:
            True if file was processed successfully, False otherwise
        """
        try:
            if not silent:
                console.print(f"[cyan]Processing:[/cyan] {file_path.name}")

            # Extract header
            extractor = get_extractor(file_path, count_rows=self.count_rows)
            metadata = extractor.extract_header(file_path)

            # Check if extraction had errors
            if metadata.error:
                if not silent:
                    console.print(f"[red]Error extracting metadata from {file_path.name}:[/red] {metadata.error}")
                self.state_manager.mark_processed(file_path, success=False, error=metadata.error)
                return False

            # Convert Pydantic model to dict and add user information
            metadata_dict = metadata.model_dump()
            metadata_dict["user_email"] = self.config.api.get_user_email()
            metadata_dict["machine_name"] = self.config.user.machine_name

            # Determine organization based on file path
            organization_handle = self.config.get_organization_for_path(file_path)
            metadata_dict["organization_handle"] = organization_handle

            # Send to backend (async) - use thread-local event loop
            loop = self._get_event_loop()
            loop.run_until_complete(self.send_metadata(metadata_dict))

            # Mark as successfully processed
            self.state_manager.mark_processed(file_path, success=True)

            if not silent:
                console.print(f"[green]✓[/green] Sent: {file_path.name}")

            return True

        except Exception as e:
            error_msg = str(e)
            if not silent:
                console.print(f"[red]Error processing {file_path.name}:[/red] {error_msg}")
            self.state_manager.mark_processed(file_path, success=False, error=error_msg)
            return False

    def _process_document_file(self, file_path: Path, silent: bool = False) -> bool:
        """Process a document file (text, code, PDF, etc.) and send chunks for embedding.

        Args:
            file_path: Path to the file
            silent: If True, suppress console output

        Returns:
            True if file was processed successfully, False otherwise
        """
        try:
            if not silent:
                console.print(f"[cyan]Processing document:[/cyan] {file_path.name}")

            # Get the appropriate document extractor
            extractor = get_document_extractor(file_path)
            if extractor is None:
                if not silent:
                    console.print(f"[yellow]No extractor available for {file_path.name}[/yellow]")
                return False

            # Extract text content
            text_metadata = extractor.extract(file_path)

            # Check for errors
            if text_metadata.error:
                if not silent:
                    console.print(f"[red]Error extracting content from {file_path.name}:[/red] {text_metadata.error}")
                self.state_manager.mark_processed(file_path, success=False, error=text_metadata.error)
                return False

            # Skip empty files
            if not text_metadata.content or not text_metadata.content.strip():
                if not silent:
                    console.print(f"[dim]Skipping empty file: {file_path.name}[/dim]")
                self.state_manager.mark_processed(file_path, success=True)
                return True

            # Chunk the content
            chunks = chunk_document(
                content=text_metadata.content,
                chunk_size=self.document_config.chunk_size,
                chunk_overlap=self.document_config.chunk_overlap,
            )

            if not chunks:
                if not silent:
                    console.print(f"[dim]No chunks generated for: {file_path.name}[/dim]")
                self.state_manager.mark_processed(file_path, success=True)
                return True

            # Compute file_id (SHA-256 of content)
            file_id = hashlib.sha256(text_metadata.content.encode()).hexdigest()

            # Determine organization
            organization_handle = self.config.get_organization_for_path(file_path)

            # Send chunks to annotation service
            loop = self._get_event_loop()
            loop.run_until_complete(
                self.send_chunks(
                    file_id=file_id,
                    file_path=file_path,
                    text_metadata=text_metadata,
                    chunks=chunks,
                    organization_handle=organization_handle,
                )
            )

            # Mark as successfully processed
            self.state_manager.mark_processed(file_path, success=True)

            if not silent:
                console.print(f"[green]✓[/green] Sent {len(chunks)} chunk(s): {file_path.name}")

            return True

        except Exception as e:
            error_msg = str(e)
            if not silent:
                console.print(f"[red]Error processing {file_path.name}:[/red] {error_msg}")
            self.state_manager.mark_processed(file_path, success=False, error=error_msg)
            return False

    async def send_metadata(self, metadata: dict) -> None:
        """Send metadata to backend or debug file."""
        if self.debug_mode and self.debug_output_file:
            # Write to debug file
            await self._write_to_debug_file(metadata)
        else:
            # Send to API
            await self._send_to_api(metadata)

    async def _write_to_debug_file(self, metadata: dict) -> None:
        """Write metadata to debug output file."""
        debug_path = Path(self.debug_output_file)

        # Create request representation
        request_data = {
            "timestamp": datetime.now().isoformat(),
            "method": "POST",
            "url": self.api_url,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": metadata,
        }

        # Append to file
        with open(debug_path, "a") as f:
            f.write(json.dumps(request_data, indent=2))
            f.write("\n" + "=" * 80 + "\n")

    async def _send_to_api(self, metadata: dict) -> None:
        """Send metadata to API endpoint."""
        # Build headers with auth credentials if available
        headers = {"Content-Type": "application/json"}

        api_key = self.config.api.get_api_key()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        user_email = self.config.api.get_user_email()
        if user_email:
            headers["X-User-Email"] = user_email

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    self.api_url,
                    json=metadata,
                    headers=headers,
                )
                response.raise_for_status()

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 401:
                    console.print(f"[red]Authentication failed:[/red] Run 'semplex auth login' to authenticate")
                else:
                    console.print(f"[yellow]Warning:[/yellow] Failed to send to API: {e}")
            except httpx.HTTPError as e:
                console.print(f"[yellow]Warning:[/yellow] Failed to send to API: {e}")

    async def send_chunks(
        self,
        file_id: str,
        file_path: Path,
        text_metadata,
        chunks: List[Dict],
        organization_handle: Optional[str] = None,
    ) -> None:
        """Send document chunks to frontend API for processing.

        Args:
            file_id: SHA-256 hash of file content
            file_path: Path to the file
            text_metadata: TextMetadata object with file content and metadata
            chunks: List of chunk dictionaries from chunk_document()
            organization_handle: Optional organization handle
        """
        payload = {
            "file_id": file_id,
            "filepath": str(file_path.absolute()),
            "filename": file_path.name,
            "file_type": file_path.suffix.lower(),
            "file_size": text_metadata.file_size,
            "chunks": chunks,
            "store_text": self.document_config.store_text,
            "user_email": self.config.api.get_user_email(),
            "organization_handle": organization_handle,
            "machine_name": self.config.user.machine_name,
        }

        if self.debug_mode and self.debug_output_file:
            # Write to debug file
            await self._write_chunks_to_debug_file(payload)
        else:
            # Send to frontend API (same flow as metadata)
            await self._send_chunks_to_api(payload)

    async def _write_chunks_to_debug_file(self, payload: dict) -> None:
        """Write chunk payload to debug output file."""
        debug_path = Path(self.debug_output_file)
        # Use the same base URL as metadata, just different endpoint
        base_url = self.api_url.replace("/api/metadata", "")
        endpoint = f"{base_url}/api/document-chunks"

        # Create request representation
        request_data = {
            "timestamp": datetime.now().isoformat(),
            "method": "POST",
            "url": endpoint,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": payload,
        }

        # Append to file
        with open(debug_path, "a") as f:
            f.write(json.dumps(request_data, indent=2))
            f.write("\n" + "=" * 80 + "\n")

    async def _send_chunks_to_api(self, payload: dict) -> None:
        """Send chunks to frontend API for processing."""
        # Use the same base URL as metadata, just different endpoint
        base_url = self.api_url.replace("/api/metadata", "")
        endpoint = f"{base_url}/api/document-chunks"

        # Build headers with auth credentials if available
        headers = {"Content-Type": "application/json"}

        api_key = self.config.api.get_api_key()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        user_email = self.config.api.get_user_email()
        if user_email:
            headers["X-User-Email"] = user_email

        # Longer timeout for large documents with many chunks
        timeout = httpx.Timeout(60.0, connect=10.0)

        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                response = await client.post(
                    endpoint,
                    json=payload,
                    headers=headers,
                )
                response.raise_for_status()

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 401:
                    console.print(f"[red]Authentication failed:[/red] Run 'semplex auth login' to authenticate")
                else:
                    error_detail = ""
                    try:
                        error_detail = e.response.text[:200]
                    except Exception:
                        pass
                    console.print(f"[yellow]Warning:[/yellow] Failed to send chunks: {e.response.status_code} {error_detail}")
            except httpx.HTTPError as e:
                console.print(f"[yellow]Warning:[/yellow] Failed to send chunks to API: {e}")


class FileWatcher:
    """Main file watcher class."""

    def __init__(self, config: Config, scan_depth: int = 0, use_polling: bool = False):
        self.config = config
        self.observer: Optional[Observer] = None
        self.handler: Optional[FileChangeHandler] = None
        self.state_manager = StateManager()
        self.scan_depth = scan_depth
        self.use_polling = use_polling
        self.current_scan_dir: Optional[str] = None

    def _collect_files_to_process(self) -> List[Path]:
        """Collect all files that need to be processed."""
        files_to_process = []

        # Get all file types (tabular + documents)
        all_file_types = self.handler.get_all_file_types()

        for directory in self.config.get_all_directories():
            dir_path = Path(directory).expanduser().resolve()
            if not dir_path.exists():
                continue

            if self.config.watch.recursive:
                # Use os.walk for recursive scanning with real-time directory progress
                for root, dirs, files in os.walk(dir_path):
                    current_dir = Path(root)

                    # Calculate depth relative to watch root
                    try:
                        relative_parts = current_dir.relative_to(dir_path).parts
                        depth = len(relative_parts)
                    except ValueError:
                        continue

                    # Filter out ignored directories (modify dirs in-place to prune traversal)
                    dirs_to_remove = []
                    for dirname in dirs:
                        dir_to_check = current_dir / dirname
                        # Check against ignore patterns
                        dir_str = str(dir_to_check.as_posix())
                        if self.handler.ignore_spec.match_file(dir_str):
                            dirs_to_remove.append(dirname)

                    # Remove ignored directories from traversal
                    for dirname in dirs_to_remove:
                        dirs.remove(dirname)

                    # Print directory being scanned if within scan_depth
                    if self.scan_depth > 0 and depth <= self.scan_depth:
                        console.print(f"[dim]Scanning {current_dir}...[/dim]")

                    # Collect files in this directory
                    for filename in files:
                        file_path = current_dir / filename

                        # Check if file type matches (tabular or document)
                        if file_path.suffix.lower() not in all_file_types:
                            continue

                        # Check file size for document files
                        if file_path.suffix.lower() in self.handler.document_file_types:
                            try:
                                if file_path.stat().st_size > self.handler.document_config.max_file_size:
                                    continue
                            except OSError:
                                continue

                        # Check ignore patterns using pathspec
                        path_str = str(file_path.as_posix())
                        if self.handler.ignore_spec.match_file(path_str):
                            continue

                        # Check if already processed
                        if self.state_manager.is_processed(file_path):
                            continue

                        files_to_process.append(file_path)
            else:
                # Non-recursive: just scan the immediate directory
                if self.scan_depth > 0:
                    console.print(f"[dim]Scanning {dir_path}...[/dim]")

                for file_path in dir_path.glob("*"):
                    if not file_path.is_file():
                        continue

                    # Check if file type matches (tabular or document)
                    if file_path.suffix.lower() not in all_file_types:
                        continue

                    # Check file size for document files
                    if file_path.suffix.lower() in self.handler.document_file_types:
                        try:
                            if file_path.stat().st_size > self.handler.document_config.max_file_size:
                                continue
                        except OSError:
                            continue

                    # Check ignore patterns using pathspec
                    path_str = str(file_path.as_posix())
                    if self.handler.ignore_spec.match_file(path_str):
                        continue

                    # Check if already processed
                    if self.state_manager.is_processed(file_path):
                        continue

                    files_to_process.append(file_path)

        return files_to_process

    def _process_file_wrapper(self, file_path: Path) -> Tuple[str, bool, Optional[str]]:
        """Wrapper for process_file that returns result info for progress tracking.

        Returns:
            Tuple of (filename, success, error_message)
        """
        try:
            success = self.handler.process_file(str(file_path), silent=True)
            return (file_path.name, success, None)
        except Exception as e:
            return (file_path.name, False, str(e))

    def _scan_existing_files(self) -> None:
        """Scan watched directories and process any unprocessed files."""
        console.print("[cyan]Scanning for existing files...[/cyan]")

        try:
            # First, collect all files to process
            files_to_process = self._collect_files_to_process()
            total_files = len(files_to_process)

            if total_files == 0:
                console.print("[dim]No new files found in watched directories[/dim]\n")
                return

            # Get effective worker count
            max_workers = self.config.watch.get_effective_max_workers()
            console.print(f"[dim]Found {total_files} file(s) to process using {max_workers} worker(s)[/dim]")

            files_processed = 0
            files_failed = 0

            # Use ThreadPoolExecutor for parallel processing
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                console=console,
            ) as progress:
                task = progress.add_task(f"[cyan]Processing files...", total=total_files)

                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    # Submit all files for processing
                    future_to_file = {
                        executor.submit(self._process_file_wrapper, file_path): file_path
                        for file_path in files_to_process
                    }

                    # Process results as they complete
                    for future in as_completed(future_to_file):
                        file_path = future_to_file[future]
                        try:
                            filename, success, error = future.result()
                            if success:
                                files_processed += 1
                                progress.console.print(f"[green]✓[/green] {filename}")
                            elif error:
                                files_failed += 1
                                progress.console.print(f"[red]✗[/red] {filename}: {error}")
                            # else: file was skipped (already processed or filtered)
                        except Exception as e:
                            files_failed += 1
                            progress.console.print(f"[red]✗[/red] {file_path.name}: {e}")

                        progress.advance(task)

            # Summary
            if files_processed > 0 or files_failed > 0:
                summary = f"[green]Processed {files_processed} file(s)[/green]"
                if files_failed > 0:
                    summary += f", [red]{files_failed} failed[/red]"
                console.print(f"\n{summary}\n")
            else:
                console.print("[dim]No new files processed[/dim]\n")

        except KeyboardInterrupt:
            console.print("\n[yellow]Scan interrupted.[/yellow]")
            raise

    def start(self) -> None:
        """Start watching directories."""
        # Save PID
        pid_path = Config.get_pid_path()
        save_pid(pid_path)

        try:
            # Setup signal handlers for graceful shutdown
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)

            # Create event handler
            self.handler = FileChangeHandler(
                file_types=self.config.watch.get_active_file_types(),
                ignore_patterns=self.config.watch.ignore_patterns,
                api_url=self.config.api.url,
                state_manager=self.state_manager,
                config=self.config,
                count_rows=self.config.watch.count_rows,
                debug_mode=self.config.api.debug_mode,
                debug_output_file=self.config.api.debug_output_file,
            )

            # Process existing files before starting the watcher
            self._scan_existing_files()

            # Create observer (use polling mode to avoid inotify limits on large directories)
            if self.use_polling:
                console.print("[yellow]Using polling mode (slower but avoids inotify limits)[/yellow]")
                self.observer = PollingObserver(timeout=5)
            else:
                self.observer = Observer()

            # Schedule directories
            for directory in self.config.get_all_directories():
                dir_path = Path(directory).expanduser()
                if not dir_path.exists():
                    console.print(f"[yellow]Warning:[/yellow] Directory not found: {directory}")
                    continue

                self.observer.schedule(
                    self.handler,
                    str(dir_path),
                    recursive=self.config.watch.recursive,
                )
                console.print(f"[green]Watching:[/green] {directory}")

            # Start observer
            self.observer.start()

            console.print("\n[bold green]File watcher started![/bold green]")
            if self.config.api.debug_mode:
                console.print(f"[yellow]Debug mode:[/yellow] Writing to {self.config.api.debug_output_file}")
            else:
                console.print(f"[cyan]API endpoint:[/cyan] {self.config.api.url}")

            console.print("\n[dim]Press Ctrl+C to stop, or use 'semplex stop'[/dim]\n")

            # Keep the watcher running
            while self.observer.is_alive():
                self.observer.join(1)

        except KeyboardInterrupt:
            self.stop()
        except Exception as e:
            console.print(f"\n[red]Error:[/red] {e}")
            self.stop()
            raise

    def stop(self) -> None:
        """Stop watching directories."""
        console.print("\n[yellow]Stopping file watcher...[/yellow]")

        if self.observer:
            try:
                self.observer.stop()
                # Only join if the observer was actually started
                if self.observer.is_alive():
                    self.observer.join(timeout=5)
            except RuntimeError:
                # Observer wasn't fully started, ignore
                pass

        # Cleanup PID file
        cleanup_pid_file(Config.get_pid_path())

        console.print("[green]File watcher stopped.[/green]")

    def _signal_handler(self, signum: int, frame) -> None:
        """Handle termination signals."""
        try:
            self.stop()
        except Exception:
            # Ignore errors during signal handling
            pass
        sys.exit(0)
