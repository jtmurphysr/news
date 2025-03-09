from abc import ABC, abstractmethod
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class FeedEntry:
    """
    Data class representing a single entry from any feed source (RSS, NewsAPI, Weather).
    
    Attributes:
        title (str): The title or headline of the entry
        content (str): The main content or description
        published (str): Publication date/time in 'YYYY-MM-DD HH:MM' format
        link (Optional[str]): URL to the full article/content, if available
        source (Optional[str]): Name of the source (e.g., "BBC News", "Weather Service")
        category (Optional[str]): Category for grouping (e.g., "Weather", "US News")
    """
    title: str
    content: str
    published: str
    link: Optional[str] = None
    source: Optional[str] = None
    category: Optional[str] = None

class FeedParser(ABC):
    """
    Abstract base class defining the interface for all feed parsers.
    
    This class provides common functionality for parsing different types of feeds
    (RSS, NewsAPI, Weather) and ensures consistent output format through the
    FeedEntry data class.
    
    Attributes:
        name (str): Name of the parser/feed source
    
    Methods:
        parse(): Abstract method that must be implemented by subclasses
        clean_content(): Helper method to clean HTML and format text
        format_date(): Helper method to parse various date formats
    """
    
    def __init__(self, name: str):
        """
        Initialize the parser with a name.
        
        Args:
            name (str): Name of the parser/feed source
        """
        self.name = name
        
    @abstractmethod
    def parse(self) -> List[FeedEntry]:
        """
        Parse the feed and return a list of entries.
        
        This method must be implemented by all subclasses to handle their
        specific feed format and return a standardized list of FeedEntry objects.
        
        Returns:
            List[FeedEntry]: List of parsed feed entries
        """
        pass
    
    def clean_content(self, content: str) -> str:
        """
        Clean content by removing HTML tags and normalizing whitespace.
        
        Args:
            content (str): Raw content string that may contain HTML
        
        Returns:
            str: Cleaned and formatted content string
        """
        import re
        from html import unescape
        
        # Remove HTML tags
        content = re.sub(r'<[^>]+>', '', content)
        # Convert HTML entities
        content = unescape(content)
        # Remove multiple spaces and newlines
        content = re.sub(r'\s+', ' ', content).strip()
        return content

    def format_date(self, date_str: str, formats: List[str]) -> str:
        """
        Try to parse a date string using multiple possible formats.
        
        Args:
            date_str (str): Date string to parse
            formats (List[str]): List of possible date formats to try
        
        Returns:
            str: Formatted date string in 'YYYY-MM-DD HH:MM' format,
                or original string if parsing fails
        
        Example formats:
            - '%a, %d %b %Y %H:%M:%S %z'  # RSS common format
            - '%Y-%m-%dT%H:%M:%SZ'        # ISO format
            - '%Y-%m-%d %H:%M:%S'         # SQL-like format
        """
        for fmt in formats:
            try:
                date_obj = datetime.strptime(date_str, fmt)
                return date_obj.strftime('%Y-%m-%d %H:%M')
            except ValueError:
                continue
        return date_str  # Return original string if no format matches 