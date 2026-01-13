"""
NCBI Gene Database Search Tool

Search NCBI Gene database for comprehensive gene information.
"""

from typing import List, Dict, Any, Optional
import xml.etree.ElementTree as ET
from .base import BaseSearchTool


class NCBIGeneSearchTool(BaseSearchTool):
    """
    NCBI Gene Database Search Tool.

    Search NCBI Gene database for comprehensive gene information including:
    - Official gene symbol and name
    - Gene summary and function
    - Genomic location and structure
    - Associated aliases and designations

    Uses NCBI E-utilities API (no API key required for reasonable usage).

    Example:
        >>> tool = NCBIGeneSearchTool(enable_cache=True)
        >>> results = tool.search("TP53")
        >>> for gene in results:
        ...     print(f"{gene['symbol']}: {gene['description']}")
    """

    def __init__(
        self,
        enable_cache: bool = True,
        cache_dir: str = ".cache",
        verbose: bool = False
    ):
        """
        Initialize NCBI Gene search tool.

        Args:
            enable_cache: Whether to enable HTTP caching (default: True)
            cache_dir: Directory for cache files (default: ".cache")
            verbose: Whether to print verbose output (default: False)
        """
        super().__init__(enable_cache=enable_cache, cache_dir=cache_dir, verbose=verbose)
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    def search(
        self,
        query: str,
        max_results: int = 10,
        organism: str = "Homo sapiens"
    ) -> List[Dict[str, Any]]:
        """
        Search NCBI Gene database.

        Args:
            query: Gene symbol or name
            max_results: Maximum number of results (default: 10)
            organism: Organism name (default: "Homo sapiens")

        Returns:
            List of gene dictionaries with standardized fields:
            [
                {
                    'gene_id': '7157',
                    'symbol': 'TP53',
                    'description': 'tumor protein p53',
                    'summary': 'This gene encodes a tumor suppressor protein...',
                    'organism': 'Homo sapiens',
                    'chromosome': '17',
                    'location': 'Chromosome 17 (7668421-7687490)',
                    'aliases': 'P53, TRP53, ...',
                    'designations': 'cellular tumor antigen p53, ...',
                    'url': 'https://www.ncbi.nlm.nih.gov/gene/7157'
                },
                ...
            ]

        Raises:
            requests.HTTPError: If API request fails
        """
        try:
            # Step 1: Search for gene IDs
            search_url = f"{self.base_url}/esearch.fcgi"
            search_params = {
                'db': 'gene',
                'term': f"{query}[Gene Name] AND {organism}[Organism]",
                'retmax': max_results,
                'retmode': 'xml'
            }

            search_response = self._get(search_url, params=search_params)
            search_response.raise_for_status()

            # Parse search results
            search_root = ET.fromstring(search_response.content)
            gene_ids = [id_elem.text for id_elem in search_root.findall('.//Id')]

            if not gene_ids:
                return []

            # Step 2: Fetch detailed information
            fetch_url = f"{self.base_url}/esummary.fcgi"
            fetch_params = {
                'db': 'gene',
                'id': ','.join(gene_ids),
                'retmode': 'xml'
            }

            fetch_response = self._get(fetch_url, params=fetch_params)
            fetch_response.raise_for_status()

            # Step 3: Parse gene details
            fetch_root = ET.fromstring(fetch_response.content)
            genes = []

            for doc_sum in fetch_root.findall('.//DocumentSummary'):
                try:
                    gene_dict = self._parse_gene(doc_sum, query)
                    if gene_dict:
                        genes.append(gene_dict)
                except Exception as e:
                    if self.verbose:
                        gene_id = doc_sum.get('uid', 'unknown')
                        print(f"Warning: Failed to parse gene {gene_id}: {e}")
                    continue

            return genes

        except Exception as e:
            if self.verbose:
                print(f"Error searching NCBI Gene: {e}")
            raise

    def _parse_gene(self, doc_sum: ET.Element, query: str) -> Optional[Dict[str, Any]]:
        """
        Parse a single gene DocumentSummary element.

        Args:
            doc_sum: XML element for DocumentSummary
            query: Original query string (used as fallback for symbol)

        Returns:
            Dictionary with gene information, or None if parsing fails
        """
        gene_id = doc_sum.get('uid', '')

        # Extract basic gene information
        symbol = self._get_element_text(doc_sum, 'Name') or query
        description = self._get_element_text(doc_sum, 'Description')
        summary = self._get_element_text(doc_sum, 'Summary')
        organism = self._get_element_text(doc_sum, 'Organism/ScientificName')

        # Extract chromosomal location
        chr_loc = self._get_element_text(doc_sum, 'GenomicInfo/GenomicInfoType/ChrLoc')
        chr_start = self._get_element_text(doc_sum, 'GenomicInfo/GenomicInfoType/ChrStart')
        chr_stop = self._get_element_text(doc_sum, 'GenomicInfo/GenomicInfoType/ChrStop')

        location = ""
        if chr_loc:
            location = f"Chromosome {chr_loc}"
            if chr_start and chr_stop:
                location += f" ({chr_start}-{chr_stop})"

        # Extract aliases and designations
        aliases = self._get_element_text(doc_sum, 'OtherAliases')
        designations = self._get_element_text(doc_sum, 'OtherDesignations')

        return {
            'gene_id': gene_id,
            'symbol': symbol,
            'description': description,
            'summary': summary,
            'organism': organism or "Homo sapiens",
            'chromosome': chr_loc,
            'location': location,
            'aliases': aliases,
            'designations': designations,
            'url': f"https://www.ncbi.nlm.nih.gov/gene/{gene_id}"
        }

    def _get_element_text(self, parent: ET.Element, path: str) -> str:
        """
        Safely extract text from XML element.

        Args:
            parent: Parent XML element
            path: XPath-like path to element

        Returns:
            Element text or empty string if not found
        """
        # Handle Item elements with Name attribute
        if '[@Name=' in path:
            parts = path.split('[@Name=')
            tag = parts[0]
            name = parts[1].strip('"]')

            for item in parent.findall(f'.//{tag}'):
                if item.get('Name') == name:
                    return item.text or ""
            return ""

        # Handle simple paths
        elem = parent.find(f'.//{path}')
        return elem.text if elem is not None and elem.text else ""
