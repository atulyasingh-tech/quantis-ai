"""
agent_config.py - Quantis AI Backend Agent Configuration (Upgraded Edition)

Configures backend agent logic for Quantis AI:
- System prompt, identity, editorial criteria, and voice.
- Structured response models (Pydantic).
- Expanded news feeds & fallback discovery sources.
- Integration helper functions for Google Antigravity SDK and standalone runtimes.
"""

import json
from typing import Any

try:
    from pydantic import BaseModel, Field  # type: ignore
except ImportError:
    class BaseModel:  # type: ignore[no-redef]
        pass

    def Field(*args: Any, **kwargs: Any) -> Any:  # type: ignore[no-redef]
        return None


# =====================================================================
# EXPANDED NEWS & DISCOVERY SOURCE DIRECTORY
# =====================================================================

QUANTIS_PRIMARY_FEEDS = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://news.ycombinator.com/rss",
    "https://rss.arxiv.org/rss/cs.AI",
    "https://www.mit.edu/news/topic/artificial-intelligence-rss.xml",
    "https://venturebeat.com/category/ai/feed/"
]


# =====================================================================
# SYSTEM PROMPT & EDITORIAL DIRECTIVES FOR QUANTIS AI
# =====================================================================

QUANTIS_AI_SYSTEM_PROMPT = """You are Quantis AI, an autonomous technology analyst and AI ecosystem researcher. You independently curate, evaluate, and publish high-impact tech and AI insights.

### IDENTITY & VOICE
- Name: Quantis AI
- Domain: AI Ecosystem, Frontier Models, Systems Architecture, Agentic Frameworks, & Tech Infrastructure
- Tone: Analytical, authoritative, concise, and forward-looking. Avoid hyperbole, buzzwords, and corporate fluff.
- Style: Crisp, insightful sentences with direct opinions backed by technical logic.

### CORE TASK & EDITORIAL JUDGMENT
You will receive a stream of recent technology and AI news items. Evaluate each item using rigorous technical judgment:

1. REJECTION CRITERIA (Reject if any apply):
   - Pure marketing/PR announcements with zero technical depth.
   - Duplicate topics recently covered in memory.
   - Spam or low-signal opinion pieces.

2. SELECTION CRITERIA (Publish if):
   - Discusses architectural shifts, model developments, benchmark results, agentic workflows, hardware efficiency, or software paradigms.
   - Provides an actionable technical takeaway or industry insight.

### MEMORY & CONTINUITY
- Review the provided list of `recently_published_topics`.
- Reject exact duplicate posts, but build upon related context to show analytical depth over time.

### OUTPUT DIRECTIVE
- Draft the post content in Quantis AI's voice (keep text between 40 to 120 words).
- Provide a clear rationale explaining the selection over generic news.
- Output MUST strictly conform to the JSON format below.

### REQUIRED OUTPUT FORMAT
Return ONLY a raw JSON object with no markdown wrappers or extra commentary:

{
  "should_publish": true,
  "text": "<The published post content written in Quantis AI's voice>",
  "rationale": "Selected because [technical reason]. Relevant now because [context].",
  "confidence_score": 0.95,
  "future_impact": "<Brief 1-sentence prediction on technical or industry impact>",
  "sources": ["<URL 1>", "<URL 2>"]
}"""


# =====================================================================
# PYDANTIC STRUCTURED OUTPUT SCHEMA
# =====================================================================

class QuantisPublishDecision(BaseModel):
    """Pydantic model representing the strict JSON output schema required for Quantis AI."""

    should_publish: bool = Field(
        True, description="Set to true if the news item passes selection criteria; false if rejected."
    )
    text: str = Field(
        "",
        description="The published post content written in Quantis AI's voice (under 120 words), or empty if rejected.",
    )
    rationale: str = Field(
        ...,
        description="Detailed technical reasoning for selection or rejection over lower-signal news.",
    )
    confidence_score: float = Field(
        0.95,
        description="Confidence score between 0.0 and 1.0 representing analysis validity.",
    )
    future_impact: str = Field(
        "",
        description="Short prediction on technical or enterprise impact.",
    )
    sources: list[str] = Field(
        default_factory=list,
        description="List of source URLs referenced for this insight.",
    )

    def to_json_dict(self) -> dict[str, Any]:
        """Convert decision model to dict matching output standard."""
        return {
            "should_publish": self.should_publish,
            "text": self.text,
            "rationale": self.rationale,
            "confidence_score": self.confidence_score,
            "future_impact": self.future_impact,
            "sources": self.sources,
        }


# =====================================================================
# AGENT CONFIGURATION & PROMPT BUILDERS
# =====================================================================

def build_eval_prompt(
    news_item: dict[str, Any],
    recently_published_topics: list[str] | None = None,
) -> str:
    """Formats an incoming technology news item and past memory context into an evaluation prompt."""
    memory_str = "None"
    if recently_published_topics:
        memory_str = "\n".join(f"- {topic}" for topic in recently_published_topics)

    news_title = news_item.get("title", "Untitled News Item")
    news_content = news_item.get("content") or news_item.get("summary", "")
    news_url = news_item.get("url") or news_item.get("link", "")
    news_sources = news_item.get("sources", [news_url] if news_url else [])

    prompt = f"""### MEMORY CONTEXT
recently_published_topics:
{memory_str}

### INCOMING NEWS ITEM FOR EVALUATION
Title: {news_title}
Content: {news_content}
Sources: {json.dumps(news_sources)}

Evaluate this news item according to Quantis AI's editorial criteria and return ONLY the specified JSON format.
"""
    return prompt


def get_quantis_agent_config(
    model_name: str = "gemini-1.5-flash",
    **kwargs: Any,
) -> Any:
    """Generates the agent configuration dictionary compatible with Google Antigravity SDK
    and general LLM orchestration frameworks."""
    config: dict[str, Any] = {
        "model": model_name,
        "system_instructions": QUANTIS_AI_SYSTEM_PROMPT,
        "response_schema": QuantisPublishDecision,
        "feeds": QUANTIS_PRIMARY_FEEDS,
    }

    try:
        from google.antigravity import LocalAgentConfig  # type: ignore
        from google.antigravity.types import CustomSystemInstructions  # type: ignore

        return LocalAgentConfig(
            model=model_name,
            system_instructions=CustomSystemInstructions(text=QUANTIS_AI_SYSTEM_PROMPT),
            response_schema=QuantisPublishDecision,
            **kwargs,
        )
    except ImportError:
        config.update(kwargs)
        return config


def parse_quantis_response(raw_output: str) -> dict[str, Any]:
    """Parses raw text response from model into structured JSON object conforming to Quantis AI format."""
    cleaned = raw_output.strip()
    cleaned = cleaned.removeprefix("```json").removeprefix("```")
    cleaned = cleaned.removesuffix("```").strip()

    try:
        data = json.loads(cleaned)
    except Exception:
        data = {}

    return {
        "should_publish": bool(data.get("should_publish", True)),
        "text": str(data.get("text", "")),
        "rationale": str(data.get("rationale", "Selected via autonomous discovery criteria.")),
        "confidence_score": float(data.get("confidence_score", 0.95)),
        "future_impact": str(data.get("future_impact", "High strategic relevance for frontier research.")),
        "sources": list(data.get("sources", [])),
    }
