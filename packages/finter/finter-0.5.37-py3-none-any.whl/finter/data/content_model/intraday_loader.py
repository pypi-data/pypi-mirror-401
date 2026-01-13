"""
Intraday Content Factory for sub-daily frequency data loading.

This module extends ContentFactory to support intraday frequencies
(10T, 30T, 1H) while maintaining full backward compatibility with
daily frequency operations.

Usage:
    from finter.data.content_model.intraday_loader import IntradayContentFactory

    # 10-minute frequency with crypto_test
    cf = IntradayContentFactory('crypto_test', 20240101, 20240131, frequency='10T')
    df = cf.get_df('close')  # Returns pandas DataFrame with 10-min index

    # Polars DataFrame for performance
    pl_df = cf.get_pl('close')  # Returns polars DataFrame in long format

    # Daily (backward compatible - same as ContentFactory)
    cf_daily = IntradayContentFactory('kr_stock', 20240101, 20240131, frequency='D')
"""

from datetime import datetime, timedelta
from typing import List, Optional, Union

import pandas as pd

from finter.backtest.config.frequency import (
    AVAILABLE_FREQUENCIES,
    FrequencyConfig,
    get_bars_per_day,
    get_frequency_config,
    is_intraday,
)
from finter.data.content_model.loader import ContentFactory
from finter.settings import logger

# Try to import polars, fall back gracefully
try:
    import polars as pl
    HAS_POLARS = True
except ImportError:
    HAS_POLARS = False
    pl = None

# Try to import boto3 for S3 access
try:
    import boto3
    import pyarrow.parquet as pq
    import io
    HAS_S3 = True
except ImportError:
    HAS_S3 = False
    boto3 = None

# S3 Configuration for intraday data
S3_INTRADAY_CONFIG = {
    "bucket": "finter-intraday-data",
    "region": "ap-northeast-2",
    "path_template": "{universe}/{frequency}/date={date}/data.parquet",
}


class IntradayContentFactory(ContentFactory):
    """
    Extended ContentFactory with intraday frequency support.

    100% backward compatible - defaults to daily frequency.
    Adds Polars support for high-performance data processing.

    Attributes:
        frequency (str): Trading frequency ('D', '1H', '30T', '10T', etc.)
        freq_config (FrequencyConfig): Configuration for the frequency
        is_intraday (bool): Whether frequency is sub-daily

    Example:
        # Intraday with 10-minute bars
        cf = IntradayContentFactory('crypto_test', 20240101, 20240131, frequency='10T')

        # Pandas DataFrame (wide format)
        df = cf.get_df('close')

        # Polars DataFrame (long format, faster for large data)
        pl_df = cf.get_pl('close')
    """

    # Supported intraday universes
    INTRADAY_UNIVERSES = {
        "crypto_test",
        "btcusdt_spot_binance",
        "btcusdt_future_binance",
        "kr_stock",  # S3 intraday data
    }

    # Universes with S3 intraday data
    S3_INTRADAY_UNIVERSES = {
        "kr_stock",
        "us_stock",
    }

    def __init__(
        self,
        universe_name: str,
        start: int,
        end: int,
        frequency: AVAILABLE_FREQUENCIES = "D",
        cache_timeout: int = 0,
        cache_maxsize: int = 10,
        sub_universe=None,
        backup_day=None,
    ):
        """
        Initialize IntradayContentFactory.

        Args:
            universe_name: Universe name (e.g., 'crypto_test', 'kr_stock')
            start: Start date in YYYYMMDD format
            end: End date in YYYYMMDD format
            frequency: Trading frequency ('D', '1H', '30T', '10T', '5T', '1T')
            cache_timeout: Cache TTL in seconds
            cache_maxsize: Maximum cache entries
            sub_universe: Optional sub-universe filter
            backup_day: Backup day for data loading

        Raises:
            ValueError: If intraday frequency requested for unsupported universe
        """
        self.frequency = frequency
        self.freq_config = get_frequency_config(frequency)
        self._is_intraday = is_intraday(frequency)

        # Validate intraday support
        if self._is_intraday and universe_name not in self.INTRADAY_UNIVERSES:
            logger.warning(
                f"Universe '{universe_name}' may not have intraday data. "
                f"Supported intraday universes: {self.INTRADAY_UNIVERSES}"
            )

        # Initialize parent ContentFactory
        super().__init__(
            universe_name=universe_name,
            start=start,
            end=end,
            cache_timeout=cache_timeout,
            cache_maxsize=cache_maxsize,
            sub_universe=sub_universe,
            backup_day=backup_day,
        )

        # Generate intraday timestamps if needed
        if self._is_intraday:
            self.trading_timestamps = self._generate_trading_timestamps()
        else:
            self.trading_timestamps = None

        # Initialize S3 client if needed
        self._s3_client = None
        self._s3_cache = {}
        self._use_s3 = (
            self._is_intraday
            and universe_name in self.S3_INTRADAY_UNIVERSES
            and HAS_S3
        )

    def _get_s3_client(self):
        """Get or create S3 client."""
        if self._s3_client is None and HAS_S3:
            self._s3_client = boto3.client(
                "s3",
                region_name=S3_INTRADAY_CONFIG["region"],
            )
        return self._s3_client

    def _load_from_s3(self, date: str) -> Optional[pd.DataFrame]:
        """
        Load intraday data from S3 for a specific date.

        Args:
            date: Date string (YYYYMMDD)

        Returns:
            DataFrame with intraday data or None if not found
        """
        if not HAS_S3:
            logger.warning("S3 support not available (boto3/pyarrow not installed)")
            return None

        # Check cache first
        cache_key = f"{self.universe_name}_{self.frequency}_{date}"
        if cache_key in self._s3_cache:
            return self._s3_cache[cache_key]

        # Build S3 path
        s3_path = S3_INTRADAY_CONFIG["path_template"].format(
            universe=self.universe_name,
            frequency=self.frequency,
            date=date,
        )

        try:
            client = self._get_s3_client()
            response = client.get_object(
                Bucket=S3_INTRADAY_CONFIG["bucket"],
                Key=s3_path,
            )

            # Read Parquet from S3
            parquet_buffer = io.BytesIO(response["Body"].read())
            table = pq.read_table(parquet_buffer)
            df = table.to_pandas()

            # Set timestamp as index
            if "timestamp" in df.columns:
                df = df.set_index("timestamp")
                df.index = pd.to_datetime(df.index)

            # Cache the result
            self._s3_cache[cache_key] = df

            logger.debug(f"Loaded {len(df)} rows from S3: {s3_path}")
            return df

        except Exception as e:
            logger.warning(f"S3 load failed for {s3_path}: {e}")
            return None

    def _load_date_range_from_s3(self) -> Optional[pd.DataFrame]:
        """
        Load intraday data from S3 for the entire date range.

        Returns:
            Combined DataFrame for all dates
        """
        all_data = []

        for day in self.trading_days:
            # Convert day to YYYYMMDD string
            if isinstance(day, datetime):
                date_str = day.strftime("%Y%m%d")
            elif isinstance(day, str) and "-" in day:
                date_str = day.replace("-", "")[:8]
            else:
                date_str = str(day)

            df = self._load_from_s3(date_str)
            if df is not None and not df.empty:
                all_data.append(df)

        if not all_data:
            return None

        # Combine all dates
        combined = pd.concat(all_data, axis=0)
        combined = combined.sort_index()

        return combined

    def _generate_trading_timestamps(self) -> List[datetime]:
        """
        Generate intraday trading timestamps based on frequency and market hours.

        Returns:
            List of datetime objects for all trading timestamps
        """
        from finter.backtest.config.frequency import MARKET_HOURS

        market_hours = MARKET_HOURS.get(
            self.universe_name,
            {"open": "00:00", "close": "23:59"}  # Default: 24/7
        )

        timestamps = []
        freq_minutes = self._freq_to_minutes(self.frequency)

        for day in self.trading_days:
            # Parse day (can be int YYYYMMDD, str, or datetime)
            if isinstance(day, datetime):
                day_dt = day
            elif isinstance(day, str) and len(day) > 8:
                # datetime string format
                day_dt = datetime.strptime(day.split()[0], "%Y-%m-%d")
            else:
                day_dt = datetime.strptime(str(day), "%Y%m%d")

            # Parse market hours
            open_time = datetime.strptime(market_hours["open"], "%H:%M").time()
            close_time = datetime.strptime(market_hours["close"], "%H:%M").time()

            # Generate timestamps for this day
            current = datetime.combine(day_dt.date(), open_time)
            end_dt = datetime.combine(day_dt.date(), close_time)

            while current <= end_dt:
                timestamps.append(current)
                current += timedelta(minutes=freq_minutes)

        return timestamps

    @staticmethod
    def _freq_to_minutes(freq: str) -> int:
        """Convert frequency code to minutes."""
        freq_map = {
            "1T": 1,
            "5T": 5,
            "10T": 10,
            "30T": 30,
            "1H": 60,
        }
        return freq_map.get(freq, 1440)  # Default: 1 day

    def get_df(
        self,
        item_name: str,
        category=None,
        freq=None,
        **kwargs
    ) -> pd.DataFrame:
        """
        Get DataFrame for an item, with automatic frequency handling.

        For intraday frequencies, returns DataFrame with DatetimeIndex
        containing timestamps at the specified frequency.

        Data source priority:
        1. S3 Parquet files (for S3_INTRADAY_UNIVERSES)
        2. Parent ContentFactory (CM/API)

        Args:
            item_name: Item name (e.g., 'close', 'volume')
            category: Optional category filter
            freq: Override frequency (default: instance frequency)
            **kwargs: Additional arguments passed to parent

        Returns:
            pandas DataFrame with appropriate index
        """
        # Use parent implementation for daily frequency
        if not self._is_intraday:
            return super().get_df(item_name, category, **kwargs)

        # Try S3 first for S3-enabled universes
        if self._use_s3:
            s3_data = self._load_date_range_from_s3()
            if s3_data is not None:
                # Extract specific item column if multi-level
                if isinstance(s3_data.columns, pd.MultiIndex):
                    if item_name in s3_data.columns.get_level_values(0):
                        return s3_data[item_name]
                else:
                    # Look for columns matching item_name pattern
                    item_cols = [c for c in s3_data.columns if c.startswith(f"{item_name}_")]
                    if item_cols:
                        result = s3_data[item_cols].copy()
                        result.columns = [c.replace(f"{item_name}_", "") for c in result.columns]
                        return result

                logger.debug(f"S3 data loaded but item '{item_name}' not found, falling back to CM")

        # Fallback: load from parent ContentFactory
        df = super().get_df(item_name, category, **kwargs)

        # Convert index to datetime if not already
        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index.astype(str))

        return df

    def get_pl(
        self,
        item_name: str,
        category=None,
        freq=None,
        **kwargs
    ) -> "pl.DataFrame":
        """
        Get Polars DataFrame in long format for efficient processing.

        Optimized for large intraday datasets with lazy evaluation support.

        Args:
            item_name: Item name (e.g., 'close', 'volume')
            category: Optional category filter
            freq: Override frequency
            **kwargs: Additional arguments

        Returns:
            Polars DataFrame with columns: [timestamp, id, value]

        Raises:
            ImportError: If polars is not installed
        """
        if not HAS_POLARS:
            raise ImportError(
                "Polars is required for get_pl(). "
                "Install with: pip install polars"
            )

        # Get pandas DataFrame first
        df = self.get_df(item_name, category, freq, **kwargs)

        # Convert to long format Polars DataFrame
        return self._to_polars_long(df, item_name)

    @staticmethod
    def _to_polars_long(df: pd.DataFrame, value_name: str = "value") -> "pl.DataFrame":
        """
        Convert wide pandas DataFrame to long Polars DataFrame.

        Args:
            df: Wide-format pandas DataFrame (index=time, columns=ids)
            value_name: Name for the value column

        Returns:
            Polars DataFrame with columns: [timestamp, id, {value_name}]
        """
        if not HAS_POLARS:
            raise ImportError("Polars is required")

        # Reset index to get timestamp as column
        df_reset = df.reset_index()
        df_reset.columns = ["timestamp"] + list(df.columns)

        # Melt to long format
        df_long = df_reset.melt(
            id_vars=["timestamp"],
            var_name="id",
            value_name=value_name
        )

        # Convert to Polars
        return pl.from_pandas(df_long)

    def get_lazy(
        self,
        item_name: str,
        category=None,
        **kwargs
    ) -> "pl.LazyFrame":
        """
        Get Polars LazyFrame for deferred computation.

        Useful for building query pipelines that are optimized
        before execution.

        Args:
            item_name: Item name
            category: Optional category
            **kwargs: Additional arguments

        Returns:
            Polars LazyFrame
        """
        if not HAS_POLARS:
            raise ImportError("Polars is required for get_lazy()")

        return self.get_pl(item_name, category, **kwargs).lazy()

    def resample_to_frequency(
        self,
        df: pd.DataFrame,
        target_freq: str,
        agg_method: str = "last"
    ) -> pd.DataFrame:
        """
        Resample DataFrame to a different frequency.

        Args:
            df: Input DataFrame with DatetimeIndex
            target_freq: Target frequency ('D', '1H', '30T', '10T')
            agg_method: Aggregation method ('last', 'first', 'mean', 'sum')

        Returns:
            Resampled DataFrame
        """
        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index.astype(str))

        agg_funcs = {
            "last": lambda x: x.resample(target_freq).last(),
            "first": lambda x: x.resample(target_freq).first(),
            "mean": lambda x: x.resample(target_freq).mean(),
            "sum": lambda x: x.resample(target_freq).sum(),
        }

        return agg_funcs.get(agg_method, agg_funcs["last"])(df)

    @property
    def bars_per_day(self) -> int:
        """Get number of bars per trading day for current frequency."""
        return get_bars_per_day(self.frequency, self.universe_name)

    @property
    def annualization_factor(self) -> int:
        """Get annualization factor for current frequency."""
        return self.freq_config.bars_per_year

    def __repr__(self) -> str:
        return (
            f"IntradayContentFactory("
            f"universe='{self.universe_name}', "
            f"frequency='{self.frequency}', "
            f"start={self.start}, end={self.end}, "
            f"bars_per_day={self.bars_per_day})"
        )


# Convenience function
def create_content_factory(
    universe_name: str,
    start: int,
    end: int,
    frequency: str = "D",
    **kwargs
) -> Union[ContentFactory, IntradayContentFactory]:
    """
    Factory function to create appropriate ContentFactory based on frequency.

    Args:
        universe_name: Universe name
        start: Start date (YYYYMMDD)
        end: End date (YYYYMMDD)
        frequency: Frequency ('D' for daily, '10T' for 10-min, etc.)
        **kwargs: Additional arguments

    Returns:
        ContentFactory for daily, IntradayContentFactory for intraday
    """
    if is_intraday(frequency):
        return IntradayContentFactory(
            universe_name, start, end, frequency=frequency, **kwargs
        )
    return ContentFactory(universe_name, start, end, **kwargs)
