"""
conftest.py — Shared pytest configuration

Sets up the test environment: ensures MODEL_PATH and SECRET_API_KEY
are available before any test imports app modules.
"""

import os

# Ensure environment variables are set for tests
os.environ.setdefault("MODEL_PATH", "models/digit_classifier_v1.pkl")
os.environ.setdefault("SECRET_API_KEY", "test-key")
os.environ.setdefault("DATABASE_URL", "sqlite:///test.db")
os.environ.setdefault("DEBUG", "true")
