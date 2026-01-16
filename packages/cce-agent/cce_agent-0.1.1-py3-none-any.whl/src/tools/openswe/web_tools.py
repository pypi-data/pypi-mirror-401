"""
Web Tools

Tools for web content fetching and document search operations.
"""

import logging
from typing import Any
from urllib.parse import urlparse

import aiohttp
from langchain_core.tools import tool

logger = logging.getLogger(__name__)


class DocumentCache:
    """Simple in-memory document cache"""

    def __init__(self):
        self._cache: dict[str, str] = {}

    def get(self, url: str) -> str | None:
        return self._cache.get(url)

    def set(self, url: str, content: str) -> None:
        self._cache[url] = content

    def clear(self) -> None:
        self._cache.clear()


# Global document cache (lazy initialization to avoid import side effects)
_document_cache: DocumentCache | None = None


def get_document_cache() -> DocumentCache:
    """Get the document cache instance (lazy initialized)."""
    global _document_cache
    if _document_cache is None:
        _document_cache = DocumentCache()
    return _document_cache


def _validate_url(url: str) -> bool:
    """Validate URL format"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


@tool
async def get_url_content(url: str, use_cache: bool = True) -> dict[str, Any]:
    """
    Fetch content from a URL with caching support.

    Args:
        url: The URL to fetch content from
        use_cache: Whether to use cached content if available (default: True)

    Returns:
        Dictionary containing the fetched content
    """
    try:
        # Validate URL
        if not _validate_url(url):
            return {"success": False, "result": f"Invalid URL format: {url}", "status": "error"}

        # Check cache first
        if use_cache:
            cached_content = get_document_cache().get(url)
            if cached_content:
                return {"success": True, "result": cached_content, "status": "success", "cached": True}

        # Fetch content
        async with aiohttp.ClientSession() as session, session.get(url, timeout=30) as response:
            if response.status != 200:
                return {"success": False, "result": f"HTTP {response.status}: Failed to fetch {url}", "status": "error"}

            content = await response.text()

            # Cache the content
            if use_cache:
                get_document_cache().set(url, content)

            return {"success": True, "result": content, "status": "success", "cached": False}

    except Exception as e:
        return {"success": False, "result": f"Error fetching URL content: {str(e)}", "status": "error"}


@tool
async def search_documents_for(url: str, query: str, use_cache: bool = True) -> dict[str, Any]:
    """
    Search for specific information within a web document.

    Args:
        url: The URL of the document to search
        query: The search query
        use_cache: Whether to use cached content if available (default: True)

    Returns:
        Dictionary containing search results
    """
    try:
        # Get document content
        content_result = await get_url_content(url, use_cache)

        if not content_result["success"]:
            return content_result

        content = content_result["result"]

        # Simple search implementation
        # In a production system, you'd want to use more sophisticated search
        lines = content.split("\n")
        matching_lines = []

        query_lower = query.lower()

        for i, line in enumerate(lines, 1):
            if query_lower in line.lower():
                matching_lines.append(f"Line {i}: {line.strip()}")

        if matching_lines:
            result = f"Found {len(matching_lines)} matches for '{query}':\n\n" + "\n".join(matching_lines[:10])
            if len(matching_lines) > 10:
                result += f"\n... and {len(matching_lines) - 10} more matches"
        else:
            result = f"No matches found for '{query}' in the document"

        return {"success": True, "result": result, "status": "success", "cached": content_result.get("cached", False)}

    except Exception as e:
        return {"success": False, "result": f"Error searching document: {str(e)}", "status": "error"}


__all__ = ["get_url_content", "search_documents_for"]
