"""File watcher for live reindexing of code changes."""

import os
import threading
import time
from typing import Callable

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .indexer import is_gitignored, is_text_file


class DebouncedFileWatcher(FileSystemEventHandler):
    """Watches filesystem for changes and triggers callbacks with debouncing.

    The watcher collects file changes over a debounce period, then calls
    the callback with all changed files. This prevents triggering on
    rapid successive changes (e.g., Vim swap files, IDE auto-save).

    The actual indexing debounce and deduplication is handled by IndexQueue.
    This watcher just groups rapid changes together.
    """

    def __init__(
        self,
        root_dir: str,
        on_change: Callable[[list[str]], None],
        debounce_seconds: float = 3.0,
    ):
        """Initialize the debounced file watcher.

        Args:
            root_dir: Root directory to watch.
            on_change: Callback function that receives list of changed files.
            debounce_seconds: Seconds to wait after last change before triggering.
        """
        self.root_dir = root_dir
        self.on_change = on_change
        self.debounce_seconds = debounce_seconds

        self._observer = Observer()
        self._changed_files: dict[str, float] = {}  # file_path -> last_change_time
        self._lock = threading.Lock()
        self._timer: threading.Timer | None = None
        self._running = False

    def _should_process_file(self, file_path: str) -> bool:
        """Check if a file should be processed for indexing.

        Args:
            file_path: Path to the file.

        Returns:
            True if the file should be indexed, False otherwise.
        """
        # Skip directories
        if not os.path.isfile(file_path):
            return False

        # Skip if outside root dir
        try:
            os.path.relpath(file_path, self.root_dir)
        except ValueError:
            return False

        # Skip if gitignored
        if is_gitignored(self.root_dir, file_path):
            return False

        # Skip if not a text file we index
        if not is_text_file(file_path):
            return False

        return True

    def _schedule_reindex(self):
        """Schedule a callback after debounce period."""
        with self._lock:
            if self._timer is not None:
                self._timer.cancel()

            self._timer = threading.Timer(
                self.debounce_seconds,
                self._process_changed_files,
            )
            self._timer.start()

    def _process_changed_files(self):
        """Process all changed files (called after debounce)."""
        with self._lock:
            files_to_reindex = list(self._changed_files.keys())
            self._changed_files.clear()
            self._timer = None

        if files_to_reindex:
            # Separate into existing files and deleted files
            existing_files = []
            deleted_files = []

            for f in files_to_reindex:
                if not os.path.exists(f):
                    # File was deleted - queue it for removal
                    deleted_files.append(f)
                elif self._should_process_file(f):
                    existing_files.append(f)

            all_files = existing_files + deleted_files

            if all_files:
                print(f"[Watch] Processing {len(existing_files)} changed, {len(deleted_files)} deleted file(s)")
                for f in existing_files:
                    rel_path = os.path.relpath(f, self.root_dir)
                    print(f"  ~ {rel_path}")
                for f in deleted_files:
                    rel_path = os.path.relpath(f, self.root_dir)
                    print(f"  - {rel_path} (deleted)")

                try:
                    self.on_change(all_files)
                except Exception as e:
                    print(f"[Watch] Error: {e}")

    def _queue_file_change(self, file_path: str):
        """Queue a file change for processing after debounce."""
        if not self._should_process_file(file_path):
            return

        with self._lock:
            self._changed_files[file_path] = time.time()

        self._schedule_reindex()

    def on_created(self, event):
        """Handle file creation events."""
        if event.is_directory:
            return
        self._queue_file_change(event.src_path)

    def on_modified(self, event):
        """Handle file modification events."""
        if event.is_directory:
            return
        self._queue_file_change(event.src_path)

    def on_deleted(self, event):
        """Handle file deletion events."""
        if event.is_directory:
            return
        # Queue deletions directly - bypass _should_process_file since file no longer exists
        with self._lock:
            self._changed_files[event.src_path] = time.time()
        self._schedule_reindex()

    def on_moved(self, event):
        """Handle file move/rename events."""
        if event.is_directory:
            return
        # Treat as delete + create
        self._queue_file_change(event.dest_path)

    def start(self):
        """Start watching the filesystem."""
        if self._running:
            return

        self._observer.schedule(self, self.root_dir, recursive=True)
        self._observer.start()
        self._running = True
        print(f"[Watch] Watching {self.root_dir} for changes (debounce: {self.debounce_seconds}s)")

    def stop(self):
        """Stop watching the filesystem."""
        if not self._running:
            return

        with self._lock:
            if self._timer is not None:
                self._timer.cancel()
                self._timer = None

        self._observer.stop()
        self._observer.join(timeout=5)
        self._running = False
        print("[Watch] Stopped")

    def is_running(self) -> bool:
        """Check if the watcher is running."""
        return self._running
