import logging
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup


logger = logging.getLogger("scraper")
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

STAR_RATINGS = {
    "one": "1 ★",
    "two": "2 ★",
    "three": "3 ★",
    "four": "4 ★",
    "five": "5 ★",
}


def parse_star_rating(card_el):
    """Extract star rating class from BeautifulSoup tag element."""
    rating_tag = card_el.select_one(".star-rating")
    if not rating_tag:
        return "N/A"

    for class_name in rating_tag.get("class", []):
        key = class_name.lower()
        if key in STAR_RATINGS:
            return STAR_RATINGS[key]

    return "N/A"


def parse_product_card(card, base_url):
    """Helper to parse raw HTML card into structured item dict."""
  
    title_tag = card.select_one("h3 a, .product-title, .title")
    title = "N/A"
    if title_tag:
        title = title_tag.get("title") or title_tag.get_text(strip=True)


    price_tag = card.select_one(".price_color, .price, .product-price")
    price = price_tag.get_text(strip=True) if price_tag else "N/A"

  
    stock_tag = card.select_one(".availability, .stock, .in-stock")
    availability = stock_tag.get_text(strip=True) if stock_tag else "In Stock"

    rating = parse_star_rating(card)


    link_tag = card.select_one("a")
    href = link_tag.get("href", "") if link_tag else ""
    product_url = urljoin(base_url, href) if href else base_url

    return {
        "title": title,
        "price": price,
        "availability": availability,
        "rating": rating,
        "url": product_url
    }


def scrape_products(target_url, limit=20):
    logger.info(f"Fetching data from: {target_url} (Limit: {limit})")

    try:
        res = requests.get(target_url, headers=HEADERS, timeout=10)
        res.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch page: {e}")
        raise RuntimeError(f"Could not reach target URL: {e}")

    soup = BeautifulSoup(res.text, "html.parser")


    cards = soup.select("article.product_pod") or soup.select(".product, .product-card, article")

    results = []
    for card in cards[:limit]:
        item = parse_product_card(card, target_url)
        results.append(item)

    return results