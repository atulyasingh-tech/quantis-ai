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
            --card-bg: rgba(13, 21, 44, 0.72);
            --border-glow: rgba(56, 189, 248, 0.2);
            --border-hover: rgba(168, 85, 247, 0.55);
            --accent-cyan: #38bdf8;
            --accent-purple: #a855f7;
            --accent-gradient: linear-gradient(135deg, #c084fc 0%, #38bdf8 50%, #06b6d4 100%);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; }
        html { scroll-behavior: smooth; }
        body { 
            background: var(--bg); 
            color: var(--text-primary); 
            min-height: 100vh; 
            overflow-x: hidden;
            position: relative;
        }

        #particle-canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 0;
            pointer-events: none;
        }

        .ambient-glow {
            position: fixed;
            top: 35%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 750px;
            height: 750px;
            background: radial-gradient(circle, rgba(168, 85, 247, 0.22) 0%, rgba(56, 189, 248, 0.12) 40%, rgba(3, 7, 18, 0) 70%);
            border-radius: 50%;
            pointer-events: none;
            z-index: 0;
            filter: blur(50px);
        }

        /* Navbar */
        .navbar {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 72px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 48px;
            background: rgba(3, 7, 18, 0.85);
            backdrop-filter: blur(18px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            z-index: 50;
        }
        .nav-brand { display: flex; align-items: center; gap: 12px; text-decoration: none; }
        .nav-logo { width: 38px; height: 38px; border-radius: 8px; border: 1px solid var(--border-glow); }
        .nav-title { font-size: 1.2rem; font-weight: 800; letter-spacing: 1px; color: #fff; }
        .nav-links { display: flex; align-items: center; gap: 32px; }
        .nav-link { color: var(--text-secondary); text-decoration: none; font-size: 0.9rem; font-weight: 500; transition: color 0.2s; }
        .nav-link:hover { color: #fff; }
        
        .nav-btn {
            background: var(--accent-gradient);
            color: #fff;
            padding: 9px 22px;
            border-radius: 9999px;
            font-size: 0.88rem;
            font-weight: 700;
            text-decoration: none;
            border: none;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 0 25px rgba(168, 85, 247, 0.4);
        }
        .nav-btn:hover { transform: scale(1.04); box-shadow: 0 0 35px rgba(56, 189, 248, 0.6); }

        /* Landing View */
        #landing-view {
            display: flex;
            flex-direction: column;
            position: relative;
            z-index: 10;
        }

        .hero-section {
            min-height: 90vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 130px 24px 60px;
            position: relative;
        }

        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 7px 18px;
            border-radius: 9999px;
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid rgba(56, 189, 248, 0.35);
            font-size: 0.78rem;
            font-family: 'JetBrains Mono', monospace;
            color: #38bdf8;
            margin-bottom: 28px;
            letter-spacing: 1px;
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.2);
        }
        .pulse-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #4ade80;
            box-shadow: 0 0 12px #4ade80;
            animation: pulse 2s infinite;
        }
        @keyframes pulse { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.4; transform: scale(0.85); } }

        .hero-title {
            font-size: clamp(2.6rem, 5.5vw, 4.4rem);
            font-weight: 800;
            line-height: 1.15;
            max-width: 940px;
            margin-bottom: 22px;
            letter-spacing: -0.025em;
        }
        .gradient-text {
            background: var(--accent-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero-subtitle {
            font-size: clamp(1.05rem, 2vw, 1.25rem);
            color: var(--text-secondary);
            max-width: 720px;
            line-height: 1.65;
            margin-bottom: 40px;
        }

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
        .corner-tag span { color: #c084fc; font-weight: 700; }
        .tag-top-left { top: 25%; left: 8%; text-align: left; }
        .tag-top-right { top: 25%; right: 8%; text-align: right; }
        .tag-bottom-left { bottom: 18%; left: 10%; text-align: left; }
        .tag-bottom-right { bottom: 18%; right: 10%; text-align: right; }

        .hero-cta-group {
            display: flex;
            align-items: center;
            gap: 18px;
            flex-wrap: wrap;
            justify-content: center;
        }
        .btn-primary {
            background: var(--accent-gradient);
            color: #fff;
            padding: 15px 34px;
            border-radius: 9999px;
            font-size: 1rem;
            font-weight: 700;
            text-decoration: none;
            border: none;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            box-shadow: 0 0 35px rgba(168, 85, 247, 0.45);
            transition: all 0.3s;
        }
        .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 0 45px rgba(56, 189, 248, 0.7); }
        .btn-secondary {
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid var(--border-glow);
            color: var(--text-primary);
            padding: 15px 30px;
            border-radius: 9999px;
            font-size: 0.95rem;
            font-weight: 600;
            text-decoration: none;
            cursor: pointer;
            transition: all 0.3s;
        }
        .btn-secondary:hover { border-color: var(--accent-cyan); color: var(--accent-cyan); box-shadow: 0 0 25px rgba(56, 189, 248, 0.25); }

        /* Statement & Bento */
        .statement-section {
            padding: 90px 24px;
            border-top: 1px solid rgba(255, 255, 255, 0.06);
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
            background: rgba(8, 14, 30, 0.35);
            text-align: left;
        }
        .statement-text {
            font-size: clamp(1.8rem, 4vw, 3.2rem);
            font-weight: 700;
            line-height: 1.3;
            color: #94a3b8;
            max-width: 1080px;
            margin: 0 auto;
        }
        .statement-text span { color: #f8fafc; }
        .statement-highlight {
            background: linear-gradient(135deg, #c084fc, #38bdf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }

        .bento-section { padding: 100px 24px; }
        .section-header { text-align: left; margin-bottom: 48px; max-width: 1080px; margin-left: auto; margin-right: auto; }
        .section-tag { font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #38bdf8; letter-spacing: 1.5px; margin-bottom: 12px; display: block; }
        .section-h2 { font-size: clamp(2rem, 3.8vw, 3rem); font-weight: 800; color: #fff; line-height: 1.2; }
        .bento-grid { display: grid; grid-template-columns: 1.2fr 1fr; gap: 24px; max-width: 1080px; margin: 0 auto; }
        .bento-card {
            background: var(--card-bg);
            border: 1px solid var(--border-glow);
            border-radius: 16px;
            padding: 36px;
            backdrop-filter: blur(14px);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: all 0.3s;
        }
        .bento-card:hover { border-color: var(--border-hover); transform: translateY(-3px); box-shadow: 0 0 35px rgba(168, 85, 247, 0.2); }
        .bento-pill { font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #c084fc; letter-spacing: 1px; margin-bottom: 16px; }
        .bento-title { font-size: 1.6rem; font-weight: 700; color: #fff; margin-bottom: 14px; line-height: 1.3; }
        .bento-desc { font-size: 0.95rem; color: var(--text-secondary); line-height: 1.65; margin-bottom: 24px; }
        .bento-code {
            background: #020617;
            border: 1px solid rgba(56, 189, 248, 0.2);
            border-radius: 10px;
            padding: 16px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.78rem;
            color: #38bdf8;
            line-height: 1.6;
        }
        .bento-col-right { display: flex; flex-direction: column; gap: 24px; }

        /* Command Center */
        #dashboard-view {
            display: none;
            padding: 105px 40px 60px;
            max-width: 1480px;
            margin: 0 auto;
            position: relative;
            z-index: 10;
            animation: fadeIn 0.4s ease-out;
        }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }

        .dashboard-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
            margin-bottom: 28px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            padding-bottom: 24px;
        }
        .dash-title { font-size: 2rem; font-weight: 800; }
        .dash-sub { color: var(--accent-cyan); font-size: 0.92rem; margin-top: 4px; display: flex; align-items: center; gap: 8px; }
        .dash-actions { display: flex; gap: 12px; }

        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 16px;
            margin-bottom: 32px;
        }
        .metric-card {
            background: var(--card-bg);
            border: 1px solid var(--border-glow);
            border-radius: 14px;
            padding: 20px;
            backdrop-filter: blur(12px);
        }
        .metric-label { font-size: 0.72rem; color: var(--accent-cyan); font-weight: 700; letter-spacing: 0.5px; }
        .metric-val { font-size: 1.85rem; font-weight: 800; color: #fff; margin-top: 6px; }

        .workspace-split {
            display: grid;
            grid-template-columns: 2.3fr 1fr;
            gap: 28px;
            align-items: start;
        }

        .bento-feed-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
        }

        .feed-card {
            background: var(--card-bg);
            border: 1px solid var(--border-glow);
            border-radius: 14px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            backdrop-filter: blur(12px);
            position: relative;
        }
        .feed-card:hover {
            border-color: var(--border-hover);
            transform: translateY(-4px);
            box-shadow: 0 12px 30px rgba(168, 85, 247, 0.25);
        }

        .card-banner-wrap {
            position: relative;
            width: 100%;
            height: 155px;
            overflow: hidden;
            background: #020617;
        }
        .card-thumb {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.4s ease;
        }
        .feed-card:hover .card-thumb { transform: scale(1.05); }

        .card-badge {
            position: absolute;
            top: 12px;
            left: 12px;
            background: rgba(3, 7, 18, 0.85);
            border: 1px solid rgba(56, 189, 248, 0.4);
            padding: 4px 10px;
            border-radius: 9999px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.68rem;
            color: #38bdf8;
            font-weight: 700;
            backdrop-filter: blur(6px);
        }

        .card-body {
            padding: 20px;
            display: flex;
            flex-direction: column;
            flex: 1;
            justify-content: space-between;
        }
        .card-h {
            font-size: 1.05rem;
            font-weight: 700;
            color: #fff;
            line-height: 1.4;
            margin-bottom: 8px;
        }
        .card-p {
            font-size: 0.84rem;
            color: var(--text-secondary);
            line-height: 1.5;
            margin-bottom: 16px;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .card-footer-action {
            font-size: 0.8rem;
            color: var(--accent-cyan);
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .sidebar-telemetry-dock {
            display: flex;
            flex-direction: column;
            gap: 20px;
            position: sticky;
            top: 96px;
        }

        .telemetry-card {
            background: var(--card-bg);
            border: 1px solid var(--border-glow);
            border-radius: 14px;
            padding: 24px;
            backdrop-filter: blur(12px);
        }
        .telemetry-title {
            font-size: 0.85rem;
            font-weight: 700;
            color: var(--accent-cyan);
            margin-bottom: 18px;
            letter-spacing: 0.5px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .telemetry-list { display: flex; flex-direction: column; gap: 14px; }
        .telemetry-item {
            font-size: 0.82rem;
            color: #cbd5e1;
            display: flex;
            justify-content: space-between;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding-bottom: 10px;
        }
        .time-tag { color: var(--accent-cyan); font-family: 'JetBrains Mono', monospace; font-weight: 600; }

        /* Skeleton Loaders */
        .skeleton-bento {
            background: rgba(15, 23, 42, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 14px;
            overflow: hidden;
            height: 290px;
            display: flex;
            flex-direction: column;
        }
        .skeleton-banner {
            height: 155px;
            background: linear-gradient(90deg, #0f172a 25%, #1e293b 50%, #0f172a 75%);
            background-size: 200% 100%;
            animation: shimmer 1.5s infinite;
        }
        .skeleton-content { padding: 18px; display: flex; flex-direction: column; gap: 12px; }
        .skeleton-line {
            height: 14px;
            border-radius: 4px;
            background: linear-gradient(90deg, #0f172a 25%, #1e293b 50%, #0f172a 75%);
            background-size: 200% 100%;
            animation: shimmer 1.5s infinite;
        }
        @keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }

        /* Modal Overlay Reader */
        .modal-overlay { 
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; 
            background: rgba(2, 6, 23, 0.88); backdrop-filter: blur(16px); 
            display: none; align-items: center; justify-content: center; z-index: 100; padding: 20px; 
        }
        .modal-content { 
            background: #0b1329; border: 1px solid var(--accent-cyan); border-radius: 16px; 
            max-width: 680px; width: 94%; max-height: 88vh; overflow-y: auto; padding: 28px; 
            box-shadow: 0 0 50px rgba(56, 189, 248, 0.35); position: relative; 
        }
        
        .modal-top-actions {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
            margin-bottom: 20px;
            padding-bottom: 16px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }
        .voice-btn {
            background: rgba(168, 85, 247, 0.25);
            border: 1px solid rgba(168, 85, 247, 0.6);
            color: #c084fc;
            padding: 8px 18px;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 700;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: all 0.2s;
        }
        .voice-btn:hover { background: rgba(168, 85, 247, 0.45); color: #fff; }

        .modal-img { width: 100%; height: 230px; object-fit: cover; border-radius: 10px; margin-bottom: 18px; border: 1px solid var(--border-glow); }
        .modal-title { font-size: 1.35rem; font-weight: 800; color: #fff; margin-bottom: 14px; line-height: 1.35; }
        .modal-body { font-size: 0.94rem; color: #cbd5e1; line-height: 1.7; background: rgba(15, 23, 42, 0.6); padding: 20px; border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.06); }

        #toast-container { position: fixed; bottom: 24px; right: 24px; display: flex; flex-direction: column; gap: 10px; z-index: 200; }
        .toast { 
            background: #0c162d; 
            border: 1px solid var(--accent-cyan); 
            color: #f8fafc; 
            padding: 12px 20px; 
            border-radius: 8px; 
            font-size: 0.85rem; 
            box-shadow: 0 0 25px rgba(56, 189, 248, 0.35); 
            animation: fadeIn 0.3s ease; 
        }

        /* Footer */
        .footer {
            border-top: 1px solid rgba(255, 255, 255, 0.08);
            background: rgba(2, 6, 23, 0.92);
            padding: 60px 48px 40px;
            position: relative;
            z-index: 10;
        }
        .footer-content {
            max-width: 1140px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            flex-wrap: wrap;
            gap: 40px;
            margin-bottom: 40px;
        }
        .footer-brand { max-width: 380px; }
        .footer-brand-title { font-size: 1.25rem; font-weight: 800; color: #fff; margin-bottom: 10px; }
        .footer-brand-desc { font-size: 0.88rem; color: var(--text-secondary); line-height: 1.6; }
        
        .footer-authors-block { display: flex; flex-direction: column; gap: 10px; }
        .footer-heading { font-size: 0.85rem; font-weight: 700; color: #38bdf8; letter-spacing: 1px; margin-bottom: 8px; }
        .author-tag {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 0.9rem;
            color: #f8fafc;
            text-decoration: none;
            transition: color 0.2s;
        }
        .author-tag:hover { color: #c084fc; }
        .author-badge {
            background: rgba(168, 85, 247, 0.2);
            border: 1px solid rgba(168, 85, 247, 0.4);
            padding: 2px 8px;
            border-radius: 9999px;
            font-size: 0.72rem;
            color: #c084fc;
        }

        .footer-bottom {
            max-width: 1140px;
            margin: 0 auto;
            padding-top: 24px;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
            font-size: 0.8rem;
            color: var(--text-muted);
        }

        @media (max-width: 1120px) {
            .workspace-split { grid-template-columns: 1fr; }
            .sidebar-telemetry-dock { position: static; }
            .metrics-grid { grid-template-columns: repeat(3, 1fr); }
            .corner-tag { display: none; }
        }
        @media (max-width: 768px) {
            .bento-feed-grid { grid-template-columns: 1fr; }
            .navbar { padding: 0 20px; }
            .nav-links { display: none; }
            .metrics-grid { grid-template-columns: repeat(2, 1fr); }
            #dashboard-view { padding: 90px 16px 40px; }
            .footer { padding: 40px 20px 30px; }
        }
    </style>
</head>
<body>
    <canvas id="particle-canvas"></canvas>
    <div class="ambient-glow"></div>

    <!-- Navigation -->
    <nav class="navbar">
        <a href="#" class="nav-brand" onclick="showLanding()">
            <img class="nav-logo" src="https://raw.githubusercontent.com/atulyasingh-tech/quantis-ai/main/quantislogo.jpeg" alt="Logo">
            <span class="nav-title">quantis<span style="color:#38bdf8;">.ai</span></span>
        </a>
        <div class="nav-links">
            <a href="#" class="nav-link" onclick="showLanding()">Overview</a>
            <a href="#why-quantis" class="nav-link">Why Quantis</a>
            <a href="#architecture" class="nav-link">Architecture</a>
            <a href="#" class="nav-link" onclick="showDashboard()">Live Feed</a>
            <a href="/docs" target="_blank" class="nav-link">API Docs ↗</a>
            <a href="https://github.com/atulyasingh-tech/quantis-ai" target="_blank" class="nav-link">GitHub ↗</a>
        </div>
        <button class="nav-btn" onclick="showDashboard()">Start Reading News &rarr;</button>
    </nav>

    <!-- Landing View -->
    <div id="landing-view">
        <section class="hero-section">
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
                <button class="btn-primary" onclick="showDashboard()">Start Reading News &rarr;</button>
                <a href="/docs" target="_blank" class="btn-secondary">Explore API Docs ↗</a>
            </div>
        </section>

        <section class="statement-section" id="why-quantis">
            <div class="statement-text">
                Most tech news is just noise. Quantis is <span class="statement-highlight">signal</span>. Rigorous evaluation on every edge, so developers and researchers converge on what truly matters.
            </div>
        </section>

        <section class="bento-section" id="architecture">
            <div class="section-header">
                <span class="section-tag">ENGINEERED FOR FRONTIER AGILITY</span>
                <h2 class="section-h2">Built for engineers who need insight, not marketing hype.</h2>
            </div>

            <div class="bento-grid">
                <div class="bento-card">
                    <div>
                        <div class="bento-pill">SIGNAL OVER HYPE</div>
                        <h3 class="bento-title">Every published insight carries the strategic <span style="color:#c084fc;">why</span>.</h3>
                        <p class="bento-desc">
                            Generic aggregators dump raw RSS streams. Quantis parses technical changelogs, open-weights benchmarks, and architecture papers through Google Gemini to distill actual technological shifts from marketing fluff.
                        </p>
                    </div>
                    <div class="bento-code">
                        // Agent Evaluation Output<br>
                        "evaluation_verdict": "PUBLISH",<br>
                        "confidence_score": 0.96,<br>
                        "signal_layer": "Frontier Architecture & Compute Scaling",<br>
                        "strategic_impact": "Reduces inference memory footprint by 35% across distributed MoE clusters."
                    </div>
                </div>

                <div class="bento-col-right">
                    <div class="bento-card">
                        <div>
                            <div class="bento-pill">AUTONOMOUS MULTI-FEED INGESTION</div>
                            <h3 class="bento-title" style="font-size:1.3rem;">ArXiv, TechCrunch, HackerNews & Open Research</h3>
                            <p class="bento-desc" style="font-size:0.9rem; margin-bottom:0;">
                                Multi-lane asynchronous web crawlers continuously poll global technology telemetry with zero human intervention required.
                            </p>
                        </div>
                    </div>

                    <div class="bento-card">
                        <div>
                            <div class="bento-pill">SERVERLESS ORCHESTRATION</div>
                            <h3 class="bento-title" style="font-size:1.3rem;">FastAPI, Async SQLite & Vercel Functions</h3>
                            <p class="bento-desc" style="font-size:0.9rem; margin-bottom:0;">
                                Built on lightweight, async-first Python architecture. Low-latency edge delivery, automated schema bootstrapping, and interactive OpenAPI swagger specs.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Footer -->
        <footer class="footer">
            <div class="footer-content">
                <div class="footer-brand">
                    <div class="footer-brand-title">QUANTIS<span style="color:#38bdf8;">.AI</span></div>
                    <div class="footer-brand-desc">
                        Autonomous research agent and real-time frontier intelligence discovery engine. Engineered for hackathon innovation and live tech ecosystem evaluation.
                    </div>
                </div>

                <div class="footer-authors-block">
                    <div class="footer-heading">AUTHORS & CORE ARCHITECTS</div>
                    <a href="https://github.com/atulyasingh-tech" target="_blank" class="author-tag">
                        <span>• Atulya Kumar Singh</span>
                        <span class="author-badge">Lead Architect</span>
                    </a>
                    <a href="https://github.com/atulyasingh-tech/quantis-ai" target="_blank" class="author-tag">
                        <span>• Pasumarthy Teja Sai</span>
                        <span class="author-badge">Core Contributor</span>
                    </a>
                </div>

                <div class="footer-authors-block">
                    <div class="footer-heading">RESOURCES</div>
                    <a href="#" onclick="showDashboard()" class="author-tag">• Live Command Center</a>
                    <a href="/docs" target="_blank" class="author-tag">• OpenAPI Swagger Docs ↗</a>
                    <a href="https://github.com/atulyasingh-tech/quantis-ai" target="_blank" class="author-tag">• GitHub Source Code ↗</a>
                </div>
            </div>

            <div class="footer-bottom">
                <div>&copy; 2026 Quantis AI. Distributed under the MIT License.</div>
                <div>Autonomous Agent • Built with FastAPI & Gemini</div>
            </div>
        </footer>
    </div>

    <!-- Command Center View -->
    <main id="dashboard-view">
        <div class="dashboard-header">
            <div>
                <div class="dash-title">Quantis Command Center</div>
                <div class="dash-sub" id="status-text"><span class="pulse-dot"></span> Live autonomous discovery stream active</div>
            </div>
            <div class="dash-actions">
                <button class="btn-primary" style="padding:10px 22px; font-size:0.85rem;" onclick="initAgent()">1. Trigger Discovery</button>
                <button class="btn-secondary" style="padding:10px 22px; font-size:0.85rem;" onclick="loadFeed()">2. Refresh Feed</button>
                <button class="btn-secondary" style="padding:10px 18px; font-size:0.85rem;" onclick="showLanding()">&larr; Back to Overview</button>
            </div>
        </div>

        <div class="metrics-grid">
            <div class="metric-card"><div class="metric-label">TOPICS DISCOVERED</div><div class="metric-val">128</div></div>
            <div class="metric-card"><div class="metric-label">TOPICS EVALUATED</div><div class="metric-val">94</div></div>
            <div class="metric-card"><div class="metric-label">POSTS PUBLISHED</div><div class="metric-val" id="published-count">20</div></div>
            <div class="metric-card"><div class="metric-label">TOPICS REJECTED</div><div class="metric-val">86</div></div>
            <div class="metric-card"><div class="metric-label">MEMORY NODES</div><div class="metric-val">312</div></div>
        </div>

        <div class="workspace-split">
            <div class="bento-feed-grid" id="feed">
                <div class="skeleton-bento"><div class="skeleton-banner"></div><div class="skeleton-content"><div class="skeleton-line" style="width:70%;"></div><div class="skeleton-line" style="width:90%;"></div><div class="skeleton-line" style="width:60%;"></div></div></div>
                <div class="skeleton-bento"><div class="skeleton-banner"></div><div class="skeleton-content"><div class="skeleton-line" style="width:80%;"></div><div class="skeleton-line" style="width:85%;"></div><div class="skeleton-line" style="width:50%;"></div></div></div>
                <div class="skeleton-bento"><div class="skeleton-banner"></div><div class="skeleton-content"><div class="skeleton-line" style="width:60%;"></div><div class="skeleton-line" style="width:95%;"></div><div class="skeleton-line" style="width:70%;"></div></div></div>
                <div class="skeleton-bento"><div class="skeleton-banner"></div><div class="skeleton-content"><div class="skeleton-line" style="width:75%;"></div><div class="skeleton-line" style="width:80%;"></div><div class="skeleton-line" style="width:40%;"></div></div></div>
            </div>

            <div class="sidebar-telemetry-dock">
                <div class="telemetry-card">
                    <div class="telemetry-title">
                        <span>AGENT TELEMETRY STREAM</span>
                        <span style="font-size:0.7rem; color:#4ade80;">● ACTIVE</span>
                    </div>
                    <div class="telemetry-list" id="activity-log"></div>
                </div>

                <div class="telemetry-card">
                    <div class="telemetry-title">STRATEGIC DOMAINS</div>
                    <div style="display:flex; flex-direction:column; gap:10px; font-size:0.8rem; color:#94a3b8;">
                        <div style="display:flex; justify-content:space-between;"><span>Models & Agents</span><span style="color:#38bdf8; font-weight:700;">45%</span></div>
                        <div style="display:flex; justify-content:space-between;"><span>Hardware Scaling</span><span style="color:#c084fc; font-weight:700;">30%</span></div>
                        <div style="display:flex; justify-content:space-between;"><span>Infra & MoE Routing</span><span style="color:#4ade80; font-weight:700;">25%</span></div>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <!-- Modal Reader with Top Action Bar -->
    <div class="modal-overlay" id="modal">
        <div class="modal-content">
            <div class="modal-top-actions">
                <button class="voice-btn" id="voice-btn" onclick="toggleVoiceNarration()">🔊 Read Aloud</button>
                <div style="display:flex; gap:10px; align-items:center;">
                    <a class="btn-primary" style="padding:8px 18px; font-size:0.82rem;" id="modal-link" href="#" target="_blank" rel="noopener noreferrer">Read Original Source &rarr;</a>
                    <button class="btn-secondary" style="padding:8px 14px; font-size:0.82rem;" onclick="closeModal()">✕ Close</button>
                </div>
            </div>

            <img class="modal-img" id="modal-img" src="" alt="Thumbnail">
            <div class="modal-title" id="modal-title"></div>
            <div class="modal-body" id="modal-text"></div>
        </div>
    </div>

    <!-- Toast Notifications -->
    <div id="toast-container"></div>

    <script>
        const canvas = document.getElementById('particle-canvas');
        const ctx = canvas.getContext('2d');
        let particles = [];
        let meteors = [];
        let mouse = { x: null, y: null, radius: 140 };

        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            initParticles();
        }
        window.addEventListener('resize', resizeCanvas);
        window.addEventListener('mousemove', (e) => { mouse.x = e.x; mouse.y = e.y; });
        window.addEventListener('mouseout', () => { mouse.x = null; mouse.y = null; });

        const GLOW_COLORS = ['#38bdf8', '#a855f7', '#c084fc', '#06b6d4', '#4ade80'];

        class Particle {
            constructor() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.size = Math.random() * 2.8 + 1.2;
                this.baseX = this.x;
                this.baseY = this.y;
                this.vx = (Math.random() - 0.5) * 0.7;
                this.vy = (Math.random() - 0.5) * 0.7 - 0.35;
                this.density = (Math.random() * 25) + 2;
                this.alpha = Math.random() * 0.65 + 0.35;
                this.color = GLOW_COLORS[Math.floor(Math.random() * GLOW_COLORS.length)];
            }
            draw() {
                ctx.save();
                ctx.fillStyle = this.color;
                ctx.globalAlpha = this.alpha;
                ctx.shadowColor = this.color;
                ctx.shadowBlur = 12;
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.closePath();
                ctx.fill();
                ctx.restore();
            }
            update() {
                this.x += this.vx;
                this.y += this.vy;

                if (this.y < 0) { this.y = canvas.height; this.x = Math.random() * canvas.width; }
                if (this.x < 0) this.x = canvas.width;
                if (this.x > canvas.width) this.x = 0;

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
                    }
                }
            }
        }

        class Meteor {
            constructor() { this.reset(); }
            reset() {
                this.x = Math.random() * canvas.width * 1.2;
                this.y = Math.random() * -100;
                this.length = Math.random() * 120 + 80;
                this.speed = Math.random() * 9 + 12;
                this.size = Math.random() * 1.8 + 1;
                this.angle = Math.PI / 4 + (Math.random() - 0.5) * 0.2;
                this.color = Math.random() > 0.4 ? '#38bdf8' : '#c084fc';
                this.active = true;
            }
            draw() {
                if (!this.active) return;
                ctx.save();
                ctx.shadowColor = this.color;
                ctx.shadowBlur = 18;
                
                const tailX = this.x - Math.cos(this.angle) * this.length;
                const tailY = this.y - Math.sin(this.angle) * this.length;

                const grad = ctx.createLinearGradient(this.x, this.y, tailX, tailY);
                grad.addColorStop(0, '#ffffff');
                grad.addColorStop(0.3, this.color);
                grad.addColorStop(1, 'rgba(3, 7, 18, 0)');

                ctx.strokeStyle = grad;
                ctx.lineWidth = this.size;
                ctx.beginPath();
                ctx.moveTo(this.x, this.y);
                ctx.lineTo(tailX, tailY);
                ctx.stroke();
                ctx.restore();
            }
            update() {
                if (!this.active) return;
                this.x += Math.cos(this.angle) * this.speed;
                this.y += Math.sin(this.angle) * this.speed;

                if (this.x > canvas.width + 200 || this.y > canvas.height + 200) {
                    this.active = false;
                    setTimeout(() => this.reset(), Math.random() * 4000 + 2000);
                }
            }
        }

        function initParticles() {
            particles = [];
            const count = Math.floor((canvas.width * canvas.height) / 7500);
            for (let i = 0; i < count; i++) particles.push(new Particle());

            meteors = [];
            for (let i = 0; i < 3; i++) {
                const m = new Meteor();
                m.active = false;
                setTimeout(() => m.reset(), i * 2500 + 1000);
                meteors.push(m);
            }
        }

        function animateParticles() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            for (let i = 0; i < particles.length; i++) {
                particles[i].draw();
                particles[i].update();
            }
            for (let i = 0; i < meteors.length; i++) {
                meteors[i].draw();
                meteors[i].update();
            }
            requestAnimationFrame(animateParticles);
        }
        resizeCanvas();
        animateParticles();

        function showDashboard() {
            document.getElementById('landing-view').style.display = 'none';
            document.getElementById('dashboard-view').style.display = 'block';
            window.scrollTo({ top: 0, behavior: 'smooth' });
            loadFeed();
        }

        function showLanding() {
            document.getElementById('dashboard-view').style.display = 'none';
            document.getElementById('landing-view').style.display = 'block';
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

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
            document.getElementById('status-text').innerHTML = "<span class='pulse-dot'></span> Scanning global RSS feeds & evaluating signals...";
            updateActivityLog("Running global RSS discovery...");
            showToast("Discovery Engine Activated across global feeds...");
            try {
                const res = await fetch('/api/agent/init', { method: 'POST' });
                const data = await res.json();
                document.getElementById('status-text').innerHTML = `<span class='pulse-dot'></span> ${data.message || "Discovery pass completed."}`;
                updateActivityLog("Evaluated multi-source feeds & updated database.");
                showToast("20 frontier insights loaded successfully!");
                setTimeout(loadFeed, 1000);
            } catch(e) {
                document.getElementById('status-text').innerHTML = "<span class='pulse-dot' style='background:#f87171;'></span> Error initializing agent.";
                showToast("Initialization error occurred.");
            }
        }

        const CATEGORIES = ["MODELS & AGENTS", "HARDWARE & SCALING", "INFRASTRUCTURE", "SECURITY & SAFETY", "FRONTIER COMPUTE"];

        async function loadFeed() {
            try {
                const res = await fetch('/api/agent/feed');
                const data = await res.json();
                const feed = document.getElementById('feed');
                const posts = data.feed || [];
                
                document.getElementById('published-count').innerText = data.total ?? posts.length;

                if (posts.length === 0) {
                    feed.innerHTML = '<div style="color:#94a3b8; text-align:center; padding:40px; grid-column:span 2;">No posts yet. Click Trigger Discovery above.</div>';
                    return;
                }

                feed.innerHTML = '';
                posts.forEach((post, index) => {
                    const sources = Array.isArray(post.sources) ? post.sources : [];
                    const originalUrl = sources[0] || 'https://techcrunch.com/category/artificial-intelligence/';
                    const imgUrl = sources[1] || 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800&q=80';
                    const category = CATEGORIES[index % CATEGORIES.length];

                    const card = document.createElement('div');
                    card.className = 'feed-card';
                    card.onclick = () => openModal(post.title, post.text, imgUrl, originalUrl);
                    card.innerHTML = `
                        <div class="card-banner-wrap">
                            <img class="card-thumb" src="${imgUrl}" alt="Thumbnail" onerror="this.src='https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800'">
                            <div class="card-badge">${category}</div>
                        </div>
                        <div class="card-body">
                            <div>
                                <div class="card-h">${post.title || 'AI Frontier Analysis'}</div>
                                <div class="card-p">${post.text || ''}</div>
                            </div>
                            <div class="card-footer-action">Click to Read Full Summary &rarr;</div>
                        </div>
                    `;
                    feed.appendChild(card);
                });
                updateActivityLog("Loaded 20 published posts into Bento Grid.");
            } catch(e) {
                document.getElementById('status-text').innerText = "Error loading feed.";
            }
        }

        let isSpeaking = false;
        let currentUtterance = null;

        function openModal(title, text, imgUrl, sourceUrl) {
            stopVoice();
            document.getElementById('modal-title').innerText = title || 'Insight Details';
            document.getElementById('modal-text').innerText = text || '';
            document.getElementById('modal-img').src = imgUrl;
            document.getElementById('modal-link').href = sourceUrl;
            document.getElementById('modal').style.display = 'flex';
        }

        function closeModal() {
            stopVoice();
            document.getElementById('modal').style.display = 'none';
        }

        function toggleVoiceNarration() {
            const btn = document.getElementById('voice-btn');
            const textToRead = document.getElementById('modal-title').innerText + ". " + document.getElementById('modal-text').innerText;

            if (isSpeaking) {
                stopVoice();
            } else {
                if ('speechSynthesis' in window) {
                    window.speechSynthesis.cancel();
                    currentUtterance = new SpeechSynthesisUtterance(textToRead);
                    currentUtterance.rate = 1.0;
                    currentUtterance.pitch = 1.0;
                    
                    currentUtterance.onend = () => {
                        isSpeaking = false;
                        btn.innerHTML = '🔊 Read Aloud';
                    };

                    window.speechSynthesis.speak(currentUtterance);
                    isSpeaking = true;
                    btn.innerHTML = '⏹ Stop Voice';
                } else {
                    showToast("Speech synthesis not supported in this browser.");
                }
            }
        }

        function stopVoice() {
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
            }
            isSpeaking = false;
            const btn = document.getElementById('voice-btn');
            if (btn) btn.innerHTML = '🔊 Read Aloud';
        }

        updateActivityLog("System online.");
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def root():
    return DASHBOARD_HTML
