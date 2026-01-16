"""
Unit tests for IntradaySimulator.

Tests:
- Initialization
- Slippage adjustment
- Weight calculation
- Vectorized backtest
- Statistics calculation
- Output resampling
- Result dataclass
"""

import pytest
from unittest.mock import Mock, patch
import numpy as np
import pandas as pd

from finter.backtest.intraday_simulator import (
    IntradaySimulator,
    IntradaySimulationResult,
)
from finter.backtest.config.frequency import (
    FrequencyConfig,
    get_frequency_config,
)


class TestIntradaySimulatorInit:
    """Test IntradaySimulator initialization."""

    def test_default_frequency(self):
        """Default frequency should be 10T."""
        sim = IntradaySimulator(
            market_type="crypto_test",
            start=20240101,
            end=20240131,
        )
        assert sim.frequency == "10T"

    def test_market_type_set(self):
        """Market type should be set."""
        sim = IntradaySimulator(
            market_type="crypto_test",
            start=20240101,
            end=20240131,
        )
        assert sim.market_type == "crypto_test"

    def test_frequency_config(self):
        """freq_config should be correct type."""
        sim = IntradaySimulator(
            market_type="crypto_test",
            start=20240101,
            end=20240131,
            frequency="10T",
        )
        assert sim.freq_config.code == "10T"
        assert sim.freq_config.bars_per_day == 39

    def test_intraday_flag(self):
        """_is_intraday should be True for intraday frequency."""
        sim = IntradaySimulator(
            market_type="crypto_test",
            start=20240101,
            end=20240131,
            frequency="10T",
        )
        assert sim._is_intraday is True

    def test_daily_flag(self):
        """_is_intraday should be False for daily frequency."""
        sim = IntradaySimulator(
            market_type="crypto_test",
            start=20240101,
            end=20240131,
            frequency="D",
        )
        assert sim._is_intraday is False


class TestSlippageAdjustment:
    """Test _adjust_slippage method."""

    def test_no_adjustment_for_daily(self):
        """Daily frequency should not adjust slippage."""
        sim = IntradaySimulator(
            market_type="crypto_test",
            start=20240101,
            end=20240131,
            frequency="D",
        )
        assert sim._adjust_slippage(10.0) == 10.0

    def test_adjustment_for_10t(self):
        """10T should reduce slippage by sqrt(bars_per_day)."""
        sim = IntradaySimulator(
            market_type="crypto_test",
            start=20240101,
            end=20240131,
            frequency="10T",
        )
        # crypto_test is 24/7, so bars_per_day = 144 for 10T
        expected = 10.0 / np.sqrt(sim._bars_per_day)
        assert abs(sim._adjust_slippage(10.0) - expected) < 0.001

    def test_zero_slippage_unchanged(self):
        """Zero slippage should remain zero."""
        sim = IntradaySimulator(
            market_type="crypto_test",
            start=20240101,
            end=20240131,
            frequency="10T",
        )
        assert sim._adjust_slippage(0.0) == 0.0


class TestCalculateWeights:
    """Test _calculate_weights method."""

    @pytest.fixture
    def sample_position(self):
        """Create sample position DataFrame."""
        dates = pd.date_range("2024-01-01", periods=10, freq="10T")
        data = {
            "A": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "B": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        }
        return pd.DataFrame(data, index=dates)

    def test_weights_sum_to_one(self, sample_position):
        """Weights should sum to ~1 in absolute terms."""
        sim = IntradaySimulator(
            market_type="crypto_test",
            start=20240101,
            end=20240131,
        )
        weights = sim._calculate_weights(sample_position)

        # Absolute sum should be 1
        weight_abs_sum = weights.abs().sum(axis=1)
        assert (np.abs(weight_abs_sum - 1.0) < 0.001).all()

    def test_weights_preserve_sign(self, sample_position):
        """Weights should preserve sign of positions."""
        sim = IntradaySimulator(
            market_type="crypto_test",
            start=20240101,
            end=20240131,
        )

        # Add some negative positions
        sample_position["C"] = -5

        weights = sim._calculate_weights(sample_position)

        # Positive positions should have positive weights
        assert (weights["A"] > 0).all()
        assert (weights["B"] > 0).all()

        # Negative positions should have negative weights
        assert (weights["C"] < 0).all()


class TestRunBacktest:
    """Test _run_backtest method."""

    @pytest.fixture
    def mock_data(self):
        """Create mock price and weight data."""
        dates = pd.date_range("2024-01-01", periods=100, freq="10T")

        prices = pd.DataFrame(
            np.random.randn(100, 3).cumsum(axis=0) + 100,
            index=dates,
            columns=["A", "B", "C"]
        )

        weights = pd.DataFrame(
            np.random.randn(100, 3) * 0.1,
            index=dates,
            columns=["A", "B", "C"]
        )
        # Normalize weights
        weights = weights.div(weights.abs().sum(axis=1), axis=0).fillna(0)

        return prices, weights

    def test_backtest_returns_dataframe(self, mock_data):
        """Backtest should return DataFrame."""
        prices, weights = mock_data
        sim = IntradaySimulator(
            market_type="crypto_test",
            start=20240101,
            end=20240131,
        )

        result = sim._run_backtest(
            prices=prices,
            weights=weights,
            initial_cash=1e8,
            buy_fee_tax=0.0,
            sell_fee_tax=0.0,
            slippage=0.0,
        )

        assert isinstance(result, pd.DataFrame)

    def test_backtest_has_required_columns(self, mock_data):
        """Backtest result should have nav, return, turnover, cost."""
        prices, weights = mock_data
        sim = IntradaySimulator(
            market_type="crypto_test",
            start=20240101,
            end=20240131,
        )

        result = sim._run_backtest(
            prices=prices,
            weights=weights,
            initial_cash=1e8,
            buy_fee_tax=0.0,
            sell_fee_tax=0.0,
            slippage=0.0,
        )

        assert "nav" in result.columns
        assert "return" in result.columns
        assert "turnover" in result.columns
        assert "cost" in result.columns

    def test_backtest_initial_nav(self, mock_data):
        """Initial NAV should be close to initial_cash."""
        prices, weights = mock_data
        sim = IntradaySimulator(
            market_type="crypto_test",
            start=20240101,
            end=20240131,
        )

        result = sim._run_backtest(
            prices=prices,
            weights=weights,
            initial_cash=1e8,
            buy_fee_tax=0.0,
            sell_fee_tax=0.0,
            slippage=0.0,
        )

        assert result["nav"].iloc[0] == 1e8


class TestCalculateStatistics:
    """Test _calculate_statistics method."""

    @pytest.fixture
    def sample_summary(self):
        """Create sample summary DataFrame."""
        dates = pd.date_range("2024-01-01", periods=100, freq="10T")
        nav = np.cumprod(1 + np.random.randn(100) * 0.01) * 1e8
        returns = np.diff(nav) / nav[:-1]
        returns = np.insert(returns, 0, 0)

        return pd.DataFrame({
            "nav": nav,
            "return": returns,
            "turnover": np.abs(np.random.randn(100) * 0.1),
            "cost": np.abs(np.random.randn(100) * 0.001),
        }, index=dates)

    def test_statistics_keys(self, sample_summary):
        """Statistics should have required keys."""
        sim = IntradaySimulator(
            market_type="crypto_test",
            start=20240101,
            end=20240131,
        )

        stats = sim._calculate_statistics(sample_summary)

        required_keys = [
            "total_return", "ann_return", "ann_volatility",
            "sharpe_ratio", "sortino_ratio", "calmar_ratio",
            "max_drawdown", "avg_turnover", "frequency", "bars_per_year"
        ]

        for key in required_keys:
            assert key in stats

    def test_frequency_in_statistics(self, sample_summary):
        """Frequency should be included in statistics."""
        sim = IntradaySimulator(
            market_type="crypto_test",
            start=20240101,
            end=20240131,
            frequency="10T",
        )

        stats = sim._calculate_statistics(sample_summary)

        assert stats["frequency"] == "10T"
        assert stats["bars_per_year"] == 252 * 39


class TestResampleSummary:
    """Test _resample_summary method."""

    @pytest.fixture
    def intraday_summary(self):
        """Create intraday summary DataFrame."""
        dates = pd.date_range("2024-01-01 09:00", periods=390, freq="1T")  # One day at 1T
        return pd.DataFrame({
            "nav": np.cumprod(1 + np.random.randn(390) * 0.001) * 1e8,
            "return": np.random.randn(390) * 0.001,
            "turnover": np.random.rand(390) * 0.01,
            "cost": np.random.rand(390) * 0.0001,
        }, index=dates)

    def test_resample_to_hourly(self, intraday_summary):
        """Resampling to hourly should reduce rows."""
        sim = IntradaySimulator(
            market_type="crypto_test",
            start=20240101,
            end=20240101,
            frequency="1T",
        )

        resampled = sim._resample_summary(intraday_summary, "1H")
        assert len(resampled) < len(intraday_summary)

    def test_resample_to_daily(self, intraday_summary):
        """Resampling to daily should give 1 row."""
        sim = IntradaySimulator(
            market_type="crypto_test",
            start=20240101,
            end=20240101,
            frequency="1T",
        )

        resampled = sim._resample_summary(intraday_summary, "D")
        assert len(resampled) == 1


class TestIntradaySimulationResult:
    """Test IntradaySimulationResult dataclass."""

    @pytest.fixture
    def sample_result(self):
        """Create sample simulation result."""
        dates = pd.date_range("2024-01-01", periods=100, freq="10T")
        summary = pd.DataFrame({
            "nav": np.linspace(1e8, 1.1e8, 100),
            "return": np.random.randn(100) * 0.01,
            "turnover": np.random.rand(100) * 0.1,
            "cost": np.random.rand(100) * 0.001,
        }, index=dates)

        weights = pd.DataFrame(
            np.random.randn(100, 3) * 0.1,
            index=dates,
            columns=["A", "B", "C"]
        )

        return IntradaySimulationResult(
            summary=summary,
            weights=weights,
            statistics={
                "total_return": 10.0,
                "sharpe_ratio": 1.5,
                "max_drawdown": -5.0,
            },
            frequency="10T",
            config=get_frequency_config("10T"),
        )

    def test_nav_property(self, sample_result):
        """nav property should return nav series."""
        assert isinstance(sample_result.nav, pd.Series)
        assert sample_result.nav.name == "nav"

    def test_returns_property(self, sample_result):
        """returns property should return return series."""
        assert isinstance(sample_result.returns, pd.Series)
        assert sample_result.returns.name == "return"

    def test_total_return_property(self, sample_result):
        """total_return should calculate correctly."""
        expected = (sample_result.nav.iloc[-1] / sample_result.nav.iloc[0] - 1) * 100
        assert abs(sample_result.total_return - expected) < 0.01

    def test_sharpe_ratio_property(self, sample_result):
        """sharpe_ratio should return from statistics."""
        assert sample_result.sharpe_ratio == 1.5

    def test_max_drawdown_property(self, sample_result):
        """max_drawdown should return from statistics."""
        assert sample_result.max_drawdown == -5.0

    def test_repr(self, sample_result):
        """repr should include key statistics."""
        repr_str = repr(sample_result)
        assert "IntradaySimulationResult" in repr_str
        assert "total_return" in repr_str
        assert "sharpe" in repr_str


class TestSimulatorRepr:
    """Test IntradaySimulator __repr__ method."""

    def test_repr_format(self):
        """repr should include key information."""
        sim = IntradaySimulator(
            market_type="crypto_test",
            start=20240101,
            end=20240131,
            frequency="10T",
        )
        repr_str = repr(sim)

        assert "IntradaySimulator" in repr_str
        assert "crypto_test" in repr_str
        assert "10T" in repr_str
        assert "20240101" in repr_str
        assert "20240131" in repr_str


class TestAlignData:
    """Test _align_data method."""

    def test_align_common_index(self):
        """Should align to common index."""
        sim = IntradaySimulator(
            market_type="crypto_test",
            start=20240101,
            end=20240131,
        )

        dates1 = pd.date_range("2024-01-01", periods=10, freq="10T")
        dates2 = pd.date_range("2024-01-01 00:30", periods=10, freq="10T")

        position = pd.DataFrame(
            np.random.randn(10, 2),
            index=dates1,
            columns=["A", "B"]
        )
        prices = pd.DataFrame(
            np.random.randn(10, 2),
            index=dates2,
            columns=["A", "B"]
        )

        aligned_pos, aligned_prices = sim._align_data(position, prices)

        # Should have common timestamps
        assert (aligned_pos.index == aligned_prices.index).all()

    def test_align_common_columns(self):
        """Should align to common columns."""
        sim = IntradaySimulator(
            market_type="crypto_test",
            start=20240101,
            end=20240131,
        )

        dates = pd.date_range("2024-01-01", periods=10, freq="10T")

        position = pd.DataFrame(
            np.random.randn(10, 3),
            index=dates,
            columns=["A", "B", "C"]
        )
        prices = pd.DataFrame(
            np.random.randn(10, 2),
            index=dates,
            columns=["A", "B"]
        )

        aligned_pos, aligned_prices = sim._align_data(position, prices)

        # Should only have common columns
        assert list(aligned_pos.columns) == ["A", "B"]
        assert list(aligned_prices.columns) == ["A", "B"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
