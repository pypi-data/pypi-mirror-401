"""
High-frequency data processor with hybrid Polars + Numba approach.

This module provides optimized data processing for intraday quantitative
analysis. It uses Polars for data manipulation and Numba for CPU-intensive
numerical operations, achieving 10-100x speedup over pure pandas.

Design Principles:
1. Polars for data manipulation (lazy evaluation, columnar)
2. NumPy arrays for intermediate computations
3. Numba JIT for CPU-intensive loops (vectorized where possible)
4. Encapsulate Numba complexity from end users

Usage:
    from finter.processing import HighFreqProcessor

    processor = HighFreqProcessor(frequency="10T")

    # Polars-first API
    zscore = processor.rolling_zscore(df, window=195)  # ~5 days for 10T
    ranked = processor.cross_sectional_rank(df)
    resampled = processor.resample(df, target_freq="1H")

    # Apply custom Numba function (internal)
    result = processor.apply_numba(values, processor._rolling_rank_numba, window=63)
"""

from dataclasses import dataclass
from typing import Callable, Literal, Optional, Union

import numpy as np
import pandas as pd

from finter.backtest.config.frequency import (
    AVAILABLE_FREQUENCIES,
    FrequencyConfig,
    get_frequency_config,
    get_rolling_window,
)

# Try to import Polars
try:
    import polars as pl
    HAS_POLARS = True
except ImportError:
    HAS_POLARS = False
    pl = None

# Try to import Numba
try:
    from numba import njit, prange
    HAS_NUMBA = True
except ImportError:
    HAS_NUMBA = False
    njit = lambda *args, **kwargs: lambda f: f  # No-op decorator
    prange = range


@dataclass
class ProcessingConfig:
    """Configuration for high-frequency processing."""
    frequency: AVAILABLE_FREQUENCIES = "10T"
    bars_per_day: int = 39
    parallel: bool = True
    chunk_size: int = 10000  # For memory-efficient processing


class HighFreqProcessor:
    """
    High-frequency data processor with hybrid Polars + Numba approach.

    Provides optimized operations for intraday quantitative analysis:
    - Rolling statistics (mean, std, zscore, rank)
    - Resampling (10T -> 1H -> D)
    - Cross-sectional operations (rank, normalize)
    - Exponential decay calculations

    Attributes:
        frequency: Trading frequency
        config: Processing configuration
        freq_config: Frequency-specific settings

    Example:
        processor = HighFreqProcessor(frequency="10T")
        zscore = processor.rolling_zscore(df, window=195)
    """

    def __init__(self, frequency: AVAILABLE_FREQUENCIES = "10T"):
        """
        Initialize processor with specified frequency.

        Args:
            frequency: Trading frequency ('10T', '30T', '1H', 'D')
        """
        self.frequency = frequency
        self.freq_config = get_frequency_config(frequency)
        self.config = ProcessingConfig(
            frequency=frequency,
            bars_per_day=self.freq_config.bars_per_day,
        )

    # =========================================================================
    # Polars API (User-facing)
    # =========================================================================

    def rolling_zscore(
        self,
        data: Union[pd.DataFrame, "pl.DataFrame"],
        window: int,
        min_periods: Optional[int] = None,
    ) -> Union[pd.DataFrame, "pl.DataFrame"]:
        """
        Calculate rolling z-score.

        Args:
            data: Input DataFrame (pandas wide or polars long)
            window: Rolling window size in bars
            min_periods: Minimum observations required (default: window)

        Returns:
            DataFrame with z-scores
        """
        min_periods = min_periods or window

        if HAS_POLARS and isinstance(data, pl.DataFrame):
            return self._rolling_zscore_polars(data, window, min_periods)
        return self._rolling_zscore_pandas(data, window, min_periods)

    def _rolling_zscore_polars(
        self,
        df: "pl.DataFrame",
        window: int,
        min_periods: int
    ) -> "pl.DataFrame":
        """Polars implementation of rolling z-score."""
        return df.with_columns([
            (
                (pl.col("value") - pl.col("value").rolling_mean(window))
                / pl.col("value").rolling_std(window)
            )
            .over("id")
            .alias("zscore")
        ])

    def _rolling_zscore_pandas(
        self,
        df: pd.DataFrame,
        window: int,
        min_periods: int
    ) -> pd.DataFrame:
        """Pandas implementation of rolling z-score."""
        rolling_mean = df.rolling(window, min_periods=min_periods).mean()
        rolling_std = df.rolling(window, min_periods=min_periods).std()
        return (df - rolling_mean) / rolling_std

    def rolling_rank(
        self,
        data: Union[pd.DataFrame, "pl.DataFrame"],
        window: int,
    ) -> Union[pd.DataFrame, "pl.DataFrame"]:
        """
        Calculate rolling percentile rank.

        Uses Numba-optimized implementation for performance.

        Args:
            data: Input DataFrame
            window: Rolling window size

        Returns:
            DataFrame with rolling ranks (0-1)
        """
        if HAS_POLARS and isinstance(data, pl.DataFrame):
            # Convert to numpy, process with Numba, convert back
            values = data.to_numpy()
            result = self._rolling_rank_numba(values, window)
            return pl.DataFrame(result, schema=data.schema)

        # Pandas path
        values = data.values
        result = self._rolling_rank_numba(values, window)
        return pd.DataFrame(result, index=data.index, columns=data.columns)

    def cross_sectional_rank(
        self,
        data: Union[pd.DataFrame, "pl.DataFrame"],
        method: Literal["average", "min", "max", "dense", "ordinal"] = "average"
    ) -> Union[pd.DataFrame, "pl.DataFrame"]:
        """
        Calculate cross-sectional rank (rank across assets at each timestamp).

        Args:
            data: Input DataFrame
            method: Ranking method

        Returns:
            DataFrame with cross-sectional ranks
        """
        if HAS_POLARS and isinstance(data, pl.DataFrame):
            return data.with_columns([
                pl.col("value").rank(method=method).over("timestamp").alias("rank")
            ])

        # Pandas: rank across columns (assets) for each row (timestamp)
        return data.rank(axis=1, method=method)

    def cross_sectional_normalize(
        self,
        data: Union[pd.DataFrame, "pl.DataFrame"],
    ) -> Union[pd.DataFrame, "pl.DataFrame"]:
        """
        Normalize cross-sectionally (demean and scale by std).

        Args:
            data: Input DataFrame

        Returns:
            Cross-sectionally normalized DataFrame
        """
        if HAS_POLARS and isinstance(data, pl.DataFrame):
            return data.with_columns([
                (
                    (pl.col("value") - pl.col("value").mean().over("timestamp"))
                    / pl.col("value").std().over("timestamp")
                ).alias("normalized")
            ])

        # Pandas
        mean = data.mean(axis=1)
        std = data.std(axis=1)
        return data.sub(mean, axis=0).div(std, axis=0)

    def resample(
        self,
        data: Union[pd.DataFrame, "pl.DataFrame"],
        target_freq: AVAILABLE_FREQUENCIES,
        agg_func: Literal["last", "first", "mean", "sum", "ohlc"] = "last"
    ) -> Union[pd.DataFrame, "pl.DataFrame"]:
        """
        Resample to lower frequency.

        Args:
            data: Input DataFrame
            target_freq: Target frequency ('1H', 'D', 'W')
            agg_func: Aggregation function

        Returns:
            Resampled DataFrame
        """
        if HAS_POLARS and isinstance(data, pl.DataFrame):
            return self._resample_polars(data, target_freq, agg_func)
        return self._resample_pandas(data, target_freq, agg_func)

    def _resample_polars(
        self,
        df: "pl.DataFrame",
        target_freq: str,
        agg_func: str
    ) -> "pl.DataFrame":
        """Polars implementation of resampling."""
        interval = self._freq_to_polars_interval(target_freq)

        if agg_func == "ohlc":
            return df.group_by_dynamic(
                "timestamp", every=interval, by="id"
            ).agg([
                pl.col("value").first().alias("open"),
                pl.col("value").max().alias("high"),
                pl.col("value").min().alias("low"),
                pl.col("value").last().alias("close"),
            ])

        agg_map = {
            "last": pl.col("value").last(),
            "first": pl.col("value").first(),
            "mean": pl.col("value").mean(),
            "sum": pl.col("value").sum(),
        }

        return df.group_by_dynamic(
            "timestamp", every=interval, by="id"
        ).agg([
            agg_map[agg_func].alias("value")
        ])

    def _resample_pandas(
        self,
        df: pd.DataFrame,
        target_freq: str,
        agg_func: str
    ) -> pd.DataFrame:
        """Pandas implementation of resampling."""
        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index.astype(str))

        if agg_func == "ohlc":
            return df.resample(target_freq).ohlc()

        agg_map = {
            "last": "last",
            "first": "first",
            "mean": "mean",
            "sum": "sum",
        }
        return df.resample(target_freq).agg(agg_map[agg_func])

    @staticmethod
    def _freq_to_polars_interval(freq: str) -> str:
        """Convert frequency code to Polars interval string."""
        freq_map = {
            "1T": "1m",
            "5T": "5m",
            "10T": "10m",
            "30T": "30m",
            "1H": "1h",
            "D": "1d",
            "W": "1w",
        }
        return freq_map.get(freq, "1d")

    def exponential_decay(
        self,
        data: Union[pd.DataFrame, "pl.DataFrame"],
        half_life: float
    ) -> Union[pd.DataFrame, "pl.DataFrame"]:
        """
        Apply exponential decay weighting.

        Args:
            data: Input DataFrame
            half_life: Half-life in bars

        Returns:
            Exponentially weighted DataFrame
        """
        if HAS_POLARS and isinstance(data, pl.DataFrame):
            values = data.select("value").to_numpy().flatten()
            result = self._exponential_decay_numba(
                values.reshape(-1, 1), half_life
            )
            return data.with_columns([
                pl.lit(result.flatten()).alias("ewm")
            ])

        # Pandas
        values = data.values
        result = self._exponential_decay_numba(values, half_life)
        return pd.DataFrame(result, index=data.index, columns=data.columns)

    # =========================================================================
    # Numba-optimized functions (Internal)
    # =========================================================================

    @staticmethod
    @njit(cache=True, parallel=True)
    def _rolling_rank_numba(
        values: np.ndarray,
        window: int
    ) -> np.ndarray:
        """
        Numba-optimized rolling rank calculation.

        Computes percentile rank within rolling window.
        Parallelized across columns for performance.

        Args:
            values: 2D numpy array (rows=time, cols=assets)
            window: Rolling window size

        Returns:
            2D array with rolling ranks (0-1)
        """
        n_rows, n_cols = values.shape
        result = np.empty_like(values)
        result[:] = np.nan

        for j in prange(n_cols):
            for i in range(window - 1, n_rows):
                window_vals = values[i - window + 1:i + 1, j]
                valid_mask = ~np.isnan(window_vals)
                valid_count = np.sum(valid_mask)

                if valid_count == 0:
                    result[i, j] = np.nan
                else:
                    current = values[i, j]
                    if np.isnan(current):
                        result[i, j] = np.nan
                    else:
                        rank = np.sum(window_vals[valid_mask] < current) + 1
                        result[i, j] = rank / valid_count

        return result

    @staticmethod
    @njit(cache=True)
    def _exponential_decay_numba(
        values: np.ndarray,
        half_life: float
    ) -> np.ndarray:
        """
        Numba-optimized exponential decay.

        Args:
            values: 2D numpy array
            half_life: Half-life parameter

        Returns:
            Exponentially decayed values
        """
        decay = np.exp(-np.log(2) / half_life)
        n_rows, n_cols = values.shape
        result = np.zeros_like(values)

        for j in range(n_cols):
            result[0, j] = values[0, j]
            for i in range(1, n_rows):
                if np.isnan(values[i, j]):
                    result[i, j] = decay * result[i - 1, j]
                else:
                    result[i, j] = decay * result[i - 1, j] + (1 - decay) * values[i, j]

        return result

    @staticmethod
    @njit(cache=True, parallel=True)
    def _rolling_volatility_numba(
        returns: np.ndarray,
        window: int
    ) -> np.ndarray:
        """
        Numba-optimized rolling volatility calculation.

        Args:
            returns: 2D array of returns
            window: Rolling window size

        Returns:
            Rolling standard deviation
        """
        n_rows, n_cols = returns.shape
        result = np.empty_like(returns)
        result[:] = np.nan

        for j in prange(n_cols):
            for i in range(window - 1, n_rows):
                window_vals = returns[i - window + 1:i + 1, j]
                valid_mask = ~np.isnan(window_vals)
                valid_count = np.sum(valid_mask)

                if valid_count < 2:
                    result[i, j] = np.nan
                else:
                    valid_vals = window_vals[valid_mask]
                    mean = np.sum(valid_vals) / valid_count
                    variance = np.sum((valid_vals - mean) ** 2) / (valid_count - 1)
                    result[i, j] = np.sqrt(variance)

        return result

    # =========================================================================
    # Utility functions
    # =========================================================================

    def apply_numba(
        self,
        data: np.ndarray,
        func: Callable,
        **kwargs
    ) -> np.ndarray:
        """
        Apply a Numba-compiled function to numpy array.

        Encapsulates Numba complexity from users.

        Args:
            data: Input numpy array
            func: Numba-compiled function
            **kwargs: Function arguments

        Returns:
            Processed numpy array
        """
        return func(data, **kwargs)

    def get_rolling_window_days(self, days: int) -> int:
        """
        Convert days to rolling window size for current frequency.

        Args:
            days: Number of days

        Returns:
            Window size in bars
        """
        return get_rolling_window(self.frequency, days)

    def to_polars(self, df: pd.DataFrame, value_col: str = "value") -> "pl.DataFrame":
        """
        Convert pandas wide DataFrame to Polars long DataFrame.

        Args:
            df: Pandas DataFrame (wide format)
            value_col: Name for value column

        Returns:
            Polars DataFrame (long format)
        """
        if not HAS_POLARS:
            raise ImportError("Polars is required")

        df_reset = df.reset_index()
        df_reset.columns = ["timestamp"] + list(df.columns)

        df_long = df_reset.melt(
            id_vars=["timestamp"],
            var_name="id",
            value_name=value_col
        )

        return pl.from_pandas(df_long)

    def to_pandas(self, df: "pl.DataFrame", value_col: str = "value") -> pd.DataFrame:
        """
        Convert Polars long DataFrame to pandas wide DataFrame.

        Args:
            df: Polars DataFrame (long format)
            value_col: Value column name

        Returns:
            Pandas DataFrame (wide format)
        """
        if not HAS_POLARS:
            raise ImportError("Polars is required")

        return df.pivot(
            index="timestamp",
            columns="id",
            values=value_col
        ).to_pandas()

    def __repr__(self) -> str:
        return (
            f"HighFreqProcessor("
            f"frequency='{self.frequency}', "
            f"bars_per_day={self.config.bars_per_day}, "
            f"polars={'available' if HAS_POLARS else 'not installed'}, "
            f"numba={'available' if HAS_NUMBA else 'not installed'})"
        )
