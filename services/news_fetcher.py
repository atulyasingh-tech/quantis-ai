import httpx
import xml.etree.ElementTree as ET
from typing import List, Dict

RSS_FEEDS = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://news.ycombinator.com/rss",
    "https://rss.arxiv.org/rss/cs.AI"
]

async def fetch_latest_news() -> List[Dict[str, str]]:
    results = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    async with httpx.AsyncClient(timeout=6.0, follow_redirects=True, headers=headers) as client:
        for feed in RSS_FEEDS:
            try:
                resp = await client.get(feed)
                if resp.status_code == 200:
                    root = ET.fromstring(resp.text)
                    for item in root.findall(".//item")[:3]:
                        title = item.findtext("title") or ""
                        link = item.findtext("link") or ""
                        desc = item.findtext("description") or ""
                        
                        # Clean basic HTML tags from description if present
                        if "<" in desc and ">" in desc:
                            import re
                            desc = re.sub('<[^<]+?>', '', desc)
                            
                        if title:
                            results.append({
                                "title": title.strip(),
                                "link": link.strip(),
                                "summary": desc.strip()
                            })
            except Exception:
                continue
                
    return results
