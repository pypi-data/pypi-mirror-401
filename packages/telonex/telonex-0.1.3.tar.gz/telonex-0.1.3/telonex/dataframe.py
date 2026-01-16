"""DataFrame integration for the Telonex SDK.

Requires optional dependencies:
    pip install telonex[dataframe]  # for pandas
    pip install telonex[polars]     # for polars
    pip install telonex[all]        # for both
"""

from typing import TYPE_CHECKING, List, Literal, Optional, Union

from telonex.download import download

if TYPE_CHECKING:
    import pandas as pd
    import polars as pl


def get_dataframe(
    api_key: str,
    exchange: str,
    channel: str,
    from_date: str,
    to_date: str,
    asset_id: Optional[str] = None,
    market_id: Optional[str] = None,
    slug: Optional[str] = None,
    outcome: Optional[str] = None,
    outcome_id: Optional[int] = None,
    engine: Literal["pandas", "polars"] = "pandas",
    download_dir: str = "./datasets",
    verbose: bool = False,
) -> Union["pd.DataFrame", "pl.DataFrame"]:
    """
    Download market data and return as a DataFrame.

    Args:
        api_key: Telonex API key (required)
        exchange: Exchange name (e.g., "polymarket")
        channel: Data channel (e.g., "quotes", "book_snapshot_5")
        from_date: Start date (inclusive) in YYYY-MM-DD format
        to_date: End date (exclusive) in YYYY-MM-DD format
        asset_id: Direct asset/token ID
        market_id: Market ID (requires outcome or outcome_id)
        slug: Market slug (requires outcome or outcome_id)
        outcome: Outcome label (e.g., "Yes", "No")
        outcome_id: Outcome index (0 or 1)
        engine: DataFrame engine - "pandas" or "polars" (default: pandas)
        download_dir: Directory to save files (default: ./datasets)
        verbose: Enable verbose logging (default: False)

    Returns:
        DataFrame with the market data (pandas or polars based on engine)

    Raises:
        ImportError: If required dependencies not installed
        ValidationError: If identifier parameters are invalid
        AuthenticationError: If API key is invalid
        NotFoundError: If data not found

    Example:
        >>> df = get_dataframe(
        ...     api_key="your-api-key",
        ...     exchange="polymarket",
        ...     channel="quotes",
        ...     slug="will-trump-win-2024",
        ...     outcome="Yes",
        ...     from_date="2025-01-01",
        ...     to_date="2025-01-07"
        ... )
    """
    # Download files
    files = download(
        api_key=api_key,
        exchange=exchange,
        channel=channel,
        from_date=from_date,
        to_date=to_date,
        download_dir=download_dir,
        asset_id=asset_id,
        market_id=market_id,
        slug=slug,
        outcome=outcome,
        outcome_id=outcome_id,
        verbose=verbose,
    )

    if not files:
        # Return empty DataFrame
        if engine == "polars":
            return _empty_polars_df()
        else:
            return _empty_pandas_df()

    # Load into DataFrame
    if engine == "polars":
        return _load_polars(files)
    else:
        return _load_pandas(files)


def _load_pandas(files: List[str]) -> "pd.DataFrame":
    """Load parquet files into pandas DataFrame."""
    try:
        import pandas as pd
    except ImportError:
        raise ImportError(
            "pandas is required for DataFrame support. "
            "Install with: pip install telonex[dataframe]"
        )

    import importlib.util

    if importlib.util.find_spec("pyarrow") is None:
        raise ImportError(
            "pyarrow is required for reading parquet files. "
            "Install with: pip install telonex[dataframe]"
        )

    if len(files) == 1:
        return pd.read_parquet(files[0])

    # Concatenate multiple files
    dfs = [pd.read_parquet(f) for f in files]
    return pd.concat(dfs, ignore_index=True)


def _load_polars(files: List[str]) -> "pl.DataFrame":
    """Load parquet files into polars DataFrame."""
    try:
        import polars as pl
    except ImportError:
        raise ImportError(
            "polars is required for polars DataFrame support. "
            "Install with: pip install telonex[polars]"
        )

    if len(files) == 1:
        return pl.read_parquet(files[0])

    # Concatenate multiple files
    dfs = [pl.read_parquet(f) for f in files]
    return pl.concat(dfs)


def _empty_pandas_df() -> "pd.DataFrame":
    """Return empty pandas DataFrame."""
    try:
        import pandas as pd

        return pd.DataFrame()
    except ImportError:
        raise ImportError(
            "pandas is required for DataFrame support. "
            "Install with: pip install telonex[dataframe]"
        )


def _empty_polars_df() -> "pl.DataFrame":
    """Return empty polars DataFrame."""
    try:
        import polars as pl

        return pl.DataFrame()
    except ImportError:
        raise ImportError(
            "polars is required for polars DataFrame support. "
            "Install with: pip install telonex[polars]"
        )
