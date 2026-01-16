"""
Embedding Provider Abstraction for Semantic Memory Retrieval

Provides a unified interface for different embedding providers (OpenAI, local models)
with vector similarity search capabilities for episodic and procedural memory.
"""

import logging
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

import numpy as np

try:
    from openai import OpenAI

    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer

    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False

try:
    from sklearn.metrics.pairwise import cosine_similarity

    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


@dataclass
class EmbeddingResult:
    """Result of embedding generation."""

    text: str
    embedding: list[float]
    model: str
    dimensions: int


@dataclass
class SimilarityResult:
    """Result of similarity search."""

    text: str
    similarity: float
    metadata: dict[str, Any] | None = None


class EmbeddingProvider(ABC):
    """Abstract base class for embedding providers."""

    @abstractmethod
    def embed_text(self, text: str) -> EmbeddingResult:
        """Generate embedding for a single text."""
        pass

    @abstractmethod
    def embed_batch(self, texts: list[str]) -> list[EmbeddingResult]:
        """Generate embeddings for multiple texts."""
        pass

    @abstractmethod
    def get_dimensions(self) -> int:
        """Get the dimension count for this provider's embeddings."""
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        """Get the model name used by this provider."""
        pass


class OpenAIEmbeddingProvider(EmbeddingProvider):
    """OpenAI embedding provider using text-embedding-3-small model."""

    def __init__(self, model: str = "text-embedding-3-small"):
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI package not available. Install with: pip install openai")

        self.model = model
        self.client = OpenAI()
        self.logger = logging.getLogger(__name__)

        # Cache for model dimensions
        self._dimensions = None

    def embed_text(self, text: str) -> EmbeddingResult:
        """Generate embedding for a single text."""
        try:
            response = self.client.embeddings.create(input=text, model=self.model)

            embedding = response.data[0].embedding

            return EmbeddingResult(text=text, embedding=embedding, model=self.model, dimensions=len(embedding))

        except Exception as e:
            self.logger.error(f"Error generating OpenAI embedding: {e}")
            raise

    def embed_batch(self, texts: list[str]) -> list[EmbeddingResult]:
        """Generate embeddings for multiple texts."""
        try:
            response = self.client.embeddings.create(input=texts, model=self.model)

            results = []
            for i, data in enumerate(response.data):
                results.append(
                    EmbeddingResult(
                        text=texts[i], embedding=data.embedding, model=self.model, dimensions=len(data.embedding)
                    )
                )

            return results

        except Exception as e:
            self.logger.error(f"Error generating OpenAI batch embeddings: {e}")
            raise

    def get_dimensions(self) -> int:
        """Get the dimension count for this provider's embeddings."""
        if self._dimensions is None:
            # Generate a test embedding to get dimensions
            result = self.embed_text("test")
            self._dimensions = result.dimensions
        return self._dimensions

    def get_model_name(self) -> str:
        """Get the model name used by this provider."""
        return self.model


class LocalEmbeddingProvider(EmbeddingProvider):
    """Local embedding provider using sentence-transformers."""

    def __init__(self, model: str = "all-MiniLM-L6-v2"):
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            raise ImportError(
                "sentence-transformers package not available. Install with: pip install sentence-transformers"
            )

        self.model_name = model
        self.model = SentenceTransformer(model)
        self.logger = logging.getLogger(__name__)

    def embed_text(self, text: str) -> EmbeddingResult:
        """Generate embedding for a single text."""
        try:
            embedding = self.model.encode(text).tolist()

            return EmbeddingResult(text=text, embedding=embedding, model=self.model_name, dimensions=len(embedding))

        except Exception as e:
            self.logger.error(f"Error generating local embedding: {e}")
            raise

    def embed_batch(self, texts: list[str]) -> list[EmbeddingResult]:
        """Generate embeddings for multiple texts."""
        try:
            embeddings = self.model.encode(texts)

            results = []
            for i, embedding in enumerate(embeddings):
                results.append(
                    EmbeddingResult(
                        text=texts[i], embedding=embedding.tolist(), model=self.model_name, dimensions=len(embedding)
                    )
                )

            return results

        except Exception as e:
            self.logger.error(f"Error generating local batch embeddings: {e}")
            raise

    def get_dimensions(self) -> int:
        """Get the dimension count for this provider's embeddings."""
        return self.model.get_sentence_embedding_dimension()

    def get_model_name(self) -> str:
        """Get the model name used by this provider."""
        return self.model_name


class InMemoryVectorIndex:
    """In-memory vector index for similarity search."""

    def __init__(self, provider: EmbeddingProvider):
        self.provider = provider
        self.embeddings: list[list[float]] = []
        self.texts: list[str] = []
        self.metadata: list[dict[str, Any]] = []
        self.logger = logging.getLogger(__name__)

        if not SKLEARN_AVAILABLE:
            self.logger.warning(
                "scikit-learn not available. Install with: pip install scikit-learn for optimal performance"
            )

    def add_text(self, text: str, metadata: dict[str, Any] | None = None):
        """Add a text and its embedding to the index."""
        try:
            result = self.provider.embed_text(text)
            self.embeddings.append(result.embedding)
            self.texts.append(text)
            self.metadata.append(metadata or {})

            self.logger.debug(f"Added text to vector index: {text[:100]}...")

        except Exception as e:
            self.logger.error(f"Error adding text to vector index: {e}")
            raise

    def add_batch(self, texts: list[str], metadata_list: list[dict[str, Any]] | None = None):
        """Add multiple texts and their embeddings to the index."""
        try:
            results = self.provider.embed_batch(texts)

            for i, result in enumerate(results):
                self.embeddings.append(result.embedding)
                self.texts.append(result.text)

                if metadata_list and i < len(metadata_list):
                    self.metadata.append(metadata_list[i])
                else:
                    self.metadata.append({})

            self.logger.debug(f"Added {len(texts)} texts to vector index")

        except Exception as e:
            self.logger.error(f"Error adding batch to vector index: {e}")
            raise

    def search(self, query: str, top_k: int = 5) -> list[SimilarityResult]:
        """Search for similar texts using cosine similarity."""
        if not self.embeddings:
            return []

        try:
            # Generate embedding for query
            query_result = self.provider.embed_text(query)
            query_embedding = np.array(query_result.embedding).reshape(1, -1)

            # Calculate similarities
            if SKLEARN_AVAILABLE:
                # Use scikit-learn for optimal performance
                embeddings_matrix = np.array(self.embeddings)
                similarities = cosine_similarity(query_embedding, embeddings_matrix)[0]
            else:
                # Fallback to manual cosine similarity
                similarities = []
                for embedding in self.embeddings:
                    similarity = self._cosine_similarity(query_result.embedding, embedding)
                    similarities.append(similarity)
                similarities = np.array(similarities)

            # Get top-k results
            top_indices = np.argsort(similarities)[::-1][:top_k]

            results = []
            for idx in top_indices:
                results.append(
                    SimilarityResult(
                        text=self.texts[idx], similarity=float(similarities[idx]), metadata=self.metadata[idx]
                    )
                )

            return results

        except Exception as e:
            self.logger.error(f"Error searching vector index: {e}")
            return []

    def _cosine_similarity(self, vec1: list[float], vec2: list[float]) -> float:
        """Calculate cosine similarity between two vectors (fallback implementation)."""
        try:
            # Convert to numpy arrays
            a = np.array(vec1)
            b = np.array(vec2)

            # Calculate cosine similarity
            dot_product = np.dot(a, b)
            norm_a = np.linalg.norm(a)
            norm_b = np.linalg.norm(b)

            if norm_a == 0 or norm_b == 0:
                return 0.0

            return dot_product / (norm_a * norm_b)

        except Exception:
            return 0.0

    def clear(self):
        """Clear all entries from the index."""
        self.embeddings.clear()
        self.texts.clear()
        self.metadata.clear()
        self.logger.debug("Cleared vector index")

    def size(self) -> int:
        """Get the number of entries in the index."""
        return len(self.embeddings)


def create_embedding_provider(provider_type: str = "auto", model: str | None = None) -> EmbeddingProvider:
    """
    Factory function to create embedding providers.

    Args:
        provider_type: "openai", "local", or "auto" (default)
        model: Optional model name to use

    Returns:
        Configured embedding provider
    """
    logger = logging.getLogger(__name__)

    env_provider = os.getenv("CCE_EMBEDDING_PROVIDER") or os.getenv("EMBEDDING_PROVIDER")
    if env_provider:
        provider_type = env_provider.strip().lower()
        logger.info("Embedding provider override set to: %s", provider_type)

    env_model = os.getenv("CCE_EMBEDDING_MODEL") or os.getenv("EMBEDDING_MODEL")
    if model is None and env_model:
        model = env_model.strip()

    if provider_type == "auto":
        # Auto-select based on available packages and API keys
        if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
            provider_type = "openai"
        elif SENTENCE_TRANSFORMERS_AVAILABLE:
            provider_type = "local"
        else:
            raise ImportError("No embedding provider available. Install openai or sentence-transformers")

    if provider_type == "openai":
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI package not available. Install with: pip install openai")

        model = model or "text-embedding-3-small"
        logger.info(f"Using OpenAI embedding provider with model: {model}")
        return OpenAIEmbeddingProvider(model=model)

    elif provider_type == "local":
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            raise ImportError(
                "sentence-transformers package not available. Install with: pip install sentence-transformers"
            )

        model = model or "all-MiniLM-L6-v2"
        logger.info(f"Using local embedding provider with model: {model}")
        return LocalEmbeddingProvider(model=model)

    else:
        raise ValueError(f"Unknown provider type: {provider_type}")
