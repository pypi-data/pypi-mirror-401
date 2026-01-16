"""Tests for config constants."""

from telonex.download import API_BASE_URL


def test_api_base_url():
    assert API_BASE_URL == "https://api.telonex.io"
