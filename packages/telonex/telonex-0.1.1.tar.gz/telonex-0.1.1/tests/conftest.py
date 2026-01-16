"""Pytest configuration and fixtures."""

import os

import pytest


@pytest.fixture
def api_key():
    """Get API key from environment or skip test."""
    key = os.environ.get("TELONEX_API_KEY")
    if not key:
        pytest.skip("TELONEX_API_KEY not set")
    return key


@pytest.fixture
def temp_download_dir(tmp_path):
    """Create a temporary download directory."""
    download_dir = tmp_path / "downloads"
    download_dir.mkdir()
    return str(download_dir)
