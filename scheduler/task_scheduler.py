from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

def start_scheduler():
    try:
        from agents.core_agent import quantis_agent
        
        # Schedule periodic execution pass
        if not scheduler.running:
            scheduler.add_job(
                quantis_agent.run_autonomous_loop,
                'interval',
                minutes=15,
                id='quantis_loop_job',
                replace_existing=True
            )
            scheduler.start()
    except Exception as e:
        print(f"Scheduler initialization bypassed in serverless context: {e}")
