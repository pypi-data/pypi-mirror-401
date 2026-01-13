"""Code indexing utilities for chunking and processing code files."""

import hashlib
import os
from dataclasses import dataclass
from pathlib import Path
from typing import List

from pathspec import PathSpec
from pathspec.patterns.gitwildmatch import GitWildMatchPattern

from .qdrant_client import CodeChunk


# Cached PathSpec instances per repo
_gitignore_cache: dict[str, PathSpec] = {}


def load_gitignore(repo_root: str) -> PathSpec:
    """Load .gitignore patterns from a repository.

    Args:
        repo_root: Root directory of the repository.

    Returns:
        PathSpec object for matching gitignore patterns.
    """
    global _gitignore_cache

    if repo_root in _gitignore_cache:
        return _gitignore_cache[repo_root]

    gitignore_path = os.path.join(repo_root, ".gitignore")

    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as f:
            patterns = f.read().splitlines()
        # Filter out comments and empty lines
        patterns = [p for p in patterns if p.strip() and not p.strip().startswith("#")]
    else:
        patterns = []

    spec = PathSpec.from_lines(GitWildMatchPattern, patterns)
    _gitignore_cache[repo_root] = spec
    return spec


def compute_file_hash(file_path: str) -> str:
    """Compute SHA256 hash of a file's content.

    Args:
        file_path: Path to the file.

    Returns:
        Hexadecimal hash string.
    """
    with open(file_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


# Language mappings for file extensions
LANGUAGE_MAP: dict[str, str] = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".jsx": "jsx",
    ".tsx": "tsx",
    ".md": "markdown",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".json": "json",
    ".html": "html",
    ".css": "css",
    ".sh": "bash",
    ".sql": "sql",
    ".txt": "text",
}


def get_language(file_path: str) -> str:
    """Get programming language from file extension."""
    ext = Path(file_path).suffix.lower()
    return LANGUAGE_MAP.get(ext, "unknown")


def is_text_file(file_path: str) -> bool:
    """Check if a file is a text file we should index."""
    ext = Path(file_path).suffix.lower()
    return ext in LANGUAGE_MAP or ext in [".toml", ".ini", ".cfg", ".conf"]


def is_gitignored(repo_root: str, file_path: str) -> bool:
    """Check if a file is gitignored using pathspec."""
    spec = load_gitignore(repo_root)
    rel_path = os.path.relpath(file_path, repo_root)
    # Normalize to forward slashes for gitignore matching
    rel_path_normalized = rel_path.replace(os.sep, "/")
    return spec.match_file(rel_path_normalized)


def generate_id(file_path: str, start_line: int, end_line: int) -> str:
    """Generate a unique ID for a code chunk."""
    content = f"{file_path}:{start_line}-{end_line}"
    return hashlib.md5(content.encode()).hexdigest()


@dataclass
class ChunkConfig:
    """Configuration for chunking.

    Defaults can be overridden via environment variables:
    - CHUNK_MAX_LINES: Maximum lines per chunk (default: 50)
    - CHUNK_OVERLAP_LINES: Overlap between chunks (default: 10)
    - CHUNK_MIN_LINES: Minimum lines for valid chunk (default: 5)
    """

    max_lines: int = int(os.getenv("CHUNK_MAX_LINES", "50"))
    overlap_lines: int = int(os.getenv("CHUNK_OVERLAP_LINES", "10"))
    min_lines: int = int(os.getenv("CHUNK_MIN_LINES", "5"))


def chunk_python_code(content: str, file_path: str) -> List[tuple[str, int, int]]:
    """Chunk Python code at function/class boundaries.

    For now, use a simpler line-based approach with context.
    TODO: Add tree-sitter for proper AST-based chunking.
    """
    lines = content.splitlines(keepends=True)
    chunks = []
    i = 0

    # Find function/class definitions for better chunk boundaries
    def_indent_starts = []
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith(("def ", "class ", "async def ")):
            def_indent_starts.append(idx)

    # Group functions/classes together
    if def_indent_starts:
        # Chunk around function/class definitions
        group_start = 0
        for j, def_line in enumerate(def_indent_starts):
            next_def = def_indent_starts[j + 1] if j + 1 < len(def_indent_starts) else len(lines)

            # Include some context before the function
            context_start = max(group_start, def_line - 5)
            chunk_content = "".join(lines[context_start:next_def])
            chunks.append((chunk_content, context_start + 1, next_def))

            group_start = next_def
    else:
        # No functions/classes, use line-based chunking
        chunks = chunk_line_based(content, file_path)

    return chunks


def chunk_line_based(
    content: str,
    file_path: str,
    config: ChunkConfig | None = None,
) -> List[tuple[str, int, int]]:
    """Chunk content by lines with overlap.

    Args:
        content: The file content to chunk.
        file_path: Path to the file (for language detection).
        config: Chunking configuration.

    Returns:
        List of (chunk_content, start_line, end_line) tuples.
    """
    if config is None:
        config = ChunkConfig()

    lines = content.splitlines(keepends=True)
    chunks = []
    i = 0

    while i < len(lines):
        # Determine chunk size
        end = min(i + config.max_lines, len(lines))

        # Skip tiny chunks at the end unless it's all we have
        if end - i < config.min_lines and i > 0:
            break

        chunk_content = "".join(lines[i:end])
        chunks.append((chunk_content, i + 1, end))

        # Move forward with overlap
        # Ensure we always make progress
        new_i = end - config.overlap_lines
        if new_i <= i:  # Prevent infinite loop
            new_i = end
        i = new_i

    return chunks


def chunk_file(
    file_path: str,
    repo_root: str,
    config: ChunkConfig | None = None,
) -> List[CodeChunk]:
    """Chunk a single file into searchable pieces.

    Args:
        file_path: Path to the file.
        repo_root: Root of the repository (for relative paths).
        config: Chunking configuration.

    Returns:
        List of CodeChunk objects.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except (UnicodeDecodeError, PermissionError):
        return []

    if not content.strip():
        return []

    language = get_language(file_path)
    rel_path = os.path.relpath(file_path, repo_root)

    # Choose chunking strategy based on language
    if language == "python":
        raw_chunks = chunk_python_code(content, file_path)
    else:
        raw_chunks = chunk_line_based(content, file_path, config)

    chunks = []
    for chunk_content, start_line, end_line in raw_chunks:
        chunk_id = generate_id(rel_path, start_line, end_line)
        chunks.append(
            CodeChunk(
                id=chunk_id,
                content=chunk_content.strip(),
                file_path=rel_path,
                start_line=start_line,
                end_line=end_line,
                language=language,
            )
        )

    return chunks


def find_code_files(
    root_dir: str,
    max_files: int | None = None,
) -> List[str]:
    """Find all code files in the repository.

    Args:
        root_dir: Root directory to search.
        max_files: Optional maximum number of files to return.

    Returns:
        List of file paths.
    """
    files = []
    for root, dirs, filenames in os.walk(root_dir):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith(".")]

        for filename in filenames:
            file_path = os.path.join(root, filename)

            if is_gitignored(root_dir, file_path):
                continue

            if is_text_file(file_path):
                files.append(file_path)
                if max_files and len(files) >= max_files:
                    return files

    return files


def index_repository(
    root_dir: str,
    embedder,
    store,
    max_files: int | None = None,
) -> dict[str, int]:
    """Index an entire codebase.

    Args:
        root_dir: Root directory of the codebase.
        embedder: GeminiEmbedder instance.
        store: QdrantCodeStore instance.
        max_files: Optional maximum number of files to index.

    Returns:
        Dictionary with indexing statistics.
    """
    files = find_code_files(root_dir, max_files)

    stats = {
        "files_found": len(files),
        "files_processed": 0,
        "chunks_created": 0,
        "chunks_embedded": 0,
        "errors": [],
    }

    # Ensure collection exists
    store.ensure_collection()

    batch_size = 10
    batch_chunks = []

    for file_path in files:
        try:
            chunks = chunk_file(file_path, root_dir)
            if not chunks:
                continue

            stats["files_processed"] += 1
            batch_chunks.extend(chunks)

            # Process batch when full
            if len(batch_chunks) >= batch_size:
                texts = [chunk.content for chunk in batch_chunks]
                embeddings = embedder.embed_batch(texts)
                # Note: Full index doesn't use file_hash tracking
                store.add_chunks(batch_chunks, embeddings)
                stats["chunks_embedded"] += len(batch_chunks)
                batch_chunks = []

            stats["chunks_created"] += len(chunks)

        except Exception as e:
            stats["errors"].append(f"{file_path}: {e}")

    # Process remaining chunks
    if batch_chunks:
        texts = [chunk.content for chunk in batch_chunks]
        embeddings = embedder.embed_batch(texts)
        store.add_chunks(batch_chunks, embeddings)
        stats["chunks_embedded"] += len(batch_chunks)

    return stats


def reindex_repository(
    root_dir: str,
    embedder,
    store,
) -> dict[str, int]:
    """Incrementally reindex only changed files.

    Compares file hashes with stored hashes and only processes:
    - New files (not in index)
    - Modified files (hash changed)
    - Deleted files (removes their chunks)

    Args:
        root_dir: Root directory of the codebase.
        embedder: GeminiEmbedder instance.
        store: QdrantCodeStore instance.

    Returns:
        Dictionary with reindexing statistics.
    """
    # Get current file metadata from Qdrant
    existing_files = store.get_file_metadata()

    # Find all code files
    current_files = find_code_files(root_dir)

    stats = {
        "files_scanned": len(current_files),
        "files_added": 0,
        "files_modified": 0,
        "files_deleted": 0,
        "files_unchanged": 0,
        "chunks_added": 0,
        "errors": [],
    }

    # Track files that still exist (to detect deletions)
    processed_rel_paths: set[str] = set()

    batch_size = 10
    batch_chunks: list = []
    current_batch_hash: str | None = None

    for file_path in current_files:
        try:
            rel_path = os.path.relpath(file_path, root_dir)
            processed_rel_paths.add(rel_path)

            # Compute current file hash
            current_hash = compute_file_hash(file_path)
            stored_hash = existing_files.get(rel_path)

            # Check if file needs reindexing
            if stored_hash is None:
                # New file
                stats["files_added"] += 1
                needs_index = True
            elif stored_hash != current_hash:
                # Modified file - delete old chunks first
                stats["files_modified"] += 1
                deleted = store.delete_chunks_for_file(rel_path)
                needs_index = True
            else:
                # Unchanged - skip
                stats["files_unchanged"] += 1
                needs_index = False

            if not needs_index:
                continue

            # Chunk the file
            chunks = chunk_file(file_path, root_dir)
            if not chunks:
                continue

            batch_chunks.extend(chunks)

            # Process batch when full or hash changes
            if len(batch_chunks) >= batch_size or (
                current_batch_hash is not None and current_batch_hash != current_hash
            ):
                texts = [chunk.content for chunk in batch_chunks]
                embeddings = embedder.embed_batch(texts)
                # Use the current hash (last file in batch)
                store.add_chunks(batch_chunks, embeddings, file_hash=current_hash)
                stats["chunks_added"] += len(batch_chunks)
                batch_chunks = []

            current_batch_hash = current_hash

        except Exception as e:
            stats["errors"].append(f"{file_path}: {e}")

    # Process remaining chunks
    if batch_chunks:
        texts = [chunk.content for chunk in batch_chunks]
        embeddings = embedder.embed_batch(texts)
        store.add_chunks(batch_chunks, embeddings, file_hash=current_batch_hash)
        stats["chunks_added"] += len(batch_chunks)

    # Detect deleted files (in index but not on disk)
    for rel_path in existing_files:
        if rel_path not in processed_rel_paths:
            stats["files_deleted"] += 1
            store.delete_chunks_for_file(rel_path)

    return stats
