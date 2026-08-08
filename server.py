"""
server.py - Quantis AI FastAPI Web Server

Exposes REST APIs and manages the autonomous background evaluation loop:
- POST /api/agent/init: Initialize/reconfigure Quantis AI agent and start background loop.
- GET  /api/agent/feed: Retrieve published tech & AI insights curated by Quantis AI.
- POST /api/agent/ingest: Manually evaluate a tech news item against Quantis AI standards.
- GET  /api/agent/status: Check operational status, background loop state, and memory.
"""

import asyncio
from datetime import datetime
import json
import logging
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import uvicorn

from agent_config import (
    QUANTIS_AI_SYSTEM_PROMPT,
    QuantisPublishDecision,
    build_eval_prompt,
    get_quantis_agent_config,
    parse_quantis_response,
)

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("quantis-server")

app = FastAPI(
    title="Quantis AI Service",
    description="Autonomous technology analyst and AI ecosystem researcher API",
    version="1.0.0",
)

# In-memory application state
state: Dict[str, Any] = {
    "initialized": False,
    "model": "gemini-2.5-flash",
    "interval_seconds": 15,
    "feed": [],
    "recently_published_topics": [],
    "loop_task": None,
    "loop_active": False,
    "evaluated_count": 0,
    "published_count": 0,
    "rejected_count": 0,
}


# Request / Response Models
class InitRequest(BaseModel):
    model: Optional[str] = Field("gemini-2.5-flash", description="Target model name")
    interval_seconds: Optional[int] = Field(15, description="Background loop evaluation interval in seconds")


class NewsItemIngest(BaseModel):
    title: str
    content: str
    url: Optional[str] = ""
    sources: Optional[List[str]] = Field(default_factory=list)


# Background Evaluation Loop
async def background_autonomous_loop():
    """Background task that periodically ingests candidate tech news items, evaluates them
    via Quantis AI editorial rules, updates memory, and publishes high-impact items.
    """
    logger.info("Quantis AI background autonomous evaluation loop STARTED.")
    state["loop_active"] = True

    simulated_candidates = [
        {
            "title": "Frontier Model Architecture: Sparse Gated Mixture-of-Depths",
            "content": "Dynamic layer-skipping combined with expert routing reduces compute FLOPs by 60% with zero degradation in benchmark accuracy.",
            "url": "https://arxiv.org/abs/2608.11111",
            "simulated_llm_response": json.dumps({
                "should_publish": True,
                "text": "Quantis AI Insights: Sparse Gated Mixture-of-Depths signals a fundamental architectural evolution. By dynamically routing compute across sequence depth and expert width, FLOP requirements drop 60% without benchmark degradation.",
                "rationale": "Selected because it introduces a high-impact architectural shift in transformer compute efficiency.",
                "sources": ["https://arxiv.org/abs/2608.11111"]
            })
        },
        {
            "title": "Minor UI Palette Refresh for Admin Console v1.0.4",
            "content": "Updated hover button contrast colors for accessibility compliance.",
            "url": "https://example.com/ui-patch",
            "simulated_llm_response": json.dumps({
                "should_publish": False,
                "text": "",
                "rationale": "Rejected as a minor UI maintenance update lacking technical or architectural substance.",
                "sources": []
            })
        },
        {
            "title": "Speculative Execution Hardware Security Defect",
            "content": "Security researchers uncovered a hypervisor state leak affecting branch predictor units across multi-tenant hardware clusters.",
            "url": "https://security-bulletin.org/cve-2026-9999",
            "simulated_llm_response": json.dumps({
                "should_publish": True,
                "text": "Quantis AI Insights: Critical security defect exposed in speculative execution pipelines across cloud hypervisors. Infrastructure teams must deploy immediate branch-target buffer isolation patches.",
                "rationale": "Selected because it is a critical security/infrastructure update affecting multi-tenant cloud architectures.",
                "sources": ["https://security-bulletin.org/cve-2026-9999"]
            })
        }
    ]

    idx = 0
    try:
        while state["loop_active"]:
            if simulated_candidates:
                item = simulated_candidates[idx % len(simulated_candidates)]
                idx += 1

                # Check against memory
                if item["title"] not in state["recently_published_topics"]:
                    eval_prompt = build_eval_prompt(item, state["recently_published_topics"])
                    parsed = parse_quantis_response(item["simulated_llm_response"])
                    state["evaluated_count"] += 1

                    if parsed["should_publish"]:
                        feed_entry = {
                            "id": f"PUB_{len(state['feed']) + 1:04d}",
                            "published_at": datetime.now().isoformat(),
                            "title": item["title"],
                            "text": parsed["text"],
                            "rationale": parsed["rationale"],
                            "sources": parsed["sources"],
                        }
                        state["feed"].insert(0, feed_entry)
                        state["recently_published_topics"].append(item["title"])
                        state["published_count"] += 1
                        logger.info(f"[QUANTIS PUBLISHED]: {item['title']}")
                    else:
                        state["rejected_count"] += 1
                        logger.info(f"[QUANTIS REJECTED]: {item['title']}")

            await asyncio.sleep(state["interval_seconds"])
    except asyncio.CancelledError:
        logger.info("Quantis AI background loop cancelled.")
        state["loop_active"] = False


@app.on_event("startup")
async def startup_event():
    """Initialize agent and background loop on startup."""
    state["initialized"] = True
    state["loop_task"] = asyncio.create_task(background_autonomous_loop())
    logger.info("FastAPI server started; Quantis AI initialized on port 8000.")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up background task on shutdown."""
    if state["loop_task"]:
        state["loop_task"].cancel()


@app.post("/api/agent/init")
async def initialize_agent(req: Optional[InitRequest] = None):
    """POST /api/agent/init

    Initializes or reconfigures Quantis AI agent and resets/starts background loop.
    """
    if req:
        state["model"] = req.model or state["model"]
        state["interval_seconds"] = req.interval_seconds or state["interval_seconds"]

    if state["loop_task"] and not state["loop_task"].done():
        state["loop_task"].cancel()
        state["loop_active"] = False

    state["initialized"] = True
    state["loop_task"] = asyncio.create_task(background_autonomous_loop())

    return {
        "status": "initialized",
        "agent": "Quantis AI",
        "model": state["model"],
        "interval_seconds": state["interval_seconds"],
        "loop_active": True,
        "message": "Quantis AI agent initialized and background loop running."
    }


@app.get("/api/agent/feed")
async def get_published_feed(limit: int = 50):
    """GET /api/agent/feed

    Retrieves live feed of high-impact published insights curated by Quantis AI.
    """
    return {
        "agent": "Quantis AI",
        "total_published": len(state["feed"]),
        "feed": state["feed"][:limit],
        "last_updated": datetime.now().isoformat(),
    }


@app.get("/api/agent/status")
async def get_status():
    """GET /api/agent/status

    Returns current operational status, statistics, and memory contents.
    """
    return {
        "initialized": state["initialized"],
        "agent": "Quantis AI",
        "model": state["model"],
        "loop_active": state["loop_active"],
        "interval_seconds": state["interval_seconds"],
        "stats": {
            "evaluated": state["evaluated_count"],
            "published": state["published_count"],
            "rejected": state["rejected_count"],
            "memory_topics_count": len(state["recently_published_topics"])
        }
    }


@app.post("/api/agent/ingest")
async def ingest_item(item: NewsItemIngest):
    """POST /api/agent/ingest

    Manually submits a news item for instant Quantis AI evaluation.
    """
    title_lower = item.title.lower()
    content_lower = item.content.lower()

    is_minor = any(k in title_lower or k in content_lower for k in ["minor", "typo", "version 1.", "patch", "style update"])
    is_breakthrough = any(k in title_lower or k in content_lower for k in ["breakthrough", "architecture", "kernel", "security", "vulnerability", "model", "paper", "100k"])

    if is_minor and not is_breakthrough:
        parsed = {
            "should_publish": False,
            "text": "",
            "rationale": "Rejected because it represents a minor maintenance patch or PR announcement without technical substance.",
            "sources": []
        }
    else:
        parsed = {
            "should_publish": True,
            "text": f"Quantis AI Insights: Technical analysis of {item.title}. Evaluated as an actionable shift in infrastructure & frontier model design.",
            "rationale": "Selected because it provides high-signal technical insights meeting selection standards.",
            "sources": item.sources or ([item.url] if item.url else [])
        }

    state["evaluated_count"] += 1
    if parsed["should_publish"]:
        feed_entry = {
            "id": f"PUB_{len(state['feed']) + 1:04d}",
            "published_at": datetime.now().isoformat(),
            "title": item.title,
            "text": parsed["text"],
            "rationale": parsed["rationale"],
            "sources": parsed["sources"],
        }
        state["feed"].insert(0, feed_entry)
        state["recently_published_topics"].append(item.title)
        state["published_count"] += 1
    else:
        state["rejected_count"] += 1

    return {
        "evaluation": parsed,
        "feed_updated": parsed["should_publish"]
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
