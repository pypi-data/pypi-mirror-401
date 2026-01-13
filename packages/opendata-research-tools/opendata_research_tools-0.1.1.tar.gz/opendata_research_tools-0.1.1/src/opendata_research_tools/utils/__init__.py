"""Utility modules for opendata-research-tools."""

from .http_cache import (
    HTTPCache,
    get_http_cache,
    cached_get,
    cached_post,
)

from .gene_resolver import (
    GeneSynonymResolver,
    GeneResolutionResult,
)

__all__ = [
    # HTTP Caching
    "HTTPCache",
    "get_http_cache",
    "cached_get",
    "cached_post",
    # Gene Resolution
    "GeneSynonymResolver",
    "GeneResolutionResult",
]
