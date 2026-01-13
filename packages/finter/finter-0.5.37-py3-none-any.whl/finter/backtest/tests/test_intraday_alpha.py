"""
Unit tests for BaseIntradayAlpha.

Tests:
- Class attributes
- Frequency configuration
- Property methods
- rolling_window helper
- get_cf method
- get_processor method
- backtest method
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import numpy as np
import pandas as pd

from finter.framework_model.intraday_alpha import (
    BaseIntradayAlpha,
    BaseAlphaV2,
    create_alpha_class,
)
from finter.backtest.config.frequency import (
    get_frequency_config,
    is_intraday,
)


class TestAlphaForTests(BaseIntradayAlpha):
    """Concrete implementation for testing."""
    universe = "crypto_test"
    frequency = "10T"

    def get(self, start: int, end: int) -> pd.DataFrame:
        """Return simple test signals."""
        dates = pd.date_range("2024-01-01", periods=100, freq="10T")
        data = np.random.randn(100, 3)
        return pd.DataFrame(data, index=dates, columns=["A", "B", "C"])


class TestBaseIntradayAlphaInit:
    """Test BaseIntradayAlpha initialization."""

    def test_default_frequency(self):
        """Default frequency should be 10T."""
        alpha = TestAlphaForTests()
        assert alpha.frequency == "10T"

    def test_universe_set(self):
        """Universe should be set from class attribute."""
        alpha = TestAlphaForTests()
        assert alpha.universe == "crypto_test"

    def test_cache_initialization(self):
        """Caches should be None initially."""
        alpha = TestAlphaForTests()
        assert alpha._cf_cache is None
        assert alpha._processor_cache is None


class TestFrequencyConfig:
    """Test freq_config property."""

    def test_freq_config_type(self):
        """freq_config should return FrequencyConfig."""
        alpha = TestAlphaForTests()
        config = alpha.freq_config
        assert config.code == "10T"
        assert config.bars_per_day == 39

    def test_is_intraday_property(self):
        """is_intraday should return True for 10T."""
        alpha = TestAlphaForTests()
        assert alpha.is_intraday is True

    def test_bars_per_day_property(self):
        """bars_per_day should return 39 for 10T."""
        alpha = TestAlphaForTests()
        assert alpha.bars_per_day == 39

    def test_annualization_factor_property(self):
        """annualization_factor should be 252 * 39."""
        alpha = TestAlphaForTests()
        assert alpha.annualization_factor == 252 * 39


class TestRollingWindow:
    """Test rolling_window method."""

    def test_rolling_window_1_day(self):
        """1 day should be 39 bars for 10T."""
        alpha = TestAlphaForTests()
        assert alpha.rolling_window(1) == 39

    def test_rolling_window_5_days(self):
        """5 days should be 195 bars for 10T."""
        alpha = TestAlphaForTests()
        assert alpha.rolling_window(5) == 195

    def test_rolling_window_63_days(self):
        """63 days (3 months) should be 2457 bars."""
        alpha = TestAlphaForTests()
        assert alpha.rolling_window(63) == 2457

    def test_rolling_window_252_days(self):
        """252 days (1 year) should be 9828 bars."""
        alpha = TestAlphaForTests()
        assert alpha.rolling_window(252) == 9828


class TestGetCf:
    """Test get_cf method."""

    @patch('finter.data.content_model.intraday_loader.IntradayContentFactory')
    def test_get_cf_creates_factory(self, mock_cf_class):
        """get_cf should create IntradayContentFactory."""
        mock_cf = Mock()
        mock_cf.start = 20240101
        mock_cf.end = 20240131
        mock_cf.universe_name = "crypto_test"
        mock_cf.frequency = "10T"
        mock_cf_class.return_value = mock_cf

        alpha = TestAlphaForTests()
        result = alpha.get_cf(20240101, 20240131)

        mock_cf_class.assert_called_once_with(
            universe_name="crypto_test",
            start=20240101,
            end=20240131,
            frequency="10T",
        )

    @patch('finter.data.content_model.intraday_loader.IntradayContentFactory')
    def test_get_cf_caches_result(self, mock_cf_class):
        """get_cf should cache and reuse the factory."""
        mock_cf = Mock()
        mock_cf.start = 20240101
        mock_cf.end = 20240131
        mock_cf.universe_name = "crypto_test"
        mock_cf.frequency = "10T"
        mock_cf_class.return_value = mock_cf

        alpha = TestAlphaForTests()

        # First call
        result1 = alpha.get_cf(20240101, 20240131)

        # Second call with same params should use cache
        result2 = alpha.get_cf(20240101, 20240131)

        # Factory should only be created once
        assert mock_cf_class.call_count == 1


class TestGetProcessor:
    """Test get_processor method."""

    @patch('finter.processing.HighFreqProcessor')
    def test_get_processor_creates_processor(self, mock_proc_class):
        """get_processor should create HighFreqProcessor."""
        mock_proc = Mock()
        mock_proc_class.return_value = mock_proc

        alpha = TestAlphaForTests()
        result = alpha.get_processor()

        mock_proc_class.assert_called_once_with(frequency="10T")

    @patch('finter.processing.HighFreqProcessor')
    def test_get_processor_caches_result(self, mock_proc_class):
        """get_processor should cache and reuse the processor."""
        mock_proc = Mock()
        mock_proc_class.return_value = mock_proc

        alpha = TestAlphaForTests()

        # First call
        result1 = alpha.get_processor()

        # Second call should use cache
        result2 = alpha.get_processor()

        # Processor should only be created once
        assert mock_proc_class.call_count == 1


class TestRepr:
    """Test __repr__ method."""

    def test_repr_format(self):
        """repr should include class name, universe, frequency."""
        alpha = TestAlphaForTests()
        repr_str = repr(alpha)

        assert "TestAlphaForTests" in repr_str
        assert "crypto_test" in repr_str
        assert "10T" in repr_str
        assert "39" in repr_str  # bars_per_day


class TestBacktest:
    """Test backtest method."""

    def test_backtest_requires_start_end(self):
        """backtest should fail without start/end."""
        alpha = TestAlphaForTests()
        alpha.start = None
        alpha.end = None

        with pytest.raises(ValueError, match="Missing required attributes"):
            alpha.backtest()

    def test_backtest_updates_attributes(self):
        """backtest should update instance attributes."""
        alpha = TestAlphaForTests()

        # Mock the internal backtest methods
        with patch.object(alpha, '_backtest_intraday') as mock_intraday:
            mock_intraday.return_value = Mock()

            alpha.backtest(
                universe="new_universe",
                start=20240101,
                end=20240131,
            )

            assert alpha.universe == "new_universe"
            assert alpha.start == 20240101
            assert alpha.end == 20240131


class TestBaseAlphaV2:
    """Test BaseAlphaV2 alias class."""

    def test_default_daily_frequency(self):
        """BaseAlphaV2 should default to daily frequency."""
        assert BaseAlphaV2.frequency == "D"


class TestCreateAlphaClass:
    """Test create_alpha_class factory function."""

    def test_creates_class_with_universe(self):
        """Created class should have correct universe."""
        AlphaClass = create_alpha_class(universe="test_universe")
        assert AlphaClass.universe == "test_universe"

    def test_creates_class_with_frequency(self):
        """Created class should have correct frequency."""
        AlphaClass = create_alpha_class(universe="test", frequency="30T")
        assert AlphaClass.frequency == "30T"

    def test_creates_class_with_get_function(self):
        """Created class should use provided get function."""
        def custom_get(self, start, end):
            return pd.DataFrame({"A": [1, 2, 3]})

        AlphaClass = create_alpha_class(
            universe="test",
            alpha_func=custom_get,
        )

        # The class should have the custom get method
        assert AlphaClass.get == custom_get


class TestDailyAlpha:
    """Test alpha with daily frequency."""

    def test_daily_is_not_intraday(self):
        """Daily alpha should not be intraday."""
        class DailyAlpha(BaseIntradayAlpha):
            universe = "kr_stock"
            frequency = "D"

            def get(self, start, end):
                return pd.DataFrame()

        alpha = DailyAlpha()
        assert alpha.is_intraday is False
        assert alpha.bars_per_day == 1
        assert alpha.annualization_factor == 252


class TestMultipleFrequencies:
    """Test alphas with different frequencies."""

    @pytest.fixture
    def alpha_classes(self):
        """Create alpha classes for different frequencies."""

        class Alpha10T(BaseIntradayAlpha):
            universe = "crypto_test"
            frequency = "10T"
            def get(self, start, end): return pd.DataFrame()

        class Alpha30T(BaseIntradayAlpha):
            universe = "crypto_test"
            frequency = "30T"
            def get(self, start, end): return pd.DataFrame()

        class Alpha1H(BaseIntradayAlpha):
            universe = "crypto_test"
            frequency = "1H"
            def get(self, start, end): return pd.DataFrame()

        return {"10T": Alpha10T, "30T": Alpha30T, "1H": Alpha1H}

    def test_10t_bars_per_day(self, alpha_classes):
        """10T should have 39 bars per day."""
        alpha = alpha_classes["10T"]()
        assert alpha.bars_per_day == 39

    def test_30t_bars_per_day(self, alpha_classes):
        """30T should have 13 bars per day."""
        alpha = alpha_classes["30T"]()
        assert alpha.bars_per_day == 13

    def test_1h_bars_per_day(self, alpha_classes):
        """1H should have 7 bars per day."""
        alpha = alpha_classes["1H"]()
        assert alpha.bars_per_day == 7

    def test_rolling_window_equivalence(self, alpha_classes):
        """63-day rolling window should be equivalent across frequencies."""
        for freq, AlphaClass in alpha_classes.items():
            alpha = AlphaClass()
            window = alpha.rolling_window(63)
            days_equivalent = window / alpha.bars_per_day
            assert abs(days_equivalent - 63) < 0.01


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
