# News Dashboard Generator

A Python application that aggregates news from various sources (RSS feeds and NewsAPI), weather information, and generates a beautiful HTML dashboard.

## Features

- Aggregates news from multiple sources:
  - RSS feeds (Autosport F1, EDM News, WRC)
  - NewsAPI (US News)
  - OpenWeather API (Weather forecast)
- Generates a clean, responsive HTML dashboard
- Customizable news sources
- Configurable output directory (perfect for web servers)
- Automatic content cleaning and formatting
- Error handling and fallbacks for missing data
- Category-based organization with customizable ordering

## Requirements

- Python 3.8+
- NewsAPI key (for US News)
- OpenWeather API key (for weather forecast)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/news-dashboard.git
cd news-dashboard
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your configuration:
```
NEWS_API=your_newsapi_key_here
WEATHER_API=your_openweather_api_key_here
OUTPUT_DIR=/path/to/output/directory  # Optional: defaults to Desktop
```

## Usage

### Basic Usage

Run the script:
```bash
python main.py
```

The script will:
1. Fetch news from all configured sources
2. Get the current weather and forecast
3. Generate an HTML file named `News_YYYY-MM-DD.html`

### Custom Output Directory

You can specify where the HTML file should be generated in two ways:

1. Environment variable in `.env`:
```
OUTPUT_DIR=/var/www/html  # Example for Apache web server
```

2. Programmatically when creating the HTMLGenerator:
```python
generator = HTMLGenerator(output_dir="/var/www/html")
generator.save_html(
    entries=entries,
    title="Daily News Dashboard",
    filename="index.html"  # Optional: custom filename
)
```

### Web Server Integration

To use with a web server:

1. Set the output directory to your web server's document root:
```
OUTPUT_DIR=/var/www/html  # Apache example
OUTPUT_DIR=/usr/share/nginx/html  # Nginx example
```

2. Optionally set a fixed filename like `index.html`:
```python
generator.save_html(entries=entries, title="News Dashboard", filename="index.html")
```

3. Set up a cron job to update the news regularly:
```bash
0 * * * * cd /path/to/news-dashboard && .venv/bin/python main.py  # Updates every hour
```

## Adding News Sources

To add new news sources, modify the `news_sources` list in `main.py`:

```python
news_sources = [
    # RSS feeds (no API key needed)
    ("https://example.com/feed.rss", "Example News"),
    # NewsAPI endpoints (requires API key)
    ("https://newsapi.org/v2/everything?q=tech", "Tech News"),
]
```

## Project Structure

- `main.py`: Entry point and configuration
- `feed_parser.py`: Base classes for parsers
- `unified_parser.py`: Combined RSS and NewsAPI parser
- `weather_parser.py`: OpenWeather API parser
- `html_generator.py`: HTML dashboard generator

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 