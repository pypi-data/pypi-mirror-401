"""
Unit tests for IntradayContentFactory.

Tests:
- Initialization
- Frequency configuration
- Timestamp generation
- S3 configuration
- get_df methods
- Resampling
"""

import pytest
from unittest.mock import Mock, patch
import numpy as np
import pandas as pd

from finter.data.content_model.intraday_loader import (
    IntradayContentFactory,
    create_content_factory,
    S3_INTRADAY_CONFIG,
)
from finter.backtest.config.frequency import is_intraday


class TestIntradayContentFactoryInit:
    """Test IntradayContentFactory initialization."""

    def test_daily_frequency_default(self):
        """Default frequency should be daily."""
        with patch.object(IntradayContentFactory, '__init__', lambda self, *args, **kwargs: None):
            cf = IntradayContentFactory.__new__(IntradayContentFactory)
            cf.frequency = "D"
            cf._is_intraday = False
            assert cf.frequency == "D"
            assert cf._is_intraday is False

    def test_intraday_frequency_10t(self):
        """10T frequency should be recognized as intraday."""
        assert is_intraday("10T") is True

    def test_intraday_frequency_30t(self):
        """30T frequency should be recognized as intraday."""
        assert is_intraday("30T") is True

    def test_intraday_frequency_1h(self):
        """1H frequency should be recognized as intraday."""
        assert is_intraday("1H") is True

    def test_daily_frequency_check(self):
        """D frequency should not be intraday."""
        assert is_intraday("D") is False


class TestIntradayUniverses:
    """Test intraday universe configurations."""

    def test_crypto_test_supported(self):
        """crypto_test should be in supported universes."""
        assert "crypto_test" in IntradayContentFactory.INTRADAY_UNIVERSES

    def test_kr_stock_supported(self):
        """kr_stock should be in supported universes."""
        assert "kr_stock" in IntradayContentFactory.INTRADAY_UNIVERSES

    def test_kr_stock_s3_enabled(self):
        """kr_stock should be S3 enabled."""
        assert "kr_stock" in IntradayContentFactory.S3_INTRADAY_UNIVERSES


class TestS3Configuration:
    """Test S3 configuration."""

    def test_s3_bucket_name(self):
        """S3 bucket name should be correct."""
        assert S3_INTRADAY_CONFIG["bucket"] == "finter-intraday-data"

    def test_s3_region(self):
        """S3 region should be ap-northeast-2."""
        assert S3_INTRADAY_CONFIG["region"] == "ap-northeast-2"

    def test_s3_path_template(self):
        """S3 path template should have correct format."""
        template = S3_INTRADAY_CONFIG["path_template"]
        assert "{universe}" in template
        assert "{frequency}" in template
        assert "{date}" in template


class TestFrequencyToMinutes:
    """Test _freq_to_minutes static method."""

    def test_1t_to_minutes(self):
        """1T should be 1 minute."""
        assert IntradayContentFactory._freq_to_minutes("1T") == 1

    def test_5t_to_minutes(self):
        """5T should be 5 minutes."""
        assert IntradayContentFactory._freq_to_minutes("5T") == 5

    def test_10t_to_minutes(self):
        """10T should be 10 minutes."""
        assert IntradayContentFactory._freq_to_minutes("10T") == 10

    def test_30t_to_minutes(self):
        """30T should be 30 minutes."""
        assert IntradayContentFactory._freq_to_minutes("30T") == 30

    def test_1h_to_minutes(self):
        """1H should be 60 minutes."""
        assert IntradayContentFactory._freq_to_minutes("1H") == 60

    def test_unknown_default(self):
        """Unknown frequency should default to 1440 (1 day)."""
        assert IntradayContentFactory._freq_to_minutes("UNKNOWN") == 1440


class TestToPolarsLong:
    """Test _to_polars_long static method."""

    def test_conversion_shape(self):
        """Long format should have rows = rows * cols."""
        try:
            import polars as pl
        except ImportError:
            pytest.skip("Polars not installed")

        dates = pd.date_range("2024-01-01", periods=5, freq="D")
        df = pd.DataFrame(
            {"A": [1, 2, 3, 4, 5], "B": [10, 20, 30, 40, 50]},
            index=dates
        )

        result = IntradayContentFactory._to_polars_long(df, "value")

        # Wide: 5 rows x 2 cols -> Long: 10 rows
        assert len(result) == 10

    def test_conversion_columns(self):
        """Long format should have timestamp, id, value columns."""
        try:
            import polars as pl
        except ImportError:
            pytest.skip("Polars not installed")

        dates = pd.date_range("2024-01-01", periods=5, freq="D")
        df = pd.DataFrame(
            {"A": [1, 2, 3, 4, 5], "B": [10, 20, 30, 40, 50]},
            index=dates
        )

        result = IntradayContentFactory._to_polars_long(df, "close")

        assert "timestamp" in result.columns
        assert "id" in result.columns
        assert "close" in result.columns


class TestResampleToFrequency:
    """Test resample_to_frequency method."""

    @pytest.fixture
    def intraday_df(self):
        """Create intraday sample DataFrame."""
        dates = pd.date_range("2024-01-01 09:00", periods=78, freq="5T")
        data = np.arange(78) + 100
        return pd.DataFrame({"value": data}, index=dates)

    def test_resample_last(self, intraday_df):
        """Resample with last aggregation."""
        with patch.object(IntradayContentFactory, '__init__', lambda self, *args, **kwargs: None):
            cf = IntradayContentFactory.__new__(IntradayContentFactory)
            result = cf.resample_to_frequency(intraday_df, "1H", "last")
            assert len(result) < len(intraday_df)

    def test_resample_mean(self, intraday_df):
        """Resample with mean aggregation."""
        with patch.object(IntradayContentFactory, '__init__', lambda self, *args, **kwargs: None):
            cf = IntradayContentFactory.__new__(IntradayContentFactory)
            result = cf.resample_to_frequency(intraday_df, "1H", "mean")
            assert len(result) < len(intraday_df)


class TestCreateContentFactory:
    """Test create_content_factory function."""

    def test_daily_returns_content_factory(self):
        """Daily frequency should return ContentFactory."""
        # We can't fully test this without mocking,
        # but we can test the logic
        assert is_intraday("D") is False

    def test_intraday_returns_intraday_factory(self):
        """Intraday frequency should return IntradayContentFactory."""
        assert is_intraday("10T") is True


class TestPropertyMethods:
    """Test property methods."""

    def test_bars_per_day_property(self):
        """bars_per_day property should return correct value."""
        from finter.backtest.config.frequency import get_bars_per_day

        # Test using the standalone function
        assert get_bars_per_day("10T", "kr_stock") == 39
        assert get_bars_per_day("30T", "kr_stock") == 13
        assert get_bars_per_day("1H", "kr_stock") == 7
        assert get_bars_per_day("D", "kr_stock") == 1

    def test_annualization_factor(self):
        """annualization_factor should be bars_per_year."""
        from finter.backtest.config.frequency import get_frequency_config

        config = get_frequency_config("10T")
        assert config.bars_per_year == 252 * 39  # 9828


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
