def test_health(client):
    """Test health endpoint returns OK status"""
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert "ok" in body and body["ok"] is True
    assert "sync" in body  # Should include sync status
    assert "service" in body

def test_health_includes_security_headers(client):
    """Test health endpoint includes HSTS security header"""
    r = client.get("/health")
    assert r.status_code == 200
    assert "strict-transport-security" in r.headers