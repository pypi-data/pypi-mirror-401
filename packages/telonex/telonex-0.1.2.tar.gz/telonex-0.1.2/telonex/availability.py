"""Availability functionality for the Telonex SDK."""

import asyncio
from typing import Any, Dict, Optional

import httpx

from telonex.constants import API_BASE_URL
from telonex.exceptions import NotFoundError, TelonexError
from telonex.models import validate_identifiers

# Default timeout (30 seconds)
DEFAULT_TIMEOUT = httpx.Timeout(30)


def get_availability(
    exchange: str,
    asset_id: Optional[str] = None,
    market_id: Optional[str] = None,
    slug: Optional[str] = None,
    outcome: Optional[str] = None,
    outcome_id: Optional[int] = None,
    timeout: httpx.Timeout = DEFAULT_TIMEOUT,
) -> Dict[str, Any]:
    """
    Get data availability for an asset.

    This endpoint is public and does not require authentication.

    Args:
        exchange: Exchange name (e.g., "polymarket")
        asset_id: Direct asset/token ID
        market_id: Market ID (requires outcome or outcome_id)
        slug: Market slug (requires outcome or outcome_id)
        outcome: Outcome label (e.g., "Yes", "No")
        outcome_id: Outcome index (0 or 1)
        timeout: HTTP timeout (default: 30 seconds)

    Returns:
        Dict with exchange info and channel date ranges

    Raises:
        ValidationError: If identifier parameters are invalid
        NotFoundError: If no data found for the identifier
        TelonexError: If the request fails
    """
    import nest_asyncio

    nest_asyncio.apply()

    return asyncio.run(
        get_availability_async(
            exchange=exchange,
            asset_id=asset_id,
            market_id=market_id,
            slug=slug,
            outcome=outcome,
            outcome_id=outcome_id,
            timeout=timeout,
        )
    )


async def get_availability_async(
    exchange: str,
    asset_id: Optional[str] = None,
    market_id: Optional[str] = None,
    slug: Optional[str] = None,
    outcome: Optional[str] = None,
    outcome_id: Optional[int] = None,
    timeout: httpx.Timeout = DEFAULT_TIMEOUT,
) -> Dict[str, Any]:
    """
    Async version of get_availability(). See get_availability() for documentation.
    """
    # Validate identifiers
    validate_identifiers(asset_id, market_id, slug, outcome, outcome_id)

    # Build query params
    params = _build_query_params(asset_id, market_id, slug, outcome, outcome_id)

    url = f"{API_BASE_URL}/v1/availability/{exchange}"

    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.get(url, params=params)

        if response.status_code == 404:
            raise NotFoundError(f"No data found for {exchange}", exchange=exchange)

        if response.status_code >= 400:
            raise TelonexError(f"Request failed: {response.text}")

        return response.json()


def _build_query_params(
    asset_id: Optional[str] = None,
    market_id: Optional[str] = None,
    slug: Optional[str] = None,
    outcome: Optional[str] = None,
    outcome_id: Optional[int] = None,
) -> dict:
    """Build query parameters dict from identifiers."""
    params: dict = {}
    if asset_id is not None:
        params["asset_id"] = asset_id
    if market_id is not None:
        params["market_id"] = market_id
    if slug is not None:
        params["slug"] = slug
    if outcome is not None:
        params["outcome"] = outcome
    if outcome_id is not None:
        params["outcome_id"] = outcome_id
    return params
