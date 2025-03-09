from datetime import datetime
from pathlib import Path
from typing import List, Optional
from feed_parser import FeedEntry

class HTMLGenerator:
    """
    Generate HTML output from feed entries with a clean, responsive design.
    
    This class handles the generation of an HTML dashboard that displays feed entries
    organized by category. It includes built-in CSS styling and supports customizable
    output locations.
    
    Features:
        - Responsive design with clean typography
        - Category-based organization with customizable order
        - Configurable output directory
        - Built-in CSS styling
        - Support for custom filenames
    
    Attributes:
        output_dir (Optional[str]): Directory where HTML files will be saved
        category_order (List[str]): List defining the order of categories
        css (str): CSS styles for the HTML output
    """
    
    def __init__(self, output_dir: Optional[str] = None):
        """
        Initialize the HTML generator.
        
        Args:
            output_dir (Optional[str]): Directory where the HTML file will be saved.
                                      If None, defaults to user's Desktop.
        """
        self.output_dir = output_dir
        # Define category order (categories not in this list will be displayed after these)
        self.category_order = ["Weather", "US News"]
        
        # CSS styles are defined here for portability (no external files needed)
        self.css = """
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .section {
                margin-bottom: 40px;
            }
            .section-title {
                text-align: center;
                color: #333;
                padding: 20px;
                background-color: #fff;
                border-radius: 5px;
                margin-bottom: 20px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            .entry {
                background-color: #fff;
                padding: 20px;
                margin-bottom: 20px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            .entry-title {
                color: #2c3e50;
                margin-top: 0;
            }
            .entry-meta {
                color: #7f8c8d;
                font-size: 0.9em;
                margin-bottom: 10px;
            }
            .entry-content {
                color: #34495e;
                line-height: 1.6;
            }
            .entry-link {
                display: inline-block;
                margin-top: 10px;
                color: #3498db;
                text-decoration: none;
            }
            .entry-link:hover {
                text-decoration: underline;
            }
            .timestamp {
                text-align: center;
                color: #95a5a6;
                font-size: 0.8em;
                margin-top: 20px;
            }
            .weather-section {
                background-color: #fff;
                padding: 20px;
                border-radius: 5px;
                margin-bottom: 40px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
        """
    
    def generate_entry_html(self, entry: FeedEntry) -> str:
        """
        Generate HTML for a single feed entry.
        
        Args:
            entry (FeedEntry): The feed entry to convert to HTML
        
        Returns:
            str: HTML string representing the entry with title, metadata,
                content preview, and optional "Read more" link
        """
        # Handle None values with defaults
        title = entry.title or "No Title"
        content = entry.content or "No content available"
        published = entry.published or "No date"
        source = entry.source or "Unknown Source"
        
        # Truncate content if it exists and is longer than 500 characters
        content_display = content[:500] + "..." if len(content) > 500 else content
        
        # Create the link HTML only if a valid link exists
        link_html = f'<a class="entry-link" href="{entry.link}" target="_blank">Read more →</a>' if entry.link else ''
        
        return f"""
        <div class="entry">
            <h2 class="entry-title">{title}</h2>
            <div class="entry-meta">
                {published} | Source: {source}
            </div>
            <div class="entry-content">
                {content_display}
            </div>
            {link_html}
        </div>
        """
    
    def generate_html(self, entries: List[FeedEntry], title: str) -> str:
        """
        Generate complete HTML document from feed entries.
        
        This method:
        1. Groups entries by category
        2. Orders categories according to self.category_order
        3. Generates HTML sections for each category
        4. Wraps everything in a complete HTML document with CSS
        
        Args:
            entries (List[FeedEntry]): List of feed entries to include
            title (str): Title for the HTML page
        
        Returns:
            str: Complete HTML document as a string
        """
        # Group entries by category
        categories = {}
        for entry in entries:
            category = entry.category or "Uncategorized"
            if category not in categories:
                categories[category] = []
            categories[category].append(entry)
        
        # Generate sections in specified order
        sections_html = ""
        
        # First, add categories in the specified order
        for category in self.category_order:
            if category in categories:
                sections_html += f"""
                <div class="section">
                    <h1 class="section-title">{category}</h1>
                    {''.join(self.generate_entry_html(entry) for entry in categories[category])}
                </div>
                """
                # Remove the category so it's not added again
                del categories[category]
        
        # Then add remaining categories
        for category, category_entries in categories.items():
            sections_html += f"""
            <div class="section">
                <h1 class="section-title">{category}</h1>
                {''.join(self.generate_entry_html(entry) for entry in category_entries)}
            </div>
            """
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title}</title>
            <meta charset="utf-8">
            <style>{self.css}</style>
        </head>
        <body>
            {sections_html}
            <div class="timestamp">
                Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            </div>
        </body>
        </html>
        """
    
    def save_html(self, entries: List[FeedEntry], title: str, filename: Optional[str] = None) -> str:
        """
        Generate and save HTML file to the configured output directory.
        
        Args:
            entries (List[FeedEntry]): List of feed entries to include
            title (str): Title of the HTML page
            filename (Optional[str]): Custom filename. If None, uses 'News_YYYY-MM-DD.html'
        
        Returns:
            str: Full path to the generated file
        
        Example:
            >>> generator = HTMLGenerator("/var/www/html")
            >>> path = generator.save_html(entries, "News Dashboard", "index.html")
            >>> print(path)
            '/var/www/html/index.html'
        """
        # Determine output directory
        if self.output_dir:
            output_path = Path(self.output_dir)
        else:
            output_path = Path.home() / "Desktop"
        
        # Ensure output directory exists
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate filename if not provided
        if not filename:
            today = datetime.now().strftime("%Y-%m-%d")
            filename = f"News_{today}.html"
        
        # Create full output path
        output_file = str(output_path / filename)
        
        # Generate and save HTML
        html_content = self.generate_html(entries, title)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        return output_file 