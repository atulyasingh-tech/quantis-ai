"""
test_agent_config.py - Unit tests for Quantis AI agent configuration
"""

import json
import unittest

from agent_config import (
    QUANTIS_AI_SYSTEM_PROMPT,
    QuantisPublishDecision,
    build_eval_prompt,
    get_quantis_agent_config,
    parse_quantis_response,
)


class TestQuantisAgentConfig(unittest.TestCase):

    def test_system_prompt_contains_identity_and_criteria(self):
        """Verify that the system prompt incorporates identity, rejection/selection criteria, and required output format."""
        self.assertIn("Quantis AI", QUANTIS_AI_SYSTEM_PROMPT)
        self.assertIn("REJECTION CRITERIA", QUANTIS_AI_SYSTEM_PROMPT)
        self.assertIn("SELECTION CRITERIA", QUANTIS_AI_SYSTEM_PROMPT)
        self.assertIn("CREDIT EFFICIENCY DIRECTIVE", QUANTIS_AI_SYSTEM_PROMPT)
        self.assertIn("REQUIRED OUTPUT FORMAT", QUANTIS_AI_SYSTEM_PROMPT)
        self.assertIn("should_publish", QUANTIS_AI_SYSTEM_PROMPT)

    def test_build_eval_prompt_without_memory(self):
        """Verify build_eval_prompt formats prompt correctly when memory is empty."""
        news_item = {
            "title": "Quantum Chip Achieves 100k Qubit Fidelity Breakthrough",
            "content": "Researchers at Lab X developed a novel error correction topology.",
            "url": "https://tech-breakthroughs.org/quantum-chip",
        }
        prompt = build_eval_prompt(news_item)
        self.assertIn("Quantum Chip Achieves 100k Qubit Fidelity Breakthrough", prompt)
        self.assertIn("https://tech-breakthroughs.org/quantum-chip", prompt)
        self.assertIn("recently_published_topics:\nNone", prompt)

    def test_build_eval_prompt_with_memory(self):
        """Verify build_eval_prompt includes recently published topics for memory continuity."""
        news_item = {
            "title": "Minor v1.2 patch released for logging library",
            "content": "Fixed a minor typo in logging output string.",
            "url": "https://example.com/patch",
        }
        memory = [
            "Supercomputing clusters adopt liquid cooling standard",
            "Frontier model v3 architecture analysis",
        ]
        prompt = build_eval_prompt(news_item, memory)
        self.assertIn("Supercomputing clusters adopt liquid cooling standard", prompt)
        self.assertIn("Frontier model v3 architecture analysis", prompt)
        self.assertIn("Minor v1.2 patch released for logging library", prompt)

    def test_parse_quantis_response_json(self):
        """Verify parse_quantis_response correctly parses valid JSON and strips codeblocks."""
        raw_json_str = """```json
{
  "should_publish": true,
  "text": "Quantis AI Insights: Breakthrough in sparse attention mechanisms reduces inference latency by 45%.",
  "rationale": "Selected because it provides a significant architectural shift in model inference efficiency.",
  "sources": ["https://arxiv.org/abs/2608.12345"]
}
```"""
        result = parse_quantis_response(raw_json_str)
        self.assertTrue(result["should_publish"])
        self.assertIn("Quantis AI Insights", result["text"])
        self.assertIn("significant architectural shift", result["rationale"])
        self.assertEqual(result["sources"], ["https://arxiv.org/abs/2608.12345"])

    def test_get_quantis_agent_config(self):
        """Verify agent config object/dict contains system instructions and schema."""
        config = get_quantis_agent_config(model_name="gemini-2.5-flash")
        if isinstance(config, dict):
            self.assertEqual(config["model"], "gemini-2.5-flash")
            self.assertEqual(config["system_instructions"], QUANTIS_AI_SYSTEM_PROMPT)
            self.assertEqual(config["response_schema"], QuantisPublishDecision)
        else:
            # LocalAgentConfig object from Google Antigravity SDK
            self.assertEqual(config.model, "gemini-2.5-flash")
            self.assertEqual(config.response_schema, QuantisPublishDecision)


if __name__ == "__main__":
    unittest.main()
