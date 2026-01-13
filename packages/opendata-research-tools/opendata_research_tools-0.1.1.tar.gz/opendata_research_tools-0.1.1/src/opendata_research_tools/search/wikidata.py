"""
WikiData Knowledge Graph Search Tool

Search WikiData for structured knowledge about entities.
"""

from typing import List, Dict, Any
from .base import BaseSearchTool


class WikiDataSearchTool(BaseSearchTool):
    """
    WikiData Knowledge Graph Search Tool.

    Search WikiData for structured information about:
    - Diseases
    - Drugs and compounds
    - Proteins and genes
    - Researchers and publications

    Example:
        >>> tool = WikiDataSearchTool(enable_cache=True)
        >>> results = tool.search("diabetes")
        >>> for entity in results:
        ...     print(f"{entity['label']}: {entity['description']}")
    """

    def search(
        self,
        query: str,
        max_results: int = 10,
        entity_type: str = "auto"
    ) -> List[Dict[str, Any]]:
        """
        Search WikiData.

        Args:
            query: Search query
            max_results: Maximum number of results (default: 10)
            entity_type: Entity type filter (auto/disease/drug/protein/gene)

        Returns:
            List of entity dictionaries:
            [
                {
                    'wikidata_id': 'Q5',
                    'label': 'Human',
                    'description': 'Common name of Homo sapiens',
                    'aliases': ['human being', 'person'],
                    'url': 'https://www.wikidata.org/wiki/Q5'
                },
                ...
            ]

        Raises:
            requests.HTTPError: If API request fails
        """
        try:
            # WikiData search API
            search_url = "https://www.wikidata.org/w/api.php"
            search_params = {
                'action': 'wbsearchentities',
                'format': 'json',
                'language': 'en',
                'search': query,
                'limit': max_results
            }

            response = self._get(search_url, params=search_params)
            response.raise_for_status()

            data = response.json()
            search_results = data.get('search', [])

            entities = []
            for result in search_results:
                entities.append({
                    'wikidata_id': result.get('id', ''),
                    'label': result.get('label', ''),
                    'description': result.get('description', ''),
                    'aliases': result.get('aliases', []),
                    'url': f"https://www.wikidata.org/wiki/{result.get('id', '')}"
                })

            return entities

        except Exception as e:
            if self.verbose:
                print(f"Error searching WikiData: {e}")
            raise
