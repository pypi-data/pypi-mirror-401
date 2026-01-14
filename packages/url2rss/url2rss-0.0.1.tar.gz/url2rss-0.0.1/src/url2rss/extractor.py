from bs4 import BeautifulSoup

def extract_items_from_html(soup: BeautifulSoup) -> list[dict]:
    items = []
    seen = set()

    for block in soup.find_all(["article", "li", "div"], recursive=True):
        a = block.find("a", href=True)
        if not a:
            continue

        link = a["href"]
        if not link.startswith("http") or link in seen:
            continue

        texts = [
            t.get_text(strip=True)
            for t in block.find_all(["h1", "h2", "h3", "h4", "span", "a"])
            if 10 <= len(t.get_text(strip=True)) <= 150
        ]

        if not texts:
            continue

        items.append({"title": texts[0], "link": link})
        seen.add(link)

    return items
