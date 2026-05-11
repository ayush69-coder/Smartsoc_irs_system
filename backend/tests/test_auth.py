"""
Unit tests for authentication endpoints
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_success():
    """Test successful login"""
    response = client.post("/api/auth/login", json={
        "username": "analyst",
        "password": "analyst123"
    })
    
    assert response.status_code == 200
    data = response.json()
    
    assert "access_token" in data
    assert "token_type" in data
    assert "user" in data
    assert "session_id" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["role"] == "analyst"

def test_login_invalid_credentials():
    """Test login with invalid credentials"""
    response = client.post("/api/auth/login", json={
        "username": "analyst",
        "password": "wrongpassword"
    })
    
    assert response.status_code == 401
    assert "Invalid username or password" in response.json()["detail"]

def test_login_nonexistent_user():
    """Test login with nonexistent user"""
    response = client.post("/api/auth/login", json={
        "username": "nonexistent",
        "password": "password123"
    })
    
    assert response.status_code == 401

def test_get_current_user():
    """Test getting current user info with valid token"""
    # First login to get token
    login_response = client.post("/api/auth/login", json={
        "username": "admin",
        "password": "admin123"
    })
    
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    # Use token to get user info
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["username"] == "admin"
    assert data["role"] == "admin"
    assert "permissions" in data
    assert "users" in data["permissions"]  # Admin should have user management

def test_get_current_user_invalid_token():
    """Test getting current user with invalid token"""
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": "Bearer invalid-token"}
    )
    
    assert response.status_code == 401

def test_get_permissions():
    """Test getting user permissions"""
    # Login as analyst
    login_response = client.post("/api/auth/login", json={
        "username": "analyst",
        "password": "analyst123"
    })
    
    token = login_response.json()["access_token"]
    
    response = client.get(
        "/api/auth/permissions",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["role"] == "analyst"
    assert "permissions" in data
    assert "review" in data["permissions"]
    assert "override" in data["permissions"]["review"]

def test_admin_only_endpoint():
    """Test admin-only endpoint access"""
    # Login as analyst (not admin)
    login_response = client.post("/api/auth/login", json={
        "username": "analyst",
        "password": "analyst123"
    })
    
    token = login_response.json()["access_token"]
    
    # Try to access admin-only endpoint
    response = client.get(
        "/api/auth/users",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 403
    assert "Requires admin role" in response.json()["detail"]

def test_admin_access():
    """Test admin access to admin-only endpoint"""
    # Login as admin
    login_response = client.post("/api/auth/login", json={
        "username": "admin",
        "password": "admin123"
    })
    
    token = login_response.json()["access_token"]
    
    # Access admin-only endpoint
    response = client.get(
        "/api/auth/users",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "users" in data
    assert "total_count" in data
    assert data["total_count"] >= 3  # Should have at least 3 demo users