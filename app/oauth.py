from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import httpx, urllib.parse

from app.config import settings
from app.db import get_db
from app.models import User, OAuthCredentials
from app.utils import encrypt

router = APIRouter(prefix="/oauth/zoho", tags=["oauth"])

def _accounts_base():
    return settings.ZOHO_ACCOUNTS_BASE.rstrip('/')

def _base():
    return settings.ZOHO_BASE.rstrip('/')

@router.get("/login")
async def login():
    params = {
        "response_type": "code",
        "client_id": settings.ZOHO_CLIENT_ID,
        "scope": settings.ZOHO_SCOPES,
        "redirect_uri": f"{settings.APP_BASE_URL}/oauth/zoho/callback",
        "access_type": "offline",
        "prompt": "consent",
    }
    url = f"{_accounts_base()}/oauth/v2/auth?{urllib.parse.urlencode(params)}"
    return RedirectResponse(url)

@router.get("/callback")
async def callback(request: Request, code: str, db: Session = Depends(get_db)):
    token_url = f"{_accounts_base()}/oauth/v2/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": settings.ZOHO_CLIENT_ID,
        "client_secret": settings.ZOHO_CLIENT_SECRET,
        "redirect_uri": f"{settings.APP_BASE_URL}/oauth/zoho/callback",
        "code": code,
    }
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(token_url, data=data)
        if r.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Token exchange failed: {r.text}")
        payload = r.json()
    access_token = payload["access_token"]
    refresh_token = payload.get("refresh_token")
    expires_in = int(payload.get("expires_in", 3600))
    expires_at = datetime.utcnow() + timedelta(seconds=expires_in)

    # For single-user use, create/find a singleton user
    user = db.query(User).first()
    if not user:
        user = User(id=None, email="owner@example.com")
        db.add(user); db.commit(); db.refresh(user)

    cred = db.query(OAuthCredentials).filter_by(user_id=user.id, provider="zoho_expense").first()
    if cred:
        cred.access_token = encrypt(access_token)
        if refresh_token:
            cred.refresh_token = encrypt(refresh_token)
        cred.expires_at = expires_at
    else:
        cred = OAuthCredentials(
            user_id=user.id,
            provider="zoho_expense",
            access_token=encrypt(access_token),
            refresh_token=encrypt(refresh_token or ""),
            expires_at=expires_at,
            scope=settings.ZOHO_SCOPES,
        )
        db.add(cred)
    db.commit()
    return RedirectResponse(url="/health")
