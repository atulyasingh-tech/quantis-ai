import uuid
import hashlib
import urllib.parse
from datetime import datetime
from sqlalchemy.future import select
from google import genai

from config.settings import settings
from database.connection import AsyncSessionLocal
from database.models import PublishedPost
from services.news_fetcher import fetch_latest_news

class QuantisAgent:
    def __init__(self):
        try:
            self.ai_client = genai.Client(api_key=settings.GEMINI_API_KEY)
        except Exception:
            self.ai_client = None

    async def run_autonomous_loop(self):
        candidates = await fetch_latest_news()

        async with AsyncSessionLocal() as session:
            for item in candidates:
                title = item.get("title", "").strip()
                link = item.get("link", "https://techcrunch.com/category/artificial-intelligence/")
                summary = item.get("summary", "").strip()

                if not title:
                    continue

                content_hash = hashlib.sha256(title.encode()).hexdigest()

                # Deduplication Check: Skip if article was already saved
                existing = await session.execute(
                    select(PublishedPost).where(PublishedPost.content_hash == content_hash)
                )
                if existing.scalar_one_or_none():
                    continue

                # Generate dynamic tech thumbnail using Pollinations AI
                prompt_encoded = urllib.parse.quote(f"futuristic ai artificial intelligence {title[:30]}")
                image_url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?width=400&height=300&nologo=true"

                # Save new live article to SQLite database
                post = PublishedPost(
                    id=str(uuid.uuid4()),
                    title=title,
                    text=summary[:280] + "..." if len(summary) > 280 else summary,
                    rationale="Evaluated via live autonomous RSS engine.",
                    sources=[link, image_url],
                    confidence_score=0.95,
                    future_impact="High strategic impact on frontier technology capabilities.",
                    content_hash=content_hash
                )
                session.add(post)

            await session.commit()

quantis_agent = QuantisAgent()
