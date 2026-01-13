"""
Base class for search tools.

Provides common interface and utilities for all search tools.
"""

from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod


class BaseSearchTool(ABC):
    """
    Base class for all search tools.

    Provides common interface for searching biomedical databases
    and returning standardized dictionary results.
    """

    def __init__(
        self,
        enable_cache: bool = True,
        cache_dir: str = ".cache",
        verbose: bool = False
    ):
        """
        Initialize search tool.

        Args:
            enable_cache: Whether to enable HTTP caching (default: True)
            cache_dir: Directory for cache files (default: ".cache")
            verbose: Whether to print verbose output (default: False)
        """
        self.enable_cache = enable_cache
        self.cache_dir = cache_dir
        self.verbose = verbose

        # Lazy initialization of HTTP cache
        self._cache = None

    @property
    def cache(self):
        """Lazy-load HTTP cache instance."""
        if self._cache is None and self.enable_cache:
            from ..utils.http_cache import HTTPCache
            self._cache = HTTPCache(
                cache_dir=self.cache_dir,
                enabled=self.enable_cache,
                verbose=self.verbose
            )
        return self._cache

    @abstractmethod
    def search(self, query: str, **kwargs) -> List[Dict[str, Any]]:
        """
        Search the database and return results.

        This method must be implemented by all subclasses.

        Args:
            query: Search query string
            **kwargs: Additional search parameters specific to each tool

        Returns:
            List of dictionaries with standardized fields

        Raises:
            NotImplementedError: If not implemented by subclass
        """
        raise NotImplementedError("Subclasses must implement search()")

    def _get(self, url: str, **kwargs):
        """
        Send GET request with optional caching.

        Args:
            url: Request URL
            **kwargs: Additional arguments for requests.get()

        Returns:
            requests.Response object
        """
        # Add default User-Agent if not provided
        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        if 'User-Agent' not in kwargs['headers']:
            kwargs['headers']['User-Agent'] = 'opendata-research-tools/1.0'
        
        if self.enable_cache and self.cache:
            return self.cache.get(url, **kwargs)
        else:
            import requests
            return requests.get(url, **kwargs)

    def _post(self, url: str, **kwargs):
        """
        Send POST request with optional caching.

        Args:
            url: Request URL
            **kwargs: Additional arguments for requests.post()

        Returns:
            requests.Response object
        """
        # Add default User-Agent if not provided
        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        if 'User-Agent' not in kwargs['headers']:
            kwargs['headers']['User-Agent'] = 'opendata-research-tools/1.0'
        
        if self.enable_cache and self.cache:
            return self.cache.post(url, **kwargs)
        else:
            import requests
            return requests.post(url, **kwargs)
