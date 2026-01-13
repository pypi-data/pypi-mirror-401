"""
Protein Structure Search Tool

Search PDB and AlphaFold databases for protein structures.
"""

from typing import List, Dict, Any
from .base import BaseSearchTool


class ProteinStructureSearchTool(BaseSearchTool):
    """
    Protein Structure Search Tool.

    Search for protein structures from:
    - PDB (Protein Data Bank) - experimental structures
    - AlphaFold - predicted structures

    Example:
        >>> tool = ProteinStructureSearchTool(enable_cache=True)
        >>> results = tool.search("TP53")
        >>> for structure in results:
        ...     print(f"{structure['pdb_id']}: {structure['method']}")
    """

    def search(
        self,
        query: str,
        max_results: int = 10,
        include_alphafold: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Search for protein structures.

        Args:
            query: Gene symbol or UniProt ID
            max_results: Maximum number of PDB structures (default: 10)
            include_alphafold: Include AlphaFold predictions (default: True)

        Returns:
            List of structure dictionaries:
            [
                {
                    'pdb_id': '1TUP',
                    'title': 'Crystal structure of...',
                    'method': 'X-RAY DIFFRACTION',
                    'resolution': '2.50',
                    'deposition_date': '1994-08-31',
                    'url': 'https://www.rcsb.org/structure/1TUP',
                    'source': 'PDB'
                },
                {
                    'alphafold_id': 'P04637',
                    'confidence': 'High',
                    'url': 'https://alphafold.ebi.ac.uk/entry/P04637',
                    'source': 'AlphaFold'
                },
                ...
            ]

        Raises:
            requests.HTTPError: If API request fails
        """
        try:
            structures = []

            # Search PDB
            pdb_structures = self._search_pdb(query, max_results)
            structures.extend(pdb_structures)

            # Search AlphaFold
            if include_alphafold:
                af_structures = self._search_alphafold(query)
                structures.extend(af_structures)

            return structures

        except Exception as e:
            if self.verbose:
                print(f"Error searching protein structures: {e}")
            raise

    def _search_pdb(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Search PDB database."""
        try:
            search_url = "https://search.rcsb.org/rcsbsearch/v2/query"
            search_query = {
                "query": {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "rcsb_entity_source_organism.rcsb_gene_name.value",
                        "operator": "exact_match",
                        "value": query
                    }
                },
                "return_type": "entry",
                "request_options": {
                    "results_content_type": ["experimental"],
                    "return_all_hits": False,
                    "pager": {
                        "start": 0,
                        "rows": max_results
                    }
                }
            }

            response = self._post(search_url, json=search_query)
            response.raise_for_status()

            data = response.json()
            result_set = data.get('result_set', [])

            structures = []
            for result in result_set:
                pdb_id = result.get('identifier', '')
                if not pdb_id:
                    continue

                # Get structure details
                summary_url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
                summary_response = self._get(summary_url)

                if summary_response.status_code == 200:
                    summary = summary_response.json()

                    structures.append({
                        'pdb_id': pdb_id,
                        'title': summary.get('struct', {}).get('title', ''),
                        'method': summary.get('exptl', [{}])[0].get('method', ''),
                        'resolution': str(summary.get('rcsb_entry_info', {}).get('resolution_combined', [None])[0] or ''),
                        'deposition_date': summary.get('rcsb_accession_info', {}).get('deposit_date', ''),
                        'url': f"https://www.rcsb.org/structure/{pdb_id}",
                        'source': 'PDB'
                    })

            return structures

        except Exception as e:
            if self.verbose:
                print(f"Warning: PDB search failed: {e}")
            return []

    def _search_alphafold(self, query: str) -> List[Dict[str, Any]]:
        """Search AlphaFold database."""
        try:
            # AlphaFold uses UniProt IDs, try to resolve gene symbol
            search_url = f"https://alphafold.ebi.ac.uk/api/prediction/{query}"

            response = self._get(search_url)

            if response.status_code == 200:
                data = response.json()
                return [{
                    'alphafold_id': data.get('uniprotAccession', query),
                    'gene_name': data.get('gene', query),
                    'organism': data.get('organism', 'Unknown'),
                    'confidence': 'High',  # Simplified
                    'url': f"https://alphafold.ebi.ac.uk/entry/{data.get('uniprotAccession', query)}",
                    'source': 'AlphaFold'
                }]

            return []

        except Exception as e:
            if self.verbose:
                print(f"Warning: AlphaFold search failed: {e}")
            return []
