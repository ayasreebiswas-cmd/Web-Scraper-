# Product Web Scraper & Dashboard

A Flask-based web application paired with a BeautifulSoup product scraper that allows users to extract product metadata (titles, prices, stock availability, star ratings, and product URLs) from target catalog pages and export results to CSV or JSON formats[cite: 5, 7, 8].

---

## 📌 Table of Contents
- [Project Overview](#-project-overview)
- [Key Features](#-key-features)
- [Technologies Used](#-technologies-used)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [Usage Instructions](#-usage-instructions)
- [API Reference](#-api-reference)
- [Submission & Links](#-submission--links)

---

## 📖 Project Overview
Developed as part of the project submission guidelines for **Synent**, this application provides an interactive web dashboard to control scraping parameters and preview extracted data in real time. 

The application targets product catalog layouts (defaulting to `https://books.toscrape.com/`), extracts key parameters using CSS selection[cite: 7], persists results into local JSON and CSV cache files, and presents data via a modern web user interface[cite: 8, 9].

---

## ✨ Key Features
- **Dynamic Web Scraping**: Fetches product title, price, stock status, star rating, and direct product link[cite: 7].
- **Interactive UI**: Dark-themed dashboard built with HTML5, standard CSS variables, and JavaScript[cite: 8, 9].
- **Configurable Limits**: Set scraping limits directly from the UI (1 to 100 items, defaults to 20).
- **Data Persistence**: Automatically writes scraped outputs to local cache files (`data/scraped_data.json` and `data/scraped_data.csv`).
- **Direct Data Export**: Download cached data directly as `.csv` or `.json` files via frontend buttons[cite: 5, 8].
- **RESTful Endpoints**: Features a POST route `/api/scrape` for programmatic scraping and retrieval[cite: 5].

---

## 🛠️ Technologies Used
- **Backend Framework**: Flask 3.0+[cite: 5, 6]
- **Web Scraping**: Requests 2.31+, BeautifulSoup4 4.12+[cite: 6, 7]
- **Frontend Stack**: Jinja2 Templates, HTML5, Vanilla JavaScript, CSS3 (Glassmorphism layout)[cite: 8, 9]
- **Data Serialization**: `csv`, `json`[cite: 5]

---

## 📂 Project Structure
```text
.
├── app.py                   # Main Flask server & route handlers
├── scraper.py               # Scraping logic and BeautifulSoup parser
├── requirements.txt         # Project dependencies
├── static/
│   ├── css/
│   │   └── style.css        # UI styling & layout
│   └── js/
│       └── main.js          # Client-side JavaScript logic
└── templates/
    └── dashboard.html       # Jinja2 HTML dashboard template
```

---

## ⚙️ Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone [https://github.com/your-username/web-scraper.git](https://github.com/your-username/web-scraper.git)
   cd web-scraper
