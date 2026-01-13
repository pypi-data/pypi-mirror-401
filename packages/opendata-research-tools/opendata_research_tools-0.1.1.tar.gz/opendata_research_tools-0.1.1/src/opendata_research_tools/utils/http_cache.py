"""
HTTP Cache System

Automatically cache HTTP GET/POST requests to reduce API calls and improve performance.

Features:
- Smart cache keys based on URL + parameters
- Configurable cache expiration (TTL)
- SSL error retry mechanism with exponential backoff
- Cache statistics tracking
- Optional caching (can be disabled)
"""

import json
import hashlib
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import requests
from requests.exceptions import SSLError
import time


class HTTPCache:
    """HTTP request caching system with automatic expiration and retry logic."""

    def __init__(
        self,
        cache_dir: str = ".cache",
        ttl_hours: Optional[int] = None,
        enabled: bool = True,
        verbose: bool = False
    ):
        """
        Initialize HTTP cache.

        Args:
            cache_dir: Directory to store cache files
            ttl_hours: Cache time-to-live in hours (default: 168 hours / 7 days)
            enabled: Whether caching is enabled (default: True)
            verbose: Whether to print cache operations (default: False)
        """
        self.enabled = enabled
        self.verbose = verbose
        self.cache_dir = Path(cache_dir)

        if self.enabled:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

        # TTL from parameter, environment variable, or default (7 days)
        if ttl_hours is None:
            ttl_days = int(os.getenv('HTTP_CACHE_TTL_DAYS', '7'))
            ttl_hours = ttl_days * 24

        self.ttl = timedelta(hours=ttl_hours)
        self.ttl_hours = ttl_hours

        # Cache statistics
        self.stats = {
            'hits': 0,
            'misses': 0,
            'total_requests': 0
        }

        if self.enabled and self.verbose:
            print(f"HTTP Cache enabled: {self.cache_dir.absolute()}")
            print(f"Cache TTL: {self.ttl_hours} hours ({self.ttl_hours // 24} days)")

    def _generate_cache_key(
        self,
        url: str,
        method: str = "GET",
        params: Optional[Dict] = None,
        data: Optional[Any] = None,
        json_data: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ) -> str:
        """
        Generate unique cache key based on request parameters.

        Args:
            url: Request URL
            method: HTTP method (GET/POST)
            params: Query parameters
            data: Request data
            json_data: JSON request data
            headers: Request headers

        Returns:
            MD5 hash as cache key
        """
        # Build dictionary with all request parameters
        cache_dict = {
            'url': url,
            'method': method.upper(),
            'params': params or {},
            'data': data if isinstance(data, (dict, str)) else str(data) if data else {},
            'json': json_data or {},
            # Only include important headers
            'headers': {k: v for k, v in (headers or {}).items()
                       if k.lower() in ['content-type', 'accept', 'authorization']}
        }

        # Serialize and hash
        cache_str = json.dumps(cache_dict, sort_keys=True, default=str)
        cache_hash = hashlib.md5(cache_str.encode()).hexdigest()

        return cache_hash

    def _get_cache_path(self, cache_key: str) -> Path:
        """Get cache file path for a given cache key."""
        return self.cache_dir / f"{cache_key}.json"

    def _is_cache_valid(self, cache_path: Path) -> bool:
        """
        Check if cached file is still valid based on TTL.

        Args:
            cache_path: Path to cache file

        Returns:
            True if cache exists and is not expired
        """
        if not cache_path.exists():
            return False

        # Check file modification time
        mtime = datetime.fromtimestamp(cache_path.stat().st_mtime)
        return datetime.now() - mtime < self.ttl

    def get(self, url: str, **kwargs) -> requests.Response:
        """
        Send GET request with caching.

        Args:
            url: Request URL
            **kwargs: Additional arguments for requests.get()

        Returns:
            requests.Response object
        """
        return self._cached_request('GET', url, **kwargs)

    def post(self, url: str, **kwargs) -> requests.Response:
        """
        Send POST request with caching.

        Args:
            url: Request URL
            **kwargs: Additional arguments for requests.post()

        Returns:
            requests.Response object
        """
        return self._cached_request('POST', url, **kwargs)

    def _cached_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        Execute HTTP request with caching and SSL retry logic.

        Args:
            method: HTTP method (GET/POST)
            url: Request URL
            **kwargs: Additional request arguments

        Returns:
            requests.Response object
        """
        self.stats['total_requests'] += 1

        # If caching is disabled, send request directly
        if not self.enabled:
            return self._send_request(method, url, **kwargs)

        # Generate cache key
        cache_key = self._generate_cache_key(
            url=url,
            method=method,
            params=kwargs.get('params'),
            data=kwargs.get('data'),
            json_data=kwargs.get('json'),
            headers=kwargs.get('headers')
        )

        cache_path = self._get_cache_path(cache_key)

        # Check cache
        if self._is_cache_valid(cache_path):
            self.stats['hits'] += 1
            if self.verbose:
                print(f"Cache HIT: {url[:80]}...")
            return self._load_from_cache(cache_path)

        # Cache miss, send actual request
        self.stats['misses'] += 1
        if self.verbose:
            print(f"Cache MISS: {url[:80]}...")

        response = self._send_request(method, url, **kwargs)

        # Save to cache
        self._save_to_cache(cache_path, response)

        return response

    def _send_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        Send HTTP request with SSL error retry mechanism.

        Args:
            method: HTTP method
            url: Request URL
            **kwargs: Request arguments

        Returns:
            requests.Response object

        Raises:
            SSLError: If SSL errors persist after retries
            ValueError: If unsupported HTTP method
        """
        max_retries = 3
        retry_delay = 1  # seconds

        for attempt in range(max_retries):
            try:
                if method.upper() == 'GET':
                    response = requests.get(url, **kwargs)
                elif method.upper() == 'POST':
                    response = requests.post(url, **kwargs)
                else:
                    raise ValueError(f"Unsupported method: {method}")

                return response

            except SSLError as e:
                if attempt < max_retries - 1:
                    if self.verbose:
                        print(f"SSL error, retrying {attempt + 1}/{max_retries - 1}...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    if self.verbose:
                        print(f"SSL error, max retries reached")
                    raise

    def _save_to_cache(self, cache_path: Path, response: requests.Response):
        """
        Save HTTP response to cache file.

        Args:
            cache_path: Path to save cache file
            response: requests.Response object to cache
        """
        cache_data = {
            'url': response.url,
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'content': response.text,
            'encoding': response.encoding,
            'timestamp': datetime.now().isoformat()
        }

        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)

    def _load_from_cache(self, cache_path: Path) -> requests.Response:
        """
        Load HTTP response from cache file.

        Args:
            cache_path: Path to cache file

        Returns:
            requests.Response object reconstructed from cache
        """
        with open(cache_path, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)

        # Create a mock Response object
        response = requests.Response()
        response.url = cache_data['url']
        response.status_code = cache_data['status_code']
        response.headers.update(cache_data['headers'])
        response._content = cache_data['content'].encode(cache_data.get('encoding', 'utf-8'))
        response.encoding = cache_data.get('encoding', 'utf-8')

        return response

    def clear_cache(self):
        """Remove all cached files."""
        import shutil
        if self.cache_dir.exists():
            shutil.rmtree(self.cache_dir)
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        if self.verbose:
            print("Cache cleared")

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache statistics
        """
        hit_rate = (self.stats['hits'] / self.stats['total_requests'] * 100
                   if self.stats['total_requests'] > 0 else 0)

        return {
            **self.stats,
            'hit_rate': f"{hit_rate:.1f}%",
            'cache_size': sum(1 for _ in self.cache_dir.glob('*.json')) if self.enabled else 0
        }

    def print_stats(self):
        """Print cache statistics to console."""
        stats = self.get_stats()
        print("\n" + "=" * 60)
        print("HTTP Cache Statistics")
        print("=" * 60)
        print(f"Total Requests: {stats['total_requests']}")
        print(f"Cache Hits: {stats['hits']}")
        print(f"Cache Misses: {stats['misses']}")
        print(f"Hit Rate: {stats['hit_rate']}")
        print(f"Cache Files: {stats['cache_size']}")
        print(f"Caching Enabled: {self.enabled}")
        print("=" * 60 + "\n")


# Global cache instance (lazy initialization)
_global_cache: Optional[HTTPCache] = None


def get_http_cache(
    cache_dir: str = ".cache",
    ttl_hours: Optional[int] = None,
    enabled: bool = True,
    verbose: bool = False
) -> HTTPCache:
    """
    Get or create global HTTP cache instance.

    Args:
        cache_dir: Cache directory path
        ttl_hours: Cache TTL in hours (default: 168 / 7 days)
        enabled: Whether caching is enabled (default: True)
        verbose: Whether to print cache operations (default: False)

    Returns:
        HTTPCache instance
    """
    global _global_cache
    if _global_cache is None:
        _global_cache = HTTPCache(
            cache_dir=cache_dir,
            ttl_hours=ttl_hours,
            enabled=enabled,
            verbose=verbose
        )
    return _global_cache


def cached_get(url: str, **kwargs) -> requests.Response:
    """
    Convenience function: Send GET request with caching.

    Uses global cache instance.

    Args:
        url: Request URL
        **kwargs: Additional arguments for requests.get()

    Returns:
        requests.Response object

    Example:
        >>> response = cached_get('https://api.example.com/data', params={'key': 'value'})
        >>> print(response.json())
    """
    cache = get_http_cache()
    return cache.get(url, **kwargs)


def cached_post(url: str, **kwargs) -> requests.Response:
    """
    Convenience function: Send POST request with caching.

    Uses global cache instance.

    Args:
        url: Request URL
        **kwargs: Additional arguments for requests.post()

    Returns:
        requests.Response object

    Example:
        >>> response = cached_post('https://api.example.com/search', json={'query': 'test'})
        >>> print(response.json())
    """
    cache = get_http_cache()
    return cache.post(url, **kwargs)
