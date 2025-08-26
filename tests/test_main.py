# Unit tests for FastAPI application
# Author: Kkasuga904
# Description: Comprehensive test suite for production deployment

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# ===========================
# Health Check Tests
# ===========================

def test_health_check():
    """Test health check endpoint for Kubernetes probes"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "fastapi-app"}

# ===========================
# Root Endpoint Tests
# ===========================

def test_root_endpoint():
    """Test root endpoint returns correct API information"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["version"] == "1.0.0"
    assert "documentation" in data
    assert data["documentation"] == "/docs"
    assert data["health"] == "/health"

# ===========================
# Hello Endpoint Tests
# ===========================

def test_hello_endpoint():
    """Test personalized greeting endpoint"""
    name = "TestUser"
    response = client.get(f"/hello/{name}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Hello, {name}!"}

def test_hello_endpoint_with_special_characters():
    """Test hello endpoint with special characters in name"""
    name = "Test-User_123"
    response = client.get(f"/hello/{name}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Hello, {name}!"}

# ===========================
# Metrics Endpoint Tests
# ===========================

def test_metrics_endpoint():
    """Test metrics endpoint for Prometheus"""
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "requests_total" in data
    assert "requests_per_second" in data
    assert "response_time_ms" in data
    assert "active_connections" in data

# ===========================
# Error Handling Tests
# ===========================

def test_not_found_endpoint():
    """Test 404 error for non-existent endpoint"""
    response = client.get("/nonexistent")
    assert response.status_code == 404

# ===========================
# CORS Tests
# ===========================

def test_cors_headers():
    """Test CORS headers are properly set"""
    response = client.get("/", headers={"Origin": "https://example.com"})
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers

# ===========================
# Performance Tests
# ===========================

def test_response_time():
    """Test API response time is within acceptable limits"""
    import time
    start = time.time()
    response = client.get("/health")
    end = time.time()
    assert response.status_code == 200
    assert (end - start) < 0.1  # Response should be under 100ms

# ===========================
# Security Tests
# ===========================

def test_no_server_header_leak():
    """Test that sensitive server information is not leaked"""
    response = client.get("/")
    # サーバー情報が漏れていないことを確認
    assert "server" not in response.headers or "uvicorn" not in response.headers.get("server", "").lower()

def test_content_type_header():
    """Test proper content-type header is set"""
    response = client.get("/")
    assert response.headers["content-type"] == "application/json"

# ===========================
# Load Testing Helper
# ===========================

@pytest.mark.parametrize("endpoint", ["/health", "/", "/metrics"])
def test_multiple_endpoints(endpoint):
    """Test multiple endpoints are accessible"""
    response = client.get(endpoint)
    assert response.status_code == 200