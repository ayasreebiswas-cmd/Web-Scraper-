import csv
import json
import logging
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file
from scraper import scrape_products

app = Flask(__name__)


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

JSON_CACHE = DATA_DIR / "scraped_data.json"
CSV_CACHE = DATA_DIR / "scraped_data.csv"

DEFAULT_URL = "https://books.toscrape.com/"


def write_cache_files(data):
    try:
        with open(JSON_CACHE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        with open(CSV_CACHE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["title", "price", "availability", "rating", "url"])
            writer.writeheader()
            writer.writerows(data)
    except IOError as err:
        app.logger.error(f"Error persisting cache files: {err}")


def read_cached_json():
    if not JSON_CACHE.exists():
        return []
    try:
        with open(JSON_CACHE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


@app.route("/")
def index():
    data = read_cached_json()
    return render_template("dashboard.html", data=data, default_url=DEFAULT_URL)


@app.route("/api/scrape", methods=["POST"])
def handle_scrape_request():
    body = request.get_json() or {}
    target_url = body.get("url", "").strip() or DEFAULT_URL

    try:
        limit = int(body.get("limit", 20))
        limit = max(1, min(limit, 100))
    except (ValueError, TypeError):
        limit = 20

    try:
        items = scrape_products(target_url, limit)
        write_cache_files(items)

        return jsonify({
            "status": "success",
            "count": len(items),
            "data": items,
            "source": target_url
        })
    except Exception as err:
        return jsonify({"status": "error", "message": str(err)}), 500


@app.route("/download/<fmt>")
def export_file(fmt):
    fmt = fmt.lower()
    if fmt not in ("csv", "json"):
        return "Unsupported format requested", 400

    target = CSV_CACHE if fmt == "csv" else JSON_CACHE

    if not target.exists():
        write_cache_files([])

    return send_file(
        target,
        as_attachment=True,
        download_name=f"scraped_data.{fmt}"
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)