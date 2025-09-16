from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.orm import Session
from app.config import settings
from app.db import get_db, SessionLocal
from app.sync import run_sync
from app.oauth import router as oauth_router
from app.routers.reports import router as reports_router
from app.routers.expenses import router as expenses_router
from app.routers.recon import router as recon_router

app = FastAPI(title="T&E Master Ledger")

# CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health(response: Response):
    # Add HSTS header for production HTTPS
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

    # Get last sync status from database
    db = SessionLocal()
    try:
        from app.models import SyncState
        sync_status = db.query(SyncState).filter(SyncState.provider == "zoho").first()
        sync_info = {
            "last_run": sync_status.last_run_at.isoformat() if sync_status and sync_status.last_run_at else None,
            "status": sync_status.status if sync_status else "Never run",
            "cursor": sync_status.cursor if sync_status else None,
        }
    except Exception:
        sync_info = {"status": "Database not available"}
    finally:
        db.close()

    return {
        "ok": True,
        "sync": sync_info,
        "service": "T&E Master Ledger"
    }

# Routers
app.include_router(oauth_router)
app.include_router(reports_router)
app.include_router(expenses_router)
app.include_router(recon_router)

# Background scheduler for sync
scheduler = AsyncIOScheduler()

@app.on_event("startup")
async def startup_event():
    scheduler.add_job(lambda: run_sync(SessionLocal()), "interval", minutes=settings.SYNC_INTERVAL_MINUTES)
    scheduler.start()

@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown(wait=False)
