import httpx
import xml.etree.ElementTree as ET
from typing import List, Dict

RSS_FEEDS = [
    "https://news.ycombinator.com/rss",
    "https://techcrunch.com/category/artificial-intelligence/feed/"
]

async def fetch_latest_news() -> List[Dict[str, str]]:
    results = []
    async with httpx.AsyncClient(timeout=10.0) as client:
        for feed in RSS_FEEDS:
            try:
                resp = await client.get(feed)
                if resp.status_code == 200:
                    root = ET.fromstring(resp.text)
                    for item in root.findall(".//item")[:5]:
                        results.append({
                            "title": item.findtext("title") or "",
                            "link": item.findtext("link") or "",
                            "summary": item.findtext("description") or ""
                        })
            except Exception:
                continue
    return results
