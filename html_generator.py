from datetime import datetime
from pathlib import Path
from typing import List, Optional
from feed_parser import FeedEntry
import os

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
    
    def __init__(self, output_dir=None):
        """
        Initialize the HTML generator.
        
        Args:
            output_dir (str, optional): Directory to save HTML files.
                                      If None, defaults to Desktop.
        """
        self.output_dir = output_dir or os.path.expanduser("~/Desktop")
        os.makedirs(self.output_dir, exist_ok=True)
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
    
    def _generate_feed_html(self, entries: List[FeedEntry], title: str, source_name: str) -> str:
        """Generate HTML for a specific feed source."""
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title} - {source_name}</title>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                    line-height: 1.6;
                    margin: 0;
                    padding: 20px;
                    background: #f5f5f5;
                }}
                .container {{
                    max-width: 800px;
                    margin: 0 auto;
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #333;
                    border-bottom: 2px solid #eee;
                    padding-bottom: 10px;
                    margin-bottom: 20px;
                }}
                .entry {{
                    margin-bottom: 20px;
                    padding-bottom: 20px;
                    border-bottom: 1px solid #eee;
                }}
                .entry:last-child {{
                    border-bottom: none;
                }}
                .entry h2 {{
                    margin: 0 0 10px 0;
                    color: #2c3e50;
                }}
                .entry h2 a {{
                    color: #2c3e50;
                    text-decoration: none;
                }}
                .entry h2 a:hover {{
                    color: #3498db;
                }}
                .entry .date {{
                    color: #7f8c8d;
                    font-size: 0.9em;
                    margin-bottom: 10px;
                }}
                .entry .content {{
                    color: #444;
                }}
                .entry .content img {{
                    max-width: 100%;
                    height: auto;
                    border-radius: 4px;
                    margin: 10px 0;
                }}
                .read-more {{
                    display: inline-block;
                    margin-top: 10px;
                    color: #3498db;
                    text-decoration: none;
                    font-weight: 500;
                }}
                .read-more:hover {{
                    text-decoration: underline;
                }}
                .back-link {{
                    display: inline-block;
                    margin-bottom: 20px;
                    color: #3498db;
                    text-decoration: none;
                }}
                .back-link:hover {{
                    text-decoration: underline;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <a href="index.html" class="back-link">← Back to Dashboard</a>
                <h1>{title} - {source_name}</h1>
        """
        
        for entry in entries:
            html += f"""
                <div class="entry">
                    <h2><a href="{entry.link}" target="_blank">{entry.title}</a></h2>
                    <div class="date">{entry.published.strftime('%B %d, %Y %I:%M %p')}</div>
                    <div class="content">{entry.content}</div>
                    <a href="{entry.link}" class="read-more" target="_blank">Read more →</a>
                </div>
            """
        
        html += """
            </div>
        </body>
        </html>
        """
        return html
    
    def _generate_index_html(self, weather_entries: List[FeedEntry], feed_links: List[tuple]) -> str:
        """Generate the main index.html file with weather and feed links."""
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>News Dashboard</title>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                    line-height: 1.6;
                    margin: 0;
                    padding: 20px;
                    background: #f5f5f5;
                }}
                .container {{
                    max-width: 800px;
                    margin: 0 auto;
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #333;
                    border-bottom: 2px solid #eee;
                    padding-bottom: 10px;
                    margin-bottom: 20px;
                }}
                .weather-section {{
                    margin-bottom: 30px;
                    padding: 20px;
                    background: #f8f9fa;
                    border-radius: 8px;
                }}
                .weather-section h2 {{
                    color: #2c3e50;
                    margin-top: 0;
                }}
                .feed-links {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                    margin-top: 30px;
                }}
                .feed-link {{
                    padding: 15px;
                    background: #f8f9fa;
                    border-radius: 8px;
                    text-decoration: none;
                    color: #2c3e50;
                    transition: all 0.3s ease;
                }}
                .feed-link:hover {{
                    background: #e9ecef;
                    transform: translateY(-2px);
                }}
                .feed-link h3 {{
                    margin: 0 0 10px 0;
                    color: #2c3e50;
                }}
                .feed-link p {{
                    margin: 0;
                    color: #6c757d;
                    font-size: 0.9em;
                }}
                .timestamp {{
                    text-align: center;
                    color: #6c757d;
                    font-size: 0.9em;
                    margin-top: 30px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>News Dashboard</h1>
        """
        
        # Add weather section if entries exist
        if weather_entries:
            html += """
                <div class="weather-section">
                    <h2>Weather</h2>
            """
            for entry in weather_entries:
                html += f"""
                    <div class="entry">
                        <h3>{entry.title}</h3>
                        <div class="content">{entry.content}</div>
                    </div>
                """
            html += "</div>"
        
        # Add feed links section
        html += """
                <h2>News Sources</h2>
                <div class="feed-links">
        """
        for name, filename in feed_links:
            html += f"""
                    <a href="{filename}" class="feed-link">
                        <h3>{name}</h3>
                        <p>View latest news from {name}</p>
                    </a>
            """
        html += "</div>"
        
        # Add timestamp
        html += f"""
                <div class="timestamp">
                    Last updated: {datetime.now().strftime('%B %d, %Y %I:%M %p')}
                </div>
            </div>
        </body>
        </html>
        """
        return html
    
    def save_html(self, entries: List[FeedEntry], title: str, weather_entries: List[FeedEntry] = None) -> str:
        """
        Save HTML files for each feed source and an index page.
        
        Args:
            entries (List[FeedEntry]): List of feed entries
            title (str): Title for the dashboard
            weather_entries (List[FeedEntry], optional): Weather entries for the index page
            
        Returns:
            str: Path to the index.html file
        """
        # Group entries by source
        entries_by_source = {}
        for entry in entries:
            if entry.source not in entries_by_source:
                entries_by_source[entry.source] = []
            entries_by_source[entry.source].append(entry)
        
        # Generate HTML files for each source
        feed_links = []
        for source, source_entries in entries_by_source.items():
            # Create a filename from the source name
            filename = f"{source.lower().replace(' ', '_')}.html"
            feed_links.append((source, filename))
            
            # Generate and save the HTML file
            html_content = self._generate_feed_html(source_entries, title, source)
            file_path = os.path.join(self.output_dir, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
        
        # Generate and save the index.html file
        index_html = self._generate_index_html(weather_entries or [], feed_links)
        index_path = os.path.join(self.output_dir, 'index.html')
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_html)
        
        return index_path 