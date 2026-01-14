from feedgen.feed import FeedGenerator
from datetime import datetime

def items_to_rss(url: str, items: list[dict]) -> str:
    fg = FeedGenerator()
    fg.title(f"Auto RSS for {url}")
    fg.link(href=url)
    fg.description("Auto-generated RSS feed")

    for item in items:
        fe = fg.add_entry()
        fe.title(item["title"])
        fe.link(href=item["link"])
        # fe.pubDate(datetime.utcnow())

    return fg.rss_str(pretty=True).decode()
