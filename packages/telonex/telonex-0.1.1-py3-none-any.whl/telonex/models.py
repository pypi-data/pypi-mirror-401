"""Data models for the Telonex SDK."""

from typing import Optional


def validate_identifiers(
    asset_id: Optional[str],
    market_id: Optional[str],
    slug: Optional[str],
    outcome: Optional[str],
    outcome_id: Optional[int],
) -> None:
    """
    Validate that exactly one valid identifier combination is provided.

    Valid combinations:
    1. asset_id alone
    2. market_id + outcome
    3. market_id + outcome_id
    4. slug + outcome
    5. slug + outcome_id

    Raises:
        ValueError: If validation fails
    """
    from telonex.exceptions import ValidationError

    has_asset_id = asset_id is not None
    has_market_id = market_id is not None
    has_slug = slug is not None
    has_outcome = outcome is not None
    has_outcome_id = outcome_id is not None

    # Can't have both outcome and outcome_id
    if has_outcome and has_outcome_id:
        raise ValidationError(
            "Cannot specify both 'outcome' and 'outcome_id'. Use one or the other."
        )

    # asset_id is exclusive - can't combine with market_id or slug
    if has_asset_id:
        if has_market_id or has_slug or has_outcome or has_outcome_id:
            raise ValidationError(
                "When using 'asset_id', do not provide market_id, slug, outcome, or outcome_id."
            )
        return  # Valid: asset_id alone

    # Can't have both market_id and slug
    if has_market_id and has_slug:
        raise ValidationError(
            "Cannot specify both 'market_id' and 'slug'. Use one or the other."
        )

    # market_id requires outcome or outcome_id
    if has_market_id:
        if not has_outcome and not has_outcome_id:
            raise ValidationError(
                "When using 'market_id', you must also provide 'outcome' or 'outcome_id'."
            )
        return  # Valid: market_id + outcome/outcome_id

    # slug requires outcome or outcome_id
    if has_slug:
        if not has_outcome and not has_outcome_id:
            raise ValidationError(
                "When using 'slug', you must also provide 'outcome' or 'outcome_id'."
            )
        return  # Valid: slug + outcome/outcome_id

    # No valid identifier provided
    raise ValidationError(
        "Must provide one of: 'asset_id', 'market_id' + outcome/outcome_id, "
        "or 'slug' + outcome/outcome_id."
    )
