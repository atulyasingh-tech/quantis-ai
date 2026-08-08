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
    <title>Quantis AI - Command Center</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
        
        body { 
            background-color: #050a14; 
            color: #e2e8f0; 
            display: flex; 
            height: 100vh; 
            overflow: hidden; 
        }

        /* Sidebar Styling */
        .sidebar { 
            width: 240px; 
            background: #080f1e; 
            border-right: 1px solid #1e293b; 
            display: flex; 
            flex-direction: column; 
            padding: 24px 16px; 
            justify-content: space-between; 
        }
        .logo-area { display: flex; align-items: center; gap: 12px; margin-bottom: 32px; }
        .logo-icon { width: 36px; height: 36px; background: #0284c7; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; color: white; box-shadow: 0 0 12px #38bdf8; }
        .logo-text { font-size: 1.2rem; font-weight: 800; letter-spacing: 1px; color: #f8fafc; }
        .logo-sub { font-size: 0.65rem; color: #38bdf8; letter-spacing: 1.5px; }

        .nav-menu { display: flex; flex-direction: column; gap: 8px; }
        .nav-item { display: flex; align-items: center; gap: 12px; padding: 10px 14px; border-radius: 8px; font-size: 0.9rem; color: #94a3b8; text-decoration: none; font-weight: 500; }
        .nav-item.active { background: #0284c7; color: white; box-shadow: 0 0 12px rgba(2, 132, 199, 0.4); }

        .status-card { background: #0c162d; border: 1px solid #1d2d50; border-radius: 10px; padding: 16px; }
        .status-title { font-size: 0.75rem; color: #94a3b8; letter-spacing: 1px; margin-bottom: 6px; }
        .status-value { font-size: 1.2rem; font-weight: bold; color: #4ade80; display: flex; align-items: center; gap: 8px; }
        .status-dot { width: 8px; height: 8px; background: #4ade80; border-radius: 50%; box-shadow: 0 0 8px #4ade80; }

        /* Main Workspace Styling */
        .main-content { flex: 1; padding: 24px; overflow-y: auto; display: flex; flex-direction: column; gap: 20px; }
        
        .header-bar { display: flex; justify-content: space-between; align-items: center; }
        .header-title { font-size: 1.4rem; font-weight: 700; color: #f8fafc; }
        .header-sub { color: #38bdf8; font-size: 0.9rem; margin-top: 4px; }
        .header-controls { display: flex; gap: 10px; align-items: center; }
        .btn-action { background: #0284c7; color: white; border: none; padding: 8px 16px; border-radius: 6px; font-weight: 600; cursor: pointer; }
        .btn-action:hover { background: #0369a1; }

        /* Top Metrics Row */
        .metrics-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; }
        .metric-card { background: #0c162d; border: 1px solid #1e293b; border-radius: 10px; padding: 14px; }
        .metric-label { font-size: 0.7rem; color: #64748b; font-weight: 700; letter-spacing: 0.5px; }
        .metric-val { font-size: 1.6rem; font-weight: 800; color: #f8fafc; margin-top: 4px; }

        /* Center Section: Feed & Activity split */
        .content-split { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; }

        /* Feed Cards */
        .feed-container { display: flex; flex-direction: column; gap: 14px; }
        .feed-card { background: #0c162d; border: 1px solid #1e293b; border-radius: 10px; padding: 16px; display: flex; gap: 16px; align-items: center; }
        .feed-card:hover { border-color: #0284c7; }
        .card-thumb { width: 100px; height: 80px; border-radius: 8px; object-fit: cover; background: #030712; }
        .card-info { flex: 1; }
        .card-h { font-size: 1rem; font-weight: 700; color: #f8fafc; margin-bottom: 6px; }
        .card-p { font-size: 0.85rem; color: #94a3b8; line-height: 1.4; }

        /* Live Timeline Panel */
        .timeline-card { background: #0c162d; border: 1px solid #1e293b; border-radius: 10px; padding: 18px; }
        .timeline-header { font-size: 0.85rem; font-weight: 700; color: #94a3b8; margin-bottom: 16px; letter-spacing: 0.5px; }
        .timeline-list { display: flex; flex-direction: column; gap: 12px; }
        .timeline-item { font-size: 0.82rem; color: #cbd5e1; display: flex; justify-content: space-between; }
        .time-tag { color: #38bdf8; font-weight: 600; }
    </style>
</head>
<body>

    <!-- Sidebar Navigation -->
    <div class="sidebar">
        <div>
            <div class="logo-area">
                <div class="logo-icon">Q</div>
                <div>
                    <div class="logo-text">QUANTIS</div>
                    <div class="logo-sub">AI FRONTIER ANALYST</div>
                </div>
            </div>
            <div class="nav-menu">
                <a class="nav-item active" href="#">Dashboard</a>
                <a class="nav-item" href="/docs" target="_blank">API Docs</a>
            </div>
        </div>

        <div class="status-card">
            <div class="status-title">AGENT STATUS</div>
            <div class="status-value"><div class="status-dot"></div> LIVE</div>
            <div style="font-size: 0.75rem; color: #64748b; margin-top: 4px;">Autonomous Mode</div>
        </div>
    </div>

    <!-- Main Content Area -->
    <div class="main-content">
        
        <div class="header-bar">
            <div>
                <div class="header-title">Quantis Command Center</div>
                <div class="header-sub" id="status-text">Quantis is actively analyzing the frontier</div>
            </div>
            <div class="header-controls">
                <button class="btn-action" onclick="initAgent()">1. Trigger Discovery</button>
                <button class="btn-action" style="background:#1e293b;" onclick="loadFeed()">2. Refresh Feed</button>
            </div>
        </div>

        <!-- Metric Stat Cards -->
        <div class="metrics-grid">
            <div class="metric-card"><div class="metric-label">TOPICS DISCOVERED</div><div class="metric-val">128</div></div>
            <div class="metric-card"><div class="metric-label">TOPICS EVALUATED</div><div class="metric-val">94</div></div>
            <div class="metric-card"><div class="metric-label">POSTS PUBLISHED</div><div class="metric-val" id="published-count">0</div></div>
            <div class="metric-card"><div class="metric-label">TOPICS REJECTED</div><div class="metric-val">86</div></div>
            <div class="metric-card"><div class="metric-label">MEMORY ENTRIES</div><div class="metric-val">312</div></div>
        </div>

        <!-- Content Grid Split -->
        <div class="content-split">
            
            <!-- Published Feed Column -->
            <div class="feed-container" id="feed">
                <div style="color: #64748b; text-align: center; padding: 40px;">Loading posts...</div>
            </div>

            <!-- Activity Log Column -->
            <div class="timeline-card">
                <div class="timeline-header">AGENT ACTIVITY</div>
                <div class="timeline-list">
                    <div class="timeline-item"><span class="time-tag">10:42 PM</span> Discovering new sources...</div>
                    <div class="timeline-item"><span class="time-tag">10:41 PM</span> Evaluating 12 new topics</div>
                    <div class="timeline-item"><span class="time-tag">10:39 PM</span> Rejected low-impact topics</div>
                    <div class="timeline-item"><span class="time-tag">10:38 PM</span> Published new posts</div>
                    <div class="timeline-item"><span class="time-tag">10:15 PM</span> Memory retention updated</div>
                </div>
            </div>

        </div>

    </div>

    <script>
        async function initAgent() {
            document.getElementById('status-text').innerText = "Scanning live sources...";
            try {
                const res = await fetch('/api/agent/init', { method: 'POST' });
                const data = await res.json();
                document.getElementById('status-text').innerText = data.message;
                setTimeout(loadFeed, 2000);
            } catch(e) {
                document.getElementById('status-text').innerText = "Error initializing agent.";
            }
        }

        async function loadFeed() {
            try {
                const res = await fetch('/api/agent/feed');
                const data = await res.json();
                const feedContainer = document.getElementById('feed');
                document.getElementById('published-count').innerText = data.total;

                if (data.feed.length === 0) {
                    feedContainer.innerHTML = '<div style="color:#64748b; text-align:center; padding:40px;">No posts yet. Click Trigger Discovery above.</div>';
                    return;
                }

                feedContainer.innerHTML = '';
                data.feed.forEach(post => {
                    const imgUrl = (post.sources && post.sources.length > 1) 
                        ? post.sources[1] 
                        : `https://image.pollinations.ai/prompt/ai%20technology%20research?width=400&height=300&nologo=true`;

                    const card = document.createElement('div');
                    card.className = 'feed-card';
                    card.innerHTML = `
                        <img class="card-thumb" src="${imgUrl}" alt="Thumbnail" onerror="this.src='https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=400'">
                        <div class="card-info">
                            <div class="card-h">${post.title || 'AI Frontier Analysis'}</div>
                            <div class="card-p">${post.text}</div>
                        </div>
                    `;
                    feedContainer.appendChild(card);
                });
            } catch(e) {
                document.getElementById('status-text').innerText = "Error loading feed.";
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
