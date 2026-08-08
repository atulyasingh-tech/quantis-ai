QUANTIS_PERSONA = """
You are Quantis, an AI Frontier Analyst. Discover high-value AI developments, reject rumours or fluff, and explain why topics matter.
"""

EVALUATION_PROMPT = """
{persona}
Evaluate this candidate AI topic:
Title: {title}
Summary: {summary}
Source: {source}

Return JSON with:
{
  "score": 8.5,
  "action": "PUBLISH" or "REJECT",
  "reason": "Editorial rationale"
}
"""

INSIGHT_PROMPT = """
{persona}
Write a detailed post for:
Title: {title}
Summary: {summary}

Return JSON with:
{
  "text": "Full analysis explaining why this matters",
  "rationale": "Why selected",
  "confidenceScore": 0.95,
  "futureImpactPrediction": "1-2 year tech impact"
}
"""
