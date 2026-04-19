"""
test_api.py — Boilerplate tests for the FastAPI endpoints

Provided as starter code for Block 8 (CI/CD).
Uses FastAPI's TestClient — no running server required.

Run with:
    pytest tests/test_api.py -v

Requirements:
    pip install httpx  (FastAPI TestClient dependency)
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

# The API key must match what's in .env for tests to pass.
# In CI, set the SECRET_API_KEY environment variable.
import os

API_KEY = os.getenv("SECRET_API_KEY", "test-key")


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


class TestHealthEndpoint:
    """Tests for GET /health."""

    def test_health_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_has_status_field(self, client):
        data = client.get("/health").json()
        assert "status" in data

    def test_health_has_model_version(self, client):
        data = client.get("/health").json()
        assert "model_version" in data


class TestClassifyEndpoint:
    """Tests for POST /classify."""

    def _make_pixels(self, value=0):
        """Create a 28×28 pixel array filled with a given value."""
        return [[value] * 28 for _ in range(28)]

    def test_classify_returns_200(self, client):
        response = client.post(
            "/classify",
            json={"pixels": self._make_pixels()},
            headers={"X-API-Key": API_KEY},
        )
        assert response.status_code == 200

    def test_classify_returns_prediction(self, client):
        response = client.post(
            "/classify",
            json={"pixels": self._make_pixels()},
            headers={"X-API-Key": API_KEY},
        )
        data = response.json()
        assert "prediction" in data
        assert "confidence" in data
        assert "scores" in data

    def test_classify_rejects_wrong_shape(self, client):
        """A 10×10 array should be rejected."""
        bad_pixels = [[0] * 10 for _ in range(10)]
        response = client.post(
            "/classify",
            json={"pixels": bad_pixels},
            headers={"X-API-Key": API_KEY},
        )
        assert response.status_code == 422

    def test_classify_rejects_missing_api_key(self, client):
        """Requests without X-API-Key should be rejected."""
        response = client.post(
            "/classify",
            json={"pixels": self._make_pixels()},
        )
        assert response.status_code in (401, 403, 422)


class TestResultsEndpoint:
    """Tests for GET /results."""

    def test_results_returns_200(self, client):
        response = client.get(
            "/results",
            headers={"X-API-Key": API_KEY},
        )
        assert response.status_code == 200
