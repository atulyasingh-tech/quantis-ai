import httpx
import xml.etree.ElementTree as ET
from typing import List, Dict

RSS_FEEDS = [
    "https://news.ycombinator.com/rss",
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://rss.arxiv.org/rss/cs.AI",
    "https://www.mit.edu/news/topic/artificial-intelligence-rss.xml"
]

async def fetch_latest_news() -> List[Dict[str, str]]:
    results = []
    async with httpx.AsyncClient(timeout=8.0, follow_redirects=True) as client:
        for feed in RSS_FEEDS:
            try:
                resp = await client.get(feed)
                if resp.status_code == 200:
                    root = ET.fromstring(resp.text)
                    for item in root.findall(".//item")[:4]:
                        title = item.findtext("title") or ""
                        link = item.findtext("link") or ""
                        desc = item.findtext("description") or ""
                        if title:
                            results.append({"title": title, "link": link, "summary": desc})
            except Exception:
                continue
    return results
