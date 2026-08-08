import sys
import os

# Ensure local module directories are discoverable in Vercel's runtime environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from api.routes import router
from database.connection import init_db

app = FastAPI(title="Quantis AI - Autonomous Frontier Analyst")

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/")
def root():
    """Redirect root page to docs or API feed."""
    return RedirectResponse(url="/docs")

app.include_router(router)
