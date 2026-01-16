"""
TradingData API for accessing trading research data.

Provides a structured API for accessing various trading data sources:
- KRX (Korea Exchange): Stocks, indices, investor data
- More markets to be added in the future

Usage:
    from finter.data import TradingData

    # Discovery
    TradingData.krx.list_datasets()           # List available datasets
    TradingData.krx.describe("trade")         # Get dataset schema/metadata

    # Aggregated data (OHLCV)
    df = TradingData.krx.agg.get(
        dataset="trade",
        symbol="KR7005930003",
        start="20250101",
        end="20250131",
        interval="1m"
    )

    # Raw data (AVRO from KRX)
    df = TradingData.krx.raw.get(tr_code="Z6000", date="20260109")
"""

import json
from typing import Any, Dict, List, Optional

import pandas as pd

from finter.settings import logger


# S3 catalog configuration
CATALOG_BUCKET = "quanda-data-production"
CATALOG_PATH = "mft/catalog.json"

# Module-level cache for catalog
_catalog_cache: Optional[Dict] = None


def _fetch_catalog(force_refresh: bool = False) -> Dict:
    """
    Fetch catalog from S3 with caching.

    Args:
        force_refresh: If True, bypass cache and fetch fresh catalog

    Returns:
        Dict containing catalog data
    """
    global _catalog_cache

    if _catalog_cache is not None and not force_refresh:
        return _catalog_cache

    try:
        from finter.framework_model.quanda_loader import get_aws_credentials
        import s3fs

        credentials = get_aws_credentials(
            object_type="name",
            object_value="mft/*",
            bucket=CATALOG_BUCKET,
            personal=False,
        )

        if credentials is None:
            logger.warning("Failed to get credentials for catalog, using fallback")
            return _get_fallback_catalog()

        fs = s3fs.S3FileSystem(
            key=credentials.aws_access_key_id,
            secret=credentials.aws_secret_access_key,
            token=credentials.aws_session_token,
        )

        s3_path = f"{CATALOG_BUCKET}/{CATALOG_PATH}"

        with fs.open(s3_path, "r") as f:
            _catalog_cache = json.load(f)

        logger.debug(f"Loaded catalog from s3://{s3_path}")
        return _catalog_cache

    except Exception as e:
        logger.warning(f"Failed to fetch catalog from S3: {e}. Using fallback.")
        return _get_fallback_catalog()


def _get_fallback_catalog() -> Dict:
    """Return minimal fallback catalog when S3 fetch fails."""
    return {
        "version": "fallback",
        "krx": {
            "raw": {
                "description": "KRX TR codes (AVRO format)",
                "requires": ["tr_code", "date"],
            },
            "agg": {
                "trade": {
                    "description": "1-minute aggregated trade data for KRX stocks",
                    "intervals": ["1m"],
                    "available_from": "2023-01-24",
                    "columns": [
                        "timestamp",
                        "board_id",
                        "session_id",
                        "open",
                        "high",
                        "low",
                        "close",
                        "trading_volume",
                        "trading_value",
                        "trading_count",
                        "buy_volume",
                        "buy_value",
                        "buy_count",
                        "sell_volume",
                        "sell_value",
                        "sell_count",
                    ],
                }
            },
        },
    }


class KrxRawNamespace:
    """
    Namespace for KRX raw data access (AVRO files from KRX).
    Access via TradingData.krx.raw
    """

    @staticmethod
    def get(tr_code: str, date: str) -> pd.DataFrame:
        """
        Load raw KRX TR data from GCS.

        Args:
            tr_code: TR code for the data (e.g., "Z6000")
            date: Date string in YYYYMMDD format (e.g., "20260109")

        Returns:
            pd.DataFrame: Raw KRX data as a pandas DataFrame

        Example:
            >>> from finter.data import TradingData
            >>> df = TradingData.krx.raw.get(tr_code="Z6000", date="20260109")
        """
        from finter.framework_model.gcs_credentials import load_krx_avro

        return load_krx_avro(date=date, tr_code=tr_code)

    @staticmethod
    def describe() -> Dict:
        """Get metadata about raw KRX data."""
        catalog = _fetch_catalog()
        return catalog.get("krx", {}).get("raw", {})


class KrxAggNamespace:
    """
    Namespace for KRX aggregated data access (OHLCV from S3 Parquet).
    Access via TradingData.krx.agg
    """

    @staticmethod
    def get(
        dataset: str,
        symbol: str,
        start: str,
        end: str,
        interval: str = "1m",
        columns: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """
        Load aggregated KRX data from S3.

        Args:
            dataset: Dataset type ("trade" for OHLCV)
            symbol: KRX symbol code (e.g., "KR7005930003" for Samsung)
            start: Start date in YYYYMMDD format (e.g., "20250101")
            end: End date in YYYYMMDD format (e.g., "20250131")
            interval: Time interval - "1m" (1 minute) (default: "1m")
            columns: Optional list of columns to load (default: all)

        Returns:
            pd.DataFrame: Aggregated data with columns like timestamp, open, high, low, close, volume

        Raises:
            ValueError: If dataset is invalid or date format is wrong

        Example:
            >>> from finter.data import TradingData
            >>> df = TradingData.krx.agg.get(
            ...     dataset="trade",
            ...     symbol="KR7005930003",
            ...     start="20250101",
            ...     end="20250115"
            ... )
        """
        # Validate dataset against catalog
        catalog = _fetch_catalog()
        agg_datasets = catalog.get("krx", {}).get("agg", {})

        if dataset not in agg_datasets:
            valid_datasets = list(agg_datasets.keys())
            raise ValueError(
                f"Invalid dataset: '{dataset}'. Valid options: {valid_datasets}"
            )

        from finter.framework_model.mft_loader import load_mft_data

        return load_mft_data(
            symbol=symbol,
            start_date=start,
            end_date=end,
            data_type=dataset,
            interval=interval,
            columns=columns,
        )

    @staticmethod
    def list_datasets() -> List[str]:
        """List available aggregated datasets."""
        catalog = _fetch_catalog()
        return list(catalog.get("krx", {}).get("agg", {}).keys())

    @staticmethod
    def describe(dataset: str) -> Dict:
        """
        Get metadata about a specific aggregated dataset.

        Args:
            dataset: Dataset name (e.g., "trade")

        Returns:
            Dict with dataset metadata
        """
        catalog = _fetch_catalog()
        agg_datasets = catalog.get("krx", {}).get("agg", {})

        if dataset not in agg_datasets:
            valid_datasets = list(agg_datasets.keys())
            raise ValueError(
                f"Unknown dataset: '{dataset}'. Available: {valid_datasets}"
            )

        return agg_datasets[dataset]


class KrxNamespace:
    """
    Namespace for KRX (Korea Exchange) data.
    Access via TradingData.krx
    """

    raw = KrxRawNamespace()
    agg = KrxAggNamespace()

    @staticmethod
    def list_datasets() -> Dict[str, Any]:
        """
        List all available datasets for KRX.

        Returns:
            Dict with 'raw' and 'agg' dataset info

        Example:
            >>> TradingData.krx.list_datasets()
            {'raw': {...}, 'agg': {'trade': {...}}}
        """
        catalog = _fetch_catalog()
        krx = catalog.get("krx", {})
        return {
            "raw": krx.get("raw", {}),
            "agg": krx.get("agg", {}),
        }

    @staticmethod
    def describe(dataset: str) -> Dict:
        """
        Get metadata about a specific dataset.

        Args:
            dataset: Dataset name (e.g., "trade", "raw")

        Returns:
            Dict with dataset metadata
        """
        catalog = _fetch_catalog()
        krx = catalog.get("krx", {})

        # Check if it's raw
        if dataset == "raw":
            return krx.get("raw", {})

        # Check agg datasets
        agg_datasets = krx.get("agg", {})
        if dataset in agg_datasets:
            return agg_datasets[dataset]

        # Not found
        available = ["raw"] + list(agg_datasets.keys())
        raise ValueError(f"Unknown dataset: '{dataset}'. Available: {available}")

    @staticmethod
    def help() -> str:
        """Print help information for KRX data access."""
        catalog = _fetch_catalog()
        krx = catalog.get("krx", {})

        help_lines = [
            "KRX (Korea Exchange) Data API",
            "=" * 30,
            "",
            "Discovery:",
            "    TradingData.krx.list_datasets()      # List available datasets",
            "    TradingData.krx.describe('trade')    # Get dataset metadata",
            "",
            "Raw Data (AVRO from KRX):",
            "    df = TradingData.krx.raw.get(tr_code='Z6000', date='20260109')",
            "",
            "Aggregated Data:",
        ]

        # Add agg datasets from catalog
        for name, info in krx.get("agg", {}).items():
            desc = info.get("description", "")
            example = info.get("example", "")
            help_lines.append(f"    - {name}: {desc}")
            if example:
                help_lines.append(f"      {example}")

        help_str = "\n".join(help_lines)
        logger.info(help_str)
        return help_str

    @staticmethod
    def refresh_catalog() -> Dict:
        """Force refresh catalog from S3."""
        return _fetch_catalog(force_refresh=True)


class TradingData:
    """
    Main entry point for trading research data.

    Markets:
        - krx: Korea Exchange data

    Example:
        >>> from finter.data import TradingData
        >>>
        >>> # Discovery
        >>> TradingData.krx.list_datasets()
        >>> TradingData.krx.describe("trade")
        >>>
        >>> # Load aggregated trade data
        >>> df = TradingData.krx.agg.get(
        ...     dataset="trade",
        ...     symbol="KR7005930003",
        ...     start="20250101",
        ...     end="20250131"
        ... )
        >>>
        >>> # Load raw KRX data
        >>> df = TradingData.krx.raw.get(tr_code="Z6000", date="20260109")
    """

    krx = KrxNamespace()

    @staticmethod
    def help() -> str:
        """Print help information for TradingData."""
        help_str = """
TradingData - Trading Research Data API
========================================

Available Markets:
    - TradingData.krx    # Korea Exchange

Usage:
    from finter.data import TradingData

    # List datasets for a market
    TradingData.krx.list_datasets()

    # Get dataset metadata
    TradingData.krx.describe("trade")

    # Load aggregated data
    df = TradingData.krx.agg.get(dataset="trade", symbol="...", start="...", end="...")

    # Load raw data
    df = TradingData.krx.raw.get(tr_code="...", date="...")

For market-specific help:
    TradingData.krx.help()
"""
        logger.info(help_str)
        return help_str

    @staticmethod
    def refresh_catalog() -> Dict:
        """Force refresh catalog from S3 for all markets."""
        return _fetch_catalog(force_refresh=True)
