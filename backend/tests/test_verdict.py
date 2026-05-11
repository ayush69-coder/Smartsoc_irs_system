"""
Unit tests for verdict endpoint
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_verdict_endpoint():
    """Test the verdict endpoint with various inputs"""
    # Test phishing URL
    response = client.post("/api/verdict", json={
        "url": "https://fake-bank-security.com/login",
        "text": "Your account has been compromised. Click here to verify your identity.",
        "source": "email"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "score" in data
    assert "action" in data
    assert "reasons" in data
    assert "explain" in data
    assert 0 <= data["score"] <= 1
    assert data["action"] in ["allow", "warn", "block"]

def test_verdict_legitimate_url():
    """Test verdict with legitimate URL"""
    response = client.post("/api/verdict", json={
        "url": "https://www.google.com",
        "text": "Search the web",
        "source": "web"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["score"] < 0.5  # Should be low risk
    assert data["action"] in ["allow", "warn"]

def test_verdict_missing_fields():
    """Test verdict with missing required fields"""
    response = client.post("/api/verdict", json={
        "url": "https://example.com"
        # Missing text and source
    })
    
    assert response.status_code == 422  # Validation error

def test_verdict_invalid_source():
    """Test verdict with invalid source"""
    response = client.post("/api/verdict", json={
        "url": "https://example.com",
        "text": "Test message",
        "source": "invalid_source"
    })
    
    assert response.status_code == 422  # Validation error

def test_verdict_explain_tokens():
    """Test that explain field contains token analysis"""
    response = client.post("/api/verdict", json={
        "url": "https://fake-bank.com",
        "text": "Urgent: Verify your account now!",
        "source": "email"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "explain" in data
    assert "tokens" in data["explain"]
    assert isinstance(data["explain"]["tokens"], list)
    
    # Check that tokens have required fields
    if data["explain"]["tokens"]:
        token = data["explain"]["tokens"][0]
        assert "token" in token
        assert "weight" in token
        assert isinstance(token["weight"], (int, float))