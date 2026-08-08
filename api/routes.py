from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from database.connection import AsyncSessionLocal
from database.models import PublishedPost
from scheduler.task_scheduler import start_scheduler
from agents.core_agent import quantis_agent

router = APIRouter(prefix="/api/agent")

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/init")
async def initialize_agent(background_tasks: BackgroundTasks):
    start_scheduler()
    
    # Run loop asynchronously in background to prevent request timeout
    background_tasks.add_task(quantis_agent.run_autonomous_loop)
    
    return {
        "status": "active",
        "message": "Quantis AI initialized successfully. Background task running.",
        "initializedAt": datetime.utcnow().isoformat()
    }

@router.get("/feed")
async def get_feed(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PublishedPost).order_by(PublishedPost.created_at.desc()))
    posts = result.scalars().all()
    
    return {
        "total": len(posts),
        "feed": [
            {
                "id": p.id,
                "createdAt": p.created_at.isoformat(),
                "title": p.title,
                "text": p.text,
                "rationale": p.rationale,
                "sources": p.sources,
                "confidenceScore": p.confidence_score,
                "futureImpactPrediction": p.future_impact
            } for p in posts
        ]
    }
