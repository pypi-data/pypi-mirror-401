"""Background indexing with progress tracking for MCP server."""

import threading
import time
import traceback
from typing import TYPE_CHECKING

from .indexer import chunk_file, compute_file_hash, find_code_files

if TYPE_CHECKING:
    from .embedder import GeminiEmbedder
    from .qdrant_client import QdrantCodeStore


class BackgroundIndexer:
    """Manages asynchronous indexing operations with progress tracking.

    State transitions:
    - idle -> indexing -> completed/error -> idle
    """

    # States
    STATE_IDLE = "idle"
    STATE_INDEXING = "indexing"
    STATE_COMPLETED = "completed"
    STATE_ERROR = "error"

    # Maximum batch size for embedding API (Gemini limit is 100)
    MAX_EMBED_BATCH = 90  # Stay under 100 to be safe

    def __init__(self):
        """Initialize the background indexer."""
        self._state = self.STATE_IDLE
        self._lock = threading.Lock()
        self._thread: threading.Thread | None = None
        self._start_time: float | None = None
        self._end_time: float | None = None
        self._error: str | None = None

        # Progress tracking
        self._files_total = 0
        self._files_processed = 0
        self._chunks_embedded = 0
        self._current_file: str | None = None
        self._errors: list[str] = []

        # Index type info
        self._index_type: str | None = None  # "full" or "incremental"
        self._root_dir: str | None = None

    def start_indexing(
        self,
        root_dir: str,
        embedder: "GeminiEmbedder",
        store: "QdrantCodeStore",
        max_files: int | None = None,
        force_reindex: bool = False,
    ) -> str:
        """Start a full indexing operation in the background.

        Args:
            root_dir: Root directory to index.
            embedder: Gemini embedder instance.
            store: Qdrant store instance.
            max_files: Optional file limit for testing.
            force_reindex: If True, clear existing index first.

        Returns:
            Status message.
        """
        with self._lock:
            if self._state == self.STATE_INDEXING:
                return "Indexing already in progress. Use get_index_progress() to check status."

            # Reset state
            self._state = self.STATE_INDEXING
            self._start_time = time.time()
            self._end_time = None
            self._error = None
            self._files_total = 0
            self._files_processed = 0
            self._chunks_embedded = 0
            self._current_file = None
            self._errors = []
            self._index_type = "force" if force_reindex else "incremental"
            self._root_dir = root_dir

        # Start background thread
        self._thread = threading.Thread(
            target=self._run_indexing,
            args=(root_dir, embedder, store, max_files, force_reindex),
            daemon=True,
        )
        self._thread.start()

        return "Indexing started in background. Use get_index_progress() to track progress."

    def _run_indexing(
        self,
        root_dir: str,
        embedder: "GeminiEmbedder",
        store: "QdrantCodeStore",
        max_files: int | None,
        force_reindex: bool,
    ):
        """Run indexing in background thread.

        If force_reindex=True: Clear collection and index all files.
        If force_reindex=False: Incremental index using file hashes.
        """
        try:
            # Clear existing index if requested
            if force_reindex and store.collection_exists():
                store.delete_collection()

            # Ensure collection exists
            store.ensure_collection()

            # Get existing file metadata for incremental reindexing
            existing_files = {} if force_reindex else store.get_file_metadata()

            # Find files to index
            files = find_code_files(root_dir, max_files)
            with self._lock:
                self._files_total = len(files)

            batch_chunks = []
            current_batch_hash = None
            processed_rel_paths: set[str] = set()

            for file_path in files:
                with self._lock:
                    self._current_file = file_path

                try:
                    rel_path = file_path.replace(root_dir, "").lstrip("/")
                    processed_rel_paths.add(rel_path)

                    # Skip unchanged files (incremental mode)
                    if not force_reindex:
                        current_hash = compute_file_hash(file_path)
                        stored_hash = existing_files.get(rel_path)

                        if stored_hash == current_hash:
                            with self._lock:
                                self._files_processed += 1
                            continue

                        # File changed - delete old chunks first
                        if stored_hash is not None:
                            store.delete_chunks_for_file(rel_path)

                    chunks = chunk_file(file_path, root_dir)
                    if not chunks:
                        with self._lock:
                            self._files_processed += 1
                        continue

                    # Add chunks in batches to stay under API limit
                    for chunk in chunks:
                        batch_chunks.append(chunk)
                        # Process batch when full
                        if len(batch_chunks) >= self.MAX_EMBED_BATCH:
                            texts = [c.content for c in batch_chunks]
                            embeddings = embedder.embed_batch(texts)
                            # Store with file_hash for incremental tracking
                            file_hash = None if force_reindex else compute_file_hash(file_path)
                            store.add_chunks(batch_chunks, embeddings, file_hash=file_hash)
                            with self._lock:
                                self._chunks_embedded += len(batch_chunks)
                            batch_chunks = []

                    current_batch_hash = None if force_reindex else compute_file_hash(file_path)
                    with self._lock:
                        self._files_processed += 1

                except Exception as e:
                    with self._lock:
                        self._errors.append(f"{file_path}: {e}\n{traceback.format_exc()}")

            # Process remaining chunks
            if batch_chunks:
                texts = [chunk.content for chunk in batch_chunks]
                embeddings = embedder.embed_batch(texts)
                file_hash = None if force_reindex else compute_file_hash(root_dir + "/" + list(processed_rel_paths)[-1] if processed_rel_paths else "")
                store.add_chunks(batch_chunks, embeddings, file_hash=file_hash)
                with self._lock:
                    self._chunks_embedded += len(batch_chunks)

            # Detect deleted files (incremental mode only)
            if not force_reindex:
                for rel_path in existing_files:
                    if rel_path not in processed_rel_paths:
                        store.delete_chunks_for_file(rel_path)

            with self._lock:
                self._state = self.STATE_COMPLETED
                self._end_time = time.time()
                self._current_file = None

        except Exception as e:
            with self._lock:
                self._state = self.STATE_ERROR
                self._error = f"{e}\n{traceback.format_exc()}"
                self._end_time = time.time()

    def get_progress(self) -> dict:
        """Get current indexing progress.

        Returns:
            Dictionary with progress information.
        """
        with self._lock:
            result = {
                "state": self._state,
                "index_type": self._index_type,
                "root_dir": self._root_dir,
                "files_total": self._files_total,
                "files_processed": self._files_processed,
                "chunks_embedded": self._chunks_embedded,
                "current_file": self._current_file,
                "errors": self._errors.copy(),
                "error": self._error,
            }

            # Calculate elapsed time
            if self._start_time:
                end = self._end_time or time.time()
                result["elapsed_seconds"] = end - self._start_time
            else:
                result["elapsed_seconds"] = 0

            return result

    def is_running(self) -> bool:
        """Check if indexing is currently running.

        Returns:
            True if indexing is in progress.
        """
        with self._lock:
            return self._state == self.STATE_INDEXING

    def stop(self) -> bool:
        """Stop the current indexing operation.

        Returns:
            True if stopped, False if nothing was running.
        """
        with self._lock:
            if self._state != self.STATE_INDEXING:
                return False

            self._state = self.STATE_IDLE
            self._current_file = None
            self._end_time = time.time()
            return True

    def get_formatted_progress(self) -> str:
        """Get a human-readable progress report.

        Returns:
            Formatted progress string.
        """
        p = self.get_progress()

        if p["state"] == self.STATE_IDLE:
            if p["index_type"]:
                # Previous run completed
                return f"""Indexing status: {p['index_type']} index {p['state']}
- Previously completed in {p.get('elapsed_seconds', 0):.1f}s
- Files processed: {p['files_processed']}
- Chunks embedded: {p['chunks_embedded']}
"""
            return "No indexing operation has been started."

        output = [f"Indexing status: {p['state']}"]

        if p["index_type"]:
            output.append(f"Type: {p['index_type']}")

        output.append(f"Files: {p['files_processed']}/{p['files_total']}")
        output.append(f"Chunks embedded: {p['chunks_embedded']}")

        if p["state"] == self.STATE_COMPLETED:
            output.append(f"Completed in {p.get('elapsed_seconds', 0):.1f}s")

        if p["current_file"] and p["state"] == self.STATE_INDEXING:
            rel_path = p["current_file"]
            if p["root_dir"] and rel_path.startswith(p["root_dir"]):
                rel_path = rel_path[len(p["root_dir"]):].lstrip("/")
            output.append(f"Current: {rel_path}")

        if p["elapsed_seconds"] and p["state"] != self.STATE_COMPLETED:
            output.append(f"Elapsed: {p['elapsed_seconds']:.1f}s")

        if p["state"] == self.STATE_ERROR and p["error"]:
            output.append(f"\nError:\n{p['error']}")

        if p["errors"]:
            output.append(f"\nFile errors ({len(p['errors'])}):")
            for err in p["errors"][:3]:
                # Show first line only for brevity
                first_line = err.split('\n')[0] if '\n' in err else err
                output.append(f"  - {first_line}")
            if len(p["errors"]) > 3:
                output.append(f"  ... and {len(p['errors']) - 3} more (check logs for details)")

        return "\n".join(output)
