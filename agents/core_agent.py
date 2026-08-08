import uuid
import hashlib
import json
from sqlalchemy.future import select
from google import genai

from config.settings import settings
from database.connection import AsyncSessionLocal
from database.models import PublishedPost, RejectedTopic
from services.news_fetcher import fetch_latest_news
from persona.prompt_templates import QUANTIS_PERSONA, EVALUATION_PROMPT, INSIGHT_PROMPT

class QuantisAgent:
    def __init__(self):
        self.ai_client = genai.Client(api_key=settings.GEMINI_API_KEY)

    async def run_autonomous_loop(self):
        candidates = await fetch_latest_news()

        async with AsyncSessionLocal() as session:
            for item in candidates:
                title, link, summary = item["title"], item["link"], item["summary"]
                content_hash = hashlib.sha256(title.encode()).hexdigest()

                # Deduplication check
                existing = await session.execute(select(PublishedPost).where(PublishedPost.content_hash == content_hash))
                if existing.scalar_one_or_none():
                    continue

                # Editorial Evaluation
                eval_req = EVALUATION_PROMPT.format(persona=QUANTIS_PERSONA, title=title, summary=summary, source=link)
                eval_res = self.ai_client.models.generate_content(model="gemini-2.5-flash", contents=eval_req)

                try:
                    eval_data = json.loads(eval_res.text.strip("```json\n").strip("```"))
                except Exception:
                    continue

                if eval_data.get("score", 0) < settings.MIN_EDITORIAL_SCORE:
                    session.add(RejectedTopic(topic_title=title, source_url=link, rejection_reason=eval_data.get("reason", "Low score"), score=eval_data.get("score", 0)))
                    await session.commit()
                    continue

                # Insight Generation
                insight_req = INSIGHT_PROMPT.format(persona=QUANTIS_PERSONA, title=title, summary=summary)
                insight_res = self.ai_client.models.generate_content(model="gemini-2.5-flash", contents=insight_req)
                post_data = json.loads(insight_res.text.strip("```json\n").strip("```"))

                # Persist to Database
                session.add(PublishedPost(
                    id=str(uuid.uuid4()),
                    title=title,
                    text=post_data["text"],
                    rationale=post_data["rationale"],
                    sources=[link],
                    confidence_score=post_data.get("confidenceScore", 0.9),
                    future_impact=post_data.get("futureImpactPrediction", ""),
                    content_hash=content_hash
                ))
                await session.commit()

quantis_agent = QuantisAgent()
