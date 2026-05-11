"""
Test live events endpoint
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_live_events_endpoint():
    """Test live events endpoint"""
    response = client.post("/api/live", json={})
    assert response.status_code == 200
    
    data = response.json()
    assert "events" in data
    assert "total" in data
    assert "limit" in data
    assert "offset" in data
    assert isinstance(data["events"], list)
    assert data["total"] >= 0
    assert data["limit"] == 10
    assert data["offset"] == 0

def test_live_events_with_pagination():
    """Test live events with pagination"""
    response = client.post("/api/live?limit=2&offset=0", json={})
    assert response.status_code == 200
    
    data = response.json()
    assert len(data["events"]) <= 2
    assert data["limit"] == 2
    assert data["offset"] == 0

def test_live_events_with_filters():
    """Test live events with domain and label filters"""
    response = client.post("/api/live?label=phishing", json={})
    assert response.status_code == 200
    
    data = response.json()
    # All events should have label=phishing
    for event in data["events"]:
        assert event["label"] == "phishing"

def test_live_events_structure():
    """Test live events have correct structure"""
    response = client.post("/api/live", json={})
    assert response.status_code == 200
    
    data = response.json()
    if data["events"]:  # If there are events
        event = data["events"][0]
        required_fields = [
            "id", "timestamp", "source", "sender", "subject", 
            "body", "url", "final_url", "label", "score", "action"
        ]
        for field in required_fields:
            assert field in event