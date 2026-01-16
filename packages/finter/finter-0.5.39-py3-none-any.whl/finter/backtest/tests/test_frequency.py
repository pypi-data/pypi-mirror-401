"""
Unit tests for frequency configuration.

Tests:
- FrequencyConfig dataclass
- BARS_PER_DAY dictionary
- get_frequency_config function
- is_intraday function
- get_bars_per_day function
"""

import pytest
from finter.backtest.config.frequency import (
    AVAILABLE_FREQUENCIES,
    BARS_PER_DAY,
    FrequencyConfig,
    get_frequency_config,
    is_intraday,
    get_bars_per_day,
    MARKET_HOURS,
)


class TestBarsPerDay:
    """Test BARS_PER_DAY dictionary."""

    def test_daily_bars(self):
        """Daily should have 1 bar per day."""
        assert BARS_PER_DAY["D"] == 1

    def test_hourly_bars(self):
        """1H should have 7 bars for KRX market hours."""
        assert BARS_PER_DAY["1H"] == 7

    def test_30min_bars(self):
        """30T should have 13 bars."""
        assert BARS_PER_DAY["30T"] == 13

    def test_10min_bars(self):
        """10T should have 39 bars."""
        assert BARS_PER_DAY["10T"] == 39

    def test_5min_bars(self):
        """5T should have 78 bars."""
        assert BARS_PER_DAY["5T"] == 78

    def test_1min_bars(self):
        """1T should have 390 bars."""
        assert BARS_PER_DAY["1T"] == 390

    def test_all_frequencies_exist(self):
        """All available frequencies should have BARS_PER_DAY entry."""
        for freq in AVAILABLE_FREQUENCIES.__args__:
            assert freq in BARS_PER_DAY


class TestFrequencyConfig:
    """Test FrequencyConfig dataclass."""

    def test_daily_config(self):
        """Daily config should have correct values."""
        config = get_frequency_config("D")
        assert config.code == "D"
        assert config.bars_per_day == 1
        assert config.bars_per_year == 252
        assert config.rolling_short == 63
        assert config.rolling_long == 252

    def test_10min_config(self):
        """10T config should have scaled values."""
        config = get_frequency_config("10T")
        assert config.code == "10T"
        assert config.bars_per_day == 39
        assert config.bars_per_year == 252 * 39  # 9828
        assert config.rolling_short == 63 * 39  # 2457
        assert config.rolling_long == 252 * 39  # 9828

    def test_30min_config(self):
        """30T config should have scaled values."""
        config = get_frequency_config("30T")
        assert config.code == "30T"
        assert config.bars_per_day == 13
        assert config.bars_per_year == 252 * 13

    def test_hourly_config(self):
        """1H config should have correct values."""
        config = get_frequency_config("1H")
        assert config.code == "1H"
        assert config.bars_per_day == 7
        assert config.bars_per_year == 252 * 7


class TestIsIntraday:
    """Test is_intraday function."""

    def test_daily_not_intraday(self):
        """Daily is not intraday."""
        assert is_intraday("D") is False

    def test_10min_is_intraday(self):
        """10T is intraday."""
        assert is_intraday("10T") is True

    def test_30min_is_intraday(self):
        """30T is intraday."""
        assert is_intraday("30T") is True

    def test_hourly_is_intraday(self):
        """1H is intraday."""
        assert is_intraday("1H") is True

    def test_5min_is_intraday(self):
        """5T is intraday."""
        assert is_intraday("5T") is True

    def test_1min_is_intraday(self):
        """1T is intraday."""
        assert is_intraday("1T") is True


class TestGetBarsPerDay:
    """Test get_bars_per_day function."""

    def test_daily(self):
        """Daily returns 1."""
        assert get_bars_per_day("D") == 1

    def test_10min(self):
        """10T returns 39."""
        assert get_bars_per_day("10T") == 39

    def test_with_universe_crypto(self):
        """Crypto universe may have different hours."""
        # crypto_test is 24/7
        bars = get_bars_per_day("10T", "crypto_test")
        assert bars > 0

    def test_with_universe_kr_stock(self):
        """KR stock uses standard market hours."""
        bars = get_bars_per_day("10T", "kr_stock")
        assert bars == 39


class TestMarketHours:
    """Test MARKET_HOURS dictionary."""

    def test_kr_stock_hours(self):
        """KR stock market hours should be 09:00-15:30."""
        hours = MARKET_HOURS.get("kr_stock", {})
        assert hours.get("open") == "09:00"
        assert hours.get("close") == "15:30"

    def test_crypto_hours(self):
        """Crypto should be 24/7."""
        hours = MARKET_HOURS.get("crypto_test", {})
        assert hours.get("open") == "00:00"
        assert hours.get("close") == "23:59"


class TestFrequencyConfigEquivalence:
    """Test rolling window equivalence."""

    def test_rolling_short_63_days(self):
        """Rolling short should be ~63 days in bars."""
        for freq in ["D", "10T", "30T", "1H"]:
            config = get_frequency_config(freq)
            days_equivalent = config.rolling_short / config.bars_per_day
            assert abs(days_equivalent - 63) < 0.01

    def test_rolling_long_252_days(self):
        """Rolling long should be ~252 days in bars."""
        for freq in ["D", "10T", "30T", "1H"]:
            config = get_frequency_config(freq)
            days_equivalent = config.rolling_long / config.bars_per_day
            assert abs(days_equivalent - 252) < 0.01


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
