"""Download functionality for the Telonex SDK."""

import asyncio
import logging
import os
import pathlib
import random
import secrets
from datetime import datetime, timedelta
from typing import Callable, List, Optional

import aiofiles
import httpx
from dateutil import parser as date_parser

from telonex.constants import API_BASE_URL
from telonex.exceptions import (
    AuthenticationError,
    DownloadError,
    EntitlementError,
    NotFoundError,
    RateLimitError,
)
from telonex.models import validate_identifiers

logger = logging.getLogger(__name__)

# Default timeout for downloads (5 minutes)
DEFAULT_TIMEOUT = httpx.Timeout(5 * 60)

# Default filename format
DEFAULT_FILE_TEMPLATE = "{exchange}_{channel}_{date}_{identifier}.parquet"


def _default_get_filename(
    exchange: str,
    channel: str,
    date: datetime,
    identifier: str,
) -> str:
    """Generate default filename for downloaded file."""
    return f"{exchange}_{channel}_{date.strftime('%Y-%m-%d')}_{identifier}.parquet"


def _parse_date(date_str: str) -> datetime:
    """Parse date string to datetime object."""
    return date_parser.isoparse(date_str)


def _generate_dates(from_date: str, to_date: str) -> List[datetime]:
    """Generate list of dates between from_date and to_date (exclusive end)."""
    start = _parse_date(from_date)
    end = _parse_date(to_date)

    dates = []
    current = start
    while current < end:
        dates.append(current)
        current += timedelta(days=1)

    return dates


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


def _get_identifier_str(
    asset_id: Optional[str] = None,
    market_id: Optional[str] = None,
    slug: Optional[str] = None,
    outcome: Optional[str] = None,
    outcome_id: Optional[int] = None,
) -> str:
    """Get a string identifier for filename purposes."""
    if asset_id:
        return asset_id
    elif market_id:
        outcome_str = outcome if outcome else str(outcome_id)
        return f"{market_id}_{outcome_str}"
    elif slug:
        outcome_str = outcome if outcome else str(outcome_id)
        return f"{slug}_{outcome_str}"
    return "unknown"


def download(
    api_key: str,
    exchange: str,
    channel: str,
    from_date: str,
    to_date: str,
    download_dir: str = "./datasets",
    asset_id: Optional[str] = None,
    market_id: Optional[str] = None,
    slug: Optional[str] = None,
    outcome: Optional[str] = None,
    outcome_id: Optional[int] = None,
    get_filename: Optional[Callable[[str, str, datetime, str], str]] = None,
    timeout: httpx.Timeout = DEFAULT_TIMEOUT,
    concurrency: int = 5,
    verbose: bool = False,
) -> List[str]:
    """
    Download market data files to disk.

    Args:
        api_key: Telonex API key (required)
        exchange: Exchange name (e.g., "polymarket")
        channel: Data channel (e.g., "quotes", "book_snapshot_5")
        from_date: Start date (inclusive) in YYYY-MM-DD format
        to_date: End date (exclusive) in YYYY-MM-DD format
        download_dir: Directory to save files (default: ./datasets)
        asset_id: Direct asset/token ID
        market_id: Market ID (requires outcome or outcome_id)
        slug: Market slug (requires outcome or outcome_id)
        outcome: Outcome label (e.g., "Yes", "No")
        outcome_id: Outcome index (0 or 1)
        get_filename: Custom filename generator function
        timeout: HTTP timeout (default: 5 minutes)
        concurrency: Max concurrent downloads (default: 5)
        verbose: Enable verbose logging (default: False)

    Returns:
        List of downloaded file paths

    Raises:
        ValidationError: If identifier parameters are invalid
        AuthenticationError: If API key is invalid
        NotFoundError: If data not found
        RateLimitError: If rate limit exceeded
        DownloadError: If download fails
    """
    import nest_asyncio

    nest_asyncio.apply()

    return asyncio.run(
        download_async(
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
            get_filename=get_filename,
            timeout=timeout,
            concurrency=concurrency,
            verbose=verbose,
        )
    )


async def download_async(
    api_key: str,
    exchange: str,
    channel: str,
    from_date: str,
    to_date: str,
    download_dir: str = "./datasets",
    asset_id: Optional[str] = None,
    market_id: Optional[str] = None,
    slug: Optional[str] = None,
    outcome: Optional[str] = None,
    outcome_id: Optional[int] = None,
    get_filename: Optional[Callable[[str, str, datetime, str], str]] = None,
    timeout: httpx.Timeout = DEFAULT_TIMEOUT,
    concurrency: int = 5,
    verbose: bool = False,
) -> List[str]:
    """
    Async version of download(). See download() for documentation.
    """
    # Validate identifiers
    validate_identifiers(asset_id, market_id, slug, outcome, outcome_id)

    # Normalize exchange and channel
    exchange_str = str(exchange)
    channel_str = str(channel)

    # Generate dates
    dates = _generate_dates(from_date, to_date)
    if not dates:
        if verbose:
            logger.info(f"No dates to download between {from_date} and {to_date}")
        return []

    # Get filename generator
    filename_fn = get_filename or _default_get_filename
    identifier = _get_identifier_str(asset_id, market_id, slug, outcome, outcome_id)

    # Build query params
    query_params = _build_query_params(asset_id, market_id, slug, outcome, outcome_id)

    # Prepare download tasks
    downloaded_files: List[str] = []

    headers = {"Authorization": f"Bearer {api_key}"}

    async with httpx.AsyncClient(
        timeout=timeout,
        headers=headers,
        follow_redirects=True,
    ) as client:
        # Semaphore for concurrency control
        semaphore = asyncio.Semaphore(concurrency)

        async def download_one(date: datetime) -> Optional[str]:
            async with semaphore:
                date_str = date.strftime("%Y-%m-%d")
                url = f"{API_BASE_URL}/v1/downloads/{exchange_str}/{channel_str}/{date_str}"

                filename = filename_fn(exchange_str, channel_str, date, identifier)
                download_path = os.path.join(download_dir, filename)

                try:
                    return await _reliably_download_file(
                        client, url, download_path, query_params, verbose=verbose
                    )
                except Exception as e:
                    logger.error(f"Failed to download {date_str}: {e}")
                    raise

        # Create tasks
        tasks = [download_one(date) for date in dates]

        # Run with exception handling
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        for result in results:
            if isinstance(result, BaseException):
                raise result
            if result is not None:
                downloaded_files.append(result)

    return downloaded_files


async def _reliably_download_file(
    client: httpx.AsyncClient,
    url: str,
    download_path: str,
    params: dict,
    max_attempts: int = 5,
    verbose: bool = False,
) -> Optional[str]:
    """
    Download a file with retry logic.

    Returns:
        Path to downloaded file, or None if file already exists
    """
    # Skip if file already exists
    if os.path.exists(download_path):
        if verbose:
            logger.info(f"File already exists: {download_path}")
        return download_path

    attempts = 0

    while True:
        attempts += 1

        try:
            return await _download_file(client, url, download_path, params)

        except asyncio.CancelledError:
            raise

        except (AuthenticationError, EntitlementError):
            # Don't retry auth errors
            raise

        except NotFoundError:
            # Log 404s and continue - data may not exist for this date
            logger.warning(f"Data not found: {url}")
            return None

        except RateLimitError as e:
            if attempts >= max_attempts:
                raise

            # Longer delay for rate limits
            delay = e.retry_after or (3 * attempts + random.random())
            if verbose:
                logger.info(f"Rate limited, retrying in {delay:.1f}s: {url}")
            await asyncio.sleep(delay)

        except Exception as e:
            if attempts >= max_attempts:
                raise

            # Exponential backoff
            delay = (2**attempts) + random.random()
            if verbose:
                logger.info(f"Download failed, retry {attempts}/{max_attempts}: {e}")
            await asyncio.sleep(delay)


async def _download_file(
    client: httpx.AsyncClient,
    url: str,
    download_path: str,
    params: dict,
) -> str:
    """
    Download a single file.

    The API returns a redirect to a presigned S3 URL.
    """
    response = await client.get(url, params=params)

    # Handle error responses
    if response.status_code == 401:
        raise AuthenticationError("Invalid or missing API key")

    if response.status_code == 403:
        # Check for downloads remaining header
        remaining = response.headers.get("X-Downloads-Remaining", "0")
        try:
            text = response.text
            raise EntitlementError(text, downloads_remaining=int(remaining))
        except ValueError:
            raise EntitlementError("Access denied", downloads_remaining=0)

    if response.status_code == 404:
        raise NotFoundError(f"Data not found: {url}", date=url.split("/")[-1])

    if response.status_code == 429:
        retry_after = int(response.headers.get("Retry-After", "60"))
        raise RateLimitError("Rate limit exceeded", retry_after=retry_after)

    if response.status_code >= 400:
        raise DownloadError(
            f"Download failed: {response.text}",
            url=url,
            status_code=response.status_code,
        )

    # Ensure directory exists
    pathlib.Path(download_path).parent.mkdir(parents=True, exist_ok=True)

    # Write to temp file first
    temp_path = f"{download_path}.{secrets.token_hex(8)}.tmp"

    try:
        async with aiofiles.open(temp_path, "wb") as f:
            await f.write(response.content)

        # Rename to final path
        try:
            os.replace(temp_path, download_path)
        except OSError:
            # File might already exist from concurrent download
            if os.path.exists(download_path):
                os.remove(temp_path)
                return download_path
            raise

        return download_path

    finally:
        # Cleanup temp file if it still exists
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass
