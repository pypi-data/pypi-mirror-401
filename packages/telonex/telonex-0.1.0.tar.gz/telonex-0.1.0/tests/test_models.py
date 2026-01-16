"""Tests for models module."""

import pytest

from telonex.exceptions import ValidationError
from telonex.models import validate_identifiers


class TestValidateIdentifiers:
    def test_valid_asset_id_only(self):
        # Should not raise
        validate_identifiers(
            asset_id="123",
            market_id=None,
            slug=None,
            outcome=None,
            outcome_id=None,
        )

    def test_valid_market_id_with_outcome(self):
        validate_identifiers(
            asset_id=None,
            market_id="0xabc",
            slug=None,
            outcome="Yes",
            outcome_id=None,
        )

    def test_valid_market_id_with_outcome_id(self):
        validate_identifiers(
            asset_id=None,
            market_id="0xabc",
            slug=None,
            outcome=None,
            outcome_id=0,
        )

    def test_valid_slug_with_outcome(self):
        validate_identifiers(
            asset_id=None,
            market_id=None,
            slug="test-market",
            outcome="No",
            outcome_id=None,
        )

    def test_valid_slug_with_outcome_id(self):
        validate_identifiers(
            asset_id=None,
            market_id=None,
            slug="test-market",
            outcome=None,
            outcome_id=1,
        )

    def test_invalid_no_identifier(self):
        with pytest.raises(ValidationError, match="Must provide one of"):
            validate_identifiers(
                asset_id=None,
                market_id=None,
                slug=None,
                outcome=None,
                outcome_id=None,
            )

    def test_invalid_asset_id_with_market_id(self):
        with pytest.raises(ValidationError, match="When using 'asset_id'"):
            validate_identifiers(
                asset_id="123",
                market_id="0xabc",
                slug=None,
                outcome=None,
                outcome_id=None,
            )

    def test_invalid_asset_id_with_outcome(self):
        with pytest.raises(ValidationError, match="When using 'asset_id'"):
            validate_identifiers(
                asset_id="123",
                market_id=None,
                slug=None,
                outcome="Yes",
                outcome_id=None,
            )

    def test_invalid_both_outcome_and_outcome_id(self):
        with pytest.raises(ValidationError, match="Cannot specify both"):
            validate_identifiers(
                asset_id=None,
                market_id="0xabc",
                slug=None,
                outcome="Yes",
                outcome_id=0,
            )

    def test_invalid_both_market_id_and_slug(self):
        with pytest.raises(ValidationError, match="Cannot specify both"):
            validate_identifiers(
                asset_id=None,
                market_id="0xabc",
                slug="test",
                outcome="Yes",
                outcome_id=None,
            )

    def test_invalid_market_id_without_outcome(self):
        with pytest.raises(ValidationError, match="must also provide"):
            validate_identifiers(
                asset_id=None,
                market_id="0xabc",
                slug=None,
                outcome=None,
                outcome_id=None,
            )

    def test_invalid_slug_without_outcome(self):
        with pytest.raises(ValidationError, match="must also provide"):
            validate_identifiers(
                asset_id=None,
                market_id=None,
                slug="test",
                outcome=None,
                outcome_id=None,
            )
