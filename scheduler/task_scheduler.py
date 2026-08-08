from apscheduler.schedulers.asyncio import AsyncIOScheduler
from agents.core_agent import quantis_agent
from config.settings import settings

scheduler = AsyncIOScheduler()

def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(quantis_agent.run_autonomous_loop, "interval", minutes=settings.FETCH_INTERVAL_MINUTES, id="quantis_loop", replace_existing=True)
        scheduler.start()
