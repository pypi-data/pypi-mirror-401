"""
Sample Intraday Alpha Models

Demonstrates usage of BaseIntradayAlpha with different frequencies
and data sources.

Usage:
    from finter.examples.intraday_alphas import CryptoMomentumAlpha

    alpha = CryptoMomentumAlpha()
    result = alpha.backtest(start=20240101, end=20240131)
    print(result)

Available Models:
- CryptoMomentumAlpha: 10T momentum on crypto_test
- CryptoMeanReversionAlpha: Mean reversion with z-score
- KRStockIntradayAlpha: KRX stock 30T momentum
"""

import pandas as pd
import numpy as np

from finter.framework_model.intraday_alpha import BaseIntradayAlpha


class CryptoMomentumAlpha(BaseIntradayAlpha):
    """
    10-minute momentum alpha for crypto.

    Strategy:
    - Buy assets with positive 1-day momentum
    - Short assets with negative 1-day momentum
    - Rebalance every 10 minutes

    Parameters:
    - Universe: crypto_test (BTC, ETH)
    - Frequency: 10T (10-minute)
    - Lookback: 1 day (39 bars)
    """

    universe = "crypto_test"
    frequency = "10T"

    def get(self, start: int, end: int) -> pd.DataFrame:
        """Generate momentum signals."""
        cf = self.get_cf(start, end)

        # Get close prices (Polars for efficiency)
        prices = cf.get_df("close")

        # 1-day momentum (39 bars for 10T)
        momentum_window = self.rolling_window(1)  # 39 bars
        returns = prices.pct_change(momentum_window)

        # Normalize to [-1, 1] range
        signals = returns.apply(lambda x: x / x.abs().max() if x.abs().max() > 0 else 0)

        return signals


class CryptoMeanReversionAlpha(BaseIntradayAlpha):
    """
    Mean reversion alpha using z-score.

    Strategy:
    - Calculate 5-day z-score of prices
    - Long when z-score < -2 (oversold)
    - Short when z-score > 2 (overbought)
    - Neutral otherwise

    Parameters:
    - Universe: crypto_test
    - Frequency: 10T
    - Z-score window: 5 days (195 bars)
    """

    universe = "crypto_test"
    frequency = "10T"

    def get(self, start: int, end: int) -> pd.DataFrame:
        """Generate mean reversion signals."""
        cf = self.get_cf(start, end)
        proc = self.get_processor()

        # Get close prices
        prices = cf.get_df("close")

        # Calculate z-score with 5-day window
        zscore_window = self.rolling_window(5)  # 195 bars
        rolling_mean = prices.rolling(zscore_window).mean()
        rolling_std = prices.rolling(zscore_window).std()

        zscore = (prices - rolling_mean) / rolling_std

        # Generate signals based on z-score
        signals = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)

        # Short overbought (z > 2)
        signals[zscore > 2] = -1.0

        # Long oversold (z < -2)
        signals[zscore < -2] = 1.0

        # Gradual signals in moderate zone
        moderate_long = (zscore < -1) & (zscore >= -2)
        signals[moderate_long] = -0.5 * zscore[moderate_long]

        moderate_short = (zscore > 1) & (zscore <= 2)
        signals[moderate_short] = -0.5 * zscore[moderate_short]

        return signals


class KRStockIntradayAlpha(BaseIntradayAlpha):
    """
    30-minute momentum alpha for Korean stocks.

    Strategy:
    - Intraday momentum for KRX stocks
    - Uses S3 intraday data when available
    - Fallback to daily data resampling

    Parameters:
    - Universe: kr_stock
    - Frequency: 30T (30-minute)
    - Lookback: 2 hours (4 bars)

    Note:
    - Requires S3 intraday data for full functionality
    - Set up data collector first: scripts/intraday-collector
    """

    universe = "kr_stock"
    frequency = "30T"

    def get(self, start: int, end: int) -> pd.DataFrame:
        """Generate intraday momentum signals for KR stocks."""
        cf = self.get_cf(start, end)

        # Get close prices
        prices = cf.get_df("close")

        # 2-hour momentum (4 bars for 30T)
        momentum_bars = 4
        returns = prices.pct_change(momentum_bars)

        # Cross-sectional rank (0-1)
        ranked = returns.rank(axis=1, pct=True)

        # Long-short: top 20% long, bottom 20% short
        signals = pd.DataFrame(0.0, index=ranked.index, columns=ranked.columns)
        signals[ranked >= 0.8] = 1.0
        signals[ranked <= 0.2] = -1.0

        return signals


class CryptoVWAPReversion(BaseIntradayAlpha):
    """
    VWAP reversion alpha.

    Strategy:
    - Track deviation from VWAP (volume-weighted average price)
    - Long when price < VWAP (discount)
    - Short when price > VWAP (premium)

    Parameters:
    - Universe: crypto_test
    - Frequency: 10T
    - VWAP window: 1 day rolling
    """

    universe = "crypto_test"
    frequency = "10T"

    def get(self, start: int, end: int) -> pd.DataFrame:
        """Generate VWAP reversion signals."""
        cf = self.get_cf(start, end)

        # Get price and volume
        close = cf.get_df("close")
        volume = cf.get_df("volume")

        # Calculate rolling VWAP (1-day window)
        vwap_window = self.rolling_window(1)

        # VWAP = sum(price * volume) / sum(volume)
        pv = close * volume
        rolling_pv = pv.rolling(vwap_window).sum()
        rolling_vol = volume.rolling(vwap_window).sum()
        vwap = rolling_pv / rolling_vol

        # Price deviation from VWAP (percentage)
        deviation = (close - vwap) / vwap

        # Generate signals: counter-trade the deviation
        signals = -deviation.clip(-0.1, 0.1) * 10  # Scale to [-1, 1]

        return signals


# Quick test function
def test_alpha(alpha_class, start: int = 20240101, end: int = 20240107):
    """
    Quick test for an alpha class.

    Args:
        alpha_class: Alpha class to test
        start: Start date
        end: End date

    Returns:
        Position DataFrame
    """
    alpha = alpha_class()
    position = alpha.get(start, end)

    print(f"Alpha: {alpha}")
    print(f"Position shape: {position.shape}")
    print(f"Position range: [{position.min().min():.3f}, {position.max().max():.3f}]")
    print(f"Non-zero entries: {(position != 0).sum().sum()}")

    return position


if __name__ == "__main__":
    # Test CryptoMomentumAlpha
    print("=" * 60)
    print("Testing CryptoMomentumAlpha")
    print("=" * 60)
    test_alpha(CryptoMomentumAlpha)

    print("\n" + "=" * 60)
    print("Testing CryptoMeanReversionAlpha")
    print("=" * 60)
    test_alpha(CryptoMeanReversionAlpha)
