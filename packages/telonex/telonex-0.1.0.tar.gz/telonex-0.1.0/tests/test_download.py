"""Tests for download module."""

from datetime import datetime

import pytest

from telonex.download import (
    _build_query_params,
    _default_get_filename,
    _generate_dates,
    _get_identifier_str,
    _parse_date,
)


class TestParseDate:
    def test_parses_date_string(self):
        result = _parse_date("2025-01-15")
        assert result.year == 2025
        assert result.month == 1
        assert result.day == 15

    def test_parses_iso_datetime(self):
        result = _parse_date("2025-01-15T10:30:00")
        assert result.year == 2025
        assert result.hour == 10


class TestGenerateDates:
    def test_generates_date_range(self):
        dates = _generate_dates("2025-01-01", "2025-01-05")
        assert len(dates) == 4  # Exclusive end
        assert dates[0].day == 1
        assert dates[-1].day == 4

    def test_empty_range(self):
        dates = _generate_dates("2025-01-01", "2025-01-01")
        assert len(dates) == 0

    def test_single_day(self):
        dates = _generate_dates("2025-01-01", "2025-01-02")
        assert len(dates) == 1
        assert dates[0].day == 1


class TestBuildQueryParams:
    def test_asset_id_only(self):
        params = _build_query_params(asset_id="123")
        assert params == {"asset_id": "123"}

    def test_market_id_with_outcome(self):
        params = _build_query_params(market_id="0xabc", outcome="Yes")
        assert params == {"market_id": "0xabc", "outcome": "Yes"}

    def test_slug_with_outcome_id(self):
        params = _build_query_params(slug="test", outcome_id=0)
        assert params == {"slug": "test", "outcome_id": 0}

    def test_empty_params(self):
        params = _build_query_params()
        assert params == {}


class TestGetIdentifierStr:
    def test_asset_id(self):
        result = _get_identifier_str(asset_id="12345678901234567890")
        assert result == "12345678901234567890"  # Full asset_id

    def test_short_asset_id(self):
        result = _get_identifier_str(asset_id="short")
        assert result == "short"

    def test_market_id_with_outcome(self):
        result = _get_identifier_str(market_id="0xabc", outcome="Yes")
        assert result == "0xabc_Yes"

    def test_slug_with_outcome_id(self):
        result = _get_identifier_str(slug="test-market", outcome_id=1)
        assert result == "test-market_1"


class TestDefaultGetFilename:
    def test_generates_filename(self):
        date = datetime(2025, 1, 15)
        result = _default_get_filename("polymarket", "quotes", date, "test123")
        assert result == "polymarket_quotes_2025-01-15_test123.parquet"
