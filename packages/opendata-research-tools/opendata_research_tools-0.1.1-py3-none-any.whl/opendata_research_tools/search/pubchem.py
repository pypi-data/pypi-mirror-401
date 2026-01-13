"""
PubChem Compound Database Search Tool

Search PubChem for chemical compounds related to targets.
"""

from typing import List, Dict, Any
import xml.etree.ElementTree as ET
from .base import BaseSearchTool


class PubChemSearchTool(BaseSearchTool):
    """
    PubChem Compound Database Search Tool.

    Search PubChem for compounds including:
    - Known inhibitors and activators
    - Chemical structure and properties
    - Molecular formula and weight
    - SMILES and InChI identifiers

    Example:
        >>> tool = PubChemSearchTool(enable_cache=True)
        >>> results = tool.search("JAK2", max_results=10)
        >>> for compound in results:
        ...     print(f"CID {compound['cid']}: {compound['name']}")
    """

    def __init__(
        self,
        enable_cache: bool = True,
        cache_dir: str = ".cache",
        verbose: bool = False
    ):
        """
        Initialize PubChem search tool.

        Args:
            enable_cache: Whether to enable HTTP caching (default: True)
            cache_dir: Directory for cache files (default: ".cache")
            verbose: Whether to print verbose output (default: False)
        """
        super().__init__(enable_cache=enable_cache, cache_dir=cache_dir, verbose=verbose)
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        self.pug_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"

    def search(
        self,
        query: str,
        max_results: int = 10,
        search_types: List[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search PubChem for compounds related to target.

        Args:
            query: Target gene/protein name (e.g., "JAK2", "TP53")
            max_results: Maximum number of results (default: 10)
            search_types: Search types to use (default: ["inhibitor", "activator"])

        Returns:
            List of compound dictionaries:
            [
                {
                    'cid': '12345',
                    'name': 'Compound Name',
                    'molecular_formula': 'C20H25N3O',
                    'molecular_weight': '323.43',
                    'smiles': 'CC(C)...',
                    'inchi': 'InChI=1S/...',
                    'url': 'https://pubchem.ncbi.nlm.nih.gov/compound/12345'
                },
                ...
            ]

        Raises:
            requests.HTTPError: If API request fails
        """
        try:
            if search_types is None:
                search_types = ["inhibitor", "activator"]

            search_terms = [f"{query} {stype}" for stype in search_types]

            all_compounds = []
            seen_cids = set()

            for search_term in search_terms:
                try:
                    # Search for compound IDs
                    search_url = f"{self.base_url}/esearch.fcgi"
                    search_params = {
                        'db': 'pccompound',
                        'term': search_term,
                        'retmax': max(5, max_results // len(search_terms)),
                        'retmode': 'xml'
                    }

                    search_response = self._get(search_url, params=search_params)
                    search_response.raise_for_status()

                    search_root = ET.fromstring(search_response.content)
                    cids = [id_elem.text for id_elem in search_root.findall('.//Id')]

                    # Filter duplicates
                    cids = [cid for cid in cids if cid not in seen_cids][:5]
                    seen_cids.update(cids)

                    if not cids:
                        continue

                    # Fetch compound details
                    for cid in cids:
                        try:
                            compound_data = self._fetch_compound_details(cid)
                            if compound_data:
                                all_compounds.append(compound_data)
                        except Exception as e:
                            if self.verbose:
                                print(f"Warning: Failed to fetch CID {cid}: {e}")
                            continue

                except Exception as e:
                    if self.verbose:
                        print(f"Warning: Search failed for '{search_term}': {e}")
                    continue

                if len(all_compounds) >= max_results:
                    break

            return all_compounds[:max_results]

        except Exception as e:
            if self.verbose:
                print(f"Error searching PubChem: {e}")
            raise

    def _fetch_compound_details(self, cid: str) -> Dict[str, Any]:
        """
        Fetch detailed information for a compound.

        Args:
            cid: PubChem Compound ID

        Returns:
            Dictionary with compound details
        """
        # Fetch compound properties
        props_url = f"{self.pug_url}/compound/cid/{cid}/property/MolecularFormula,MolecularWeight,IUPACName,InChI,CanonicalSMILES/JSON"

        props_response = self._get(props_url)
        props_response.raise_for_status()

        props_data = props_response.json()

        if 'PropertyTable' not in props_data or 'Properties' not in props_data['PropertyTable']:
            return None

        props = props_data['PropertyTable']['Properties'][0]

        return {
            'cid': cid,
            'name': props.get('IUPACName', f'Compound {cid}'),
            'molecular_formula': props.get('MolecularFormula', ''),
            'molecular_weight': str(props.get('MolecularWeight', '')),
            'smiles': props.get('CanonicalSMILES', ''),
            'inchi': props.get('InChI', ''),
            'url': f"https://pubchem.ncbi.nlm.nih.gov/compound/{cid}"
        }
