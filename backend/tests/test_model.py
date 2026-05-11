"""
Test model status endpoint
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_model_status_endpoint():
    """Test model status endpoint"""
    response = client.get("/api/model/status")
    assert response.status_code == 200
    
    data = response.json()
    assert "models" in data
    assert "ensemble" in data
    assert "performance" in data
    assert isinstance(data["models"], list)
    assert len(data["models"]) > 0

def test_model_status_structure():
    """Test model status response structure"""
    response = client.get("/api/model/status")
    assert response.status_code == 200
    
    data = response.json()
    
    # Check models structure
    for model in data["models"]:
        assert "name" in model
        assert "version" in model
        assert "type" in model
        assert "created_at" in model
        assert "last_trained" in model
        assert "metrics" in model
        assert "algorithm" in model
    
    # Check ensemble structure
    ensemble = data["ensemble"]
    assert "active_model" in ensemble
    assert "fallback_model" in ensemble
    assert "confidence_threshold" in ensemble
    
    # Check performance structure
    performance = data["performance"]
    assert "avg_inference_time_ms" in performance
    assert "throughput_per_second" in performance
    assert "memory_usage_mb" in performance

def test_model_metadata_loaded():
    """Test that model metadata is properly loaded"""
    response = client.get("/api/model/status")
    assert response.status_code == 200
    
    data = response.json()
    
    # Check that we have the expected models
    model_names = [model["name"] for model in data["models"]]
    expected_models = ["text_model_v1", "url_model_v2", "visual_model_v1", "ensemble_model_v1"]
    
    for expected_model in expected_models:
        assert expected_model in model_names