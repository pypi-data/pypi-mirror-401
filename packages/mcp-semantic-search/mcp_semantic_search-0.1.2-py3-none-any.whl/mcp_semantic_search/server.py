"""MCP server for semantic code search."""

import argparse
import os
import threading
import traceback
from pathlib import Path

from fastmcp import FastMCP

from .embedder import GeminiEmbedder
from .index_queue import IndexQueue
from .indexer import find_code_files
from .qdrant_client import QdrantCodeStore
from .watcher import DebouncedFileWatcher

# Create the FastMCP server
mcp = FastMCP("semantic-search")

# Initialize clients (lazy initialization)
_embedder: GeminiEmbedder | None = None
_store: QdrantCodeStore | None = None

# Index queue (lazy initialization)
_index_queue: IndexQueue | None = None

# Live watcher (lazy initialization)
_watcher: DebouncedFileWatcher | None = None

# Root directory - set at startup via args or env
_ROOT_DIR: str | None = None


def get_root_dir() -> str:
    """Get the repository root directory.

    Uses the following priority:
    1. Value set via --root-dir argument at startup
    2. MCP_ROOT_DIR environment variable
    3. Current working directory

    Returns:
        The root directory path.
    """
    global _ROOT_DIR
    if _ROOT_DIR is not None:
        return _ROOT_DIR

    # Check environment variable
    env_root = os.getenv("MCP_ROOT_DIR")
    if env_root and os.path.isdir(env_root):
        _ROOT_DIR = env_root
        return _ROOT_DIR

    # Default to current working directory
    _ROOT_DIR = os.getcwd()
    return _ROOT_DIR


def get_embedder() -> GeminiEmbedder:
    """Get or create the embedder instance."""
    global _embedder
    if _embedder is None:
        _embedder = GeminiEmbedder()
    return _embedder


def get_store() -> QdrantCodeStore:
    """Get or create the store instance."""
    global _store
    if _store is None:
        _store = QdrantCodeStore()
    return _store


def get_index_queue() -> IndexQueue:
    """Get or create the index queue instance."""
    global _index_queue
    if _index_queue is None:
        embedder = get_embedder()
        store = get_store()
        _index_queue = IndexQueue(embedder, store, debounce_seconds=3.0)
    return _index_queue


@mcp.tool()
def index_codebase(
    root_dir: str | None = None,
    max_files: int | None = None,
    force_reindex: bool = False,
) -> dict:
    """Index the codebase for semantic search.

    This operation adds files to the indexing queue immediately (no debounce).
    Use get_status() to track progress.

    Args:
        root_dir: Root directory of the codebase. Defaults to MCP config or current directory.
        max_files: Maximum number of files to index (for testing). None for all.
        force_reindex: If True, clear existing index and reindex all files.

    Returns:
        Dict with status indicating indexing has started.
    """
    if root_dir is None:
        root_dir = get_root_dir()

    store = get_store()
    queue = get_index_queue()

    # Clear existing index if requested
    if force_reindex and store.collection_exists():
        store.delete_collection()
        print("[index_codebase] Cleared existing index")

    # Ensure collection exists
    store.ensure_collection()

    # Start queue if not running
    if not queue.is_running():
        queue.start()

    # Find all code files and add to queue (immediately, no debounce)
    files = find_code_files(root_dir, max_files)
    queue.add_files(files, root_dir=root_dir, skip_debounce=True)

    return {
        "status": "success",
        "files_queued": len(files),
        "message": "Use get_status() to track progress."
    }


@mcp.tool()
def search_code(
    query: str,
    limit: int = 10,
    score_threshold: float = 0.5,
) -> dict:
    """Search the codebase using natural language.

    Args:
        query: Natural language search query (e.g., "how does authentication work").
        limit: Maximum number of results to return.
        score_threshold: Minimum similarity score (0-1). Lower = more results.

    Returns:
        Dict with search results.
    """
    embedder = get_embedder()
    store = get_store()

    if not store.collection_exists():
        return {"error": "No index found. Please run index_codebase() first."}

    query_embedding = embedder.embed_query(query)
    results = store.search(
        query_embedding=query_embedding,
        limit=limit,
        score_threshold=score_threshold,
    )

    if not results:
        return {"query": query, "results": []}

    formatted_results = []
    for result in results:
        formatted_results.append({
            "file": result["file_path"],
            "lines": f"{result['start_line']}-{result['end_line']}",
            "score": round(result["score"], 3),
            "content": result["content"]
        })

    return {
        "query": query,
        "count": len(formatted_results),
        "results": formatted_results
    }


@mcp.tool()
def get_status() -> dict:
    """Get the current index status and queue progress.

    Returns:
        Dict with collection info, statistics, and real-time queue status.
    """
    store = get_store()

    if not store.collection_exists():
        return {"error": "No index found. Collection does not exist."}

    info = store.get_collection_info()
    file_counts = store.count_chunks_by_file()

    # Top files by chunk count
    sorted_files = sorted(file_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    top_files = [{"file": fp, "chunks": count} for fp, count in sorted_files]

    status_data = {
        "collection": {
            "name": info["name"],
            "total_chunks": info["points_count"],
            "files_indexed": len(file_counts)
        },
        "queue": {
            "running": False
        },
        "top_files_by_chunk_count": top_files
    }

    # Add queue status if running
    queue = get_index_queue()
    if queue.is_running():
        progress = queue.get_progress()
        queue_data = {
            "running": progress["running"],
            "files_processed": progress["files_processed"],
            "queued": progress["queued"],
            "pending": progress["pending"],
            "chunks_embedded": progress["chunks_embedded"]
        }

        if progress["current_file"]:
            rel_path = progress["current_file"]
            if progress["root_dir"] and rel_path.startswith(progress["root_dir"]):
                rel_path = rel_path[len(progress["root_dir"]):].lstrip("/")
            queue_data["current_file"] = rel_path

        if progress["errors"]:
            queue_data["errors"] = len(progress["errors"])

        status_data["queue"] = queue_data

    return status_data


@mcp.tool()
def clear_index() -> dict:
    """Clear the entire index.

    Use this to start fresh or recover from errors.

    Returns:
        Dict with confirmation status.
    """
    store = get_store()

    if store.collection_exists():
        store.delete_collection()
        return {"status": "success", "message": "Index cleared successfully."}

    return {"status": "success", "message": "No index to clear."}


@mcp.tool()
def search_file(
    query: str,
    file_path: str,
    limit: int = 5,
) -> dict:
    """Search within a specific file.

    Args:
        query: Natural language search query.
        file_path: Path to the file to search within.
        limit: Maximum number of results.

    Returns:
        Dict with search results from the specified file.
    """
    embedder = get_embedder()
    store = get_store()

    if not store.collection_exists():
        return {"error": "No index found. Please run index_codebase() first."}

    query_embedding = embedder.embed_query(query)
    results = store.search(
        query_embedding=query_embedding,
        limit=limit,
        file_filter=file_path,
    )

    if not results:
        return {"query": query, "file": file_path, "results": []}

    formatted_results = []
    for result in results:
        formatted_results.append({
            "lines": f"{result['start_line']}-{result['end_line']}",
            "score": round(result["score"], 3),
            "content": result["content"]
        })

    return {
        "query": query,
        "file": file_path,
        "count": len(formatted_results),
        "results": formatted_results
    }


@mcp.resource("qdrant://status")
def get_status_resource() -> str:
    """Resource for getting index status."""
    return get_status()


# ===== Live Watch Tools =====


def _on_files_changed(changed_files: list[str]):
    """Callback for file changes - adds to queue with debounce."""
    queue = get_index_queue()
    root_dir = get_root_dir()

    # Ensure queue is running
    if not queue.is_running():
        queue.start()

    # Add files with debounce (handled by queue)
    queue.add_files(changed_files, root_dir=root_dir, skip_debounce=False)


@mcp.tool()
def start_live_watch(root_dir: str | None = None, debounce_seconds: float = 3.0) -> dict:
    """Start live file watching for automatic reindexing.

    When enabled, the server will automatically detect file changes and
    add them to the indexing queue with debouncing.

    Args:
        root_dir: Root directory to watch. Defaults to MCP config or current directory.
        debounce_seconds: Seconds to wait after last change before adding to queue.

    Returns:
        Dict with status.
    """
    global _watcher

    if root_dir is None:
        root_dir = get_root_dir()

    # Stop existing watcher if running
    if _watcher is not None and _watcher.is_running():
        _watcher.stop()

    # Ensure queue exists and is running
    queue = get_index_queue()
    if not queue.is_running():
        queue.start()

    # Ensure collection exists before watching
    store = get_store()
    store.ensure_collection()

    # Update queue debounce if changed
    if queue.debounce_seconds != debounce_seconds:
        queue.debounce_seconds = debounce_seconds

    # Create the watcher
    _watcher = DebouncedFileWatcher(
        root_dir=root_dir,
        on_change=_on_files_changed,
        debounce_seconds=debounce_seconds,
    )

    _watcher.start()

    return {
        "status": "success",
        "running": True,
        "watching": root_dir,
        "debounce_seconds": debounce_seconds
    }


@mcp.tool()
def stop_live_watch() -> dict:
    """Stop the live file watcher.

    Returns:
        Dict with status.
    """
    global _watcher

    if _watcher is None or not _watcher.is_running():
        return {"status": "stopped", "message": "Live watch is not running."}

    _watcher.stop()
    return {"status": "stopped", "running": False}


@mcp.tool()
def get_live_watch_status() -> dict:
    """Get the status of the live file watcher.

    Returns:
        Dict with current state.
    """
    global _watcher

    if _watcher is None:
        return {
            "status": "not_initialized",
            "running": False,
            "message": "Use start_live_watch() to enable automatic reindexing."
        }

    if _watcher.is_running():
        queue = get_index_queue()
        progress = queue.get_progress()
        return {
            "status": "running",
            "running": True,
            "watching": _watcher.root_dir,
            "debounce_seconds": _watcher.debounce_seconds,
            "queue": {
                "queued": progress["queued"],
                "pending": progress["pending"]
            }
        }
    else:
        return {"status": "stopped", "running": False}


def _auto_start():
    """Auto-start indexing and live watch on startup."""

    def startup_task():
        """Run startup tasks in background."""
        try:
            root_dir = get_root_dir()
            store = get_store()
            queue = get_index_queue()

            # Ensure collection exists
            store.ensure_collection()

            # Start the queue worker
            if not queue.is_running():
                queue.start()

            # Check if we need initial indexing
            info = store.get_collection_info()
            if info.get('points_count', 0) == 0:
                # Empty collection - run initial indexing
                files = find_code_files(root_dir)
                queue.add_files(files, root_dir=root_dir, skip_debounce=True)
                print(f"[Startup] Initial indexing: {len(files)} files queued")

            # Start live watch
            global _watcher
            _watcher = DebouncedFileWatcher(
                root_dir=root_dir,
                on_change=_on_files_changed,
                debounce_seconds=3.0,
            )
            _watcher.start()
            print("[Startup] Live watch started")

        except Exception as e:
            print(f"[Startup] Error: {e}\n{traceback.format_exc()}")

    # Run startup in background thread to not block MCP startup
    thread = threading.Thread(target=startup_task, daemon=True)
    thread.start()


def main():
    """Main entry point for the MCP server."""
    # Parse command-line arguments before starting MCP
    parser = argparse.ArgumentParser(description="Semantic Search MCP Server")
    parser.add_argument(
        "--root-dir",
        type=str,
        help="Root directory of the codebase to index. "
             "Defaults to MCP_ROOT_DIR env var or current working directory.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )
    parser.add_argument(
        "--no-auto-start",
        action="store_true",
        help="Disable automatic indexing and live watch on startup.",
    )

    # Parse only known args (let FastMCP handle the rest)
    args, unknown = parser.parse_known_args()

    # Set root directory from argument if provided
    if args.root_dir:
        global _ROOT_DIR
        _ROOT_DIR = os.path.abspath(args.root_dir)

    # Auto-start indexing and live watch unless disabled
    if not args.no_auto_start:
        _auto_start()

    # Start the MCP server
    mcp.run()


if __name__ == "__main__":
    main()
