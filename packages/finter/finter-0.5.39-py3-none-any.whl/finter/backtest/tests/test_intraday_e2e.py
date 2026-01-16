"""
End-to-end tests for the Intraday Trading Platform.

Tests the full pipeline:
1. Frequency configuration
2. IntradayContentFactory data loading
3. HighFreqProcessor data processing
4. BaseIntradayAlpha model definition
5. IntradaySimulator backtesting
6. Result statistics calculation

Usage:
    pytest finter/backtest/tests/test_intraday_e2e.py -v

Note:
    Some tests require network access to crypto_test universe.
    Tests with @pytest.mark.integration require live data.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import numpy as np
import pandas as pd
from datetime import datetime

# Core imports
from finter.backtest.config.frequency import (
    AVAILABLE_FREQUENCIES,
    BARS_PER_DAY,
    FrequencyConfig,
    get_frequency_config,
    is_intraday,
    get_bars_per_day,
)
from finter.processing.high_freq import HighFreqProcessor
from finter.framework_model.intraday_alpha import BaseIntradayAlpha
from finter.backtest.intraday_simulator import IntradaySimulator, IntradaySimulationResult


# =============================================================================
# Test Fixtures
# =============================================================================

@pytest.fixture
def mock_prices():
    """Generate mock price data for testing."""
    np.random.seed(42)
    dates = pd.date_range("2024-01-01 09:00", periods=390, freq="10T")  # 10 days
    tickers = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]

    data = {}
    for ticker in tickers:
        # Random walk with drift
        returns = np.random.randn(390) * 0.01 + 0.0001
        prices = 100 * np.cumprod(1 + returns)
        data[ticker] = prices

    return pd.DataFrame(data, index=dates)


@pytest.fixture
def mock_volume():
    """Generate mock volume data for testing."""
    np.random.seed(42)
    dates = pd.date_range("2024-01-01 09:00", periods=390, freq="10T")
    tickers = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]

    data = {}
    for ticker in tickers:
        volumes = np.random.lognormal(10, 1, 390)
        data[ticker] = volumes

    return pd.DataFrame(data, index=dates)


# =============================================================================
# E2E Test: Frequency System
# =============================================================================

class TestE2EFrequencySystem:
    """End-to-end test for frequency system."""

    def test_all_frequencies_have_config(self):
        """All frequencies should have valid configurations."""
        for freq in ["D", "1H", "30T", "10T", "5T", "1T"]:
            config = get_frequency_config(freq)
            assert isinstance(config, FrequencyConfig)
            assert config.code == freq
            assert config.bars_per_day > 0
            assert config.bars_per_year > 0
            assert config.rolling_short > 0
            assert config.rolling_long > 0

    def test_bars_per_day_scaling(self):
        """Higher frequency should have more bars per day."""
        assert BARS_PER_DAY["D"] < BARS_PER_DAY["1H"]
        assert BARS_PER_DAY["1H"] < BARS_PER_DAY["30T"]
        assert BARS_PER_DAY["30T"] < BARS_PER_DAY["10T"]
        assert BARS_PER_DAY["10T"] < BARS_PER_DAY["5T"]
        assert BARS_PER_DAY["5T"] < BARS_PER_DAY["1T"]

    def test_rolling_windows_equivalent_days(self):
        """Rolling windows should be equivalent in days across frequencies."""
        for freq in ["D", "10T", "30T", "1H"]:
            config = get_frequency_config(freq)

            # rolling_short should be ~63 days
            short_days = config.rolling_short / config.bars_per_day
            assert abs(short_days - 63) < 0.01

            # rolling_long should be ~252 days
            long_days = config.rolling_long / config.bars_per_day
            assert abs(long_days - 252) < 0.01


# =============================================================================
# E2E Test: Data Processing Pipeline
# =============================================================================

class TestE2EDataProcessing:
    """End-to-end test for data processing pipeline."""

    def test_processor_zscore_pipeline(self, mock_prices):
        """Test z-score calculation pipeline."""
        processor = HighFreqProcessor(frequency="10T")

        # Calculate rolling z-score (5 days = 195 bars)
        window = processor.get_rolling_window_days(5)
        assert window == 195

        zscore = processor.rolling_zscore(mock_prices, window=window)

        # Output shape should match input
        assert zscore.shape == mock_prices.shape

        # Valid z-scores should be in reasonable range
        valid = zscore.dropna()
        assert valid.abs().mean().mean() < 5

    def test_processor_cross_sectional_rank(self, mock_prices):
        """Test cross-sectional ranking pipeline."""
        processor = HighFreqProcessor(frequency="10T")

        ranked = processor.cross_sectional_rank(mock_prices)

        # Ranks should be 1, 2, 3 for 3 assets
        assert ranked.shape == mock_prices.shape
        assert set(ranked.iloc[-1].values) == {1.0, 2.0, 3.0}

    def test_processor_resample_pipeline(self, mock_prices):
        """Test resampling pipeline."""
        processor = HighFreqProcessor(frequency="10T")

        # Resample 10T to hourly
        hourly = processor.resample(mock_prices, target_freq="1H", agg_func="last")

        # Should have fewer rows
        assert len(hourly) < len(mock_prices)

        # Resample to daily
        daily = processor.resample(mock_prices, target_freq="D", agg_func="last")

        # Should have even fewer rows
        assert len(daily) < len(hourly)


# =============================================================================
# E2E Test: Alpha Model Pipeline
# =============================================================================

class TestMomentumAlpha(BaseIntradayAlpha):
    """Test momentum alpha for E2E testing."""
    universe = "crypto_test"
    frequency = "10T"

    def __init__(self, mock_prices=None):
        super().__init__()
        self._mock_prices = mock_prices

    def get(self, start: int, end: int) -> pd.DataFrame:
        """Generate momentum signals."""
        if self._mock_prices is not None:
            prices = self._mock_prices
        else:
            # Would use cf.get_df("close") in real scenario
            dates = pd.date_range("2024-01-01", periods=100, freq="10T")
            prices = pd.DataFrame(
                np.random.randn(100, 3).cumsum(axis=0) + 100,
                index=dates,
                columns=["A", "B", "C"]
            )

        # 1-day momentum (39 bars for 10T)
        momentum_window = self.rolling_window(1)
        returns = prices.pct_change(momentum_window)

        # Normalize signals
        signals = returns.div(returns.abs().max(axis=1), axis=0).fillna(0)
        return signals


class TestE2EAlphaModel:
    """End-to-end test for alpha model pipeline."""

    def test_alpha_initialization(self, mock_prices):
        """Test alpha model initialization."""
        alpha = TestMomentumAlpha(mock_prices=mock_prices)

        assert alpha.universe == "crypto_test"
        assert alpha.frequency == "10T"
        assert alpha.is_intraday is True
        assert alpha.bars_per_day == 39

    def test_alpha_get_signals(self, mock_prices):
        """Test alpha signal generation."""
        alpha = TestMomentumAlpha(mock_prices=mock_prices)

        signals = alpha.get(20240101, 20240110)

        # Signals should have same shape as prices
        assert signals.shape == mock_prices.shape

        # Signals should be normalized to [-1, 1]
        assert signals.max().max() <= 1.0
        assert signals.min().min() >= -1.0

    def test_alpha_rolling_window_helper(self, mock_prices):
        """Test rolling window helper method."""
        alpha = TestMomentumAlpha(mock_prices=mock_prices)

        # 1 day = 39 bars
        assert alpha.rolling_window(1) == 39

        # 5 days = 195 bars
        assert alpha.rolling_window(5) == 195

        # 63 days = 2457 bars
        assert alpha.rolling_window(63) == 2457


# =============================================================================
# E2E Test: Simulation Pipeline
# =============================================================================

class TestE2ESimulation:
    """End-to-end test for simulation pipeline."""

    def test_simulator_initialization(self):
        """Test simulator initialization."""
        sim = IntradaySimulator(
            market_type="crypto_test",
            start=20240101,
            end=20240110,
            frequency="10T",
        )

        assert sim.market_type == "crypto_test"
        assert sim.frequency == "10T"
        assert sim._is_intraday is True
        # crypto_test is 24/7, so 144 bars per day (24*60/10)
        assert sim._bars_per_day == 144

    def test_simulator_slippage_adjustment(self):
        """Test slippage is adjusted for intraday."""
        sim = IntradaySimulator(
            market_type="crypto_test",
            start=20240101,
            end=20240110,
            frequency="10T",
        )

        # Original slippage
        original = 10.0

        # Adjusted should be smaller
        adjusted = sim._adjust_slippage(original)

        assert adjusted < original
        # Use actual bars_per_day from simulator (crypto_test = 144)
        assert abs(adjusted - original / np.sqrt(sim._bars_per_day)) < 0.001

    def test_simulator_weight_calculation(self, mock_prices):
        """Test weight calculation."""
        sim = IntradaySimulator(
            market_type="crypto_test",
            start=20240101,
            end=20240110,
        )

        # Create non-zero positions (use random values, not pct_change which has NaN)
        np.random.seed(42)
        positions = pd.DataFrame(
            np.random.randn(len(mock_prices), len(mock_prices.columns)),
            index=mock_prices.index,
            columns=mock_prices.columns
        )

        weights = sim._calculate_weights(positions)

        # Weights should sum to ~1 in absolute terms
        abs_sum = weights.abs().sum(axis=1)
        assert (np.abs(abs_sum - 1.0) < 0.001).all()

    def test_simulator_backtest_run(self, mock_prices):
        """Test full backtest run with mock data."""
        sim = IntradaySimulator(
            market_type="crypto_test",
            start=20240101,
            end=20240110,
        )

        # Create simple positions (momentum-like)
        positions = mock_prices.pct_change(39).fillna(0)

        # Normalize positions
        positions = positions.div(positions.abs().sum(axis=1), axis=0).fillna(0)

        # Run backtest
        summary = sim._run_backtest(
            prices=mock_prices,
            weights=positions,
            initial_cash=1e8,
            buy_fee_tax=0.0,
            sell_fee_tax=0.0,
            slippage=0.0,
        )

        # Check output
        assert "nav" in summary.columns
        assert "return" in summary.columns
        assert summary["nav"].iloc[0] == 1e8
        assert len(summary) == len(mock_prices)

    def test_simulator_statistics_calculation(self, mock_prices):
        """Test statistics calculation."""
        sim = IntradaySimulator(
            market_type="crypto_test",
            start=20240101,
            end=20240110,
            frequency="10T",
        )

        # Create mock summary
        dates = mock_prices.index
        nav = np.linspace(1e8, 1.1e8, len(dates))
        returns = np.diff(nav) / nav[:-1]
        returns = np.insert(returns, 0, 0)

        summary = pd.DataFrame({
            "nav": nav,
            "return": returns,
            "turnover": np.abs(np.random.randn(len(dates)) * 0.1),
            "cost": np.abs(np.random.randn(len(dates)) * 0.001),
        }, index=dates)

        stats = sim._calculate_statistics(summary)

        # Check all required statistics
        assert "total_return" in stats
        assert "ann_return" in stats
        assert "ann_volatility" in stats
        assert "sharpe_ratio" in stats
        assert "max_drawdown" in stats
        assert "frequency" in stats
        assert stats["frequency"] == "10T"
        assert stats["bars_per_year"] == 252 * 39


# =============================================================================
# E2E Test: Full Pipeline Integration
# =============================================================================

class TestE2EFullPipeline:
    """End-to-end test for complete pipeline integration."""

    def test_full_pipeline_mock_data(self, mock_prices, mock_volume):
        """Test complete pipeline with mock data."""
        # Step 1: Create processor
        processor = HighFreqProcessor(frequency="10T")

        # Step 2: Calculate signals
        # Momentum signal (1-day return)
        returns = mock_prices.pct_change(39).fillna(0)

        # Z-score normalization (5-day window)
        zscore = processor.rolling_zscore(returns, window=195)

        # Cross-sectional rank
        ranked = processor.cross_sectional_rank(zscore)

        # Step 3: Generate positions
        # Long top, short bottom
        positions = pd.DataFrame(0.0, index=ranked.index, columns=ranked.columns)
        positions[ranked >= 2.5] = 1.0
        positions[ranked <= 1.5] = -1.0

        # Step 4: Create simulator
        sim = IntradaySimulator(
            market_type="crypto_test",
            start=20240101,
            end=20240110,
            frequency="10T",
        )

        # Step 5: Calculate weights
        weights = sim._calculate_weights(positions)

        # Step 6: Run backtest
        summary = sim._run_backtest(
            prices=mock_prices,
            weights=weights,
            initial_cash=1e8,
            buy_fee_tax=3.0,
            sell_fee_tax=3.0,
            slippage=5.0,
        )

        # Step 7: Calculate statistics
        stats = sim._calculate_statistics(summary)

        # Step 8: Create result
        result = IntradaySimulationResult(
            summary=summary,
            weights=weights,
            statistics=stats,
            frequency="10T",
            config=get_frequency_config("10T"),
        )

        # Verify complete pipeline
        assert isinstance(result, IntradaySimulationResult)
        assert result.frequency == "10T"
        assert len(result.summary) == len(mock_prices)
        assert "total_return" in result.statistics
        assert "sharpe_ratio" in result.statistics

    def test_daily_vs_intraday_consistency(self, mock_prices):
        """Test that daily and intraday use consistent scaling."""
        # Daily config
        daily_config = get_frequency_config("D")

        # Intraday config
        intraday_config = get_frequency_config("10T")

        # Annualization should scale proportionally
        expected_ratio = BARS_PER_DAY["10T"] / BARS_PER_DAY["D"]
        actual_ratio = intraday_config.bars_per_year / daily_config.bars_per_year

        assert abs(expected_ratio - actual_ratio) < 0.01

    def test_backward_compatibility_daily(self, mock_prices):
        """Test that daily frequency works as expected."""
        # Resample to daily
        daily_prices = mock_prices.resample("D").last()

        # Create daily simulator
        sim = IntradaySimulator(
            market_type="crypto_test",
            start=20240101,
            end=20240110,
            frequency="D",
        )

        # Should not be intraday
        assert sim._is_intraday is False

        # Slippage should not be adjusted for daily
        assert sim._adjust_slippage(10.0) == 10.0


# =============================================================================
# E2E Test: Result Dataclass
# =============================================================================

class TestE2EResultDataclass:
    """End-to-end test for result dataclass."""

    def test_result_properties(self, mock_prices):
        """Test result dataclass properties."""
        dates = mock_prices.index
        nav = np.linspace(1e8, 1.1e8, len(dates))
        returns = np.diff(nav) / nav[:-1]
        returns = np.insert(returns, 0, 0)

        summary = pd.DataFrame({
            "nav": nav,
            "return": returns,
            "turnover": np.abs(np.random.randn(len(dates)) * 0.1),
            "cost": np.abs(np.random.randn(len(dates)) * 0.001),
        }, index=dates)

        weights = pd.DataFrame(
            np.random.randn(len(dates), 3) * 0.1,
            index=dates,
            columns=mock_prices.columns
        )

        result = IntradaySimulationResult(
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

        # Test properties
        assert isinstance(result.nav, pd.Series)
        assert isinstance(result.returns, pd.Series)
        assert abs(result.total_return - 10.0) < 0.1  # Calculated from nav
        assert result.sharpe_ratio == 1.5
        assert result.max_drawdown == -5.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
