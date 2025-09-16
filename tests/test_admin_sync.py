import pytest

def test_admin_sync_rejects_missing_token(client):
    """Test admin sync endpoint rejects requests without token"""
    r = client.post("/expenses/admin/sync")
    assert r.status_code in (400, 401, 422)

def test_admin_sync_rejects_invalid_token(client):
    """Test admin sync endpoint rejects invalid tokens"""
    r = client.post("/expenses/admin/sync", headers={"x-admin-token": "wrong-token"})
    assert r.status_code == 401
    body = r.json()
    assert "Unauthorized" in body.get("detail", "")

def test_admin_sync_accepts_valid_header(client, monkeypatch):
    """Test admin sync endpoint accepts valid token in header"""
    def fake_run_sync(db):  # Mock to avoid hitting DB/Zoho
        return {"status": "success", "reports_synced": 0, "expenses_synced": 0}

    from app.routers import expenses as mod
    monkeypatch.setattr(mod, "run_sync", fake_run_sync)

    r = client.post("/expenses/admin/sync", headers={"x-admin-token": "test-admin"})
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True
    assert "message" in body

def test_admin_sync_rate_limiting(client, monkeypatch):
    """Test admin sync endpoint is rate limited"""
    def fake_run_sync(db):
        return {"status": "success", "reports_synced": 0, "expenses_synced": 0}

    from app.routers import expenses as mod
    monkeypatch.setattr(mod, "run_sync", fake_run_sync)

    # Make multiple rapid requests to trigger rate limit
    for _ in range(12):  # Limit is 10/minute
        client.post("/expenses/admin/sync", headers={"x-admin-token": "test-admin"})

    # This should be rate limited
    r = client.post("/expenses/admin/sync", headers={"x-admin-token": "test-admin"})
    assert r.status_code == 429  # Rate limited