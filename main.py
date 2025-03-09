#!/usr/bin/env python3
"""
News Dashboard Generator

This script aggregates news from various sources (RSS feeds, NewsAPI) and weather
information into a single, beautifully formatted HTML dashboard.

Environment Variables:
    NEWS_API: API key for NewsAPI
    WEATHER_API: API key for OpenWeather API
    OUTPUT_DIR: Optional directory for HTML output (defaults to Desktop)

The script will:
1. Load configuration from environment variables
2. Initialize parsers for each news source
3. Fetch and parse content from all sources
4. Generate an HTML dashboard
5. Save the dashboard to the specified location

Example:
    $ export NEWS_API=your_key_here
    $ export WEATHER_API=your_key_here
    $ export OUTPUT_DIR=/var/www/html
    $ python main.py
"""

import os
from typing import List
from dotenv import load_dotenv
from feed_parser import FeedEntry
from unified_parser import UnifiedNewsParser
from weather_parser import WeatherParser
from html_generator import HTMLGenerator

def main():
    """
    Main function that orchestrates the news dashboard generation.
    
    This function:
    1. Loads API keys from environment variables
    2. Configures news sources
    3. Initializes appropriate parsers
    4. Collects and sorts entries
    5. Generates the HTML dashboard
    
    The function handles missing API keys gracefully, skipping
    sources that require missing keys while still processing
    other sources.
    """
    # Load environment variables
    load_dotenv()
    news_api_key = os.getenv('NEWS_API')
    weather_api_key = os.getenv('WEATHER_API')
    
    # Get output directory from environment or use default (Desktop)
    output_dir = os.getenv('OUTPUT_DIR')
    
    if not news_api_key:
        print("Warning: NEWS_API key not found in environment variables")
    if not weather_api_key:
        print("Warning: WEATHER_API key not found in environment variables")
    
    # Initialize news sources
    news_sources = [
        # RSS feeds (no API key needed)
        ("https://www.autosport.com/rss/feed/f1", "Autosport F1"),
        ("https://edm.com/.rss/full/", "EDM News"),
        ("https://www.autosport.com/rss/feed/wrc", "WRC News"),
        # NewsAPI endpoints (requires API key)
        ("https://newsapi.org/v2/top-headlines", "US News"),
    ]
    
    # Initialize parsers
    parsers = []
    
    # Add news parsers
    for url, name in news_sources:
        # Only add NewsAPI parser if we have an API key
        if "newsapi.org" in url and not news_api_key:
            continue
        parsers.append(UnifiedNewsParser(
            url=url,
            name=name,
            api_key=news_api_key if "newsapi.org" in url else None
        ))
    
    # Add Weather parser if API key is available
    if weather_api_key:
        parsers.append(WeatherParser(weather_api_key))
    
    # Collect all entries
    all_entries: List[FeedEntry] = []
    for parser in parsers:
        try:
            entries = parser.parse()
            print(f"Parsed {len(entries)} entries from {parser.name}")
            all_entries.extend(entries)
        except Exception as e:
            print(f"Error parsing {parser.name}: {str(e)}")
    
    # Sort entries by date (newest first)
    all_entries.sort(key=lambda x: x.published, reverse=True)
    
    # Generate HTML
    generator = HTMLGenerator(output_dir=output_dir)
    output_file = generator.save_html(
        entries=all_entries,
        title="Daily News Dashboard",
        filename="index.html"  # Optional: use a specific filename
    )
    
    print(f"\nHTML file generated: {output_file}")

if __name__ == "__main__":
    main()