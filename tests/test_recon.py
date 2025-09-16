import io
import pytest

def test_recon_upload_valid_csv(client):
    """Test reconciliation CSV upload with valid data"""
    content = "date,merchant,amount\n2025-01-01,STARBUCKS,5.50\n2025-01-02,UBER,12.75\n"
    files = {"file": ("report.csv", io.BytesIO(content.encode()), "text/csv")}

    r = client.post("/recon/upload", files=files)
    assert r.status_code == 200
    data = r.json()
    assert "total_rows" in data
    assert data["total_rows"] == 2
    assert data["successful_rows"] == 2
    assert data["error_rows"] == 0

def test_recon_upload_invalid_file_type(client):
    """Test reconciliation upload rejects non-CSV files"""
    content = "not a csv file"
    files = {"file": ("report.txt", io.BytesIO(content.encode()), "text/plain")}

    r = client.post("/recon/upload", files=files)
    assert r.status_code == 400
    assert "CSV format" in r.json().get("detail", "")

def test_recon_upload_missing_columns(client):
    """Test reconciliation upload validates required columns"""
    content = "wrong,columns,here\n1,2,3\n"
    files = {"file": ("report.csv", io.BytesIO(content.encode()), "text/csv")}

    r = client.post("/recon/upload", files=files)
    assert r.status_code == 400
    assert "must contain columns" in r.json().get("detail", "")

def test_recon_upload_invalid_amounts(client):
    """Test reconciliation upload handles invalid amount values"""
    content = "date,merchant,amount\n2025-01-01,STARBUCKS,invalid_amount\n"
    files = {"file": ("report.csv", io.BytesIO(content.encode()), "text/csv")}

    r = client.post("/recon/upload", files=files)
    assert r.status_code == 200
    data = r.json()
    assert data["error_rows"] == 1
    assert data["successful_rows"] == 0

def test_recon_upload_rate_limiting(client):
    """Test reconciliation upload is rate limited"""
    content = "date,merchant,amount\n2025-01-01,TEST,1.00\n"
    files = {"file": ("report.csv", io.BytesIO(content.encode()), "text/csv")}

    # Make multiple rapid uploads to trigger rate limit
    for _ in range(6):  # Limit is 5/minute
        client.post("/recon/upload", files=files)

    # This should be rate limited
    r = client.post("/recon/upload", files=files)
    assert r.status_code == 429  # Rate limited

def test_match_candidates_empty_merchant(client):
    """Test match candidates endpoint with empty merchant"""
    r = client.get("/recon/match-candidates/")
    assert r.status_code == 404  # FastAPI should return 404 for empty path param

def test_match_candidates_valid_merchant(client):
    """Test match candidates endpoint with valid merchant"""
    r = client.get("/recon/match-candidates/starbucks")
    assert r.status_code == 200
    data = r.json()
    assert "query" in data
    assert "candidates" in data
    assert "count" in data
    assert data["query"]["merchant"] == "starbucks"

def test_create_match_invalid_expense(client):
    """Test create match with non-existent expense"""
    r = client.post("/recon/match", json={
        "expense_id": 99999,
        "company_reference": "TEST-REF-001"
    })
    assert r.status_code == 404
    assert "not found" in r.json().get("detail", "").lower()