"""
Telonex Python SDK

Python client for Telonex prediction market data API.

Example:
    >>> from telonex import download, get_dataframe
    >>>
    >>> # Download data to disk
    >>> download(
    ...     api_key="your-api-key",
    ...     exchange="polymarket",
    ...     channel="quotes",
    ...     asset_id="21742633...",
    ...     from_date="2025-01-01",
    ...     to_date="2025-01-07",
    ... )
    >>>
    >>> # Or load directly into DataFrame
    >>> df = get_dataframe(
    ...     api_key="your-api-key",
    ...     exchange="polymarket",
    ...     channel="quotes",
    ...     slug="will-trump-win-2024",
    ...     outcome="Yes",
    ...     from_date="2025-01-01",
    ...     to_date="2025-01-07",
    ... )
"""

from telonex._version import __version__
from telonex.availability import get_availability, get_availability_async
from telonex.download import download, download_async
from telonex.exceptions import (
    AuthenticationError,
    DownloadError,
    EntitlementError,
    NotFoundError,
    RateLimitError,
    TelonexError,
    ValidationError,
)


# Optional DataFrame support - import lazily to avoid requiring pandas/polars
def get_dataframe(*args, **kwargs):
    """
    Download market data and return as a DataFrame.

    Requires optional dependencies:
        pip install telonex[dataframe]  # for pandas
        pip install telonex[polars]     # for polars

    See telonex.dataframe.get_dataframe for full documentation.
    """
    from telonex.dataframe import get_dataframe as _get_dataframe

    return _get_dataframe(*args, **kwargs)


__all__ = [
    # Version
    "__version__",
    # Core functions
    "download",
    "download_async",
    "get_availability",
    "get_availability_async",
    "get_dataframe",
    # Exceptions
    "TelonexError",
    "AuthenticationError",
    "NotFoundError",
    "RateLimitError",
    "ValidationError",
    "DownloadError",
    "EntitlementError",
]
