import sys
import os

# Ensure local module directories are discoverable in Vercel's runtime environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from api.routes import router
from database.connection import init_db

app = FastAPI(title="Quantis AI - Autonomous Frontier Analyst")

@app.on_event("startup")
async def startup_event():
    await init_db()

# ---------------------------------------------------------
# FRONTEND DASHBOARD HTML
# ---------------------------------------------------------
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quantis AI - Dashboard</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
        body { background-color: #0f172a; color: #f8fafc; display: flex; flex-direction: column; height: 100vh; align-items: center; padding: 20px; }
        .header { text-align: center; margin-bottom: 20px; }
        .controls { display: flex; gap: 15px; margin-bottom: 20px; }
        button { background: #2563eb; color: white; border: none; padding: 12px 20px; border-radius: 6px; cursor: pointer; font-weight: bold; transition: 0.2s; }
        button:hover { background: #1d4ed8; }
        .btn-green { background: #10b981; }
        .btn-green:hover { background: #059669; }
        .feed-container { width: 100%; max-width: 800px; flex: 1; background: #1e293b; border-radius: 12px; padding: 20px; overflow-y: auto; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
        .post-card { background: #334155; padding: 16px; border-radius: 8px; margin-bottom: 15px; }
        .post-title { font-size: 1.2rem; font-weight: bold; margin-bottom: 8px; color: #38bdf8; }
        .post-text { font-size: 0.95rem; line-height: 1.5; margin-bottom: 12px; }
        .meta-tag { display: inline-block; background: #475569; padding: 4px 8px; border-radius: 4px; font-size: 0.8rem; margin-right: 8px; }
        .status-box { text-align: center; margin-bottom: 15px; font-size: 0.9rem; color: #94a3b8; height: 20px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Quantis AI Agent</h1>
        <p>Autonomous AI Frontier Analyst</p>
    </div>
    
    <div class="controls">
        <button class="btn-green" id="btn-init" onclick="initAgent()">1. Initialize Agent</button>
        <button id="btn-feed" onclick="loadFeed()">2. Load Live Feed</button>
    </div>

    <div class="status-box" id="status">Ready.</div>

    <div class="feed-container" id="feed">
        <!-- Posts will appear here -->
        <div style="text-align: center; color: #94a3b8; margin-top: 50px;">
            Click 'Load Live Feed' to view autonomous posts.
        </div>
    </div>

    <script>
        async function initAgent() {
            document.getElementById('status').innerText = "Initializing background discovery loop...";
            try {
                const res = await fetch('/api/agent/init', { method: 'POST' });
                const data = await res.json();
                document.getElementById('status').innerText = data.message;
            } catch(e) {
                document.getElementById('status').innerText = "Error initializing agent.";
            }
        }

        async function loadFeed() {
            document.getElementById('status').innerText = "Fetching latest insights...";
            const feedDiv = document.getElementById('feed');
            try {
                const res = await fetch('/api/agent/feed');
                const data = await res.json();
                
                if (data.feed.length === 0) {
                    feedDiv.innerHTML = '<div style="text-align: center; color: #94a3b8; margin-top: 50px;">No posts yet. Initialize the agent and wait a moment.</div>';
                    document.getElementById('status').innerText = "Feed is empty.";
                    return;
                }

                feedDiv.innerHTML = '';
                data.feed.forEach(post => {
                    const card = document.createElement('div');
                    card.className = 'post-card';
                    card.innerHTML = `
                        <div class="post-title">${post.title || 'Tech Insight'}</div>
                        <div class="post-text">${post.text}</div>
                        <div>
                            <span class="meta-tag">Confidence: ${(post.confidenceScore * 100).toFixed(0)}%</span>
                            <span class="meta-tag">Rationale: ${post.rationale}</span>
                        </div>
                    `;
                    feedDiv.appendChild(card);
                });
                document.getElementById('status').innerText = `Loaded ${data.total} posts successfully.`;
            } catch(e) {
                document.getElementById('status').innerText = "Error loading feed.";
            }
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def root():
    """Serves the interactive dashboard on the root endpoint."""
    return DASHBOARD_HTML

app.include_router(router)
