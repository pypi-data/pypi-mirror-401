"""Tests for API endpoints.

Copyright (c) Krishnakanth Allika
License: CC-BY-NC-SA-4.0
"""

import pytest
from fastapi.testclient import TestClient
from fetchyt.api import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200


def test_health_endpoint():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_extract_endpoint_missing_url():
    """Test extract endpoint with missing URL."""
    response = client.post("/api/v1/extract", json={})
    assert response.status_code == 422  # Validation error


def test_extract_endpoint_invalid_url():
    """Test extract endpoint with invalid URL."""
    response = client.post("/api/v1/extract", json={"url": "not-a-valid-url"})
    assert response.status_code == 400


def test_download_endpoint_missing_url():
    """Test download endpoint with missing URL."""
    response = client.post("/api/v1/download", json={})
    assert response.status_code == 422  # Validation error


def test_status_endpoint_not_found():
    """Test status endpoint with non-existent task."""
    response = client.get("/api/v1/status/non-existent-task")
    assert response.status_code == 404


def test_cleanup_endpoint():
    """Test cleanup endpoint."""
    response = client.delete("/api/v1/task/some-task-id")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
