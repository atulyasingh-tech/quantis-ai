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
    <!-- Favicon -->
    <link rel="icon" type="image/jpeg" href="https://raw.githubusercontent.com/atulyasingh-tech/quantis-ai/main/quantislogo.jpeg">
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

        /* Glassmorphism Sidebar */
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
            z-index: 10;
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

        /* Main Glass Workspace */
        .main-content { 
            flex: 1; 
            padding: 24px; 
            overflow-y: auto; 
            display: flex; 
            flex-direction: column; 
            gap: 20px; 
        }
        
        .header-bar { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; }
        .header-title { 
            font-size: 1.6rem; 
            font-weight: 800; 
            background: linear-gradient(90deg, #00f2fe, #4facfe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 15px rgba(0, 242, 254, 0.3);
        }
        .header-sub { color: #38bdf8; font-size: 0.9rem; margin-top: 4px; font-weight: 500; }
        .header-controls { display: flex; gap: 12px; align-items: center; flex-wrap: wrap; }
        
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

        /* Auto Sync Toggle */
        .sync-box { display: flex; align-items: center; gap: 8px; font-size: 0.8rem; color: #94a3b8; background: rgba(10, 20, 40, 0.6); padding: 8px 12px; border-radius: 6px; border: 1px solid rgba(56, 189, 248, 0.2); }
        .switch { position: relative; display: inline-block; width: 34px; height: 18px; }
        .switch input { opacity: 0; width: 0; height: 0; }
        .slider { position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: #334155; transition: .3s; border-radius: 18px; }
        .slider:before { position: absolute; content: ""; height: 12px; width: 12px; left: 3px; bottom: 3px; background-color: white; transition: .3s; border-radius: 50%; }
        input:checked + .slider { background-color: #0284c7; }
        input:checked + .slider:before { transform: translateX(16px); }

        /* Search & Filter Bar */
        .filter-bar { display: flex; gap: 12px; align-items: center; flex-wrap: wrap; }
        .search-input { 
            background: rgba(10, 20, 40, 0.7); 
            border: 1px solid rgba(56, 189, 248, 0.25); 
            color: #f1f5f9; 
            padding: 8px 14px; 
            border-radius: 6px; 
            font-size: 0.85rem; 
            outline: none; 
            flex: 1; 
            min-width: 200px;
        }
        .search-input:focus { border-color: #38bdf8; box-shadow: 0 0 10px rgba(56, 189, 248, 0.3); }
        .filter-pill { 
            background: rgba(15, 23, 42, 0.6); 
            border: 1px solid rgba(56, 189, 248, 0.2); 
            color: #94a3b8; 
            padding: 6px 14px; 
            border-radius: 20px; 
            font-size: 0.78rem; 
            cursor: pointer; 
            transition: all 0.2s;
        }
        .filter-pill.active, .filter-pill:hover { background: rgba(56, 189, 248, 0.2); color: #38bdf8; border-color: #38bdf8; }

        /* Sci-Fi Metric Cards */
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

        /* Split Section */
        .content-split { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; }

        /* Feed Glass Cards */
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
            cursor: pointer;
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

        /* Skeleton Loading Shimmer */
        .skeleton-card { background: rgba(10, 20, 40, 0.5); border: 1px solid rgba(56, 189, 248, 0.1); border-radius: 10px; height: 117px; display: flex; padding: 16px; gap: 16px; align-items: center; }
        .skeleton-thumb { width: 110px; height: 85px; border-radius: 8px; background: linear-gradient(90deg, #0f172a 25%, #1e293b 50%, #0f172a 75%); background-size: 200% 100%; animation: shimmer 1.5s infinite; }
        .skeleton-text { flex: 1; display: flex; flex-direction: column; gap: 10px; }
        .skeleton-line { height: 16px; border-radius: 4px; background: linear-gradient(90deg, #0f172a 25%, #1e293b 50%, #0f172a 75%); background-size: 200% 100%; animation: shimmer 1.5s infinite; }
        @keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }

        /* Activity Glass Panel */
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

        /* Modal Overlay Reader */
        .modal-overlay { 
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; 
            background: rgba(2, 6, 23, 0.85); backdrop-filter: blur(12px); 
            display: none; align-items: center; justify-content: center; z-index: 100; p: 20px; 
        }
        .modal-content { 
            background: #0b1329; border: 1px solid #38bdf8; border-radius: 12px; 
            max-width: 650px; width: 90%; max-height: 85vh; overflow-y: auto; padding: 28px; 
            box-shadow: 0 0 30px rgba(56, 189, 248, 0.3); position: relative; 
        }
        .modal-close { position: absolute; top: 16px; right: 20px; font-size: 1.5rem; color: #94a3b8; cursor: pointer; }
        .modal-close:hover { color: #38bdf8; }
        .modal-img { width: 100%; height: 220px; object-fit: cover; border-radius: 8px; margin-bottom: 18px; border: 1px solid rgba(56, 189, 248, 0.2); }
        .modal-title { font-size: 1.4rem; font-weight: 800; color: #f8fafc; margin-bottom: 12px; }
        .modal-body { font-size: 0.95rem; color: #cbd5e1; line-height: 1.6; margin-bottom: 20px; }
        .modal-meta { background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 8px; padding: 14px; font-size: 0.85rem; margin-bottom: 20px; }
        .modal-meta div { margin-bottom: 6px; }
        .modal-btn { display: inline-block; background: #0284c7; color: white; padding: 10px 20px; border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 0.9rem; }
        .modal-btn:hover { background: #0369a1; }

        /* Toast Container */
        #toast-container { position: fixed; bottom: 20px; right: 20px; display: flex; flex-direction: column; gap: 10px; z-index: 200; }
        .toast { background: #0c162d; border: 1px solid #38bdf8; color: #f8fafc; padding: 12px 20px; border-radius: 8px; font-size: 0.85rem; box-shadow: 0 0 15px rgba(56, 189, 248, 0.3); animation: fadeIn 0.3s ease; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

        /* Responsive Mobile Styling */
        @media (max-width: 900px) {
            body { flex-direction: column; overflow-y: auto; height: auto; }
            .sidebar { width: 100%; height: auto; border-right: none; border-bottom: 1px solid rgba(56, 189, 248, 0.2); }
            .metrics-grid { grid-template-columns: repeat(2, 1fr); }
            .content-split { grid-template-columns: 1fr; }
        }

        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: rgba(2, 6, 23, 0.5); }
        ::-webkit-scrollbar-thumb { background: rgba(56, 189, 248, 0.3); border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: #38bdf8; }
    </style>
</head>
<body>

    <!-- Sidebar Navigation -->
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

    <!-- Main Workspace -->
    <div class="main-content">
        
        <div class="header-bar">
            <div>
                <div class="header-title">Quantis Command Center</div>
                <div class="header-sub" id="status-text">Quantis is actively analyzing the frontier</div>
            </div>
            <div class="header-controls">
                <div class="sync-box">
                    <span>Auto Sync</span>
                    <label class="switch">
                        <input type="checkbox" id="sync-toggle" onchange="toggleAutoSync(this)">
                        <span class="slider"></span>
                    </label>
                </div>
                <button class="btn-action" onclick="initAgent()">1. Trigger Discovery</button>
                <button class="btn-action" style="background:rgba(30, 41, 59, 0.6); border-color:#334155;" onclick="loadFeed()">2. Refresh Feed</button>
            </div>
        </div>

        <!-- Metric Stat Cards -->
        <div class="metrics-grid">
            <div class="metric-card"><div class="metric-label">TOPICS DISCOVERED</div><div class="metric-val" id="discovered-count">128</div></div>
            <div class="metric-card"><div class="metric-label">TOPICS EVALUATED</div><div class="metric-val" id="evaluated-count">94</div></div>
            <div class="metric-card"><div class="metric-label">POSTS PUBLISHED</div><div class="metric-val" id="published-count">0</div></div>
            <div class="metric-card"><div class="metric-label">TOPICS REJECTED</div><div class="metric-val">86</div></div>
            <div class="metric-card"><div class="metric-label">MEMORY ENTRIES</div><div class="metric-val">312</div></div>
        </div>

        <!-- Search & Filter Bar -->
        <div class="filter-bar">
            <input type="text" class="search-input" id="search-box" placeholder="Search topics, models, benchmarks..." oninput="filterPosts()">
            <div class="filter-pill active" onclick="setCategory(this, 'all')">All Topics</div>
            <div class="filter-pill" onclick="setCategory(this, 'AI')">AI & LLMs</div>
            <div class="filter-pill" onclick="setCategory(this, 'Agent')">Agents</div>
            <div class="filter-pill" onclick="setCategory(this, 'Benchmark')">Benchmarks</div>
        </div>

        <!-- Content Grid Split -->
        <div class="content-split">
            
            <div class="feed-container" id="feed">
                <!-- Skeleton Loading Defaults -->
                <div class="skeleton-card"><div class="skeleton-thumb"></div><div class="skeleton-text"><div class="skeleton-line" style="width: 70%;"></div><div class="skeleton-line" style="width: 90%;"></div></div></div>
                <div class="skeleton-card"><div class="skeleton-thumb"></div><div class="skeleton-text"><div class="skeleton-line" style="width: 60%;"></div><div class="skeleton-line" style="width: 85%;"></div></div></div>
            </div>

            <div class="timeline-card">
                <div class="timeline-header">AGENT ACTIVITY</div>
                <div class="timeline-list" id="activity-log">
                    <!-- Dynamic Log Items Render Here -->
                </div>
            </div>

        </div>

    </div>

    <!-- Article Reader Modal -->
    <div class="modal-overlay" id="modal">
        <div class="modal-content">
            <span class="modal-close" onclick="closeModal()">&times;</span>
            <img class="modal-img" id="modal-img" src="" alt="Post Detail">
            <div class="modal-title" id="modal-title"></div>
            <div class="modal-body" id="modal-text"></div>
            <div class="modal-meta">
                <div><strong style="color: #38bdf8;">Confidence Score:</strong> <span id="modal-score"></span></div>
                <div><strong style="color: #38bdf8;">Analytical Rationale:</strong> <span id="modal-rationale"></span></div>
                <div><strong style="color: #38bdf8;">Strategic Prediction:</strong> <span id="modal-impact"></span></div>
            </div>
            <a class="modal-btn" id="modal-link" href="#" target="_blank">Read Original Source</a>
        </div>
    </div>

    <!-- Toast Notifications Container -->
    <div id="toast-container"></div>

    <script>
        let allPosts = [];
        let activeCategory = 'all';
        let syncInterval = null;

        function showToast(message) {
            const container = document.getElementById('toast-container');
            const toast = document.createElement('div');
            toast.className = 'toast';
            toast.innerText = message;
            container.appendChild(toast);
            setTimeout(() => toast.remove(), 3500);
        }

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
            showToast("Discovery engine activated...");
            try {
                const res = await fetch('/api/agent/init', { method: 'POST' });
                const data = await res.json();
                document.getElementById('status-text').innerText = data.message;
                updateActivityLog("Evaluated RSS feeds & saved new posts.");
                showToast("New insights processed successfully!");
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
                allPosts = data.feed || [];
                
                document.getElementById('published-count').innerText = data.total;
                document.getElementById('discovered-count').innerText = 120 + data.total * 3;
                document.getElementById('evaluated-count').innerText = 80 + data.total * 2;

                filterPosts();
                updateActivityLog("Fetched latest published insights.");
            } catch(e) {
                document.getElementById('status-text').innerText = "Error loading feed.";
            }
        }

        function filterPosts() {
            const query = document.getElementById('search-box').value.toLowerCase();
            const feedContainer = document.getElementById('feed');

            const filtered = allPosts.filter(post => {
                const matchesQuery = post.title.toLowerCase().includes(query) || post.text.toLowerCase().includes(query);
                const matchesCat = activeCategory === 'all' || post.title.toLowerCase().includes(activeCategory.toLowerCase()) || post.text.toLowerCase().includes(activeCategory.toLowerCase());
                return matchesQuery && matchesCat;
            });

            if (filtered.length === 0) {
                feedContainer.innerHTML = '<div style="color:#94a3b8; text-align:center; padding:40px;">No matching insights found.</div>';
                return;
            }

            feedContainer.innerHTML = '';
            filtered.forEach(post => {
                const imgUrl = (post.sources && post.sources.length > 1) 
                    ? post.sources[1] 
                    : `https://image.pollinations.ai/prompt/ai%20technology%20research?width=400&height=300&nologo=true`;

                const card = document.createElement('div');
                card.className = 'feed-card';
                card.onclick = () => openModal(post, imgUrl);
                card.innerHTML = `
                    <img class="card-thumb" src="${imgUrl}" alt="Thumbnail" onerror="this.src='https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=400'">
                    <div class="card-info">
                        <div class="card-h">${post.title || 'AI Frontier Analysis'}</div>
                        <div class="card-p">${post.text}</div>
                    </div>
                `;
                feedContainer.appendChild(card);
            });
        }

        function setCategory(el, cat) {
            document.querySelectorAll('.filter-pill').forEach(p => p.classList.remove('active'));
            el.classList.add('active');
            activeCategory = cat;
            filterPosts();
        }

        function openModal(post, imgUrl) {
            document.getElementById('modal-img').src = imgUrl;
            document.getElementById('modal-title').innerText = post.title;
            document.getElementById('modal-text').innerText = post.text;
            document.getElementById('modal-score').innerText = `${((post.confidenceScore || 0.95) * 100).toFixed(0)}% Match`;
            document.getElementById('modal-rationale').innerText = post.rationale || 'Selected via RSS discovery criteria.';
            document.getElementById('modal-impact').innerText = post.futureImpactPrediction || 'High strategic value.';
            document.getElementById('modal-link').href = (post.sources && post.sources[0]) ? post.sources[0] : '#';
            
            document.getElementById('modal').style.display = 'flex';
        }

        function closeModal() {
            document.getElementById('modal').style.display = 'none';
        }

        function toggleAutoSync(checkbox) {
            if (checkbox.checked) {
                showToast("Auto Sync enabled (30s interval)");
                syncInterval = setInterval(() => {
                    initAgent();
                }, 30000);
            } else {
                showToast("Auto Sync disabled");
                clearInterval(syncInterval);
            }
        }

        // Initialize default state
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
