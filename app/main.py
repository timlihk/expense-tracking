from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.orm import Session
from app.config import settings
from app.db import get_db, SessionLocal
from app.sync import run_sync
from app.oauth import router as oauth_router
from app.routers.reports import router as reports_router
from app.routers.expenses import router as expenses_router

app = FastAPI(title="T&E Master Ledger")

@app.get("/health")
async def health():
    return {"ok": True}

# Routers
app.include_router(oauth_router)
app.include_router(reports_router)
app.include_router(expenses_router)

# Background scheduler for sync
scheduler = AsyncIOScheduler()

@app.on_event("startup")
async def startup_event():
    scheduler.add_job(lambda: run_sync(SessionLocal()), "interval", minutes=settings.SYNC_INTERVAL_MINUTES)
    scheduler.start()

@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown(wait=False)
