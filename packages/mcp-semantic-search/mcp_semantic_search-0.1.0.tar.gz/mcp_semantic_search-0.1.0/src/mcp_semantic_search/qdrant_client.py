"""Qdrant client wrapper for storing and searching code embeddings."""

import hashlib
import os
from collections import Counter
from dataclasses import dataclass
from typing import Any, List

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)
from qdrant_client.http.models import (
    Filter,
    FieldCondition,
    MatchValue,
)


@dataclass
class CodeChunk:
    """A chunk of code with metadata."""

    id: str
    content: str
    file_path: str
    start_line: int
    end_line: int
    language: str


def get_collection_name() -> str:
    """Generate a stable collection name from WORKSPACE_DIR."""
    workspace = os.getenv("WORKSPACE_DIR", os.getcwd())
    hash_suffix = hashlib.sha256(workspace.encode()).hexdigest()[:16]
    return f"code-{hash_suffix}"


class QdrantCodeStore:
    """Qdrant client for storing and searching code embeddings."""

    VECTOR_SIZE = 768  # Gemini embedding dimension

    def __init__(
        self,
        url: str | None = None,
        collection_name: str | None = None,
    ):
        """Initialize the Qdrant client.

        Args:
            url: Qdrant server URL. Defaults to QDRANT_URL env var or http://localhost:6333.
            collection_name: Collection name. Defaults to hash of WORKSPACE_DIR.
        """
        self.url = url or os.getenv("QDRANT_URL", "http://localhost:6333")
        self.collection_name = collection_name or get_collection_name()
        self.client = QdrantClient(url=self.url)

    def ensure_collection(self) -> None:
        """Ensure the collection exists, creating it if necessary."""
        collections = self.client.get_collections().collections
        collection_names = {c.name for c in collections}

        if self.collection_name not in collection_names:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.VECTOR_SIZE,
                    distance=Distance.COSINE,
                ),
            )
            print(f"Created collection: {self.collection_name}")

    def delete_collection(self) -> None:
        """Delete the collection."""
        self.client.delete_collection(self.collection_name)
        print(f"Deleted collection: {self.collection_name}")

    def collection_exists(self) -> bool:
        """Check if the collection exists."""
        collections = self.client.get_collections().collections
        collection_names = {c.name for c in collections}
        return self.collection_name in collection_names

    def get_collection_info(self) -> dict[str, Any]:
        """Get information about the collection."""
        if not self.collection_exists():
            return {"exists": False}

        info = self.client.get_collection(self.collection_name)
        result = {
            "exists": True,
            "name": self.collection_name,
            "points_count": getattr(info, "points_count", 0),
        }
        return result

    def add_chunks(
        self, chunks: List[CodeChunk], embeddings: List[List[float]], file_hash: str | None = None
    ) -> None:
        """Add code chunks with their embeddings to the collection.

        Args:
            chunks: List of code chunks to add.
            embeddings: List of embedding vectors, one per chunk.
            file_hash: Optional hash of the source file for change tracking.
        """
        if len(chunks) != len(embeddings):
            raise ValueError("Number of chunks must match number of embeddings")

        points = [
            PointStruct(
                id=chunk.id,
                vector=embedding,
                payload={
                    "content": chunk.content,
                    "file_path": chunk.file_path,
                    "start_line": chunk.start_line,
                    "end_line": chunk.end_line,
                    "language": chunk.language,
                    "file_hash": file_hash,
                },
            )
            for chunk, embedding in zip(chunks, embeddings)
        ]

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )
        print(f"Added {len(points)} chunks to collection")

    def search(
        self,
        query_embedding: List[float],
        limit: int = 10,
        score_threshold: float = 0.5,
        file_filter: str | None = None,
    ) -> List[dict[str, Any]]:
        """Search for similar code chunks.

        Args:
            query_embedding: The query embedding vector.
            limit: Maximum number of results to return.
            score_threshold: Minimum similarity score (0-1).
            file_filter: Optional file path pattern to filter results.

        Returns:
            List of search results with metadata.
        """
        search_filter = None
        if file_filter:
            search_filter = Filter(
                must=[FieldCondition(key="file_path", match=MatchValue(value=file_filter))]
            )

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,  # Can be a list[float] directly
            query_filter=search_filter,
            limit=limit,
            score_threshold=score_threshold,
        )

        return [
            {
                "score": point.score,
                "content": point.payload.get("content", ""),
                "file_path": point.payload.get("file_path", ""),
                "start_line": point.payload.get("start_line", 0),
                "end_line": point.payload.get("end_line", 0),
                "language": point.payload.get("language", ""),
            }
            for point in results.points
        ]

    def count_chunks_by_file(self) -> dict[str, int]:
        """Get count of chunks per file."""
        # Get all points with their payloads
        # Note: This is a simplified version - for large collections
        # you'd want to use scroll API with pagination

        results, _ = self.client.scroll(
            collection_name=self.collection_name,
            limit=10000,
            with_payload=["file_path"],
        )

        file_counts = Counter(point.payload.get("file_path", "unknown") for point in results)
        return dict(file_counts)

    def get_file_metadata(self) -> dict[str, str]:
        """Get metadata for all indexed files.

        Returns:
            Dict mapping file_path to file_hash.
        """
        file_metadata: dict[str, str] = {}

        # Use scroll to get all points with file_hash
        offset = None
        limit = 1000

        while True:
            results, offset = self.client.scroll(
                collection_name=self.collection_name,
                limit=limit,
                offset=offset,
                with_payload=["file_path", "file_hash"],
            )

            for point in results:
                file_path = point.payload.get("file_path")
                file_hash = point.payload.get("file_hash")
                if file_path and file_hash:
                    # Only store once per file (first chunk we encounter)
                    if file_path not in file_metadata:
                        file_metadata[file_path] = file_hash

            if offset is None:
                break

        return file_metadata

    def delete_chunks_for_file(self, file_path: str) -> int:
        """Delete all chunks for a specific file.

        Args:
            file_path: Relative path to the file.

        Returns:
            Number of chunks deleted.
        """
        # First, find all points for this file
        filter = Filter(must=[FieldCondition(key="file_path", match=MatchValue(value=file_path))])

        # Get the points to find their IDs
        results, _ = self.client.scroll(
            collection_name=self.collection_name,
            limit=10000,
            scroll_filter=filter,
            with_payload=False,
        )

        if not results:
            return 0

        # Delete by IDs
        point_ids = [point.id for point in results]
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=point_ids,
        )

        return len(point_ids)
