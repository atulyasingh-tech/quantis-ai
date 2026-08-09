from fastapi import APIRouter
from sqlalchemy.future import select
from datetime import datetime

from database.connection import AsyncSessionLocal, init_db
from database.models import PublishedPost
from agents.core_agent import quantis_agent

router = APIRouter(prefix="/api/agent")

@router.post("/init")
async def initialize_agent():
    # Ensure database schema exists in /tmp/
    await init_db()
    
    # Run autonomous loop to populate feed
    await quantis_agent.run_autonomous_loop()
    
    return {
        "status": "active",
        "message": "Quantis AI initialized successfully. Feed updated.",
        "initializedAt": datetime.utcnow().isoformat()
    }

@router.get("/feed")
async def get_feed():
    await init_db()
    
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(PublishedPost).order_by(PublishedPost.created_at.desc()))
        posts = result.scalars().all()
        
        return {
            "total": len(posts),
            "feed": [
                {
                    "id": p.id,
                    "createdAt": p.created_at.isoformat() if p.created_at else "",
                    "title": p.title,
                    "text": p.text,
                    "rationale": p.rationale,
                    "sources": p.sources,
                    "confidenceScore": p.confidence_score,
                    "futureImpactPrediction": p.future_impact
                } for p in posts
            ]
        }
