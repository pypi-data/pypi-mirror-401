"""
Unit tests for HighFreqProcessor.

Tests:
- Initialization
- Rolling z-score calculation
- Rolling rank calculation
- Cross-sectional rank
- Cross-sectional normalize
- Resampling
- Exponential decay
"""

import pytest
import numpy as np
import pandas as pd

from finter.processing.high_freq import HighFreqProcessor, ProcessingConfig


class TestHighFreqProcessorInit:
    """Test HighFreqProcessor initialization."""

    def test_default_init(self):
        """Default initialization with 10T frequency."""
        proc = HighFreqProcessor()
        assert proc.frequency == "10T"
        assert proc.freq_config.bars_per_day == 39

    def test_custom_frequency(self):
        """Custom frequency initialization."""
        proc = HighFreqProcessor(frequency="30T")
        assert proc.frequency == "30T"
        assert proc.freq_config.bars_per_day == 13

    def test_daily_frequency(self):
        """Daily frequency initialization."""
        proc = HighFreqProcessor(frequency="D")
        assert proc.frequency == "D"
        assert proc.freq_config.bars_per_day == 1

    def test_config_type(self):
        """Config should be ProcessingConfig."""
        proc = HighFreqProcessor()
        assert isinstance(proc.config, ProcessingConfig)


class TestRollingZscore:
    """Test rolling_zscore function."""

    @pytest.fixture
    def sample_df(self):
        """Create sample DataFrame for testing."""
        np.random.seed(42)
        dates = pd.date_range("2024-01-01", periods=100, freq="10T")
        data = np.random.randn(100, 3) * 10 + 100
        return pd.DataFrame(data, index=dates, columns=["A", "B", "C"])

    def test_zscore_shape(self, sample_df):
        """Output should have same shape as input."""
        proc = HighFreqProcessor()
        result = proc.rolling_zscore(sample_df, window=10)
        assert result.shape == sample_df.shape

    def test_zscore_columns(self, sample_df):
        """Output should have same columns."""
        proc = HighFreqProcessor()
        result = proc.rolling_zscore(sample_df, window=10)
        assert list(result.columns) == list(sample_df.columns)

    def test_zscore_nan_initial(self, sample_df):
        """Initial values should be NaN."""
        proc = HighFreqProcessor()
        window = 10
        result = proc.rolling_zscore(sample_df, window=window)
        assert result.iloc[:window - 1].isna().all().all()

    def test_zscore_range(self, sample_df):
        """Z-scores should typically be in reasonable range."""
        proc = HighFreqProcessor()
        result = proc.rolling_zscore(sample_df, window=20)
        valid = result.dropna()
        assert valid.abs().mean().mean() < 5  # Most z-scores within 5 std


class TestRollingRank:
    """Test rolling_rank function."""

    @pytest.fixture
    def sample_df(self):
        """Create sample DataFrame for testing."""
        np.random.seed(42)
        dates = pd.date_range("2024-01-01", periods=100, freq="10T")
        data = np.random.randn(100, 3) * 10 + 100
        return pd.DataFrame(data, index=dates, columns=["A", "B", "C"])

    def test_rank_shape(self, sample_df):
        """Output should have same shape as input."""
        proc = HighFreqProcessor()
        result = proc.rolling_rank(sample_df, window=10)
        assert result.shape == sample_df.shape

    def test_rank_range(self, sample_df):
        """Ranks should be between 0 and 1."""
        proc = HighFreqProcessor()
        result = proc.rolling_rank(sample_df, window=10)
        valid = result.dropna()
        assert (valid >= 0).all().all()
        assert (valid <= 1).all().all()


class TestCrossSectionalRank:
    """Test cross_sectional_rank function."""

    @pytest.fixture
    def sample_df(self):
        """Create sample DataFrame for testing."""
        dates = pd.date_range("2024-01-01", periods=10, freq="D")
        data = {
            "A": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "B": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
            "C": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        }
        return pd.DataFrame(data, index=dates)

    def test_cs_rank_shape(self, sample_df):
        """Output should have same shape as input."""
        proc = HighFreqProcessor()
        result = proc.cross_sectional_rank(sample_df)
        assert result.shape == sample_df.shape

    def test_cs_rank_first_row(self, sample_df):
        """First row ranks should be correct."""
        proc = HighFreqProcessor()
        result = proc.cross_sectional_rank(sample_df)
        # A=1 (rank 1), B=10 (rank 3), C=5 (rank 2)
        assert result.iloc[0]["A"] == 1.0
        assert result.iloc[0]["B"] == 3.0
        assert result.iloc[0]["C"] == 2.0


class TestCrossSectionalNormalize:
    """Test cross_sectional_normalize function."""

    @pytest.fixture
    def sample_df(self):
        """Create sample DataFrame for testing."""
        dates = pd.date_range("2024-01-01", periods=10, freq="D")
        data = {
            "A": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "B": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
            "C": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        }
        return pd.DataFrame(data, index=dates)

    def test_cs_normalize_shape(self, sample_df):
        """Output should have same shape as input."""
        proc = HighFreqProcessor()
        result = proc.cross_sectional_normalize(sample_df)
        assert result.shape == sample_df.shape

    def test_cs_normalize_mean_zero(self, sample_df):
        """Each row should have mean approximately zero."""
        proc = HighFreqProcessor()
        result = proc.cross_sectional_normalize(sample_df)
        row_means = result.mean(axis=1)
        assert (row_means.abs() < 1e-10).all()


class TestResample:
    """Test resample function."""

    @pytest.fixture
    def intraday_df(self):
        """Create intraday sample DataFrame."""
        dates = pd.date_range("2024-01-01 09:00", periods=78, freq="5T")  # One day of 5T
        data = np.arange(78).reshape(-1, 1) + 100
        return pd.DataFrame(data, index=dates, columns=["value"])

    def test_resample_10t_to_1h(self, intraday_df):
        """Resample 5T to 1H should reduce rows."""
        proc = HighFreqProcessor(frequency="5T")
        result = proc.resample(intraday_df, target_freq="1H", agg_func="last")
        assert len(result) < len(intraday_df)

    def test_resample_to_daily(self, intraday_df):
        """Resample to daily should have 1 row."""
        proc = HighFreqProcessor(frequency="5T")
        result = proc.resample(intraday_df, target_freq="D", agg_func="last")
        assert len(result) == 1


class TestExponentialDecay:
    """Test exponential_decay function."""

    @pytest.fixture
    def sample_df(self):
        """Create sample DataFrame."""
        dates = pd.date_range("2024-01-01", periods=50, freq="10T")
        data = np.random.randn(50, 2) * 10 + 100
        return pd.DataFrame(data, index=dates, columns=["A", "B"])

    def test_decay_shape(self, sample_df):
        """Output should have same shape as input."""
        proc = HighFreqProcessor()
        result = proc.exponential_decay(sample_df, half_life=10)
        assert result.shape == sample_df.shape


class TestUtilityFunctions:
    """Test utility functions."""

    def test_get_rolling_window_days(self):
        """Test day to bar conversion."""
        proc = HighFreqProcessor(frequency="10T")
        # 10T has 39 bars per day
        assert proc.get_rolling_window_days(1) == 39
        assert proc.get_rolling_window_days(5) == 195
        assert proc.get_rolling_window_days(63) == 2457

    def test_repr(self):
        """Test string representation."""
        proc = HighFreqProcessor(frequency="10T")
        repr_str = repr(proc)
        assert "HighFreqProcessor" in repr_str
        assert "10T" in repr_str
        assert "39" in repr_str


class TestFrequencyConversion:
    """Test frequency conversion helper."""

    def test_freq_to_polars_interval(self):
        """Test frequency to Polars interval conversion."""
        proc = HighFreqProcessor()

        assert proc._freq_to_polars_interval("1T") == "1m"
        assert proc._freq_to_polars_interval("10T") == "10m"
        assert proc._freq_to_polars_interval("30T") == "30m"
        assert proc._freq_to_polars_interval("1H") == "1h"
        assert proc._freq_to_polars_interval("D") == "1d"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
