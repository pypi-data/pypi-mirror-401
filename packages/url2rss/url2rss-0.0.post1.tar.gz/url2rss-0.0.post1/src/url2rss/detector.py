from urllib.parse import urlparse, parse_qs

def detect_page_type(url: str) -> str:
    parsed = urlparse(url)

    if any(x in parsed.path.lower() for x in ("rss", "feed", "atom")):
        return "RSS"

    qs = parse_qs(parsed.query)
    if any(k in qs for k in ("q", "s", "search", "query")):
        return "SEARCH"

    if any(x in parsed.path.lower() for x in ("news", "category", "topics", "search")):
        return "LISTING"

    return "UNKNOWN"
