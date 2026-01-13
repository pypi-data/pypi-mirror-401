"""
LumenFeed News Search Tool

Search for recent industry news, press releases, and commercial developments.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import os
import re
from .base import BaseSearchTool


class NewsSearchTool(BaseSearchTool):
    """
    LumenFeed News Search Tool.

    Search for recent industry news from LumenFeed API including:
    - Business news and press releases
    - Clinical trial announcements
    - Regulatory approvals
    - Product launches
    - Market trends

    Requires LUMENFEED_API environment variable.

    Example:
        >>> import os
        >>> os.environ['LUMENFEED_API'] = 'your-api-key'
        >>> tool = NewsSearchTool(enable_cache=True)
        >>> results = tool.search("cancer immunotherapy")
        >>> for article in results:
        ...     print(f"{article['title']} - {article['source']}")
    """

    def search(
        self,
        query: str,
        max_results: int = 10,
        days_back: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Search LumenFeed for recent news articles.

        Args:
            query: Search query for news articles
            max_results: Maximum number of results (default: 10)
            days_back: Number of days to look back (default: 30)

        Returns:
            List of article dictionaries:
            [
                {
                    'article_id': 'abc123',
                    'title': 'Article Title',
                    'source': 'Publisher Name',
                    'author': 'John Doe',
                    'published_at': '2024-01-15 10:30:00',
                    'url': 'https://example.com/article',
                    'content_excerpt': 'Article summary...',
                    'category': 'Clinical Research',
                    'keywords': ['cancer', 'immunotherapy'],
                    'sentiment_label': 'Positive',
                    'publisher_id': 'publisher123',
                    'company_mentions': 'Merck Inc, Pfizer Inc'
                },
                ...
            ]

        Raises:
            ValueError: If LUMENFEED_API environment variable is not set
            requests.HTTPError: If API request fails
        """
        try:
            # Get API key from environment
            api_key = os.getenv('LUMENFEED_API')
            if not api_key:
                raise ValueError(
                    "LUMENFEED_API environment variable not set. "
                    "Please set your LumenFeed API key."
                )

            # LumenFeed API endpoint
            base_url = "https://api.lumenfeed.com/api/v1/articles"

            # Calculate date range as Unix timestamp
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            start_timestamp = int(start_date.timestamp())
            end_timestamp = int(end_date.timestamp())

            # Prepare search parameters
            params = {
                'q': query,
                'per_page': min(max_results, 100),  # API max is 100
                'page': 1,
                'sort_by': 'date_desc',
                'filter_by': f'language:=en && published_at:>={start_timestamp} && published_at:<={end_timestamp}',
                'query_by': 'title,content_excerpt,author,keywords'
            }

            # Set up headers with API key
            headers = {
                'X-API-Key': api_key,
                'Content-Type': 'application/json',
                'User-Agent': 'OpenDataResearchTools/1.0'
            }

            # Make API request
            response = self._get(base_url, params=params, headers=headers, timeout=30)

            # Handle specific error cases
            if response.status_code == 401:
                raise ValueError("Invalid LumenFeed API key")
            elif response.status_code == 429:
                raise Exception("LumenFeed API quota limit exceeded")
            elif response.status_code == 503:
                raise Exception("LumenFeed service temporarily unavailable")

            response.raise_for_status()
            data = response.json()

            # Extract articles from response
            raw_articles = data.get('data', [])

            articles = []
            for article in raw_articles:
                # Extract article information
                article_id = article.get('id', '')
                title = article.get('title', 'No title')
                content_excerpt = article.get('content_excerpt', '')
                author = article.get('author', 'Unknown')
                keywords = article.get('keywords', [])
                publisher_id = article.get('publisher_id', 'Unknown')
                sentiment_label = article.get('sentiment_label', 'Neutral')
                published_at = article.get('published_at', '')
                source_link = article.get('source_link', '')

                # Format publication date
                pub_date = self._format_date(published_at)

                # Categorize article
                category = self._categorize_news(title, content_excerpt)

                # Extract company mentions
                company_mentions = self._extract_companies(f"{title} {content_excerpt}")

                articles.append({
                    'article_id': article_id,
                    'title': title,
                    'source': article.get('source', publisher_id),
                    'author': author,
                    'published_at': pub_date,
                    'url': source_link,
                    'content_excerpt': content_excerpt,
                    'category': category,
                    'keywords': keywords,
                    'sentiment_label': sentiment_label,
                    'publisher_id': publisher_id,
                    'company_mentions': company_mentions
                })

            return articles

        except Exception as e:
            if self.verbose:
                print(f"Error searching LumenFeed news: {e}")
            raise

    def _format_date(self, published_at: Any) -> str:
        """Format publication date from various formats."""
        if not published_at:
            return ''

        try:
            if isinstance(published_at, (int, float)):
                # Unix timestamp
                dt = datetime.fromtimestamp(published_at)
                return dt.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(published_at, str):
                # Try different date formats
                for fmt in ['%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%d', '%Y-%m-%dT%H:%M:%S']:
                    try:
                        dt = datetime.strptime(published_at.replace('Z', ''), fmt.replace('Z', ''))
                        return dt.strftime('%Y-%m-%d %H:%M:%S')
                    except:
                        continue
            return str(published_at)
        except:
            return str(published_at)

    def _categorize_news(self, title: str, description: str) -> str:
        """Categorize news based on content."""
        title_lower = title.lower()
        desc_lower = description.lower()

        if any(word in title_lower or word in desc_lower for word in ['clinical', 'trial', 'study', 'research']):
            return 'Clinical Research'
        elif any(word in title_lower or word in desc_lower for word in ['fda', 'approval', 'regulatory', 'clearance']):
            return 'Regulatory Approval'
        elif any(word in title_lower or word in desc_lower for word in ['funding', 'investment', 'series', 'venture']):
            return 'Funding & Investment'
        elif any(word in title_lower or word in desc_lower for word in ['patent', 'intellectual property', 'ip']):
            return 'Intellectual Property'
        elif any(word in title_lower or word in desc_lower for word in ['launch', 'product', 'release']):
            return 'Product Launch'
        else:
            return 'General News'

    def _extract_companies(self, text: str) -> str:
        """Extract company mentions from text."""
        companies = []
        company_patterns = [
            r'([A-Z][a-zA-Z]+ (?:Inc|Corp|Ltd|LLC|Pharmaceuticals|Therapeutics|Biotech))',
            r'([A-Z][a-zA-Z]+ (?:& Co|Group|Holdings))',
        ]

        for pattern in company_patterns:
            matches = re.findall(pattern, text)
            companies.extend(matches)

        return ', '.join(companies[:3]) if companies else ''
