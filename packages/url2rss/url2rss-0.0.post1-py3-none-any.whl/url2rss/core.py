import requests
from bs4 import BeautifulSoup
from .detector import detect_page_type
from .extractor import extract_items_from_html
from .browser import fetch_html_js
from .renderer import items_to_rss
import feedparser

def url_to_rss(url: str) -> str:
    page_type = detect_page_type(url)

    headers = {"User-Agent": "Mozilla/5.0"}

    # Native RSS → just return it
    if page_type == "RSS":
        feed = feedparser.parse(url)
        if not feed.entries:
            raise RuntimeError("Invalid RSS feed")
        items = [
            {"title": e.title, "link": e.link}
            for e in feed.entries
            if hasattr(e, "title") and hasattr(e, "link")
        ]
        return items_to_rss(url, items)

    # SEARCH or LISTING → try static HTML first
    if page_type in ("SEARCH", "LISTING"):
        resp = requests.get(url, headers=headers, timeout=20)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "lxml")
        items = extract_items_from_html(soup)

        if items:
            return items_to_rss(url, items)

    # UNKNOWN or failed HTML → JS rendering fallback
    html = fetch_html_js(url)
    soup = BeautifulSoup(html, "lxml")
    items = extract_items_from_html(soup)

    if not items:
        raise RuntimeError("Unable to extract items from URL")

    return items_to_rss(url, items)
