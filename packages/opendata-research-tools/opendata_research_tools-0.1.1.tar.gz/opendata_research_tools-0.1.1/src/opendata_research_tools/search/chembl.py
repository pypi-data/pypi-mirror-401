"""
ChEMBL Bioactive Compounds Search Tool

Search ChEMBL for bioactive compounds and drug candidates.
"""

from typing import List, Dict, Any, Optional
from .base import BaseSearchTool


class ChEMBLSearchTool(BaseSearchTool):
    """
    ChEMBL Bioactive Compounds Search Tool.

    Search ChEMBL database for bioactive compounds including:
    - IC50, EC50, Ki values
    - Target-compound associations
    - Bioactivity data
    - Structure-activity relationships

    Example:
        >>> tool = ChEMBLSearchTool(enable_cache=True)
        >>> results = tool.search(target="JAK2", activity_type="inhibitor")
        >>> for compound in results:
        ...     print(f"{compound['molecule_chembl_id']}: {compound['activity_value']} {compound['activity_units']}")
    """

    def search(
        self,
        target: str,
        activity_type: str = "all",
        max_results: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Search ChEMBL for bioactive compounds.

        Args:
            target: Target protein/gene name
            activity_type: Activity type filter - "inhibitor", "activator", "all" (default: "all")
            max_results: Maximum number of compounds (default: 50)

        Returns:
            List of compound dictionaries:
            [
                {
                    'molecule_chembl_id': 'CHEMBL123456',
                    'target_chembl_id': 'CHEMBL1234',
                    'target_name': 'Tyrosine-protein kinase JAK2',
                    'activity_type': 'IC50',
                    'activity_value': '10.5',
                    'activity_units': 'nM',
                    'activity_relation': '=',
                    'assay_description': '...',
                    'url': 'https://www.ebi.ac.uk/chembl/compound_report_card/CHEMBL123456/'
                },
                ...
            ]

        Raises:
            requests.HTTPError: If API request fails
        """
        try:
            # Step 1: Search for target
            target_url = "https://www.ebi.ac.uk/chembl/api/data/target/search"
            target_params = {'q': target, 'format': 'json'}

            target_response = self._get(target_url, params=target_params)
            target_response.raise_for_status()

            target_data = target_response.json()
            targets = target_data.get('targets', [])

            if not targets:
                return []

            # Get first target
            target_id = targets[0].get('target_chembl_id')
            target_name = targets[0].get('pref_name', target)
            target_type = targets[0].get('target_type', 'Unknown')

            # Step 2: Search for bioactivities
            activity_url = "https://www.ebi.ac.uk/chembl/api/data/activity"
            activity_params = {
                'target_chembl_id': target_id,
                'limit': max_results * 2,  # Get more to allow filtering
                'format': 'json'
            }

            activity_response = self._get(activity_url, params=activity_params)
            activity_response.raise_for_status()

            activity_data = activity_response.json()
            activities = activity_data.get('activities', [])

            if not activities:
                return []

            # Step 3: Group and filter activities
            compounds = []
            seen_molecules = set()

            for activity in activities:
                molecule_id = activity.get('molecule_chembl_id')
                if not molecule_id or molecule_id in seen_molecules:
                    continue

                activity_type_val = activity.get('standard_type', '')
                activity_value = activity.get('standard_value', '')
                activity_units = activity.get('standard_units', '')
                activity_relation = activity.get('standard_relation', '')
                assay_desc = activity.get('assay_description', '')

                # Filter by activity type if specified
                if activity_type != "all":
                    if activity_type == "inhibitor" and activity_type_val not in ['IC50', 'Ki', 'Kd']:
                        continue
                    elif activity_type == "activator" and activity_type_val not in ['EC50', 'AC50']:
                        continue

                compounds.append({
                    'molecule_chembl_id': molecule_id,
                    'target_chembl_id': target_id,
                    'target_name': target_name,
                    'target_type': target_type,
                    'activity_type': activity_type_val,
                    'activity_value': activity_value,
                    'activity_units': activity_units,
                    'activity_relation': activity_relation,
                    'assay_description': assay_desc,
                    'url': f"https://www.ebi.ac.uk/chembl/compound_report_card/{molecule_id}/"
                })

                seen_molecules.add(molecule_id)

                if len(compounds) >= max_results:
                    break

            return compounds

        except Exception as e:
            if self.verbose:
                print(f"Error searching ChEMBL: {e}")
            raise
