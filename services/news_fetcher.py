import httpx
import xml.etree.ElementTree as ET
import html
import re

GLOBAL_FEEDS = [
    {"source": "TechCrunch AI", "url": "https://techcrunch.com/category/artificial-intelligence/feed/"},
    {"source": "VentureBeat AI", "url": "https://venturebeat.com/category/ai/feed/"},
    {"source": "Ars Technica Tech", "url": "https://feeds.arstechnica.com/arstechnica/technology-lab"},
    {"source": "ArXiv AI Research", "url": "https://export.arxiv.org/rss/cs.AI"},
    {"source": "The Verge AI", "url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"},
    {"source": "MIT Tech Review", "url": "https://www.technologyreview.com/feed/"}
]

def clean_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', '', text)
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

async def fetch_latest_news():
    articles = []
    
    async with httpx.AsyncClient(timeout=4.0, follow_redirects=True, headers={"User-Agent": "QuantisAI/1.0"}) as client:
        for feed in GLOBAL_FEEDS:
            try:
                res = await client.get(feed["url"])
                if res.status_code == 200:
                    root = ET.fromstring(res.content)
                    
                    # Handles standard RSS 2.0
                    items = root.findall('.//item')
                    # Handles Atom feeds
                    if not items:
                        items = root.findall('.//{http://www.w3.org/2005/Atom}entry')
                    
                    for item in items[:4]:
                        title = ""
                        link = ""
                        summary = ""
                        
                        # RSS
                        t_elem = item.find('title')
                        l_elem = item.find('link')
                        d_elem = item.find('description')
                        
                        # Atom fallback
                        if t_elem is None:
                            t_elem = item.find('{http://www.w3.org/2005/Atom}title')
                        if l_elem is None:
                            l_elem = item.find('{http://www.w3.org/2005/Atom}link')
                        if d_elem is None:
                            d_elem = item.find('{http://www.w3.org/2005/Atom}summary')

                        if t_elem is not None and t_elem.text:
                            title = clean_text(t_elem.text)
                        
                        if l_elem is not None:
                            link = l_elem.text or l_elem.attrib.get('href', '')
                        
                        if d_elem is not None and d_elem.text:
                            summary = clean_text(d_elem.text)
                        
                        if title and len(title) > 10:
                            articles.append({
                                "title": title,
                                "link": link or "https://techcrunch.com/",
                                "summary": summary if summary else f"Strategic technology coverage reported via {feed['source']}."
                            })
            except Exception:
                continue

    return articles
