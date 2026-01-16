# telonex

Python SDK for [Telonex](https://telonex.io) - prediction market data provider.

[![PyPI version](https://badge.fury.io/py/telonex.svg)](https://badge.fury.io/py/telonex)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Installation

```bash
pip install telonex
```

For DataFrame support:

```bash
pip install telonex[dataframe]  # pandas support
pip install telonex[polars]     # polars support
pip install telonex[all]        # both
```

## Quick Start

### Download Data to Disk

```python
from telonex import download

# Download using asset_id
download(
    api_key="your-api-key",
    exchange="polymarket",
    channel="quotes",
    asset_id="21742633143463906290569050155826241533067272736897614950488156847949938836455",
    from_date="2025-01-01",
    to_date="2025-01-07",
    download_dir="./data",
)

# Download using slug + outcome
download(
    api_key="your-api-key",
    exchange="polymarket",
    channel="book_snapshot_5",
    slug="will-trump-win-2024",
    outcome="Yes",
    from_date="2025-01-01",
    to_date="2025-01-07",
)
```

### Load Directly into DataFrame

```python
from telonex import get_dataframe

# Load into pandas DataFrame
df = get_dataframe(
    api_key="your-api-key",
    exchange="polymarket",
    channel="quotes",
    slug="will-trump-win-2024",
    outcome="Yes",
    from_date="2025-01-01",
    to_date="2025-01-07",
)

# Load into polars DataFrame
df = get_dataframe(
    api_key="your-api-key",
    exchange="polymarket",
    channel="quotes",
    asset_id="21742633...",
    from_date="2025-01-01",
    to_date="2025-01-07",
    engine="polars",
)
```

### Async Support

```python
import asyncio
from telonex import download_async

async def main():
    await download_async(
        api_key="your-api-key",
        exchange="polymarket",
        channel="book_snapshot_5",
        asset_id="21742633...",
        from_date="2025-01-01",
        to_date="2025-01-07",
    )

asyncio.run(main())
```

### Check Data Availability

```python
from telonex import get_availability

# Check what date ranges are available (no API key required)
availability = get_availability(
    exchange="polymarket",
    asset_id="21742633143463906290569050155826241533067272736897614950488156847949938836455",
)

# Returns a dict with channel availability
for channel, dates in availability["channels"].items():
    print(f"{channel}: {dates['from_date']} to {dates['to_date']}")
```

## Identifier Options

You can identify the data you want using one of these combinations:

| Option | Parameters | Example |
|--------|-----------|---------|
| Asset ID | `asset_id` | `asset_id="21742633..."` |
| Market ID + Outcome | `market_id`, `outcome` | `market_id="0xabc...", outcome="Yes"` |
| Market ID + Outcome ID | `market_id`, `outcome_id` | `market_id="0xabc...", outcome_id=0` |
| Slug + Outcome | `slug`, `outcome` | `slug="will-trump-win", outcome="Yes"` |
| Slug + Outcome ID | `slug`, `outcome_id` | `slug="will-trump-win", outcome_id=0` |

## Available Channels

| Channel | Description |
|---------|-------------|
| `quotes` | Trade quotes/prices |
| `book_snapshot_5` | Order book snapshots (top 5 levels) |
| `book_snapshot_25` | Order book snapshots (top 25 levels) |
| `book_snapshot_full` | Full order book snapshots |
| `transactions` | On-chain transactions |

## Parameters

### `download()` / `download_async()`

**Returns:** `List[str]` - List of downloaded file paths

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | str | required | Telonex API key |
| `exchange` | str | required | Exchange name (e.g., "polymarket") |
| `channel` | str | required | Data channel |
| `from_date` | str | required | Start date (inclusive), YYYY-MM-DD |
| `to_date` | str | required | End date (exclusive), YYYY-MM-DD |
| `download_dir` | str | `"./datasets"` | Directory to save files |
| `concurrency` | int | 5 | Max concurrent downloads |
| `verbose` | bool | False | Enable verbose logging |

### `get_dataframe()`

**Returns:** `pandas.DataFrame` or `polars.DataFrame`

Same parameters as above, plus:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `engine` | str | `"pandas"` | DataFrame engine ("pandas" or "polars") |
| `cache_dir` | str | None | Cache directory (temp dir if None) |

### `get_availability()` / `get_availability_async()`

**Returns:** `dict` - Availability info with channel date ranges

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `exchange` | str | required | Exchange name (e.g., "polymarket") |
| `asset_id` | str | None | Asset/token ID |
| `market_id` | str | None | Market ID (requires outcome) |
| `slug` | str | None | Market slug (requires outcome) |
| `outcome` | str | None | Outcome label (e.g., "Yes") |
| `outcome_id` | int | None | Outcome index (0 or 1) |

*Note: No API key required for availability endpoints.*

## Error Handling

```python
from telonex import (
    download,
    get_availability,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    EntitlementError,
)

# Download errors
try:
    download(...)
except AuthenticationError:
    print("Invalid API key")
except RateLimitError as e:
    print(f"Rate limited, retry after {e.retry_after}s")
except EntitlementError as e:
    print(f"Access denied. Downloads remaining: {e.downloads_remaining}")
```

## Caching

Downloaded files are cached locally. If a file already exists, it won't be re-downloaded. To force re-download, delete the cached file or use a different `download_dir`.

## Links

- [Telonex Website](https://telonex.io)
- [API Documentation](https://telonex.io/docs)
