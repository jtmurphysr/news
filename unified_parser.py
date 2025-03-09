import feedparser
import ssl
import re
from datetime import datetime
from typing import List, Dict, Any
import requests
from feed_parser import FeedParser, FeedEntry

class UnifiedNewsParser(FeedParser):
    """
    A unified parser that handles both RSS feeds and NewsAPI endpoints.
    
    This class automatically detects the feed type based on the URL and applies
    the appropriate parsing strategy. It handles SSL certificate verification,
    user agent configuration, and various date formats.
    
    Features:
        - Automatic feed type detection
        - SSL certificate handling
        - Custom user agent for RSS feeds
        - Fallback content handling
        - HTML cleaning and CDATA removal
        - Multiple date format support
    
    Attributes:
        url (str): URL of the feed (RSS or NewsAPI endpoint)
        api_key (Optional[str]): API key for NewsAPI (not needed for RSS feeds)
        name (str): Name of the feed source (inherited from FeedParser)
    """
    
    def __init__(self, url: str, name: str, api_key: str = None):
        """
        Initialize the unified parser.
        
        Args:
            url (str): URL of the feed to parse
            name (str): Name of the feed source
            api_key (Optional[str]): API key for NewsAPI endpoints
        """
        super().__init__(name)
        self.url = url
        self.api_key = api_key
        
        # Configure SSL context for RSS feeds
        if hasattr(ssl, '_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context
        
        # Configure user agent for RSS feeds
        feedparser.USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    
    def is_newsapi_url(self) -> bool:
        """
        Check if the URL is a NewsAPI endpoint.
        
        Returns:
            bool: True if the URL is a NewsAPI endpoint, False otherwise
        """
        return "newsapi.org" in self.url
    
    def parse_newsapi(self) -> List[FeedEntry]:
        """
        Parse content from a NewsAPI endpoint.
        
        This method handles:
        - API authentication
        - Response validation
        - Date parsing
        - Content extraction with fallbacks
        
        Returns:
            List[FeedEntry]: List of parsed news entries
        
        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.api_key:
            print(f"Error: NewsAPI key required for {self.url}")
            return []
            
        try:
            params = {
                'apiKey': self.api_key
            }
            
            # Add country parameter for top-headlines endpoint
            if 'top-headlines' in self.url:
                params['country'] = 'us'
            
            response = requests.get(self.url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') != 'ok':
                print(f"Error from NewsAPI: {data.get('message', 'Unknown error')}")
                return []
            
            entries = []
            for article in data['articles']:
                # Format the date
                published = article.get('publishedAt', '')
                if published:
                    try:
                        date_obj = datetime.strptime(published, '%Y-%m-%dT%H:%M:%SZ')
                        published = date_obj.strftime('%Y-%m-%d %H:%M')
                    except ValueError:
                        published = "No date available"
                else:
                    published = "No date available"
                
                # Get content with fallbacks
                content = article.get('description') or article.get('content') or "No content available"
                
                entries.append(FeedEntry(
                    title=article.get('title', 'No title'),
                    content=content,
                    published=published,
                    link=article.get('url', ''),
                    source=f"{self.name} - {article.get('source', {}).get('name', 'Unknown')}",
                    category=self.name
                ))
            
            return entries
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching from NewsAPI: {str(e)}")
            return []
    
    def parse_rss(self) -> List[FeedEntry]:
        """
        Parse content from an RSS feed.
        
        This method handles:
        - Feed validation
        - HTML cleaning
        - CDATA removal
        - Multiple date formats
        - Content extraction with fallbacks
        
        Returns:
            List[FeedEntry]: List of parsed feed entries
        """
        feed = feedparser.parse(self.url)
        
        if not feed.entries:
            print(f"Error: Could not parse feed at {self.url}")
            return []
            
        entries = []
        date_formats = [
            '%a, %d %b %Y %H:%M:%S %z',  # RFC 822 format
            '%a, %d %b %Y %H:%M:%S',     # RFC 822 without timezone
            '%Y-%m-%d %H:%M:%S',         # ISO-like format
        ]
        
        for entry in feed.entries:
            # Clean title
            title = entry.get('title', 'No title')
            title = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', title)
            
            # Get content with fallbacks
            content = ''
            if 'content' in entry:
                content = entry['content'][0]['value']
            elif 'summary' in entry:
                content = entry['summary']
            elif 'description' in entry:
                content = entry['description']
            else:
                content = 'No content available'
                
            # Clean content
            content = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', content)
            content = self.clean_content(content)
            
            # Format date
            published = entry.get('published', entry.get('updated', ''))
            if published:
                published = self.format_date(published, date_formats)
            else:
                published = "No date available"
            
            entries.append(FeedEntry(
                title=title.strip(),
                content=content,
                published=published,
                link=entry.get('link', ''),
                source=self.name,
                category=self.name
            ))
            
        return entries
    
    def parse(self) -> List[FeedEntry]:
        """
        Parse content based on URL type.
        
        This method automatically detects whether the URL is a NewsAPI endpoint
        or an RSS feed and calls the appropriate parsing method.
        
        Returns:
            List[FeedEntry]: List of parsed entries from either source
        """
        if self.is_newsapi_url():
            return self.parse_newsapi()
        else:
            return self.parse_rss() 