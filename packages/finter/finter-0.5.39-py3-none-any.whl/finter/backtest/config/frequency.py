"""
Frequency configuration for intraday/daily/weekly trading.

This module defines frequency types and configurations for extending
the backtesting framework from daily to intraday (10-minute) support.

Usage:
    from finter.backtest.config.frequency import (
        AVAILABLE_FREQUENCIES,
        BARS_PER_DAY,
        FrequencyConfig,
        get_frequency_config,
    )

    config = get_frequency_config("10T")
    print(config.bars_per_year)  # 9828
"""

from dataclasses import dataclass
from typing import Dict, Optional

from typing_extensions import Literal


# Available frequency types
AVAILABLE_FREQUENCIES = Literal["D", "1H", "30T", "10T", "5T", "1T"]

# Bars per trading day by frequency (KRX: 09:00-15:30 = 6.5 hours)
BARS_PER_DAY: Dict[str, int] = {
    "D": 1,
    "1H": 7,       # 6.5h rounded up
    "30T": 13,     # 6.5h * 2
    "10T": 39,     # 6.5h * 6
    "5T": 78,      # 6.5h * 12
    "1T": 390,     # 6.5h * 60
}

# Market-specific trading hours
MARKET_HOURS: Dict[str, Dict[str, str]] = {
    "kr_stock": {"open": "09:00", "close": "15:30"},
    "us_stock": {"open": "09:30", "close": "16:00"},
    "us_etf": {"open": "09:30", "close": "16:00"},
    "crypto_test": {"open": "00:00", "close": "23:59"},  # 24/7
}

# Bars per day for US market (6.5 hours)
BARS_PER_DAY_US: Dict[str, int] = {
    "D": 1,
    "1H": 7,
    "30T": 13,
    "10T": 39,
    "5T": 78,
    "1T": 390,
}

# Bars per day for crypto (24 hours)
BARS_PER_DAY_CRYPTO: Dict[str, int] = {
    "D": 1,
    "1H": 24,
    "30T": 48,
    "10T": 144,
    "5T": 288,
    "1T": 1440,
}


@dataclass(frozen=True)
class FrequencyConfig:
    """
    Configuration for a specific trading frequency.

    Attributes:
        code: Pandas frequency code (e.g., "10T", "D")
        label: Human-readable label (e.g., "10 Minutes")
        bars_per_day: Number of bars in a trading day
        bars_per_year: Annualization factor (bars_per_day * 252)
        rolling_short: Short-term rolling window (~63 days equivalent)
        rolling_long: Long-term rolling window (~252 days equivalent)
        cache_ttl_hours: Cache time-to-live in hours
        min_history_bars: Minimum bars required for statistics
        chart_resample: Optional resample frequency for chart display
    """
    code: str
    label: str
    bars_per_day: int
    bars_per_year: int
    rolling_short: int
    rolling_long: int
    cache_ttl_hours: int
    min_history_bars: int
    chart_resample: Optional[str] = None

    def __repr__(self) -> str:
        return (
            f"FrequencyConfig(code={self.code!r}, "
            f"bars_per_year={self.bars_per_year}, "
            f"rolling_short={self.rolling_short})"
        )


# Pre-configured frequency configs
FREQUENCY_CONFIGS: Dict[str, FrequencyConfig] = {
    "1T": FrequencyConfig(
        code="1T",
        label="1 Minute",
        bars_per_day=390,
        bars_per_year=390 * 252,       # 98,280
        rolling_short=390 * 63,         # ~24,570 bars (~63 days)
        rolling_long=390 * 252,         # ~98,280 bars (~1 year)
        cache_ttl_hours=2,
        min_history_bars=3900,          # ~10 days
        chart_resample="10T",
    ),
    "5T": FrequencyConfig(
        code="5T",
        label="5 Minutes",
        bars_per_day=78,
        bars_per_year=78 * 252,        # 19,656
        rolling_short=78 * 63,          # ~4,914 bars
        rolling_long=78 * 252,
        cache_ttl_hours=4,
        min_history_bars=780,           # ~10 days
        chart_resample="1H",
    ),
    "10T": FrequencyConfig(
        code="10T",
        label="10 Minutes",
        bars_per_day=39,
        bars_per_year=39 * 252,        # 9,828
        rolling_short=39 * 63,          # ~2,457 bars
        rolling_long=39 * 252,
        cache_ttl_hours=4,
        min_history_bars=390,           # ~10 days
        chart_resample="1H",
    ),
    "30T": FrequencyConfig(
        code="30T",
        label="30 Minutes",
        bars_per_day=13,
        bars_per_year=13 * 252,        # 3,276
        rolling_short=13 * 63,          # ~819 bars
        rolling_long=13 * 252,
        cache_ttl_hours=6,
        min_history_bars=130,           # ~10 days
        chart_resample="D",
    ),
    "1H": FrequencyConfig(
        code="1H",
        label="1 Hour",
        bars_per_day=7,
        bars_per_year=7 * 252,         # 1,764
        rolling_short=7 * 63,           # ~441 bars
        rolling_long=7 * 252,
        cache_ttl_hours=12,
        min_history_bars=70,            # ~10 days
        chart_resample="D",
    ),
    "D": FrequencyConfig(
        code="D",
        label="Daily",
        bars_per_day=1,
        bars_per_year=252,
        rolling_short=63,
        rolling_long=252,
        cache_ttl_hours=24,
        min_history_bars=30,
        chart_resample=None,
    ),
    "W": FrequencyConfig(
        code="W",
        label="Weekly",
        bars_per_day=0,                 # N/A
        bars_per_year=52,
        rolling_short=13,               # ~3 months
        rolling_long=52,                # ~1 year
        cache_ttl_hours=48,
        min_history_bars=12,
        chart_resample=None,
    ),
}


def get_frequency_config(freq: str) -> FrequencyConfig:
    """
    Get frequency configuration for a given frequency code.

    Args:
        freq: Frequency code (e.g., "10T", "D", "W")

    Returns:
        FrequencyConfig for the specified frequency.
        Defaults to daily ("D") if not found.

    Example:
        >>> config = get_frequency_config("10T")
        >>> config.bars_per_year
        9828
    """
    return FREQUENCY_CONFIGS.get(freq, FREQUENCY_CONFIGS["D"])


def get_annualization_factor(freq: str) -> int:
    """
    Get the annualization factor for a given frequency.

    Args:
        freq: Frequency code

    Returns:
        Number of bars per year for the frequency.

    Example:
        >>> get_annualization_factor("10T")
        9828
        >>> get_annualization_factor("D")
        252
    """
    config = get_frequency_config(freq)
    return config.bars_per_year


def get_bars_per_day(freq: str, market: str = "kr_stock") -> int:
    """
    Get bars per trading day for a given frequency and market.

    Args:
        freq: Frequency code
        market: Market type (kr_stock, us_stock, crypto_test)

    Returns:
        Number of bars per trading day.

    Example:
        >>> get_bars_per_day("10T", "kr_stock")
        39
        >>> get_bars_per_day("10T", "crypto_test")
        144
    """
    if market in ("crypto_test", "btcusdt_spot_binance", "btcusdt_future_binance"):
        return BARS_PER_DAY_CRYPTO.get(freq, 1)
    return BARS_PER_DAY.get(freq, 1)


def is_intraday(freq: str) -> bool:
    """
    Check if frequency is intraday (sub-daily).

    Args:
        freq: Frequency code

    Returns:
        True if intraday frequency, False otherwise.

    Example:
        >>> is_intraday("10T")
        True
        >>> is_intraday("D")
        False
    """
    return freq in ("1T", "5T", "10T", "30T", "1H")


def freq_to_pandas(freq: str) -> str:
    """
    Convert frequency code to pandas-compatible string.

    Args:
        freq: Frequency code

    Returns:
        Pandas frequency string.

    Example:
        >>> freq_to_pandas("10T")
        '10T'
        >>> freq_to_pandas("D")
        'D'
    """
    # Most codes are already pandas-compatible
    return freq


def get_rolling_window(freq: str, days: int = 63) -> int:
    """
    Get rolling window size in bars for a given frequency and day count.

    Args:
        freq: Frequency code
        days: Number of days for the rolling window

    Returns:
        Number of bars for the rolling window.

    Example:
        >>> get_rolling_window("10T", 63)
        2457
        >>> get_rolling_window("D", 63)
        63
    """
    config = get_frequency_config(freq)
    if freq == "W":
        return max(1, days // 7)
    return config.bars_per_day * days
