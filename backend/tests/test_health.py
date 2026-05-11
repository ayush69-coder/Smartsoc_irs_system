"""
Test health endpoint
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_endpoint():
    """Test health endpoint returns expected response"""
    response = client.get("/api/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "ok"
    assert "uptime" in data
    assert data["version"] == "v1-dev"
    assert "timestamp" in data
    assert isinstance(data["uptime"], (int, float))
    assert data["uptime"] >= 0