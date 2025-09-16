import httpx
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.config import settings
from app.models import OAuthCredentials
from app.utils import decrypt, encrypt

ACCOUNTS_BASE = settings.ZOHO_ACCOUNTS_BASE.rstrip('/')
API_BASE = settings.ZOHO_BASE.rstrip('/')

async def get_valid_token(db: Session) -> str:
    cred = db.query(OAuthCredentials).filter_by(provider="zoho_expense").first()
    if not cred:
        raise RuntimeError("Zoho OAuth not configured")
    # refresh if about to expire
    if cred.expires_at and (cred.expires_at - datetime.utcnow()).total_seconds() < 120:
        await refresh_token(db, cred)
    return decrypt(cred.access_token)

async def refresh_token(db: Session, cred: OAuthCredentials):
    token_url = f"{ACCOUNTS_BASE}/oauth/v2/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": settings.ZOHO_CLIENT_ID,
        "client_secret": settings.ZOHO_CLIENT_SECRET,
        "refresh_token": decrypt(cred.refresh_token),
    }
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(token_url, data=data)
        r.raise_for_status()
        payload = r.json()
    new_access = payload["access_token"]
    expires_in = int(payload.get("expires_in", 3600))
    cred.access_token = encrypt(new_access)
    cred.expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
    db.commit()

async def list_expenses(db: Session, modified_after: datetime | None = None, page: int = 1, per_page: int = 200):
    token = await get_valid_token(db)
    headers = {"Authorization": f"Zoho-oauthtoken {token}"}
    params = {"page": page, "per_page": per_page}
    # NOTE: adjust query params to match Zoho Expense API filters for modified_time if available
    if modified_after:
        params["modified_time"] = modified_after.isoformat()
    url = f"{API_BASE}/expense/v1/expenses"
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(url, params=params, headers=headers)
        r.raise_for_status()
        return r.json()

async def list_reports(db: Session, modified_after: datetime | None = None, page: int = 1, per_page: int = 200):
    token = await get_valid_token(db)
    headers = {"Authorization": f"Zoho-oauthtoken {token}"}
    params = {"page": page, "per_page": per_page}
    if modified_after:
        params["modified_time"] = modified_after.isoformat()
    url = f"{API_BASE}/expense/v1/reports"
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(url, params=params, headers=headers)
        r.raise_for_status()
        return r.json()
