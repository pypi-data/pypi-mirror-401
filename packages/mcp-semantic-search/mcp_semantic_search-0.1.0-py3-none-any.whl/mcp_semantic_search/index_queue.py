"""Centralized indexing queue with debouncing and deduplication."""

import os
import queue
import threading
import time
import traceback
from typing import TYPE_CHECKING

from .indexer import chunk_file, compute_file_hash, is_gitignored, is_text_file

if TYPE_CHECKING:
    from .embedder import GeminiEmbedder
    from .qdrant_client import QdrantCodeStore


class IndexQueue:
    """Centralized queue for indexing operations with debouncing and deduplication.

    Architecture:
    - index_codebase() adds files immediately (skip_debounce=True)
    - Live watcher adds files with per-file debounce
    - Single worker thread processes queue sequentially
    - Files are deduplicated: if already queued, skip

    State flow: pending (debouncing) -> queued -> processing -> indexed
    """

    def __init__(
        self,
        embedder: "GeminiEmbedder",
        store: "QdrantCodeStore",
        debounce_seconds: float = 3.0,
    ):
        """Initialize the indexing queue.

        Args:
            embedder: Gemini embedder instance.
            store: Qdrant store instance.
            debounce_seconds: Seconds to wait before indexing a changed file.
        """
        self.embedder = embedder
        self.store = store
        self.debounce_seconds = debounce_seconds

        # Queue of files to index (file paths)
        self._queue: queue.Queue[str] = queue.Queue()

        # Files currently being processed (for deduplication)
        self._processing: set[str] = set()
        self._queued: set[str] = set()

        # Pending debounced files: file_path -> timer_expiry_time
        self._pending: dict[str, float] = {}
        self._pending_timers: dict[str, threading.Timer] = {}

        # Worker management
        self._worker_thread: threading.Thread | None = None
        self._running = False
        self._lock = threading.Lock()

        # Progress tracking
        self._files_seen = 0
        self._files_processed = 0
        self._chunks_embedded = 0
        self._start_time: float | None = None
        self._errors: list[str] = []
        self._current_file: str | None = None
        self._root_dir: str | None = None

    def start(self):
        """Start the queue worker thread."""
        with self._lock:
            if self._running:
                return
            self._running = True
            self._start_time = time.time()

        self._worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self._worker_thread.start()
        print("[IndexQueue] Worker started")

    def stop(self):
        """Stop the queue worker thread."""
        with self._lock:
            if not self._running:
                return
            self._running = False

        # Cancel all pending timers
        with self._lock:
            for timer in self._pending_timers.values():
                timer.cancel()
            self._pending_timers.clear()
            self._pending.clear()

        # Wait for worker to finish
        if self._worker_thread:
            self._worker_thread.join(timeout=5)
        print("[IndexQueue] Worker stopped")

    def is_running(self) -> bool:
        """Check if the queue worker is running."""
        with self._lock:
            return self._running

    def add_files(self, file_paths: list[str], root_dir: str, skip_debounce: bool = False):
        """Add files to the indexing queue.

        Args:
            file_paths: List of file paths to index.
            root_dir: Root directory for relative path computation.
            skip_debounce: If True, add immediately (for batch indexing).
                          If False, apply per-file debounce (for live watcher).
        """
        with self._lock:
            self._root_dir = root_dir

        if skip_debounce:
            # Add immediately (for index_codebase)
            for file_path in file_paths:
                self._enqueue_immediate(file_path)
        else:
            # Add with per-file debounce (for live watcher)
            for file_path in file_paths:
                self._enqueue_with_debounce(file_path)

    def _enqueue_immediate(self, file_path: str):
        """Enqueue a file immediately, canceling any pending debounce."""
        with self._lock:
            # Cancel pending timer if exists
            if file_path in self._pending_timers:
                self._pending_timers[file_path].cancel()
                del self._pending_timers[file_path]
            if file_path in self._pending:
                del self._pending[file_path]

            # Skip if already queued or processing
            if file_path in self._queued or file_path in self._processing:
                return

            self._queued.add(file_path)
            self._files_seen += 1

        self._queue.put(file_path)

    def _enqueue_with_debounce(self, file_path: str):
        """Schedule a file for indexing after debounce.

        If the file is already pending/queued/processing, the debounce is reset.
        """
        with self._lock:
            # Cancel existing timer if any
            if file_path in self._pending_timers:
                self._pending_timers[file_path].cancel()

            # Skip if already being processed
            if file_path in self._processing:
                return

            # If already queued, remove and re-pending (will be re-added after debounce)
            if file_path in self._queued:
                # Can't remove from Queue, so we'll mark it for re-processing
                # For simplicity, we keep it queued and will skip duplicates during processing
                pass

            # Set new debounce timer
            expiry_time = time.time() + self.debounce_seconds
            self._pending[file_path] = expiry_time

            timer = threading.Timer(
                self.debounce_seconds,
                self._finalize_debounce,
                args=[file_path]
            )
            self._pending_timers[file_path] = timer
            timer.start()

    def _finalize_debounce(self, file_path: str):
        """Move file from pending to queued after debounce completes."""
        with self._lock:
            if file_path in self._pending:
                del self._pending[file_path]
            if file_path in self._pending_timers:
                del self._pending_timers[file_path]

            # Skip if already queued or processing
            if file_path in self._queued or file_path in self._processing:
                return

            self._queued.add(file_path)
            self._files_seen += 1

        self._queue.put(file_path)

    def _worker_loop(self):
        """Worker thread that processes files from the queue."""
        batch_size = 10
        batch_files: list[str] = []

        while self._running:
            try:
                # Get file with timeout to allow checking _running
                try:
                    file_path = self._queue.get(timeout=0.5)
                except queue.Empty:
                    # Check if there are more files to batch
                    if batch_files:
                        self._process_batch(batch_files)
                        batch_files = []
                    continue

                with self._lock:
                    self._processing.add(file_path)
                    self._queued.discard(file_path)
                    self._current_file = file_path

                # Collect into batch
                batch_files.append(file_path)

                # Process batch when full or immediately if queue is empty
                if len(batch_files) >= batch_size or self._queue.empty():
                    self._process_batch(batch_files)
                    batch_files = []

            except Exception as e:
                with self._lock:
                    self._errors.append(f"Worker error: {e}\n{traceback.format_exc()}")

        # Process remaining batch
        if batch_files:
            self._process_batch(batch_files)

    def _process_batch(self, file_paths: list[str]):
        """Process a batch of files."""
        if not self._running:
            return

        # Ensure collection exists
        self.store.ensure_collection()

        # Get existing metadata for incremental check
        existing_files = self.store.get_file_metadata()

        for file_path in file_paths:
            try:
                # Check if file still exists and should be indexed
                if not self._should_index_file(file_path):
                    # File was deleted or shouldn't be indexed
                    rel_path = file_path.replace(self._root_dir, "").lstrip("/") if self._root_dir else file_path
                    self.store.delete_chunks_for_file(rel_path)
                    continue

                rel_path = file_path.replace(self._root_dir, "").lstrip("/") if self._root_dir else file_path

                # Check if file changed (incremental)
                current_hash = compute_file_hash(file_path)
                stored_hash = existing_files.get(rel_path)

                if stored_hash == current_hash:
                    # File unchanged, skip
                    continue

                # Delete old chunks if any
                if stored_hash is not None:
                    self.store.delete_chunks_for_file(rel_path)

                # Chunk and index
                chunks = chunk_file(file_path, self._root_dir or "")
                if not chunks:
                    continue

                # Process in sub-batches to stay under API limit
                sub_batch_size = 90
                sub_batch = []

                for chunk in chunks:
                    sub_batch.append(chunk)
                    if len(sub_batch) >= sub_batch_size:
                        self._index_sub_batch(sub_batch, current_hash)
                        sub_batch = []

                if sub_batch:
                    self._index_sub_batch(sub_batch, current_hash)

                with self._lock:
                    self._files_processed += 1

            except Exception as e:
                with self._lock:
                    self._errors.append(f"{file_path}: {e}\n{traceback.format_exc()}")
            finally:
                with self._lock:
                    self._processing.discard(file_path)

        self._queue.task_done()

    def _should_index_file(self, file_path: str) -> bool:
        """Check if a file should be indexed."""
        if not os.path.isfile(file_path):
            return False

        if self._root_dir and is_gitignored(self._root_dir, file_path):
            return False

        if not is_text_file(file_path):
            return False

        return True

    def _index_sub_batch(self, chunks: list, file_hash: str):
        """Index a sub-batch of chunks."""
        texts = [chunk.content for chunk in chunks]
        embeddings = self.embedder.embed_batch(texts)
        self.store.add_chunks(chunks, embeddings, file_hash=file_hash)

        with self._lock:
            self._chunks_embedded += len(chunks)

    def get_progress(self) -> dict:
        """Get current indexing progress."""
        with self._lock:
            pending_count = len(self._pending)
            queued_count = self._queue.qsize()
            processing_count = len(self._processing)

            return {
                "running": self._running,
                "files_seen": self._files_seen,
                "files_processed": self._files_processed,
                "chunks_embedded": self._chunks_embedded,
                "pending": pending_count,
                "queued": queued_count,
                "processing": processing_count,
                "current_file": self._current_file,
                "root_dir": self._root_dir,
                "errors": self._errors.copy(),
                "elapsed_seconds": time.time() - self._start_time if self._start_time else 0,
            }

    def get_formatted_progress(self) -> str:
        """Get a human-readable progress report."""
        p = self.get_progress()

        if not p["running"] and p["files_processed"] == 0:
            return "No indexing operation has been started."

        output = [f"Indexing: {'running' if p['running'] else 'stopped'}"]
        output.append(f"Files: {p['files_processed']} processed, {p['pending']} pending, {p['queued']} queued")
        output.append(f"Chunks embedded: {p['chunks_embedded']}")

        if p["current_file"]:
            rel_path = p["current_file"]
            if p["root_dir"] and rel_path.startswith(p["root_dir"]):
                rel_path = rel_path[len(p["root_dir"]):].lstrip("/")
            output.append(f"Current: {rel_path}")

        if p["errors"]:
            output.append(f"\nErrors: {len(p['errors'])}")
            for err in p["errors"][:3]:
                output.append(f"  - {err.split(chr(10))[0]}")

        return "\n".join(output)
