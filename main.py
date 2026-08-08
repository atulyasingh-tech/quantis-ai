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
        
        body { 
            /* High-tech HUD background setup */
            background: #020617 url('https://raw.githubusercontent.com/atulyasingh-tech/quantis-ai/main/quantisbg.jpeg') no-repeat center center fixed;
            background-size: cover;
            color: #f1f5f9; 
            min-height: 100vh; 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            padding: 40px 20px; 
        }

        .hero { text-align: center; margin-bottom: 25px; max-width: 700px; }
        .hero h1 { 
            font-size: 2.8rem; 
            font-weight: 800; 
            background: linear-gradient(90deg, #00f2fe, #4facfe); 
            -webkit-background-clip: text; 
            -webkit-text-fill-color: transparent; 
            text-shadow: 0 0 20px rgba(0, 242, 254, 0.4);
            margin-bottom: 6px; 
            letter-spacing: 1px;
        }
        .hero p { color: #38bdf8; font-size: 0.95rem; font-weight: 500; letter-spacing: 0.5px; }

        .controls { display: flex; gap: 14px; margin-bottom: 20px; }
        button { 
            background: rgba(14, 165, 233, 0.2); 
            color: #38bdf8; 
            border: 1px solid #0284c7; 
            padding: 10px 22px; 
            border-radius: 6px; 
            font-weight: 600; 
            cursor: pointer; 
            transition: all 0.25s ease; 
            backdrop-filter: blur(8px);
            box-shadow: 0 0 10px rgba(2, 132, 199, 0.3);
        }
        button:hover { 
            background: rgba(14, 165, 233, 0.4); 
            border-color: #38bdf8;
            box-shadow: 0 0 15px rgba(56, 189, 248, 0.6);
            transform: translateY(-2px);
        }
        .btn-green { 
            background: rgba(16, 185, 129, 0.2); 
            color: #34d399; 
            border-color: #059669; 
            box-shadow: 0 0 10px rgba(5, 150, 105, 0.3);
        }
        .btn-green:hover { 
            background: rgba(16, 185, 129, 0.4); 
            border-color: #34d399;
            box-shadow: 0 0 15px rgba(52, 211, 153, 0.6);
        }

        .status-badge { 
            background: rgba(15, 23, 42, 0.6); 
            border: 1px solid rgba(56, 189, 248, 0.3); 
            padding: 6px 18px; 
            border-radius: 20px; 
            font-size: 0.8rem; 
            color: #38bdf8; 
            margin-bottom: 30px; 
            backdrop-filter: blur(10px);
            box-shadow: 0 0 10px rgba(56, 189, 248, 0.2);
        }

        .feed-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); 
            gap: 24px; 
            width: 100%; 
            max-width: 1100px; 
        }

        /* Sci-Fi Glassmorphism Card Style */
        .card { 
            background: rgba(10, 20, 40, 0.65); 
            border: 1px solid rgba(56, 189, 248, 0.25); 
            border-radius: 10px; 
            overflow: hidden; 
            display: flex; 
            flex-direction: column; 
            transition: all 0.3s ease; 
            backdrop-filter: blur(12px);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
        }
        .card:hover { 
            transform: translateY(-4px); 
            border-color: #38bdf8; 
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
        }
        .card-img { width: 100%; height: 180px; object-fit: cover; background: #020617; border-bottom: 1px solid rgba(56, 189, 248, 0.15); }
        .card-body { padding: 18px; display: flex; flex-direction: column; flex: 1; }
        .card-title { font-size: 1.1rem; font-weight: 700; color: #f8fafc; margin-bottom: 10px; line-height: 1.4; }
        .card-text { font-size: 0.88rem; color: #94a3b8; line-height: 1.6; flex: 1; }
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
        <div style="grid-column: 1/-1; text-align: center; color: #38bdf8; padding: 40px;">
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
                    feedGrid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; color: #94a3b8; padding: 40px;">No posts found. Trigger discovery loop above.</div>';
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
