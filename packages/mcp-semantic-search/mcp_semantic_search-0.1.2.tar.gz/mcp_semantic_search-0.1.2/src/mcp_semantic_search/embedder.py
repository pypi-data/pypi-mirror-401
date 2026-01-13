"""Gemini embedding client for generating text embeddings."""

import os
from typing import List

from google import genai


class GeminiEmbedder:
    """Client for generating embeddings using Google Gemini API."""

    # Available models and their dimensions
    MODELS: dict[str, int] = {
        "text-embedding-004": 768,
        "embedding-001": 768,
        "gemini-embedding-001": 768,
    }

    # Default model
    DEFAULT_MODEL = "text-embedding-004"

    def __init__(
        self,
        api_key: str | None = None,
        model_name: str | None = None,
    ):
        """Initialize the Gemini embedder.

        Args:
            api_key: Gemini API key. If None, reads from GEMINI_API_KEY env var.
            model_name: Model to use. If None, reads from GEMINI_EMBEDDING_MODEL env var
                       or uses DEFAULT_MODEL.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY must be set via environment variable or argument"
            )

        # Initialize the client with the API key
        self.client = genai.Client(api_key=self.api_key)

        self.model_name = model_name or os.getenv(
            "GEMINI_EMBEDDING_MODEL", self.DEFAULT_MODEL
        )

        # Normalize model name (remove 'models/' prefix if present)
        if self.model_name.startswith("models/"):
            self.model_name = self.model_name.replace("models/", "")

        if self.model_name not in self.MODELS:
            raise ValueError(
                f"Unknown model: {self.model_name}. "
                f"Available: {list(self.MODELS.keys())}"
            )
        self.embedding_dim = self.MODELS[self.model_name]

    def embed(self, text: str) -> List[float]:
        """Generate embedding for a single text.

        Args:
            text: The text to embed.

        Returns:
            A list of floats representing the embedding vector.
        """
        result = self.client.models.embed_content(
            model=self.model_name,
            contents=text,
        )
        # Extract embedding from response
        # result.embeddings[0] is a ContentEmbedding object with 'values' attribute
        return list(result.embeddings[0].values)

    # Gemini API batch limit
    MAX_BATCH_SIZE = 100

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts.

        Uses the batch API for better performance.
        Automatically splits into chunks if exceeding API limits.

        Args:
            texts: List of texts to embed.

        Returns:
            A list of embedding vectors.
        """
        if not texts:
            return []

        all_embeddings = []

        # Process in chunks of MAX_BATCH_SIZE
        for i in range(0, len(texts), self.MAX_BATCH_SIZE):
            batch = texts[i:i + self.MAX_BATCH_SIZE]
            result = self.client.models.embed_content(
                model=self.model_name,
                contents=batch,
            )
            # Extract embeddings from response
            batch_embeddings = [list(embedding.values) for embedding in result.embeddings]
            all_embeddings.extend(batch_embeddings)

        return all_embeddings

    def embed_query(self, query: str) -> List[float]:
        """Generate embedding for a search query.

        Note: The new API uses the same endpoint for queries and documents.

        Args:
            query: The search query to embed.

        Returns:
            A list of floats representing the embedding vector.
        """
        return self.embed(query)
