#!/bin/bash

# Set the working directory to the script's location
cd "$(dirname "$0")"

# Set the output directory (same as in .env)
OUTPUT_DIR="/var/www/html"  # Adjust this to match your OUTPUT_DIR

# Get yesterday's date in YYYY-MM-DD format
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)

# If index.html exists, rename it with yesterday's date
if [ -f "${OUTPUT_DIR}/news.html" ]; then
    mv "${OUTPUT_DIR}/news.html" "${OUTPUT_DIR}/news_${YESTERDAY}.html"
fi

# Activate virtual environment and run the script
source .venv/bin/activate
python main.py

# Deactivate virtual environment
deactivate 
