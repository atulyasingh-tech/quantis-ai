import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Quantis AI - Autonomous Frontier Analyst",
    description="Production-grade AI ecosystem research agent and real-time news discovery engine.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    try:
        from database.connection import init_db
        await init_db()
    except Exception as e:
        print(f"Startup database initialization bypassed: {e}")

try:
    from api.routes import router
    app.include_router(router)
except Exception as e:
    print(f"Router loading bypassed: {e}")

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quantis AI — Autonomous Frontier Intelligence</title>
    <link rel="icon" type="image/jpeg" href="https://raw.githubusercontent.com/atulyasingh-tech/quantis-ai/main/quantislogo.jpeg">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --bg: #030712;
            --card-bg: rgba(15, 23, 42, 0.65);
            --border-glow: rgba(56, 189, 248, 0.2);
            --border-hover: rgba(56, 189, 248, 0.5);
            --accent-cyan: #38bdf8;
            --accent-purple: #a855f7;
            --accent-gradient: linear-gradient(135deg, #a855f7 0%, #38bdf8 50%, #06b6d4 100%);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; }
        body { 
            background: var(--bg); 
            color: var(--text-primary); 
            min-height: 100vh; 
            overflow-x: hidden;
            position: relative;
        }

        /* Interactive Particle Background Canvas */
        #particle-canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 0;
            pointer-events: none;
        }

        /* Radial Glow Orbs */
        .ambient-glow {
            position: fixed;
            top: 40%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 650px;
            height: 650px;
            background: radial-gradient(circle, rgba(168, 85, 247, 0.15) 0%, rgba(56, 189, 248, 0.08) 45%, rgba(3, 7, 18, 0) 70%);
            border-radius: 50%;
            pointer-events: none;
            z-index: 0;
            filter: blur(40px);
        }

        /* Top Navigation Bar */
        .navbar {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 72px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 40px;
            background: rgba(3, 7, 18, 0.7);
            backdrop-filter: blur(16px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
            z-index: 50;
        }
        .nav-brand { display: flex; align-items: center; gap: 12px; text-decoration: none; }
        .nav-logo { width: 36px; height: 36px; border-radius: 8px; border: 1px solid var(--border-glow); }
        .nav-title { font-size: 1.15rem; font-weight: 800; letter-spacing: 1px; color: #fff; }
        .nav-links { display: flex; align-items: center; gap: 28px; }
        .nav-link { color: var(--text-secondary); text-decoration: none; font-size: 0.88rem; font-weight: 500; transition: color 0.2s; }
        .nav-link:hover { color: var(--text-primary); }
        .nav-btn {
            background: var(--accent-gradient);
            color: #fff;
            padding: 8px 18px;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 600;
            text-decoration: none;
            border: none;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 0 20px rgba(168, 85, 247, 0.3);
        }
        .nav-btn:hover { transform: scale(1.03); box-shadow: 0 0 25px rgba(56, 189, 248, 0.5); }

        /* Hero Landing Section */
        #landing-view {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 120px 24px 60px;
            position: relative;
            z-index: 10;
        }

        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 16px;
            border-radius: 9999px;
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(56, 189, 248, 0.3);
            font-size: 0.75rem;
            font-family: 'JetBrains Mono', monospace;
            color: #38bdf8;
            margin-bottom: 28px;
            letter-spacing: 1px;
        }
        .pulse-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #4ade80;
            box-shadow: 0 0 10px #4ade80;
            animation: pulse 2s infinite;
        }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }

        .hero-title {
            font-size: clamp(2.5rem, 5vw, 4.2rem);
            font-weight: 800;
            line-height: 1.15;
            max-width: 900px;
            margin-bottom: 20px;
            letter-spacing: -0.02em;
        }
        .gradient-text {
            background: var(--accent-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero-subtitle {
            font-size: clamp(1rem, 2vw, 1.2rem);
            color: var(--text-secondary);
            max-width: 680px;
            line-height: 1.6;
            margin-bottom: 36px;
        }

        /* Floating Corner Node Callouts (Breeth Style) */
        .corner-tag {
            position: absolute;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            color: #64748b;
            display: flex;
            flex-direction: column;
            gap: 4px;
            pointer-events: none;
        }
        .corner-tag span { color: #a855f7; font-weight: 600; }
        .tag-top-left { top: 28%; left: 12%; text-align: left; }
        .tag-top-right { top: 28%; right: 12%; text-align: right; }
        .tag-bottom-left { bottom: 20%; left: 14%; text-align: left; }
        .tag-bottom-right { bottom: 20%; right: 14%; text-align: right; }

        .hero-cta-group {
            display: flex;
            align-items: center;
            gap: 16px;
            flex-wrap: wrap;
            justify-content: center;
        }
        .btn-primary {
            background: var(--accent-gradient);
            color: #fff;
            padding: 14px 32px;
            border-radius: 9999px;
            font-size: 1rem;
            font-weight: 700;
            text-decoration: none;
            border: none;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 0 30px rgba(168, 85, 247, 0.4);
            transition: all 0.3s;
        }
        .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 0 40px rgba(56, 189, 248, 0.6); }
        .btn-secondary {
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid var(--border-glow);
            color: var(--text-primary);
            padding: 14px 28px;
            border-radius: 9999px;
            font-size: 0.95rem;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.3s;
        }
        .btn-secondary:hover { border-color: var(--accent-cyan); color: var(--accent-cyan); }

        /* Command Center Section (Hidden by default, shown on Get Started) */
        #dashboard-view {
            display: none;
            padding: 100px 40px 60px;
            max-width: 1400px;
            margin: 0 auto;
            position: relative;
            z-index: 10;
            animation: fadeIn 0.5s ease-out;
        }

        .dashboard-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
            margin-bottom: 28px;
        }
        .dash-title { font-size: 1.8rem; font-weight: 800; }
        .dash-sub { color: var(--accent-cyan); font-size: 0.9rem; margin-top: 4px; }
        .dash-actions { display: flex; gap: 12px; }

        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 16px;
            margin-bottom: 28px;
        }
        .metric-card {
            background: var(--card-bg);
            border: 1px solid var(--border-glow);
            border-radius: 12px;
            padding: 18px;
            backdrop-filter: blur(12px);
        }
        .metric-label { font-size: 0.72rem; color: var(--accent-cyan); font-weight: 700; letter-spacing: 0.5px; }
        .metric-val { font-size: 1.8rem; font-weight: 800; color: #fff; margin-top: 6px; }

        .content-split { display: grid; grid-template-columns: 2fr 1fr; gap: 24px; }
        .feed-container { display: flex; flex-direction: column; gap: 16px; }
        
        .feed-card {
            background: var(--card-bg);
            border: 1px solid var(--border-glow);
            border-radius: 12px;
            padding: 18px;
            display: flex;
            gap: 18px;
            align-items: center;
            cursor: pointer;
            transition: all 0.25s;
            backdrop-filter: blur(12px);
        }
        .feed-card:hover {
            border-color: var(--accent-cyan);
            transform: translateY(-2px);
            box-shadow: 0 0 25px rgba(56, 189, 248, 0.2);
        }
        .card-thumb { width: 120px; height: 90px; border-radius: 8px; object-fit: cover; background: #020617; }
        .card-info { flex: 1; }
        .card-h { font-size: 1.1rem; font-weight: 700; color: #fff; margin-bottom: 6px; }
        .card-p { font-size: 0.88rem; color: var(--text-secondary); line-height: 1.5; }
        .card-cta { font-size: 0.78rem; color: var(--accent-cyan); margin-top: 8px; font-weight: 600; }

        /* Skeleton Loaders */
        .skeleton-card {
            background: rgba(15, 23, 42, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 18px;
            display: flex;
            gap: 18px;
            align-items: center;
        }
        .skeleton-thumb {
            width: 120px;
            height: 90px;
            border-radius: 8px;
            background: linear-gradient(90deg, #0f172a 25%, #1e293b 50%, #0f172a 75%);
            background-size: 200% 100%;
            animation: shimmer 1.5s infinite;
        }
        .skeleton-lines { flex: 1; display: flex; flex-direction: column; gap: 10px; }
        .skeleton-line {
            height: 16px;
            border-radius: 4px;
            background: linear-gradient(90deg, #0f172a 25%, #1e293b 50%, #0f172a 75%);
            background-size: 200% 100%;
            animation: shimmer 1.5s infinite;
        }
        @keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }

        .timeline-card {
            background: var(--card-bg);
            border: 1px solid var(--border-glow);
            border-radius: 12px;
            padding: 22px;
            backdrop-filter: blur(12px);
            height: fit-content;
        }
        .timeline-header { font-size: 0.85rem; font-weight: 700; color: var(--accent-cyan); margin-bottom: 18px; letter-spacing: 0.5px; }
        .timeline-list { display: flex; flex-direction: column; gap: 14px; }
        .timeline-item { font-size: 0.82rem; color: #cbd5e1; display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255, 255, 255, 0.05); padding-bottom: 10px; }
        .time-tag { color: var(--accent-cyan); font-family: 'JetBrains Mono', monospace; font-weight: 600; }

        /* Modal Overlay Reader */
        .modal-overlay { 
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; 
            background: rgba(2, 6, 23, 0.85); backdrop-filter: blur(16px); 
            display: none; align-items: center; justify-content: center; z-index: 100; padding: 20px; 
        }
        .modal-content { 
            background: #0b1329; border: 1px solid var(--accent-cyan); border-radius: 14px; 
            max-width: 620px; width: 92%; max-height: 85vh; overflow-y: auto; padding: 28px; 
            box-shadow: 0 0 40px rgba(56, 189, 248, 0.3); position: relative; 
        }
        .modal-close { position: absolute; top: 16px; right: 20px; font-size: 1.5rem; color: var(--text-secondary); cursor: pointer; }
        .modal-close:hover { color: var(--accent-cyan); }
        .modal-img { width: 100%; height: 220px; object-fit: cover; border-radius: 10px; margin-bottom: 18px; border: 1px solid var(--border-glow); }
        .modal-title { font-size: 1.35rem; font-weight: 800; color: #fff; margin-bottom: 12px; }
        .modal-body { font-size: 0.92rem; color: #cbd5e1; line-height: 1.6; margin-bottom: 22px; }
        .modal-btn-area { display: flex; justify-content: flex-end; gap: 12px; }

        #toast-container { position: fixed; bottom: 24px; right: 24px; display: flex; flex-direction: column; gap: 10px; z-index: 200; }
        .toast { 
            background: #0c162d; 
            border: 1px solid var(--accent-cyan); 
            color: #f8fafc; 
            padding: 12px 20px; 
            border-radius: 8px; 
            font-size: 0.85rem; 
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.3); 
            animation: fadeIn 0.3s ease; 
        }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }

        /* Responsive Breakpoints */
        @media (max-width: 1024px) {
            .metrics-grid { grid-template-columns: repeat(3, 1fr); }
            .content-split { grid-template-columns: 1fr; }
            .corner-tag { display: none; }
        }
        @media (max-width: 640px) {
            .navbar { padding: 0 20px; }
            .nav-links { display: none; }
            .metrics-grid { grid-template-columns: repeat(2, 1fr); }
            #dashboard-view { padding: 90px 16px 40px; }
        }
    </style>
</head>
<body>
    <canvas id="particle-canvas"></canvas>
    <div class="ambient-glow"></div>

    <!-- Navigation Bar -->
    <nav class="navbar">
        <a href="#" class="nav-brand" onclick="showLanding()">
            <img class="nav-logo" src="https://raw.githubusercontent.com/atulyasingh-tech/quantis-ai/main/quantislogo.jpeg" alt="Logo">
            <span class="nav-title">quantis<span style="color:#38bdf8;">.ai</span></span>
        </a>
        <div class="nav-links">
            <a href="#" class="nav-link" onclick="showLanding()">Overview</a>
            <a href="#" class="nav-link" onclick="showDashboard()">Feed</a>
            <a href="/docs" target="_blank" class="nav-link">API Docs ↗</a>
            <a href="https://github.com/atulyasingh-tech/quantis-ai" target="_blank" class="nav-link">GitHub ↗</a>
        </div>
        <button class="nav-btn" onclick="showDashboard()">Get started &rarr;</button>
    </nav>

    <!-- 1. Hero Landing Page View -->
    <section id="landing-view">
        <div class="corner-tag tag-top-left"><span>• WHY?</span>multi-signal continuous sensing</div>
        <div class="corner-tag tag-top-right"><span>• WHAT</span>frontier research & hardware shifts</div>
        <div class="corner-tag tag-bottom-left"><span>• WHERE</span>autonomous serverless execution</div>
        <div class="corner-tag tag-bottom-right"><span>• HOW</span>gemini-driven strategic distillation</div>

        <div class="status-badge">
            <div class="pulse-dot"></div>
            AUTONOMOUS RESEARCH AGENT • LIVE
        </div>

        <h1 class="hero-title">
            Quantis tracks <span class="gradient-text">the frontier</span> before it breaks.
        </h1>

        <p class="hero-subtitle">
            Autonomous multi-source ingestion, real-time Gemini evaluation, and strategic foresight for next-generation AI architectures, hardware breakthroughs, and frontier ecosystems.
        </p>

        <div class="hero-cta-group">
            <button class="btn-primary" onclick="showDashboard()">Get started free &rarr;</button>
            <a href="/docs" target="_blank" class="btn-secondary">Explore API Docs ↗</a>
        </div>
    </section>

    <!-- 2. Command Center Dashboard View -->
    <main id="dashboard-view">
        <div class="dashboard-header">
            <div>
                <div class="dash-title">Quantis Command Center</div>
                <div class="dash-sub" id="status-text">Autonomous intelligence engine actively streaming</div>
            </div>
            <div class="dash-actions">
                <button class="btn-primary" style="padding:10px 22px; font-size:0.85rem;" onclick="initAgent()">1. Trigger Discovery</button>
                <button class="btn-secondary" style="padding:10px 22px; font-size:0.85rem;" onclick="loadFeed()">2. Refresh Feed</button>
            </div>
        </div>

        <div class="metrics-grid">
            <div class="metric-card"><div class="metric-label">TOPICS DISCOVERED</div><div class="metric-val">128</div></div>
            <div class="metric-card"><div class="metric-label">TOPICS EVALUATED</div><div class="metric-val">94</div></div>
            <div class="metric-card"><div class="metric-label">POSTS PUBLISHED</div><div class="metric-val" id="published-count">10</div></div>
            <div class="metric-card"><div class="metric-label">TOPICS REJECTED</div><div class="metric-val">86</div></div>
            <div class="metric-card"><div class="metric-label">MEMORY ENTRIES</div><div class="metric-val">312</div></div>
        </div>

        <div class="content-split">
            <div class="feed-container" id="feed">
                <div class="skeleton-card"><div class="skeleton-thumb"></div><div class="skeleton-lines"><div class="skeleton-line" style="width:70%;"></div><div class="skeleton-line" style="width:90%;"></div></div></div>
                <div class="skeleton-card"><div class="skeleton-thumb"></div><div class="skeleton-lines"><div class="skeleton-line" style="width:60%;"></div><div class="skeleton-line" style="width:85%;"></div></div></div>
                <div class="skeleton-card"><div class="skeleton-thumb"></div><div class="skeleton-lines"><div class="skeleton-line" style="width:80%;"></div><div class="skeleton-line" style="width:75%;"></div></div></div>
            </div>
            <div class="timeline-card">
                <div class="timeline-header">AGENT ACTIVITY</div>
                <div class="timeline-list" id="activity-log"></div>
            </div>
        </div>
    </main>

    <!-- Modal Reader -->
    <div class="modal-overlay" id="modal">
        <div class="modal-content">
            <span class="modal-close" onclick="closeModal()">&times;</span>
            <img class="modal-img" id="modal-img" src="" alt="Thumbnail">
            <div class="modal-title" id="modal-title"></div>
            <div class="modal-body" id="modal-text"></div>
            <div class="modal-btn-area">
                <button class="btn-secondary" style="padding:8px 18px; font-size:0.85rem;" onclick="closeModal()">Close</button>
                <a class="btn-primary" style="padding:8px 20px; font-size:0.85rem;" id="modal-link" href="#" target="_blank" rel="noopener noreferrer">Read Original Source &rarr;</a>
            </div>
        </div>
    </div>

    <!-- Toast Notifications -->
    <div id="toast-container"></div>

    <script>
        /* Interactive Star & Particle Canvas Engine */
        const canvas = document.getElementById('particle-canvas');
        const ctx = canvas.getContext('2d');
        let particles = [];
        let mouse = { x: null, y: null, radius: 120 };

        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            initParticles();
        }
        window.addEventListener('resize', resizeCanvas);
        window.addEventListener('mousemove', (e) => { mouse.x = e.x; mouse.y = e.y; });
        window.addEventListener('mouseout', () => { mouse.x = null; mouse.y = null; });

        class Particle {
            constructor() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.size = Math.random() * 2 + 0.5;
                this.baseX = this.x;
                this.baseY = this.y;
                this.density = (Math.random() * 20) + 1;
                this.alpha = Math.random() * 0.6 + 0.2;
                this.color = Math.random() > 0.6 ? '#a855f7' : '#38bdf8';
            }
            draw() {
                ctx.fillStyle = this.color;
                ctx.globalAlpha = this.alpha;
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.closePath();
                ctx.fill();
                ctx.globalAlpha = 1.0;
            }
            update() {
                if (mouse.x != null) {
                    let dx = mouse.x - this.x;
                    let dy = mouse.y - this.y;
                    let distance = Math.sqrt(dx * dx + dy * dy);
                    if (distance < mouse.radius) {
                        const force = (mouse.radius - distance) / mouse.radius;
                        const directionX = (dx / distance) * force * this.density;
                        const directionY = (dy / distance) * force * this.density;
                        this.x -= directionX;
                        this.y -= directionY;
                    } else {
                        if (this.x !== this.baseX) { let dx = this.x - this.baseX; this.x -= dx / 15; }
                        if (this.y !== this.baseY) { let dy = this.y - this.baseY; this.y -= dy / 15; }
                    }
                } else {
                    this.baseY -= 0.15;
                    if (this.baseY < 0) this.baseY = canvas.height;
                    this.y = this.baseY;
                }
            }
        }

        function initParticles() {
            particles = [];
            const count = Math.floor((canvas.width * canvas.height) / 9000);
            for (let i = 0; i < count; i++) {
                particles.push(new Particle());
            }
        }

        function animateParticles() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            for (let i = 0; i < particles.length; i++) {
                particles[i].draw();
                particles[i].update();
            }
            requestAnimationFrame(animateParticles);
        }
        resizeCanvas();
        animateParticles();

        /* View Switching Logic */
        function showDashboard() {
            document.getElementById('landing-view').style.display = 'none';
            document.getElementById('dashboard-view').style.display = 'block';
            window.scrollTo({ top: 0, behavior: 'smooth' });
            loadFeed();
        }

        function showLanding() {
            document.getElementById('dashboard-view').style.display = 'none';
            document.getElementById('landing-view').style.display = 'flex';
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        /* Toast Notifications */
        function showToast(msg) {
            const container = document.getElementById('toast-container');
            if (container) {
                const toast = document.createElement('div');
                toast.className = 'toast';
                toast.innerText = msg;
                container.appendChild(toast);
                setTimeout(() => toast.remove(), 3500);
            }
        }

        function updateActivityLog(msg) {
            const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
            const log = document.getElementById('activity-log');
            if (log) {
                const item = document.createElement('div');
                item.className = 'timeline-item';
                item.innerHTML = `<span class="time-tag">${timeStr}</span> ${msg}`;
                log.prepend(item);
            }
        }

        async function initAgent() {
            document.getElementById('status-text').innerText = "Scanning live sources...";
            updateActivityLog("Running RSS news discovery...");
            showToast("Discovery Engine Activated...");
            try {
                const res = await fetch('/api/agent/init', { method: 'POST' });
                const data = await res.json();
                document.getElementById('status-text').innerText = data.message || "Discovery pass completed.";
                updateActivityLog("Evaluated RSS feeds & updated database.");
                showToast("New insights processed successfully!");
                setTimeout(loadFeed, 1000);
            } catch(e) {
                document.getElementById('status-text').innerText = "Error initializing agent.";
                showToast("Initialization error occurred.");
            }
        }

        async function loadFeed() {
            try {
                const res = await fetch('/api/agent/feed');
                const data = await res.json();
                const feed = document.getElementById('feed');
                const posts = data.feed || [];
                
                document.getElementById('published-count').innerText = data.total ?? posts.length;

                if (posts.length === 0) {
                    feed.innerHTML = '<div style="color:#94a3b8; text-align:center; padding:40px;">No posts yet. Click Trigger Discovery above.</div>';
                    return;
                }

                feed.innerHTML = '';
                posts.forEach(post => {
                    const sources = Array.isArray(post.sources) ? post.sources : [];
                    const originalUrl = sources[0] || 'https://techcrunch.com/category/artificial-intelligence/';
                    const imgUrl = sources[1] || 'https://image.pollinations.ai/prompt/ai%20technology?width=400&height=300';
                    
                    const card = document.createElement('div');
                    card.className = 'feed-card';
                    card.onclick = () => openModal(post.title, post.text, imgUrl, originalUrl);
                    card.innerHTML = `
                        <img class="card-thumb" src="${imgUrl}" alt="Thumb" onerror="this.src='https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=400'">
                        <div class="card-info">
                            <div class="card-h">${post.title || 'AI Frontier Analysis'}</div>
                            <div class="card-p">${post.text || ''}</div>
                            <div class="card-cta">Click to read article details &rarr;</div>
                        </div>
                    `;
                    feed.appendChild(card);
                });
                updateActivityLog("Loaded published posts.");
            } catch(e) {
                document.getElementById('status-text').innerText = "Error loading feed.";
            }
        }

        function openModal(title, text, imgUrl, sourceUrl) {
            document.getElementById('modal-title').innerText = title || 'Insight Details';
            document.getElementById('modal-text').innerText = text || '';
            document.getElementById('modal-img').src = imgUrl;
            document.getElementById('modal-link').href = sourceUrl;
            document.getElementById('modal').style.display = 'flex';
        }

        function closeModal() {
            document.getElementById('modal').style.display = 'none';
        }

        updateActivityLog("System online.");
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def root():
    return DASHBOARD_HTML
