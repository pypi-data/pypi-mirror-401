"""
OpenData Research Tools
======================

A lightweight Python library for searching biomedical databases and returning
standardized data.

Quick Start
-----------
>>> from opendata_research_tools.search import PubMedSearchTool
>>>
>>> # Search PubMed
>>> tool = PubMedSearchTool(enable_cache=True)
>>> results = tool.search(query="cancer immunotherapy", max_results=10)
>>>
>>> # Results is a list of dictionaries
>>> for article in results:
...     print(f"{article['title']} (PMID: {article['pmid']})")

Features
--------
- Search 10+ biomedical databases
- Standardized dictionary output
- Optional HTTP caching
- Gene symbol resolution
- Minimal dependencies (only requests)

"""

from .version import __version__, __version_info__

# Utils
from .utils import (
    HTTPCache,
    get_http_cache,
    cached_get,
    cached_post,
    GeneSynonymResolver,
    GeneResolutionResult,
)

# Search tools
from .search import (
    BaseSearchTool,
    PubMedSearchTool,
    NCBIGeneSearchTool,
    UniProtSearchTool,
    ChEMBLSearchTool,
    PubChemSearchTool,
    ProteinStructureSearchTool,
    WikiDataSearchTool,
    ClinicalTrialsSearchTool,
    NewsSearchTool,
    PatentSearchTool,
)

__all__ = [
    # Version
    "__version__",
    "__version_info__",
    # Utils
    "HTTPCache",
    "get_http_cache",
    "cached_get",
    "cached_post",
    "GeneSynonymResolver",
    "GeneResolutionResult",
    # Search tools
    "BaseSearchTool",
    "PubMedSearchTool",
    "NCBIGeneSearchTool",
    "UniProtSearchTool",
    "ChEMBLSearchTool",
    "PubChemSearchTool",
    "ProteinStructureSearchTool",
    "WikiDataSearchTool",
    "ClinicalTrialsSearchTool",
    "NewsSearchTool",
    "PatentSearchTool",
]
