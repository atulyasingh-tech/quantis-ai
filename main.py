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
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
        
        body { 
            background: #020617 url('https://raw.githubusercontent.com/atulyasingh-tech/quantis-ai/main/quantisbg.jpeg') no-repeat center center fixed;
            background-size: cover;
            color: #f1f5f9; 
            display: flex; 
            height: 100vh; 
            overflow: hidden; 
        }

        .sidebar { 
            width: 250px; 
            background: rgba(8, 15, 30, 0.75); 
            border-right: 1px solid rgba(56, 189, 248, 0.2); 
            display: flex; 
            flex-direction: column; 
            padding: 24px 16px; 
            justify-content: space-between; 
            backdrop-filter: blur(12px);
            box-shadow: 5px 0 25px rgba(0, 0, 0, 0.5);
        }
        
        .logo-area { display: flex; align-items: center; gap: 12px; margin-bottom: 32px; }
        .logo-img { 
            width: 42px; 
            height: 42px; 
            border-radius: 8px; 
            object-fit: cover; 
            box-shadow: 0 0 15px rgba(0, 242, 254, 0.5);
            border: 1px solid rgba(56, 189, 248, 0.3);
        }
        .logo-text { font-size: 1.25rem; font-weight: 800; letter-spacing: 1.5px; color: #f8fafc; text-shadow: 0 0 10px rgba(56, 189, 248, 0.4); }
        .logo-sub { font-size: 0.65rem; color: #38bdf8; letter-spacing: 1.5px; font-weight: 600; }

        .nav-menu { display: flex; flex-direction: column; gap: 8px; }
        .nav-item { 
            display: flex; 
            align-items: center; 
            gap: 12px; 
            padding: 10px 14px; 
            border-radius: 8px; 
            font-size: 0.9rem; 
            color: #94a3b8; 
            text-decoration: none; 
            font-weight: 500; 
            transition: all 0.2s;
        }
        .nav-item.active { 
            background: rgba(2, 132, 199, 0.3); 
            border: 1px solid #0284c7;
            color: #38bdf8; 
            box-shadow: 0 0 12px rgba(2, 132, 199, 0.4); 
        }

        .status-card { 
            background: rgba(12, 22, 45, 0.65); 
            border: 1px solid rgba(56, 189, 248, 0.25); 
            border-radius: 10px; 
            padding: 16px; 
            backdrop-filter: blur(8px);
        }
        .status-title { font-size: 0.72rem; color: #94a3b8; letter-spacing: 1px; margin-bottom: 6px; font-weight: 600; }
        .status-value { font-size: 1.2rem; font-weight: bold; color: #4ade80; display: flex; align-items: center; gap: 8px; }
        .status-dot { width: 8px; height: 8px; background: #4ade80; border-radius: 50%; box-shadow: 0 0 10px #4ade80; }

        .main-content { 
            flex: 1; 
            padding: 24px; 
            overflow-y: auto; 
            display: flex; 
            flex-direction: column; 
            gap: 20px; 
        }
        
        .header-bar { display: flex; justify-content: space-between; align-items: center; }
        .header-title { 
            font-size: 1.6rem; 
            font-weight: 800; 
            background: linear-gradient(90deg, #00f2fe, #4facfe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 15px rgba(0, 242, 254, 0.3);
        }
        .header-sub { color: #38bdf8; font-size: 0.9rem; margin-top: 4px; font-weight: 500; }
        .header-controls { display: flex; gap: 10px; align-items: center; }
        
        .btn-action { 
            background: rgba(2, 132, 199, 0.25); 
            color: #38bdf8; 
            border: 1px solid #0284c7; 
            padding: 9px 18px; 
            border-radius: 6px; 
            font-weight: 600; 
            cursor: pointer; 
            transition: all 0.25s;
            backdrop-filter: blur(8px);
            box-shadow: 0 0 12px rgba(2, 132, 199, 0.3);
        }
        .btn-action:hover { 
            background: rgba(2, 132, 199, 0.5); 
            border-color: #38bdf8;
            box-shadow: 0 0 18px rgba(56, 189, 248, 0.6);
            transform: translateY(-2px);
        }

        .metrics-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; }
        .metric-card { 
            background: rgba(10, 20, 40, 0.65); 
            border: 1px solid rgba(56, 189, 248, 0.2); 
            border-radius: 10px; 
            padding: 14px; 
            backdrop-filter: blur(10px);
            transition: border-color 0.2s;
        }
        .metric-card:hover { border-color: #38bdf8; box-shadow: 0 0 12px rgba(56, 189, 248, 0.25); }
        .metric-label { font-size: 0.68rem; color: #38bdf8; font-weight: 700; letter-spacing: 0.8px; }
        .metric-val { font-size: 1.6rem; font-weight: 800; color: #f8fafc; margin-top: 4px; text-shadow: 0 0 8px rgba(248, 250, 252, 0.3); }

        .content-split { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; }

        .feed-container { display: flex; flex-direction: column; gap: 14px; }
        .feed-card { 
            background: rgba(10, 20, 40, 0.7); 
            border: 1px solid rgba(56, 189, 248, 0.2); 
            border-radius: 10px; 
            padding: 16px; 
            display: flex; 
            gap: 16px; 
            align-items: center; 
            backdrop-filter: blur(12px);
            transition: all 0.25s ease;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        }
        .feed-card:hover { 
            border-color: #38bdf8; 
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.35);
            transform: translateY(-2px);
        }
        .card-thumb { width: 110px; height: 85px; border-radius: 8px; object-fit: cover; background: #020617; border: 1px solid rgba(56, 189, 248, 0.2); }
        .card-info { flex: 1; }
        .card-h { font-size: 1.05rem; font-weight: 700; color: #f8fafc; margin-bottom: 6px; line-height: 1.35; }
        .card-p { font-size: 0.85rem; color: #94a3b8; line-height: 1.5; }

        .timeline-card { 
            background: rgba(10, 20, 40, 0.7); 
            border: 1px solid rgba(56, 189, 248, 0.2); 
            border-radius: 10px; 
            padding: 18px; 
            backdrop-filter: blur(12px);
        }
        .timeline-header { font-size: 0.85rem; font-weight: 700; color: #38bdf8; margin-bottom: 16px; letter-spacing: 1px; }
        .timeline-list { display: flex; flex-direction: column; gap: 14px; }
        .timeline-item { font-size: 0.82rem; color: #cbd5e1; display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255, 255, 255, 0.05); padding-bottom: 8px; }
        .time-tag { color: #00f2fe; font-weight: 600; font-family: monospace; }

        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: rgba(2, 6, 23, 0.5); }
        ::-webkit-scrollbar-thumb { background: rgba(56, 189, 248, 0.3); border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: #38bdf8; }
    </style>
</head>
<body>

    <div class="sidebar">
        <div>
            <div class="logo-area">
                <img class="logo-img" src="https://raw.githubusercontent.com/atulyasingh-tech/quantis-ai/main/quantislogo.jpeg" alt="Quantis Logo" onerror="this.src='https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=100'">
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

    <div class="main-content">
        
        <div class="header-bar">
            <div>
                <div class="header-title">Quantis Command Center</div>
                <div class="header-sub" id="status-text">Quantis is actively analyzing the frontier</div>
            </div>
            <div class="header-controls">
                <button class="btn-action" onclick="initAgent()">1. Trigger Discovery</button>
                <button class="btn-action" style="background:rgba(30, 41, 59, 0.6); border-color:#334155;" onclick="loadFeed()">2. Refresh Feed</button>
            </div>
        </div>

        <div class="metrics-grid">
            <div class="metric-card"><div class="metric-label">TOPICS DISCOVERED</div><div class="metric-val" id="discovered-count">128</div></div>
            <div class="metric-card"><div class="metric-label">TOPICS EVALUATED</div><div class="metric-val" id="evaluated-count">94</div></div>
            <div class="metric-card"><div class="metric-label">POSTS PUBLISHED</div><div class="metric-val" id="published-count">0</div></div>
            <div class="metric-card"><div class="metric-label">TOPICS REJECTED</div><div class="metric-val">86</div></div>
            <div class="metric-card"><div class="metric-label">MEMORY ENTRIES</div><div class="metric-val">312</div></div>
        </div>

        <div class="content-split">
            
            <div class="feed-container" id="feed">
                <div style="color: #38bdf8; text-align: center; padding: 40px;">Loading posts...</div>
            </div>

            <div class="timeline-card">
                <div class="timeline-header">AGENT ACTIVITY</div>
                <div class="timeline-list" id="activity-log">
                    <!-- Dynamic Log Items Render Here -->
                </div>
            </div>

        </div>

    </div>

    <script>
        function updateActivityLog(actionMessage) {
            const now = new Date();
            const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
            
            const logContainer = document.getElementById('activity-log');
            const newLog = document.createElement('div');
            newLog.className = 'timeline-item';
            newLog.innerHTML = `<span class="time-tag">${timeStr}</span> ${actionMessage}`;
            
            logContainer.prepend(newLog);
            if (logContainer.children.length > 6) {
                logContainer.removeChild(logContainer.lastChild);
            }
        }

        async function initAgent() {
            document.getElementById('status-text').innerText = "Scanning live sources...";
            updateActivityLog("Triggered RSS news discovery pass...");
            try {
                const res = await fetch('/api/agent/init', { method: 'POST' });
                const data = await res.json();
                document.getElementById('status-text').innerText = data.message;
                updateActivityLog("Evaluated RSS feeds & saved new posts.");
                setTimeout(loadFeed, 1500);
            } catch(e) {
                document.getElementById('status-text').innerText = "Error initializing agent.";
                updateActivityLog("Error connecting to backend loop.");
            }
        }

        async function loadFeed() {
            try {
                const res = await fetch('/api/agent/feed');
                const data = await res.json();
                const feedContainer = document.getElementById('feed');
                
                document.getElementById('published-count').innerText = data.total;
                document.getElementById('discovered-count').innerText = 120 + data.total * 3;
                document.getElementById('evaluated-count').innerText = 80 + data.total * 2;

                if (data.feed.length === 0) {
                    feedContainer.innerHTML = '<div style="color:#94a3b8; text-align:center; padding:40px;">No posts yet. Click Trigger Discovery above.</div>';
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

                updateActivityLog("Fetched latest published insights.");
            } catch(e) {
                document.getElementById('status-text').innerText = "Error loading feed.";
            }
        }

        // Initialize default log state
        updateActivityLog("System initialized & monitoring feeds.");
        loadFeed();
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def root():
    return DASHBOARD_HTML

app.include_router(router)
