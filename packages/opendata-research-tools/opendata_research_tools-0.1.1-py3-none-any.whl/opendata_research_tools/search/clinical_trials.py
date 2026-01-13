"""
ClinicalTrials.gov Search Tool

Search ClinicalTrials.gov for clinical trial information.
"""

from typing import List, Dict, Any
from .base import BaseSearchTool


class ClinicalTrialsSearchTool(BaseSearchTool):
    """
    ClinicalTrials.gov Search Tool.

    Search for clinical trials from ClinicalTrials.gov including:
    - Trial status and phase
    - Study design and enrollment
    - Interventions and outcomes
    - Sponsor information

    Example:
        >>> tool = ClinicalTrialsSearchTool(enable_cache=True)
        >>> results = tool.search("cancer immunotherapy", status="recruiting")
        >>> for trial in results:
        ...     print(f"{trial['nct_id']}: {trial['title']}")
    """

    def search(
        self,
        query: str,
        max_results: int = 50,
        status: str = "all",
        phase: str = "all"
    ) -> List[Dict[str, Any]]:
        """
        Search ClinicalTrials.gov for trials.

        Args:
            query: Search query (gene/drug/disease name)
            max_results: Maximum number of trials (default: 50)
            status: Trial status filter - "recruiting", "completed", "all" (default: "all")
            phase: Trial phase filter - "phase1", "phase2", "phase3", "phase4", "all" (default: "all")

        Returns:
            List of trial dictionaries:
            [
                {
                    'nct_id': 'NCT12345678',
                    'title': 'Brief Title',
                    'official_title': 'Full Official Title',
                    'overall_status': 'RECRUITING',
                    'study_type': 'INTERVENTIONAL',
                    'phases': ['PHASE2', 'PHASE3'],
                    'enrollment_count': 150,
                    'start_date': '2024-01-15',
                    'completion_date': '2026-12-31',
                    'sponsor': 'University Medical Center',
                    'conditions': ['Cancer', 'Melanoma'],
                    'interventions': ['Drug: Pembrolizumab', 'Drug: Nivolumab'],
                    'primary_outcomes': ['Overall Survival', 'Progression Free Survival'],
                    'brief_summary': 'Study description...',
                    'url': 'https://clinicaltrials.gov/study/NCT12345678',
                    'keywords': ['immunotherapy', 'checkpoint inhibitor']
                },
                ...
            ]

        Raises:
            requests.HTTPError: If API request fails
        """
        try:
            # ClinicalTrials.gov API v2
            base_url = "https://clinicaltrials.gov/api/v2/studies"

            # Build query parameters
            params = {
                'query.term': query,
                'pageSize': min(max_results, 100),  # API limit per request
                'format': 'json'
            }

            # Add status filter
            if status != "all" and status.lower() != "all":
                status_map = {
                    'recruiting': 'RECRUITING',
                    'completed': 'COMPLETED',
                    'active': 'ACTIVE_NOT_RECRUITING',
                    'terminated': 'TERMINATED',
                    'suspended': 'SUSPENDED',
                    'withdrawn': 'WITHDRAWN'
                }
                params['filter.overallStatus'] = status_map.get(status.lower(), status.upper())

            # Add phase filter
            if phase != "all" and phase.lower() != "all":
                phase_map = {
                    'phase1': 'PHASE1',
                    'phase2': 'PHASE2',
                    'phase3': 'PHASE3',
                    'phase4': 'PHASE4',
                    'early_phase1': 'EARLY_PHASE1'
                }
                params['filter.phase'] = phase_map.get(phase.lower(), phase.upper())

            # Make API request
            response = self._get(base_url, params=params)
            response.raise_for_status()

            data = response.json()
            studies = data.get('studies', [])

            trials = []
            for study in studies:
                try:
                    protocol = study.get('protocolSection', {})
                    identification = protocol.get('identificationModule', {})
                    status_module = protocol.get('statusModule', {})
                    design = protocol.get('designModule', {})
                    arms = protocol.get('armsInterventionsModule', {})
                    outcomes = protocol.get('outcomesModule', {})
                    description = protocol.get('descriptionModule', {})

                    # Extract key information
                    nct_id = identification.get('nctId', 'Unknown')
                    enrollment_info = design.get('enrollmentInfo', {})

                    trial_data = {
                        'nct_id': nct_id,
                        'title': identification.get('briefTitle', 'No title'),
                        'official_title': identification.get('officialTitle', ''),
                        'overall_status': status_module.get('overallStatus', 'Unknown'),
                        'study_type': design.get('studyType', 'Unknown'),
                        'phases': design.get('phases', []),
                        'enrollment_count': enrollment_info.get('count', 0),
                        'start_date': status_module.get('startDateStruct', {}).get('date', ''),
                        'completion_date': status_module.get('completionDateStruct', {}).get('date', ''),
                        'sponsor': identification.get('organization', {}).get('fullName', 'Unknown'),
                        'conditions': protocol.get('conditionsModule', {}).get('conditions', []),
                        'interventions': [i.get('name', '') for i in arms.get('interventions', [])] if arms.get('interventions') else [],
                        'primary_outcomes': [o.get('measure', '') for o in outcomes.get('primaryOutcomes', [])] if outcomes.get('primaryOutcomes') else [],
                        'brief_summary': description.get('briefSummary', ''),
                        'url': f"https://clinicaltrials.gov/study/{nct_id}",
                        'keywords': protocol.get('conditionsModule', {}).get('keywords', [])
                    }

                    trials.append(trial_data)

                except Exception as e:
                    if self.verbose:
                        print(f"Warning: Error processing trial: {e}")
                    continue

            return trials

        except Exception as e:
            if self.verbose:
                print(f"Error searching ClinicalTrials.gov: {e}")
            raise
