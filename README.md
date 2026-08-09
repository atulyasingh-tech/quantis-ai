# ⚡ Quantis AI — Autonomous Frontier Technology Analyst

> **Live Application:** [quantis-ai-teal.vercel.app](https://quantis-ai-teal.vercel.app/)  
> **Interactive API Reference:** [quantis-ai-teal.vercel.app/docs](https://quantis-ai-teal.vercel.app/docs)

Quantis AI is an autonomous, serverless technology research agent and real-time news discovery engine. It continuously monitors high-signal RSS research feeds, evaluates tech signals using Google Gemini, generates strategic impact predictions, and publishes deduplicated insights with full source attribution.

---

## 🌟 Key Features

- **Autonomous News Discovery:** Scans curated RSS feeds across AI research, systems architecture, cloud infrastructure, and frontier hardware.
- **LLM-Powered Technical Evaluation:** Leverages Google Gemini to evaluate incoming news items against strict editorial criteria, filtering out PR marketing hype.
- **Interactive Reader Modal:** Click any published insight to view detailed analytical rationales, confidence scores, and direct links to original publisher sources.
- **Serverless Glassmorphism Dashboard:** Production-ready UI with animated skeleton loaders, real-time activity timelines, and toast notifications.
- **OpenAPI / Swagger Integration:** Fully documented FastAPI endpoints with interactive testing specs at `/docs`.

---

## 🛠️ Tech Stack

- **Backend Framework:** FastAPI (Python 3.11)
- **Intelligence Engine:** Google Gemini API (`google-genai`)
- **Data Persistence:** SQLAlchemy + `aiosqlite` (Async SQLite)
- **Feed Ingestion:** `httpx` + XML ElementTree (Cache-Busted Async Ingestion)
- **Dynamic Media:** Pollinations AI (On-the-fly topic image synthesis)
- **Deployment:** Vercel Serverless Functions (`@vercel/python`)

---

## 🚀 API Architecture & Endpoints

Quantis AI exposes a RESTful API structure for autonomous orchestration:

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/agent/init` | Triggers the autonomous discovery pass, parses RSS feeds, and persists evaluated posts. |
| `GET` | `/api/agent/feed` | Fetches all published frontier insights ordered by creation timestamp. |
| `GET` | `/docs` | Interactive Swagger UI documentation for live API testing. |

---

## 💻 Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/atulyasingh-tech/quantis-ai.git](https://github.com/atulyasingh-tech/quantis-ai.git)
   cd quantis-ai

---

## 🔬 Proof of Agentic Development & LLM Orchestration

In compliance with hackathon verification guidelines for autonomous AI agents and prompt/byte-coded generation:

- **AI Collaboration & Development Chat Log:** [View Full Gemini Development & Architectural Chat Log](https://share.gemini.google/E5APfTe2MF7w)
- **Framework Integration:** Developed using patterns adapted from the **Google Antigravity SDK** (`agent_config.py`), utilizing structured Pydantic schema constraints (`QuantisPublishDecision`) and deterministic JSON output validation.
- **Autonomous Execution Loop:** The core discovery pass operates asynchronously via `agents/core_agent.py`, executing live web feed parsing, deduplication hashing, and real-time LLM signal evaluation without hardcoded static responses.

---

## 📄 License

This project is licensed under the **MIT License**.

```text
MIT License

Copyright (c) 2026 Atulya Kumar Singh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.  
   

   
