"""
Unit tests for policies endpoint
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_policies_list():
    """Test getting policies list"""
    response = client.get("/api/policies")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "policies" in data
    assert isinstance(data["policies"], list)

def test_policies_evaluate():
    """Test policy evaluation"""
    response = client.post("/api/policies/evaluate", json={
        "url": "https://fake-bank.com",
        "text": "Urgent: Verify your account",
        "source": "email",
        "score": 0.9
    })
    
    assert response.status_code == 200
    data = response.json()
    
    assert "action" in data
    assert "reason" in data
    assert "matched_policies" in data
    assert data["action"] in ["allow", "warn", "block"]

def test_policies_evaluate_high_score():
    """Test policy evaluation with high score"""
    response = client.post("/api/policies/evaluate", json={
        "url": "https://legitimate-bank.com",
        "text": "Monthly statement",
        "source": "email",
        "score": 0.3
    })
    
    assert response.status_code == 200
    data = response.json()
    
    # Low score should result in allow
    assert data["action"] == "allow"

def test_policies_evaluate_missing_fields():
    """Test policy evaluation with missing fields"""
    response = client.post("/api/policies/evaluate", json={
        "url": "https://example.com",
        "text": "",
        "source": "email",
        "score": 0.5
    })
    
    assert response.status_code == 200  # Should handle gracefully
    data = response.json()
    assert "action" in data

def test_policies_stats():
    """Test policies statistics"""
    response = client.get("/api/policies/stats")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "total_policies" in data
    assert "enabled_policies" in data
    assert "policy_types" in data
    assert isinstance(data["policy_types"], dict)