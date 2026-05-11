"""
Test graph query endpoint
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_graph_query_endpoint():
    """Test graph query endpoint with demo domain"""
    response = client.get("/api/graph/query?domain=fake-bank-verification.com")
    assert response.status_code == 200
    
    data = response.json()
    assert "domain" in data
    assert "neighbors" in data
    assert "cluster_score" in data
    assert "node_info" in data
    assert data["domain"] == "fake-bank-verification.com"
    assert isinstance(data["neighbors"], list)
    assert isinstance(data["cluster_score"], (int, float))

def test_graph_query_unknown_domain():
    """Test graph query with unknown domain"""
    response = client.get("/api/graph/query?domain=unknown-domain.com")
    assert response.status_code == 200
    
    data = response.json()
    assert data["domain"] == "unknown-domain.com"
    assert data["neighbors"] == []
    assert data["cluster_score"] == 0.0
    assert data["node_info"] is None

def test_graph_query_structure():
    """Test graph query response structure"""
    response = client.get("/api/graph/query?domain=fake-microsoft-security.net")
    assert response.status_code == 200
    
    data = response.json()
    
    # Check neighbors structure
    for neighbor in data["neighbors"]:
        assert "domain" in neighbor
        assert "type" in neighbor
        assert "label" in neighbor
        assert "source" in neighbor
    
    # Check node_info structure
    if data["node_info"]:
        node_info = data["node_info"]
        assert "type" in node_info
        assert "label" in node_info
        assert "source" in node_info
        assert "timestamp" in node_info
        assert "degree" in node_info