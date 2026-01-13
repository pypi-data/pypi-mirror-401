"""
PubMed Literature Search Tool

Search PubMed database for scientific publications and return standardized results.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from .base import BaseSearchTool


class PubMedSearchTool(BaseSearchTool):
    """
    PubMed Scientific Literature Search Tool.

    Search PubMed database for peer-reviewed research papers, clinical studies,
    and scientific discoveries. Returns title, authors, abstract, and publication details.

    Example:
        >>> tool = PubMedSearchTool(enable_cache=True)
        >>> results = tool.search("cancer immunotherapy", max_results=10)
        >>> for article in results:
        ...     print(f"{article['title']} (PMID: {article['pmid']})")
    """

    def search(
        self,
        query: str,
        max_results: int = 20,
        days_back: Optional[int] = 365,
        use_webenv: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Search PubMed database.

        Args:
            query: Search query (supports OR combinations, e.g., "TP53 OR P53")
            max_results: Maximum number of results to return (default: 20)
            days_back: Only include articles from last N days (default: 365, None for no limit)
            use_webenv: Use WebEnv for efficient batch retrieval (default: True)

        Returns:
            List of article dictionaries with standardized fields:
            [
                {
                    'pmid': '12345678',
                    'title': 'Article Title',
                    'authors': ['John Doe', 'Jane Smith'],
                    'authors_short': 'Doe J, Smith J',
                    'journal': 'Nature',
                    'journal_abbr': 'Nature',
                    'year': '2023',
                    'month': '06',
                    'day': '15',
                    'volume': '123',
                    'issue': '4',
                    'pages': '456-789',
                    'abstract': 'Full abstract text...',
                    'doi': '10.1234/example',
                    'keywords': ['cancer', 'therapy'],
                    'publication_types': ['Journal Article', 'Research Support'],
                    'url': 'https://pubmed.ncbi.nlm.nih.gov/12345678/'
                },
                ...
            ]

        Raises:
            requests.HTTPError: If API request fails
        """
        try:
            # Build query with optional date filter
            if days_back is not None:
                end_date = datetime.now()
                start_date = end_date - timedelta(days=days_back)
                date_filter = f"({start_date.strftime('%Y/%m/%d')}[PDAT]:{end_date.strftime('%Y/%m/%d')}[PDAT])"
                full_query = f"{query} AND {date_filter}"
            else:
                full_query = query

            # Step 1: Search PubMed
            search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
            search_params = {
                'db': 'pubmed',
                'term': full_query,
                'retmax': max_results,
                'retmode': 'xml',
                'usehistory': 'y' if use_webenv else 'n'
            }

            search_response = self._get(search_url, params=search_params)
            search_response.raise_for_status()

            # Parse search results
            search_root = ET.fromstring(search_response.content)
            pmids = [id_elem.text for id_elem in search_root.findall('.//Id')]

            if not pmids:
                return []

            # Step 2: Fetch detailed information
            fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

            # Use WebEnv for efficient batch retrieval if available
            webenv_elem = search_root.find('.//WebEnv')
            querykey_elem = search_root.find('.//QueryKey')

            if use_webenv and webenv_elem is not None and querykey_elem is not None:
                fetch_params = {
                    'db': 'pubmed',
                    'query_key': querykey_elem.text,
                    'WebEnv': webenv_elem.text,
                    'retmax': max_results,
                    'retmode': 'xml'
                }
            else:
                # Fallback to direct ID retrieval
                fetch_params = {
                    'db': 'pubmed',
                    'id': ','.join(pmids),
                    'retmode': 'xml'
                }

            fetch_response = self._get(fetch_url, params=fetch_params)
            fetch_response.raise_for_status()

            # Step 3: Parse article details
            fetch_root = ET.fromstring(fetch_response.content)
            articles = []

            for article in fetch_root.findall('.//PubmedArticle'):
                try:
                    article_dict = self._parse_article(article)
                    if article_dict:
                        articles.append(article_dict)
                except Exception as e:
                    # Skip articles that fail to parse
                    if self.verbose:
                        print(f"Warning: Failed to parse article: {e}")
                    continue

            return articles

        except Exception as e:
            if self.verbose:
                print(f"Error searching PubMed: {e}")
            raise

    def _parse_article(self, article: ET.Element) -> Optional[Dict[str, Any]]:
        """
        Parse a single PubMed article XML element.

        Args:
            article: XML element for PubmedArticle

        Returns:
            Dictionary with article information, or None if parsing fails
        """
        # Extract title
        title_elem = article.find('.//ArticleTitle')
        title = title_elem.text if title_elem is not None else "No title available"

        # Extract authors
        authors = []
        for author in article.findall('.//Author'):
            lastname = author.find('LastName')
            forename = author.find('ForeName')
            if lastname is not None and forename is not None:
                authors.append(f"{forename.text} {lastname.text}")

        # Short author format (Last Initial)
        authors_short = []
        for author in article.findall('.//Author'):
            lastname = author.find('LastName')
            forename = author.find('ForeName')
            if lastname is not None and forename is not None:
                initial = forename.text[0] if forename.text else ""
                authors_short.append(f"{lastname.text} {initial}")

        # Extract abstract
        abstract_texts = []
        for abstract_elem in article.findall('.//Abstract/AbstractText'):
            if abstract_elem.text:
                label = abstract_elem.get('Label', '')
                text = abstract_elem.text
                if label:
                    abstract_texts.append(f"{label}: {text}")
                else:
                    abstract_texts.append(text)

        abstract = " ".join(abstract_texts) if abstract_texts else "No abstract available"

        # Extract publication date
        pub_date = article.find('.//PubDate')
        year = "Unknown"
        month = ""
        day = ""
        if pub_date is not None:
            year_elem = pub_date.find('Year')
            month_elem = pub_date.find('Month')
            day_elem = pub_date.find('Day')
            year = year_elem.text if year_elem is not None else "Unknown"
            month = month_elem.text if month_elem is not None else ""
            day = day_elem.text if day_elem is not None else ""

        # Extract journal information
        journal_elem = article.find('.//Journal/Title')
        journal = journal_elem.text if journal_elem is not None else "Unknown journal"

        journal_abbr_elem = article.find('.//Journal/ISOAbbreviation')
        journal_abbr = journal_abbr_elem.text if journal_abbr_elem is not None else journal

        # Extract volume, issue, pages
        volume_elem = article.find('.//Volume')
        issue_elem = article.find('.//Issue')
        pagination_elem = article.find('.//Pagination/MedlinePgn')

        volume = volume_elem.text if volume_elem is not None else ""
        issue = issue_elem.text if issue_elem is not None else ""
        pages = pagination_elem.text if pagination_elem is not None else ""

        # Extract PMID
        pmid_elem = article.find('.//PMID')
        pmid = pmid_elem.text if pmid_elem is not None else "Unknown"

        # Extract DOI
        doi = ""
        for article_id in article.findall('.//ArticleId'):
            if article_id.get('IdType') == 'doi':
                doi = article_id.text
                break

        # Extract keywords
        keywords = []
        for keyword in article.findall('.//Keyword'):
            if keyword.text:
                keywords.append(keyword.text)

        # Extract publication types
        pub_types = []
        for pub_type in article.findall('.//PublicationType'):
            if pub_type.text:
                pub_types.append(pub_type.text)

        return {
            'pmid': pmid,
            'title': title,
            'authors': authors,
            'authors_short': ', '.join(authors_short[:3]) + (' et al.' if len(authors_short) > 3 else ''),
            'authors_full': ', '.join(authors),
            'journal': journal,
            'journal_abbr': journal_abbr,
            'year': year,
            'month': month,
            'day': day,
            'volume': volume,
            'issue': issue,
            'pages': pages,
            'abstract': abstract,
            'doi': doi,
            'keywords': keywords,
            'publication_types': pub_types,
            'url': f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            'doi_url': f"https://doi.org/{doi}" if doi else ""
        }
