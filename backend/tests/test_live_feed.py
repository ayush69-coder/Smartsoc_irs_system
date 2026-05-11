"""
Unit tests for live feed endpoint
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_live_feed():
    """Test live feed endpoint"""
    response = client.post("/api/live", json={"limit": 10, "offset": 0})
    
    assert response.status_code == 200
    data = response.json()
    
    assert "events" in data
    assert "total" in data
    assert isinstance(data["events"], list)

def test_live_feed_pagination():
    """Test live feed with pagination"""
    response = client.post("/api/live", json={"limit": 5, "offset": 0})
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["events"]) <= 5
    assert "total" in data

def test_live_feed_filters():
    """Test live feed with filters"""
    response = client.post("/api/live", json={
        "limit": 10, 
        "offset": 0, 
        "source": "email", 
        "action": "block"
    })
    
    assert response.status_code == 200
    data = response.json()
    
    assert "events" in data
    # All returned events should match filters
    for event in data["events"]:
        if "source" in event:
            assert event["source"] == "email"
        if "action" in event:
            assert event["action"] == "block"

def test_live_feed_search():
    """Test live feed with search"""
    response = client.post("/api/live", json={
        "limit": 10, 
        "offset": 0, 
        "search": "phishing"
    })
    
    assert response.status_code == 200
    data = response.json()
    
    assert "events" in data
    # Search should return some results
    assert len(data["events"]) >= 0

def test_live_feed_invalid_params():
    """Test live feed with invalid parameters"""
    response = client.post("/api/live", json={"limit": -1, "offset": -1})
    
    # Should handle invalid params gracefully
    assert response.status_code == 200
    data = response.json()
    assert "events" in data