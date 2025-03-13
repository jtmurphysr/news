# News Dashboard Generator

A Python-based news dashboard that aggregates content from various sources (RSS feeds, NewsAPI) and weather information into a clean, modern web interface.

## Features

- **Multiple News Sources**: Aggregates content from:
  - RSS feeds (Autosport F1, EDM News, WRC News)
  - NewsAPI (US News)
  - OpenWeather API (Weather information)
- **Clean, Modern Interface**: Responsive design with a clean, modern layout
- **Separate Pages**: Each news source has its own dedicated page
- **Weather Dashboard**: Main page includes weather information and links to all news sources
- **Easy Navigation**: Back-to-dashboard links on all pages
- **Automatic Updates**: Can be scheduled to run daily via cron job

## Prerequisites

- Python 3.8 or higher
- API keys for:
  - NewsAPI (https://newsapi.org)
  - OpenWeather API (https://openweathermap.org/api)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd news-dashboard
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with your API keys:
   ```
   NEWS_API=your_newsapi_key_here
   WEATHER_API=your_openweather_key_here
   OUTPUT_DIR=/path/to/output/directory  # Optional, defaults to Desktop
   ```

## Usage

1. Run the script:
   ```bash
   python main.py
   ```

2. The script will generate:
   - `index.html`: Main dashboard with weather and links to all news sources
   - `autosport_f1.html`: F1 news from Autosport
   - `edm_news.html`: EDM news
   - `wrc_news.html`: WRC news
   - `us_news.html`: US news from NewsAPI

## Setting Up Daily Updates (Ubuntu)

1. Create a shell script `update_news.sh`:
   ```bash
   #!/bin/bash
   cd "$(dirname "$0")"
   OUTPUT_DIR="/var/www/nodorks.net"  # Update this path
   YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)
   
   # Rename existing news.html if it exists
   if [ -f "$OUTPUT_DIR/news.html" ]; then
       mv "$OUTPUT_DIR/news.html" "$OUTPUT_DIR/news_$YESTERDAY.html"
   fi
   
   # Activate virtual environment and run the script
   source venv/bin/activate
   python main.py
   deactivate
   ```

2. Make the script executable:
   ```bash
   chmod +x update_news.sh
   ```

3. Set up the cron job:
   ```bash
   crontab -e
   ```
   Add the following line to run at 4 AM daily:
   ```
   0 4 * * * /full/path/to/update_news.sh >> /var/log/news_update.log 2>&1
   ```

4. Create and set permissions for the log file:
   ```bash
   sudo touch /var/log/news_update.log
   sudo chown your_username:your_username /var/log/news_update.log
   ```

## Project Structure

```
news-dashboard/
├── main.py              # Main script
├── feed_parser.py       # Feed entry data structure
├── unified_parser.py    # Unified parser for different feed types
├── weather_parser.py    # Weather API parser
├── html_generator.py    # HTML generation
├── requirements.txt     # Python dependencies
├── .env                # Environment variables (create this)
└── README.md           # This file
```

## Customization

### Adding New News Sources

To add a new RSS feed, update the `news_sources` list in `main.py`:

```python
news_sources = [
    ("https://example.com/feed", "Source Name"),
    # Add your new source here
]
```

### Modifying the Layout

The HTML templates and styles are defined in `html_generator.py`. You can modify the CSS and HTML structure to customize the appearance.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 