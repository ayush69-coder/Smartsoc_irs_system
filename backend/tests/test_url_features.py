"""
Unit tests for URL features endpoint
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_url_features_endpoint():
    """Test the URL features endpoint"""
    response = client.post("/api/url/features", json={"url": "https://fake-bank-security.com/login"})
    
    assert response.status_code == 200
    data = response.json()
    
    # Check required fields
    required_fields = [
        "length", "token_entropy", "has_punycode", "has_at_symbol",
        "has_credentials", "num_subdomains", "path_entropy", "is_shortener"
    ]
    
    for field in required_fields:
        assert field in data
        assert isinstance(data[field], (int, float, bool))

def test_url_features_legitimate():
    """Test URL features with legitimate URL"""
    response = client.post("/api/url/features", json={"url": "https://www.google.com"})
    
    assert response.status_code == 200
    data = response.json()
    
    # Legitimate URLs should have reasonable entropy
    assert data["token_entropy"] > 0
    assert data["length"] > 0
    assert data["has_credentials"] == False
    assert data["is_shortener"] == False

def test_url_features_suspicious():
    """Test URL features with suspicious URL"""
    response = client.post("/api/url/features", json={"url": "https://fake-bank-security-verification.com/secure/login/verify"})
    
    assert response.status_code == 200
    data = response.json()
    
    # Suspicious URLs should have reasonable features
    assert data["length"] > 20
    assert data["token_entropy"] > 0
    assert data["has_credentials"] == False

def test_url_features_missing_url():
    """Test URL features with missing URL parameter"""
    response = client.post("/api/url/features", json={})
    
    assert response.status_code == 422  # Validation error

def test_url_features_invalid_url():
    """Test URL features with invalid URL"""
    response = client.post("/api/url/features", json={"url": "not-a-valid-url"})
    
    assert response.status_code == 200  # Should handle gracefully
    data = response.json()
    assert "length" in data