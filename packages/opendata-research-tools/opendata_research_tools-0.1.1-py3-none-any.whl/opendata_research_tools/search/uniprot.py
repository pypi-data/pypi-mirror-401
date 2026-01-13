"""
UniProt Protein Database Search Tool

Search UniProt for comprehensive protein information.
"""

from typing import List, Dict, Any, Optional
from .base import BaseSearchTool


class UniProtSearchTool(BaseSearchTool):
    """
    UniProt Protein Database Search Tool.

    Search UniProt for comprehensive protein information including:
    - Protein sequence and structure
    - Functional annotation
    - Subcellular localization
    - Disease associations
    - PDB structure IDs
    - AlphaFold model links

    Uses UniProt REST API (no API key required).

    Example:
        >>> tool = UniProtSearchTool(enable_cache=True)
        >>> results = tool.search("TP53")
        >>> for protein in results:
        ...     print(f"{protein['protein_name']} ({protein['uniprot_id']})")
    """

    def __init__(
        self,
        enable_cache: bool = True,
        cache_dir: str = ".cache",
        verbose: bool = False
    ):
        """
        Initialize UniProt search tool.

        Args:
            enable_cache: Whether to enable HTTP caching (default: True)
            cache_dir: Directory for cache files (default: ".cache")
            verbose: Whether to print verbose output (default: False)
        """
        super().__init__(enable_cache=enable_cache, cache_dir=cache_dir, verbose=verbose)
        self.base_url = "https://rest.uniprot.org"

    def search(
        self,
        query: str,
        max_results: int = 5,
        organism: str = "Homo sapiens"
    ) -> List[Dict[str, Any]]:
        """
        Search UniProt for protein information.

        Args:
            query: Gene symbol or protein name
            max_results: Maximum number of results (default: 5)
            organism: Organism name (default: "Homo sapiens")

        Returns:
            List of protein dictionaries with standardized fields:
            [
                {
                    'uniprot_id': 'P04637',
                    'entry_name': 'P53_HUMAN',
                    'protein_name': 'Cellular tumor antigen p53',
                    'gene_names': ['TP53', 'P53'],
                    'organism': 'Homo sapiens',
                    'sequence_length': 393,
                    'function': 'Acts as a tumor suppressor...',
                    'subcellular_location': ['Nucleus', 'Cytoplasm'],
                    'pdb_ids': ['1TUP', '1TSR', ...],
                    'alphafold_id': 'P04637',
                    'url': 'https://www.uniprot.org/uniprotkb/P04637'
                },
                ...
            ]

        Raises:
            requests.HTTPError: If API request fails
        """
        try:
            # Map organism to taxonomy ID
            organism_map = {
                "Homo sapiens": "9606",
                "Mus musculus": "10090",
                "Rattus norvegicus": "10116",
                "Danio rerio": "7955",
                "Drosophila melanogaster": "7227",
                "Caenorhabditis elegans": "6239"
            }

            organism_id = organism_map.get(organism, "9606")

            # Search UniProt
            search_url = f"{self.base_url}/uniprotkb/search"
            search_params = {
                'query': f'(gene:{query}) AND (organism_id:{organism_id})',
                'format': 'json',
                'size': max_results,
                'fields': 'accession,id,gene_names,protein_name,organism_name,length,cc_function,cc_subcellular_location,xref_pdb,xref_alphafolddb'
            }

            search_response = self._get(search_url, params=search_params)
            search_response.raise_for_status()

            search_data = search_response.json()

            if 'results' not in search_data or not search_data['results']:
                return []

            proteins = []

            for result in search_data['results']:
                try:
                    protein_dict = self._parse_protein(result, query)
                    if protein_dict:
                        proteins.append(protein_dict)
                except Exception as e:
                    if self.verbose:
                        uniprot_id = result.get('primaryAccession', 'unknown')
                        print(f"Warning: Failed to parse protein {uniprot_id}: {e}")
                    continue

            return proteins

        except Exception as e:
            if self.verbose:
                print(f"Error searching UniProt: {e}")
            raise

    def _parse_protein(self, result: Dict, query: str) -> Optional[Dict[str, Any]]:
        """
        Parse a single UniProt result entry.

        Args:
            result: UniProt API result dictionary
            query: Original query string (used as fallback)

        Returns:
            Dictionary with protein information, or None if parsing fails
        """
        # Extract basic information
        uniprot_id = result.get('primaryAccession', 'Unknown')
        entry_name = result.get('uniProtkbId', '')

        # Extract protein names
        protein_name = ''
        if 'proteinDescription' in result:
            protein_desc = result['proteinDescription']
            if 'recommendedName' in protein_desc:
                protein_name = protein_desc['recommendedName'].get('fullName', {}).get('value', '')
            elif 'submittedName' in protein_desc and protein_desc['submittedName']:
                protein_name = protein_desc['submittedName'][0].get('fullName', {}).get('value', '')

        # Extract gene names
        gene_names = []
        if 'genes' in result and result['genes']:
            for gene in result['genes']:
                if 'geneName' in gene:
                    gene_names.append(gene['geneName']['value'])

        # Extract organism
        organism = result.get('organism', {}).get('scientificName', 'Homo sapiens')

        # Extract sequence length
        sequence_length = result.get('sequence', {}).get('length', 0)

        # Extract function
        function = ''
        if 'comments' in result:
            for comment in result['comments']:
                if comment.get('commentType') == 'FUNCTION':
                    texts = comment.get('texts', [])
                    if texts:
                        function = texts[0].get('value', '')
                        break

        # Extract subcellular location
        subcellular_location = []
        if 'comments' in result:
            for comment in result['comments']:
                if comment.get('commentType') == 'SUBCELLULAR LOCATION':
                    locations = comment.get('subcellularLocations', [])
                    for loc in locations:
                        if 'location' in loc:
                            subcellular_location.append(loc['location'].get('value', ''))

        # Extract PDB IDs
        pdb_ids = []
        if 'uniProtKBCrossReferences' in result:
            for xref in result['uniProtKBCrossReferences']:
                if xref.get('database') == 'PDB':
                    pdb_ids.append(xref.get('id', ''))

        # Extract AlphaFold DB ID
        alphafold_id = ''
        if 'uniProtKBCrossReferences' in result:
            for xref in result['uniProtKBCrossReferences']:
                if xref.get('database') == 'AlphaFoldDB':
                    alphafold_id = xref.get('id', '')
                    break

        return {
            'uniprot_id': uniprot_id,
            'entry_name': entry_name,
            'protein_name': protein_name,
            'gene_names': gene_names,
            'organism': organism,
            'sequence_length': sequence_length,
            'function': function,
            'subcellular_location': subcellular_location,
            'pdb_ids': pdb_ids,
            'alphafold_id': alphafold_id,
            'alphafold_url': f"https://alphafold.ebi.ac.uk/entry/{alphafold_id}" if alphafold_id else "",
            'url': f"https://www.uniprot.org/uniprotkb/{uniprot_id}"
        }
