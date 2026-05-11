"""
Test render endpoint
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_render_endpoint():
    """Test render endpoint with demo domain"""
    response = client.post(
        "/api/render",
        json={
            "url": "https://fake-bank-verification.com/verify"
        }
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "screenshot" in data
    assert "dom" in data
    assert "title" in data
    assert "status" in data
    assert data["status"] in ["rendered", "fallback"]

def test_render_with_non_demo_domain():
    """Test render endpoint with non-demo domain"""
    response = client.post(
        "/api/render",
        json={
            "url": "https://example.com"
        }
    )
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "fallback"
    assert "screenshot" in data
    assert "dom" in data

def test_render_dom_structure():
    """Test render DOM structure"""
    response = client.post(
        "/api/render",
        json={
            "url": "https://fake-microsoft-security.net/secure"
        }
    )
    assert response.status_code == 200
    
    data = response.json()
    dom = data["dom"]
    assert "html" in dom
    assert "text_content" in dom
    assert "links" in dom
    assert "forms" in dom
    assert isinstance(dom["links"], list)
    assert isinstance(dom["forms"], list)