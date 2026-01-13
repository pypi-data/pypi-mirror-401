"""MCP Semantic Search - Semantic code search using embeddings and vector storage."""

from .embedder import GeminiEmbedder
from .index_queue import IndexQueue
from .indexer import (
    chunk_file,
    compute_file_hash,
    find_code_files,
)
from .qdrant_client import CodeChunk, QdrantCodeStore
from .watcher import DebouncedFileWatcher

__version__ = "0.1.0"

__all__ = [
    "IndexQueue",
    "GeminiEmbedder",
    "QdrantCodeStore",
    "CodeChunk",
    "chunk_file",
    "compute_file_hash",
    "find_code_files",
    "DebouncedFileWatcher",
]
