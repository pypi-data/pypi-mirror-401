"""Tests for availability module."""

from telonex.availability import _build_query_params


class TestBuildQueryParams:
    def test_asset_id_only(self):
        params = _build_query_params(asset_id="123")
        assert params == {"asset_id": "123"}

    def test_market_id_with_outcome(self):
        params = _build_query_params(market_id="0xabc", outcome="Yes")
        assert params == {"market_id": "0xabc", "outcome": "Yes"}

    def test_slug_with_outcome_id(self):
        params = _build_query_params(slug="test-market", outcome_id=0)
        assert params == {"slug": "test-market", "outcome_id": 0}

    def test_empty_params(self):
        params = _build_query_params()
        assert params == {}
