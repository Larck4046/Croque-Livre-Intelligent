# Catalogue Croque-Livre

A French-language book catalog management application built with Flask.

## Overview

This application allows users to:
- View available books in the collection
- Add new books manually or by scanning ISBN codes
- Borrow and return books
- Search the book collection

## Project Structure

```
├── main_script.py     # Flask server entry point
├── scanner.py         # ISBN scanning functionality (uses Google Books API and BookFinder)
├── data_base.py       # Data management for the book catalog
├── data_base.json     # JSON file storing book data
├── static/            # CSS and JavaScript files
│   ├── app.js
│   └── styles.css
└── templates/         # HTML templates
    └── index.html
```

## Tech Stack

- **Backend**: Python 3.12 with Flask
- **Frontend**: HTML, CSS, JavaScript
- **Data Storage**: JSON file (data_base.json)
- **External APIs**: Google Books API, BookFinder

## Running the Application

The Flask server runs on port 5000:
```bash
python main_script.py
```

## Dependencies

- Flask
- BeautifulSoup4 (for web scraping)
- Requests (for HTTP requests)
