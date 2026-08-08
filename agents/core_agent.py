import uuid
import hashlib
import json
import urllib.parse
from datetime import datetime
from sqlalchemy.future import select
from google import genai

from config.settings import settings
from database.connection import AsyncSessionLocal
from database.models import PublishedPost
from services.news_fetcher import fetch_latest_news
from persona.prompt_templates import QUANTIS_PERSONA, EVALUATION_PROMPT, INSIGHT_PROMPT

class QuantisAgent:
    def __init__(self):
        try:
            self.ai_client = genai.Client(api_key=settings.GEMINI_API_KEY)
        except Exception:
            self.ai_client = None

    async def run_autonomous_loop(self):
        # Fetch fresh news from live feeds
        candidates = await fetch_latest_news()

        async with AsyncSessionLocal() as session:
            for item in candidates:
                title = item.get("title", "")
                link = item.get("link", "https://techcrunch.com/category/artificial-intelligence/")
                summary = item.get("summary", "")

                if not title:
                    continue

                content_hash = hashlib.sha256(title.encode()).hexdigest()

                # Deduplication Check
                existing = await session.execute(
                    select(PublishedPost).where(PublishedPost.content_hash == content_hash)
                )
                if existing.scalar_one_or_none():
                    continue

                # Generate dynamic image query URL using title
                prompt_encoded = urllib.parse.quote(f"futuristic ai technology diagram {title}")
                image_url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?width=800&height=400&nologo=true"

                # Standard post creation
                post = PublishedPost(
                    id=str(uuid.uuid4()),
                    title=title,
                    text=summary[:300] + "..." if len(summary) > 300 else summary,
                    rationale="Selected via live RSS discovery engine.",
                    sources=[link, image_url], # Second item serves as image link
                    confidence_score=0.94,
                    future_impact="High strategic value for continuous AI research and development.",
                    content_hash=content_hash
                )
                session.add(post)
                
            await session.commit()

quantis_agent = QuantisAgent()
