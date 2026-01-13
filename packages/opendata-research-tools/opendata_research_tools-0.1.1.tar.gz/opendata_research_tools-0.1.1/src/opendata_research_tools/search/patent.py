"""
Patent Search Tool

Search patent databases for intellectual property information.

NOTE: Free patent APIs (PatentsView) have been discontinued. This tool currently
returns empty results. For production use, consider:
- EPO OPS API (free but requires registration)
- Google Patents BigQuery (requires Google Cloud account)
- Commercial APIs (SerpAPI, SearchAPI)
"""

from typing import List, Dict, Any
from .base import BaseSearchTool


class PatentSearchTool(BaseSearchTool):
    """
    Patent Search Tool.

    Search for patents related to genes, drugs, and technologies.

    **IMPORTANT**: Free patent APIs have been discontinued. This tool currently
    returns empty results. Manual patent searches can be done at:
    - Google Patents: https://patents.google.com/
    - USPTO: https://www.uspto.gov/
    - EPO: https://worldwide.espacenet.com/

    For API access in production:
    - EPO OPS API (free but requires registration)
    - Google Patents BigQuery (requires Google Cloud account)
    - Lens.org API (free for academic use, requires registration)
    - Commercial APIs (SerpAPI, SearchAPI)

    Example:
        >>> tool = PatentSearchTool()
        >>> results = tool.search("CRISPR gene editing")
        >>> # Returns empty list - patent APIs discontinued
        >>> print(len(results))
        0
    """

    def search(
        self,
        query: str,
        max_results: int = 30,
        jurisdiction: str = "all"
    ) -> List[Dict[str, Any]]:
        """
        Search patent databases.

        **NOTE**: This method currently returns empty results as free patent APIs
        have been discontinued. The interface is maintained for future implementation
        when a suitable API becomes available.

        Args:
            query: Search query (gene/drug/technology name)
            max_results: Maximum number of patents (default: 30)
            jurisdiction: Patent jurisdiction filter - "US", "EP", "all" (default: "all")

        Returns:
            Empty list (patent search currently disabled):
            [
                # When enabled, would return:
                {
                    'patent_number': 'US1234567A',
                    'title': 'Patent Title',
                    'assignee': 'Company Name',
                    'inventors': ['John Doe', 'Jane Smith'],
                    'filing_date': '2023-01-15',
                    'grant_date': '2024-06-20',
                    'status': 'Active',
                    'jurisdiction': 'US',
                    'abstract': 'Patent abstract...',
                    'url': 'https://patents.google.com/patent/US1234567A',
                    'classification': ['A61K', 'C12N']
                },
                ...
            ]

        Raises:
            NotImplementedError: Patent search is currently disabled
        """
        if self.verbose:
            print("Patent search is currently disabled.")
            print("Free patent APIs (PatentsView) have been discontinued.")
            print(f"Manual search recommended at: https://patents.google.com/?q={query.replace(' ', '+')}")
            print("\nFor API access in production:")
            print("- EPO OPS API (free but requires registration)")
            print("- Google Patents BigQuery (requires Google Cloud account)")
            print("- Commercial APIs (SerpAPI, SearchAPI)")

        # Return empty list as free patent APIs are discontinued
        return []

    def get_manual_search_urls(self, query: str) -> Dict[str, str]:
        """
        Get URLs for manual patent searches.

        Args:
            query: Search query

        Returns:
            Dictionary of search URLs:
            {
                'google_patents': 'https://patents.google.com/?q=...',
                'uspto': 'https://www.uspto.gov/',
                'epo': 'https://worldwide.espacenet.com/...'
            }
        """
        query_encoded = query.replace(' ', '+')
        return {
            'google_patents': f'https://patents.google.com/?q={query_encoded}',
            'uspto': 'https://www.uspto.gov/',
            'epo': f'https://worldwide.espacenet.com/patent/search?q={query_encoded}'
        }
