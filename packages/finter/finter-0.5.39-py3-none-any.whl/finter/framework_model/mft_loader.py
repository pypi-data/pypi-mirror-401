"""
MFT (Minute-Frequency Trade) OHLCV data loader.
Loads KRX stock OHLCV data from S3 Hive-partitioned Parquet files.
"""

import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import List

import pandas as pd
import s3fs

from finter.framework_model.quanda_loader import get_aws_credentials
from finter.settings import logger


# S3 Configuration
MFT_BUCKET = "quanda-data-production"
MFT_PATH_TEMPLATE = "mft/{interval}/type={data_type}/symbol={symbol}/month={month}/data.parquet"


def _build_s3_paths(
    symbol: str,
    start_date: str,
    end_date: str,
    data_type: str = "trade",
    interval: str = "1m"
) -> List[str]:
    """
    Build list of S3 paths for the date range.

    Args:
        symbol: KRX symbol code (e.g., "KR7005930003")
        start_date: Start date in YYYYMMDD format
        end_date: End date in YYYYMMDD format
        data_type: Data type ("trade" or "quote")
        interval: Time interval ("1m", "10s", etc.)

    Returns:
        List of S3 paths to Parquet files
    """
    start = datetime.strptime(start_date, "%Y%m%d")
    end = datetime.strptime(end_date, "%Y%m%d")

    paths = []
    current = start.replace(day=1)  # Start of month

    while current <= end:
        month_str = current.strftime("%Y-%m")
        path = MFT_PATH_TEMPLATE.format(
            interval=interval,
            data_type=data_type,
            symbol=symbol,
            month=month_str
        )
        paths.append(f"s3://{MFT_BUCKET}/{path}")
        current += relativedelta(months=1)

    return paths


def load_mft_data(
    symbol: str,
    start_date: str,
    end_date: str,
    data_type: str = "trade",
    interval: str = "1m",
    columns: List[str] = None
) -> pd.DataFrame:
    """
    Load MFT OHLCV data from S3.

    Args:
        symbol: KRX symbol code (e.g., "KR7005930003")
        start_date: Start date in YYYYMMDD format
        end_date: End date in YYYYMMDD format
        data_type: "trade" for OHLCV, "quote" for bid/ask (default: "trade")
        interval: Time interval - "1m" for 1 minute, "10s" for 10 seconds (default: "1m")
        columns: Optional list of columns to load (default: all)

    Returns:
        pd.DataFrame with OHLCV data, filtered to date range

    Raises:
        ValueError: If date format is invalid
        PermissionError: If credentials cannot be obtained

    Example:
        >>> df = load_mft_data("KR7005930003", "20250101", "20250115")
        >>> df = load_mft_data("KR7005930003", "20250101", "20250115", interval="10s")
    """
    # Validate date format
    date_pattern = r'^\d{8}$'
    if not re.match(date_pattern, start_date):
        raise ValueError(f"Invalid date format: {start_date}. Expected YYYYMMDD format.")
    if not re.match(date_pattern, end_date):
        raise ValueError(f"Invalid date format: {end_date}. Expected YYYYMMDD format.")

    # Get AWS credentials once with wildcard for all mft files
    credentials = get_aws_credentials(
        object_type="name",
        object_value="mft/*",
        bucket=MFT_BUCKET,
        personal=False
    )

    if credentials is None:
        raise PermissionError("Failed to get AWS credentials for MFT data")

    # Create S3 filesystem with credentials
    fs = s3fs.S3FileSystem(
        key=credentials.aws_access_key_id,
        secret=credentials.aws_secret_access_key,
        token=credentials.aws_session_token
    )

    # Build S3 paths
    paths = _build_s3_paths(symbol, start_date, end_date, data_type, interval)

    # Read Parquet files
    all_dfs = []
    for path in paths:
        try:
            # Remove s3:// prefix for s3fs
            s3_path = path.replace("s3://", "")

            with fs.open(s3_path, "rb") as f:
                df = pd.read_parquet(f, columns=columns, engine="pyarrow")
                all_dfs.append(df)

        except FileNotFoundError:
            logger.warning(f"File not found: {path}")
            continue
        except Exception as e:
            logger.warning(f"Error reading {path}: {e}")
            continue

    if not all_dfs:
        logger.warning(f"No data found for {symbol} between {start_date} and {end_date}")
        return pd.DataFrame()

    # Combine all data
    result = pd.concat(all_dfs, ignore_index=True)

    # Filter to exact date range and convert to KST (Korean stocks)
    if "timestamp" in result.columns:
        result["timestamp"] = pd.to_datetime(result["timestamp"])

        # Parse dates as KST (Korea Standard Time) since input dates are KST
        KST = "Asia/Seoul"
        start_dt = pd.to_datetime(start_date).tz_localize(KST)
        end_dt = (pd.to_datetime(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)).tz_localize(KST)

        # Convert timestamp to KST for comparison and output
        if result["timestamp"].dt.tz is not None:
            # Data has timezone, convert to KST
            result["timestamp"] = result["timestamp"].dt.tz_convert(KST)
        else:
            # Data is naive (assumed UTC), localize as UTC then convert to KST
            result["timestamp"] = result["timestamp"].dt.tz_localize("UTC").dt.tz_convert(KST)

        # Filter by date range (now both are in KST)
        result = result[(result["timestamp"] >= start_dt) & (result["timestamp"] <= end_dt)]
        result = result.sort_values("timestamp").reset_index(drop=True)

    logger.info(f"Loaded {len(result)} rows for {symbol} ({start_date} ~ {end_date})")
    return result
