# url2rss

url2rss is a lightweight Python library that converts any public web page (news pages, search results, listings) into a valid RSS XML feed.

It automatically handles both static HTML and JavaScript-rendered pages, making it easy to generate RSS feeds from sites that don’t provide one.

---

## Installation
```sh
pip install url2rss
```

---

## Basic Usage
```py
from url2rss import url_to_rss

rss_xml = url_to_rss("https://www.aljazeera.com/search/cricket")
print(rss_xml)
```
The function returns a ready-to-use RSS XML string.

---

## Save RSS to a File
```py
from url2rss import url_to_rss

rss_xml = url_to_rss("https://globalnews.ca/?s=cricket")

with open("feed.xml", "w", encoding="utf-8") as f:
    f.write(rss_xml)

```

---