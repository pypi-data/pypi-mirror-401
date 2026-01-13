"""
Gene Synonym Resolver

Stateless gene symbol resolution with multi-database querying.
Supports NCBI Gene and MyGene.info databases with intelligent caching.

Features:
- Query multiple gene databases (NCBI Gene, MyGene.info)
- Merge and deduplicate results
- Confidence scoring for disambiguation
- In-memory caching with TTL
- Extract gene symbols from text
"""

from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
import requests
import json
import re
from datetime import datetime, timedelta


@dataclass
class GeneResolutionResult:
    """Result of gene symbol resolution."""
    canonical_symbol: str
    entrez_id: Optional[str] = None
    ensembl_id: Optional[str] = None
    uniprot_ids: List[str] = field(default_factory=list)
    official_name: Optional[str] = None
    organism: str = "Homo sapiens"
    aliases: List[str] = field(default_factory=list)
    synonyms: List[str] = field(default_factory=list)
    chromosome: Optional[str] = None
    confidence_score: float = 0.0
    source: str = "unknown"

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary.

        Returns:
            Dictionary representation of the gene resolution result
        """
        return {
            'canonical_symbol': self.canonical_symbol,
            'entrez_id': self.entrez_id,
            'ensembl_id': self.ensembl_id,
            'uniprot_ids': self.uniprot_ids,
            'official_name': self.official_name,
            'organism': self.organism,
            'aliases': self.aliases,
            'synonyms': self.synonyms,
            'chromosome': self.chromosome,
            'confidence_score': self.confidence_score,
            'source': self.source
        }


class GeneSynonymResolver:
    """
    Stateless gene symbol resolution with multi-database querying.

    Queries NCBI Gene and MyGene.info to resolve gene symbols, IDs, and aliases
    to canonical symbols with metadata.
    """

    def __init__(self, cache_ttl: int = 86400, default_organism: str = "Homo sapiens"):
        """
        Initialize gene resolver.

        Args:
            cache_ttl: Cache time-to-live in seconds (default: 86400 / 24 hours)
            default_organism: Default organism for gene searches (default: "Homo sapiens")
        """
        self.cache_ttl = cache_ttl
        self.default_organism = default_organism
        self._cache: Dict[str, tuple[GeneResolutionResult, datetime]] = {}

    def resolve(
        self,
        query: str,
        use_llm_disambiguation: bool = False,
        organism: Optional[str] = None
    ) -> GeneResolutionResult:
        """
        Resolve gene query to canonical symbol.

        Args:
            query: Gene name, symbol, or identifier
            use_llm_disambiguation: Use LLM for disambiguation (placeholder, not implemented)
            organism: Target organism (default: uses default_organism from __init__)

        Returns:
            GeneResolutionResult with canonical symbol and metadata

        Raises:
            ValueError: If no gene found for query

        Example:
            >>> resolver = GeneSynonymResolver()
            >>> result = resolver.resolve("TP53")
            >>> print(result.canonical_symbol)  # "TP53"
            >>> print(result.entrez_id)  # "7157"
        """
        # Use default organism if not specified
        target_organism = organism or self.default_organism

        # Check cache first (include organism in cache key)
        cache_key = f"{query}|{target_organism}"
        cached = self._get_from_cache(cache_key)
        if cached:
            return cached

        # Query multiple databases
        ncbi_results = self._query_ncbi_gene(query, target_organism)
        mygene_results = self._query_mygene_info(query, target_organism)

        # Merge results
        all_results = self._merge_results(ncbi_results, mygene_results)

        # Filter by organism
        all_results = [r for r in all_results if r.organism == target_organism]

        if not all_results:
            raise ValueError(
                f"No {target_organism} gene found for query: {query}. "
                f"Try alternative names, check spelling, or specify a different organism."
            )

        # If single result, return it
        if len(all_results) == 1:
            result = all_results[0]
            self._add_to_cache(cache_key, result)
            return result

        # Multiple results - use LLM disambiguation if enabled
        if use_llm_disambiguation:
            result = self._llm_disambiguate(query, all_results)
        else:
            # Return highest confidence result
            result = max(all_results, key=lambda x: x.confidence_score)

        self._add_to_cache(cache_key, result)
        return result

    def _query_ncbi_gene(
        self,
        query: str,
        organism: str = "Homo sapiens"
    ) -> List[GeneResolutionResult]:
        """
        Query NCBI Gene database.

        Args:
            query: Gene name or symbol
            organism: Target organism (default: "Homo sapiens")

        Returns:
            List of gene resolution results
        """
        try:
            # Step 1: Search for gene with organism filter
            search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

            # Build search term: prioritize exact matches
            search_term = f'({query}[Gene Name] OR {query}[Gene Symbol]) AND "{organism}"[Organism]'

            search_params = {
                'db': 'gene',
                'term': search_term,
                'retmode': 'json',
                'retmax': 10,
                'tool': 'opendata_research_tools',
                'email': 'research@example.com'
            }

            search_response = requests.get(search_url, params=search_params, timeout=30)
            search_response.raise_for_status()
            search_data = search_response.json()

            gene_ids = search_data.get('esearchresult', {}).get('idlist', [])
            if not gene_ids:
                return []

            # Step 2: Fetch detailed information
            summary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
            summary_params = {
                'db': 'gene',
                'id': ','.join(gene_ids[:5]),
                'retmode': 'json',
                'tool': 'opendata_research_tools',
                'email': 'research@example.com'
            }

            summary_response = requests.get(summary_url, params=summary_params, timeout=30)
            summary_response.raise_for_status()
            summary_data = summary_response.json()

            return self._parse_ncbi_results(summary_data.get('result', {}), query)

        except Exception as e:
            # Silent failure - return empty list if API is unavailable
            return []

    def _query_mygene_info(
        self,
        query: str,
        organism: str = "Homo sapiens"
    ) -> List[GeneResolutionResult]:
        """
        Query MyGene.info API.

        Args:
            query: Gene name or symbol
            organism: Target organism (default: "Homo sapiens")

        Returns:
            List of gene resolution results
        """
        try:
            # Map organism to MyGene.info species parameter
            species_map = {
                "Homo sapiens": "human",
                "Mus musculus": "mouse",
                "Rattus norvegicus": "rat",
                "Danio rerio": "zebrafish",
                "Drosophila melanogaster": "fruitfly",
                "Caenorhabditis elegans": "worm"
            }

            species = species_map.get(organism, "human")

            base_url = "https://mygene.info/v3/query"
            params = {
                'q': query,
                'species': species,
                'fields': 'symbol,name,alias,other_names,ensembl.gene,entrezgene,uniprot',
                'size': 10
            }

            response = requests.get(base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            return self._parse_mygene_results(data, organism)

        except Exception as e:
            # Silent failure - return empty list if API is unavailable
            return []

    def _parse_ncbi_results(
        self,
        ncbi_data: Dict,
        query: str
    ) -> List[GeneResolutionResult]:
        """
        Parse NCBI Gene results.

        Args:
            ncbi_data: NCBI API response data
            query: Original query string for scoring

        Returns:
            List of parsed gene resolution results
        """
        results = []

        for gene_id, gene_info in ncbi_data.items():
            if gene_id == 'uids':
                continue

            try:
                # Extract gene symbol
                gene_symbol = gene_info.get('name', '')

                # Extract aliases
                aliases = []
                other_aliases = gene_info.get('otheraliases', '')
                if other_aliases:
                    aliases = [a.strip() for a in other_aliases.split(',') if a.strip()]

                # Extract synonyms
                synonyms = []
                other_designations = gene_info.get('otherdesignations', '')
                if other_designations:
                    synonyms = [s.strip() for s in other_designations.split('|') if s.strip()]

                # Calculate confidence score based on match quality
                confidence = 0.8  # Base NCBI confidence

                # Boost score for exact symbol match
                if gene_symbol.upper() == query.upper():
                    confidence = 0.95
                # Boost score for exact alias match
                elif any(alias.upper() == query.upper() for alias in aliases):
                    confidence = 0.9
                # Boost score for exact synonym match
                elif any(syn.upper() == query.upper() for syn in synonyms):
                    confidence = 0.85

                result = GeneResolutionResult(
                    canonical_symbol=gene_symbol,
                    entrez_id=str(gene_id),
                    official_name=gene_info.get('description', ''),
                    organism=gene_info.get('organism', {}).get('scientificname', 'Homo sapiens'),
                    chromosome=gene_info.get('chromosome', ''),
                    aliases=aliases,
                    synonyms=synonyms,
                    confidence_score=confidence,
                    source='NCBI Gene'
                )

                results.append(result)

            except Exception as e:
                continue

        return results

    def _parse_mygene_results(
        self,
        mygene_data: Dict,
        organism: str = "Homo sapiens"
    ) -> List[GeneResolutionResult]:
        """
        Parse MyGene.info results.

        Args:
            mygene_data: MyGene.info API response data
            organism: Target organism for filtering

        Returns:
            List of parsed gene resolution results
        """
        results = []

        hits = mygene_data.get('hits', [])
        for hit in hits:
            try:
                # Extract gene symbol
                gene_symbol = hit.get('symbol', '')

                # Extract aliases
                aliases = []
                if 'alias' in hit:
                    alias_data = hit['alias']
                    if isinstance(alias_data, list):
                        aliases = alias_data
                    elif isinstance(alias_data, str):
                        aliases = [alias_data]

                # Extract synonyms
                synonyms = []
                if 'other_names' in hit:
                    other_names = hit['other_names']
                    if isinstance(other_names, list):
                        synonyms = other_names
                    elif isinstance(other_names, str):
                        synonyms = [other_names]

                # Extract UniProt IDs
                uniprot_ids = []
                if 'uniprot' in hit:
                    uniprot = hit['uniprot']
                    if isinstance(uniprot, dict) and 'Swiss-Prot' in uniprot:
                        swiss_prot = uniprot['Swiss-Prot']
                        if isinstance(swiss_prot, list):
                            uniprot_ids = swiss_prot
                        elif isinstance(swiss_prot, str):
                            uniprot_ids = [swiss_prot]

                # Extract Ensembl ID
                ensembl_id = None
                if 'ensembl' in hit:
                    ensembl = hit['ensembl']
                    if isinstance(ensembl, dict):
                        ensembl_id = ensembl.get('gene', '')

                # Calculate confidence score (normalize MyGene score to 0-1 range)
                raw_score = hit.get('_score', 0)
                confidence = min(1.0, raw_score / 100.0)

                result = GeneResolutionResult(
                    canonical_symbol=gene_symbol,
                    entrez_id=str(hit.get('entrezgene', '')),
                    ensembl_id=ensembl_id,
                    uniprot_ids=uniprot_ids,
                    official_name=hit.get('name', ''),
                    organism=organism,
                    aliases=aliases,
                    synonyms=synonyms,
                    confidence_score=confidence,
                    source='MyGene.info'
                )

                results.append(result)

            except Exception as e:
                continue

        return results

    def _merge_results(
        self,
        ncbi_results: List[GeneResolutionResult],
        mygene_results: List[GeneResolutionResult]
    ) -> List[GeneResolutionResult]:
        """
        Merge and deduplicate results from multiple sources.

        Args:
            ncbi_results: Results from NCBI Gene
            mygene_results: Results from MyGene.info

        Returns:
            Merged list of unique results
        """
        merged: Dict[str, GeneResolutionResult] = {}

        # Add NCBI results
        for result in ncbi_results:
            if result.entrez_id:
                merged[result.entrez_id] = result

        # Merge MyGene results
        for result in mygene_results:
            if result.entrez_id and result.entrez_id in merged:
                # Merge with existing
                existing = merged[result.entrez_id]

                # Combine aliases and synonyms
                existing.aliases = list(set(existing.aliases + result.aliases))
                existing.synonyms = list(set(existing.synonyms + result.synonyms))

                # Add missing fields
                if not existing.ensembl_id and result.ensembl_id:
                    existing.ensembl_id = result.ensembl_id
                if not existing.uniprot_ids and result.uniprot_ids:
                    existing.uniprot_ids = result.uniprot_ids

                # Use the higher confidence score
                existing.confidence_score = max(existing.confidence_score, result.confidence_score)
                existing.source = f"{existing.source} + {result.source}"

            elif result.entrez_id:
                # New result
                merged[result.entrez_id] = result

        return list(merged.values())

    def _llm_disambiguate(
        self,
        query: str,
        candidates: List[GeneResolutionResult]
    ) -> GeneResolutionResult:
        """
        Use LLM to disambiguate between multiple gene matches.

        Note: This is a placeholder for LLM integration.
        Currently returns the highest confidence result.

        Args:
            query: Original query string
            candidates: List of candidate results

        Returns:
            Best matching result
        """
        # TODO: Implement LLM-based disambiguation
        # This would involve:
        # 1. Format candidates as structured prompt
        # 2. Call LLM with context about the query
        # 3. Parse LLM response to select best match

        # For now, return highest confidence
        return max(candidates, key=lambda x: x.confidence_score)

    def _get_from_cache(self, query: str) -> Optional[GeneResolutionResult]:
        """
        Get result from cache if not expired.

        Args:
            query: Cache key

        Returns:
            Cached result if available and not expired, None otherwise
        """
        if query in self._cache:
            result, timestamp = self._cache[query]
            if datetime.now() - timestamp < timedelta(seconds=self.cache_ttl):
                return result
            else:
                # Expired, remove from cache
                del self._cache[query]
        return None

    def _add_to_cache(self, query: str, result: GeneResolutionResult):
        """
        Add result to cache.

        Args:
            query: Cache key
            result: Result to cache
        """
        self._cache[query] = (result, datetime.now())

    def extract_symbols(self, text: str) -> List[str]:
        """
        Extract potential gene symbols from text.

        Looks for uppercase words 2-10 characters long, filtering out
        common non-gene acronyms.

        Args:
            text: Free-form text that may contain gene symbols

        Returns:
            List of potential gene symbols

        Example:
            >>> resolver = GeneSynonymResolver()
            >>> symbols = resolver.extract_symbols("TP53 and BRCA1 are important genes")
            >>> print(symbols)  # ["TP53", "BRCA1"]
        """
        # Simple extraction: look for uppercase words 2-10 characters
        pattern = r'\b[A-Z][A-Z0-9]{1,9}\b'
        matches = re.findall(pattern, text)

        # Filter out common non-gene words
        common_words = {'DNA', 'RNA', 'ATP', 'GTP', 'FDA', 'USA', 'UK', 'EU', 'WHO', 'NIH'}
        symbols = [m for m in matches if m not in common_words]

        return list(set(symbols))  # Remove duplicates

    def get_search_terms(self, result: GeneResolutionResult) -> Set[str]:
        """
        Generate comprehensive search terms from resolution result.

        Includes canonical symbol, official name, aliases, and synonyms.

        Args:
            result: Gene resolution result

        Returns:
            Set of search terms for literature/database searches

        Example:
            >>> resolver = GeneSynonymResolver()
            >>> result = resolver.resolve("TP53")
            >>> terms = resolver.get_search_terms(result)
            >>> print(terms)  # {"TP53", "tumor protein p53", "P53", ...}
        """
        terms = set()

        # Add canonical symbol and name
        if result.canonical_symbol:
            terms.add(result.canonical_symbol)
        if result.official_name:
            terms.add(result.official_name)

        # Add aliases and synonyms
        terms.update(result.aliases)
        terms.update(result.synonyms)

        # Clean terms
        cleaned = {t.strip() for t in terms if t and len(t.strip()) > 1}

        return cleaned
