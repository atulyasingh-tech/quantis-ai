"""agent_config.py - Quantis AI Backend Agent Configuration

This module configures the backend agent logic for Quantis AI:
- System prompt, identity, editorial criteria, and voice.
- Structured response models (Pydantic).
- Integration helper functions for Google Antigravity SDK and standalone runtimes.
"""

import json
from typing import Any

try:
    from pydantic import BaseModel, Field  # type: ignore
except ImportError:
    # Graceful fallback if pydantic is not present in environment
    class BaseModel:  # type: ignore[no-redef]
        pass

    def Field(*args: Any, **kwargs: Any) -> Any:  # type: ignore[no-redef]
        return None


# =====================================================================
# SYSTEM PROMPT & EDITORIAL DIRECTIVES FOR QUANTIS AI
# =====================================================================

QUANTIS_AI_SYSTEM_PROMPT = """You are Quantis AI, an autonomous technology analyst and AI ecosystem researcher. You independently curate, evaluate, and publish high-impact tech and AI insights.

### IDENTITY & VOICE
- Name: Quantis AI
- Domain: AI Ecosystem, Frontier Models, Systems Architecture, & Tech Infrastructure
- Tone: Analytical, authoritative, concise, and forward-looking. Avoid hyperbole, buzzwords, and corporate fluff.
- Style: Crisp, insightful sentences with direct opinions backed by technical logic.

### CORE TASK & EDITORIAL JUDGMENT
You will receive a stream of recent technology and AI news items. You MUST NOT publish every item. Apply strict editorial standards:

1. REJECTION CRITERIA (Reject if any apply):
   - Pure marketing/PR announcements without technical substance.
   - Minor version bumps or standard product maintenance updates.
   - Topics already covered recently in memory.
   - Generic hype or low-signal opinion pieces.

2. SELECTION CRITERIA (Publish ONLY if):
   - Represents a significant architectural shift, breakthrough benchmark, or critical security/infrastructure update.
   - Provides an original, actionable tech insight or paradigm shift.

### MEMORY & CONTINUITY
- Review the provided list of `recently_published_topics`.
- Reject any topic that repeats an existing post.
- If a new topic directly relates to past posts, build upon that knowledge to demonstrate continuity.

### CREDIT EFFICIENCY DIRECTIVE
- Perform your judgment and draft the post in a single response.
- Keep the final post text under 150 words to minimize token output.
- Ensure the output strictly conforms to the JSON format below.

### REQUIRED OUTPUT FORMAT
Return ONLY a raw JSON object with no markdown wrappers or extra commentary:

{
  "should_publish": true,
  "text": "<The published post content written in Quantis AI's voice>",
  "rationale": "Selected because [reason]. Relevant now because [context]. Chosen over lower-signal news.",
  "sources": ["<URL 1>", "<URL 2>"]
}"""


# =====================================================================
# PYDANTIC STRUCTURED OUTPUT SCHEMA
# =====================================================================

class QuantisPublishDecision(BaseModel):
    """Pydantic model representing the strict JSON output schema required for Quantis AI."""

    should_publish: bool = Field(
        ..., description="Set to true if the news item passes selection criteria; false if rejected."
    )
    text: str = Field(
        "",
        description="The published post content written in Quantis AI's voice (under 150 words), or empty if rejected.",
    )
    rationale: str = Field(
        ...,
        description="Detailed technical reasoning for selection or rejection over lower-signal news.",
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
            "sources": self.sources,
        }


# =====================================================================
# AGENT CONFIGURATION & PROMPT BUILDERS
# =====================================================================

def build_eval_prompt(
    news_item: dict[str, Any],
    recently_published_topics: list[str] | None = None,
) -> str:
    """Formats an incoming technology news item and past memory context into an evaluation prompt.

    Args:
        news_item: Dict containing news item details (title, summary/content, url, domain, etc.).
        recently_published_topics: List of recently published topic titles/summaries for memory continuity.

    Returns:
        Formatted prompt string.
    """
    memory_str = "None"
    if recently_published_topics:
        memory_str = "\n".join(f"- {topic}" for topic in recently_published_topics)

    news_title = news_item.get("title", "Untitled News Item")
    news_content = news_item.get("content") or news_item.get("summary", "")
    news_url = news_item.get("url", "")
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
    model_name: str = "gemini-2.5-flash",
    **kwargs: Any,
) -> Any:
    """Generates the agent configuration dictionary compatible with Google Antigravity SDK
    and general LLM orchestration frameworks.

    Args:
        model_name: The target model string.
        **kwargs: Additional parameters passed to agent config.

    Returns:
        Configuration dictionary or LocalAgentConfig object containing system instructions and response schema.
    """
    config: dict[str, Any] = {
        "model": model_name,
        "system_instructions": QUANTIS_AI_SYSTEM_PROMPT,
        "response_schema": QuantisPublishDecision,
    }

    # Attempt integration with Google Antigravity SDK if available
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
        # Return fallback configuration dictionary
        config.update(kwargs)
        return config


def parse_quantis_response(raw_output: str) -> dict[str, Any]:
    """Parses raw text response from model into structured JSON object conforming to Quantis AI format.

    Args:
        raw_output: Raw output string from LLM response.

    Returns:
        Parsed dict containing should_publish, text, rationale, and sources.
    """
    cleaned = raw_output.strip()
    cleaned = cleaned.removeprefix("```json").removeprefix("```")
    cleaned = cleaned.removesuffix("```").strip()

    data = json.loads(cleaned)
    # Validate against schema fields
    return {
        "should_publish": bool(data.get("should_publish", False)),
        "text": str(data.get("text", "")),
        "rationale": str(data.get("rationale", "")),
        "sources": list(data.get("sources", [])),
    }
