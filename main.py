import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from api.routes import router
from database.connection import init_db

app = FastAPI(title="Quantis AI - Autonomous Frontier Analyst")

@app.on_event("startup")
async def startup_event():
    await init_db()

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quantis AI - Autonomous Frontier Analyst</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
        body { background-color: #0b0f19; color: #f1f5f9; min-height: 100vh; display: flex; flex-direction: column; align-items: center; padding: 30px 20px; }
        .hero { text-align: center; margin-bottom: 30px; max-width: 700px; }
        .hero h1 { font-size: 2.5rem; font-weight: 800; background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 8px; }
        .hero p { color: #94a3b8; font-size: 1rem; }
        .controls { display: flex; gap: 12px; margin-bottom: 24px; }
        button { background: #2563eb; color: white; border: none; padding: 12px 24px; border-radius: 8px; font-weight: 600; cursor: pointer; transition: all 0.2s ease; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3); }
        button:hover { transform: translateY(-2px); background: #1d4ed8; }
        .btn-green { background: #10b981; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3); }
        .btn-green:hover { background: #059669; }
        .status-badge { background: #1e293b; border: 1px solid #334155; padding: 6px 16px; border-radius: 20px; font-size: 0.85rem; color: #38bdf8; margin-bottom: 24px; }
        .feed-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 24px; width: 100%; max-width: 1100px; }
        .card { background: #161e2e; border: 1px solid #243044; border-radius: 12px; overflow: hidden; display: flex; flex-direction: column; transition: transform 0.2s, border-color 0.2s; }
        .card:hover { transform: translateY(-4px); border-color: #38bdf8; }
        .card-img { width: 100%; height: 180px; object-fit: cover; background: #0f172a; }
        .card-body { padding: 20px; display: flex; flex-direction: column; flex: 1; }
        .card-title { font-size: 1.15rem; font-weight: 700; color: #f8fafc; margin-bottom: 10px; line-height: 1.4; }
        .card-text { font-size: 0.9rem; color: #cbd5e1; line-height: 1.6; flex: 1; }
    </style>
</head>
<body>
    <div class="hero">
        <h1>Quantis AI Agent</h1>
        <p>Autonomous AI Frontier Analyst • Real-time Research & Insights</p>
    </div>

    <div class="controls">
        <button class="btn-green" onclick="initAgent()">1. Trigger Discovery</button>
        <button onclick="loadFeed()">2. Refresh Feed</button>
    </div>

    <div class="status-badge" id="status">System Online & Ready</div>

    <div class="feed-grid" id="feed">
        <div style="grid-column: 1/-1; text-align: center; color: #64748b; padding: 40px;">
            Click 'Trigger Discovery' to initiate real-time autonomous analysis.
        </div>
    </div>

    <script>
        async function initAgent() {
            document.getElementById('status').innerText = "Scanning live RSS feeds & evaluating topics...";
            try {
                const res = await fetch('/api/agent/init', { method: 'POST' });
                const data = await res.json();
                document.getElementById('status').innerText = data.message;
                setTimeout(loadFeed, 3000);
            } catch(e) {
                document.getElementById('status').innerText = "Error initializing agent.";
            }
        }

        async function loadFeed() {
            document.getElementById('status').innerText = "Fetching latest feed...";
            try {
                const res = await fetch('/api/agent/feed');
                const data = await res.json();
                const feedGrid = document.getElementById('feed');
                
                if (data.feed.length === 0) {
                    feedGrid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; color: #64748b; padding: 40px;">No posts found. Trigger discovery loop above.</div>';
                    document.getElementById('status').innerText = "Feed empty.";
                    return;
                }

                feedGrid.innerHTML = '';
                data.feed.forEach(post => {
                    const imgUrl = (post.sources && post.sources.length > 1) 
                        ? post.sources[1] 
                        : `https://image.pollinations.ai/prompt/ai%20technology%20research?width=800&height=400&nologo=true`;

                    const card = document.createElement('div');
                    card.className = 'card';
                    card.innerHTML = `
                        <img class="card-img" src="${imgUrl}" alt="Post banner" onerror="this.src='https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800'">
                        <div class="card-body">
                            <div class="card-title">${post.title || 'Frontier AI Insight'}</div>
                            <div class="card-text">${post.text}</div>
                        </div>
                    `;
                    feedGrid.appendChild(card);
                });
                document.getElementById('status').innerText = `Loaded ${data.total} posts successfully.`;
            } catch(e) {
                document.getElementById('status').innerText = "Error loading feed.";
            }
        }

        loadFeed();
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def root():
    return DASHBOARD_HTML

app.include_router(router)
