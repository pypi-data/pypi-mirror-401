"""
Base class for intraday alpha models.

Extends BaseAlpha with intraday-specific features:
- Explicit frequency parameter
- IntradayContentFactory integration
- HighFreqProcessor for optimized data processing
- Automatic IntradaySimulator selection

Usage:
    from finter.framework_model.intraday_alpha import BaseIntradayAlpha

    class MyIntradayAlpha(BaseIntradayAlpha):
        universe = "crypto_test"
        frequency = "10T"

        def get(self, start, end):
            cf = self.get_cf(start, end)
            proc = self.get_processor()

            # Polars for large data
            prices = cf.get_pl("close")
            signals = proc.rolling_zscore(prices, window=195)  # ~5 days

            return signals.to_pandas()

    alpha = MyIntradayAlpha()
    result = alpha.backtest(start=20240101, end=20240131)
"""

from abc import ABCMeta, abstractmethod
from typing import Optional

import pandas as pd

from finter.backtest.config.frequency import (
    AVAILABLE_FREQUENCIES,
    FrequencyConfig,
    get_frequency_config,
    is_intraday,
)
from finter.framework_model.alpha import BaseAlpha


class BaseIntradayAlpha(BaseAlpha):
    """
    Base class for intraday alpha models.

    Extends BaseAlpha with:
    - Explicit frequency attribute
    - IntradayContentFactory helper
    - HighFreqProcessor helper
    - Automatic IntradaySimulator selection for backtesting

    Class Attributes:
        universe (str): Universe name (e.g., 'crypto_test', 'kr_stock')
        frequency (AVAILABLE_FREQUENCIES): Trading frequency ('10T', '30T', '1H', 'D')
        start (int): Start date (YYYYMMDD)
        end (int): End date (YYYYMMDD)

    Example:
        class MomentumAlpha(BaseIntradayAlpha):
            universe = "crypto_test"
            frequency = "10T"

            def get(self, start, end):
                cf = self.get_cf(start, end)
                prices = cf.get_df("close")
                return prices.pct_change(39)  # 1-day momentum for 10T
    """

    # Class attributes (override in subclass)
    universe: str = None
    frequency: AVAILABLE_FREQUENCIES = "10T"  # Default: 10-minute
    start: int = None
    end: int = None
    data_handler = None

    # Instance caches
    _cf_cache: Optional["IntradayContentFactory"] = None
    _processor_cache: Optional["HighFreqProcessor"] = None

    def __init__(self):
        """Initialize the intraday alpha."""
        super().__init__()
        self._cf_cache = None
        self._processor_cache = None

    @abstractmethod
    def get(self, start: int, end: int) -> pd.DataFrame:
        """
        Generate alpha signals.

        Must be implemented by subclasses.

        Args:
            start: Start date (YYYYMMDD for daily, YYYYMMDDHHMM for intraday)
            end: End date (same format as start)

        Returns:
            DataFrame with DatetimeIndex and ticker columns.
            Values are position weights (signed for long/short).
        """
        pass

    def get_cf(self, start: int, end: int) -> "IntradayContentFactory":
        """
        Get or create IntradayContentFactory for this alpha.

        Caches the factory for reuse within the same date range.

        Args:
            start: Start date
            end: End date

        Returns:
            IntradayContentFactory instance

        Example:
            cf = self.get_cf(20240101, 20240131)
            prices = cf.get_df("close")
        """
        from finter.data.content_model.intraday_loader import IntradayContentFactory

        # Check if cache is valid
        if (
            self._cf_cache is not None
            and self._cf_cache.start == start
            and self._cf_cache.end == end
            and self._cf_cache.universe_name == self.universe
            and self._cf_cache.frequency == self.frequency
        ):
            return self._cf_cache

        # Create new factory
        self._cf_cache = IntradayContentFactory(
            universe_name=self.universe,
            start=start,
            end=end,
            frequency=self.frequency,
        )
        return self._cf_cache

    def get_processor(self) -> "HighFreqProcessor":
        """
        Get HighFreqProcessor for optimized data processing.

        Caches the processor for reuse.

        Returns:
            HighFreqProcessor instance

        Example:
            proc = self.get_processor()
            zscore = proc.rolling_zscore(data, window=195)
        """
        from finter.processing import HighFreqProcessor

        if self._processor_cache is None:
            self._processor_cache = HighFreqProcessor(frequency=self.frequency)
        return self._processor_cache

    @property
    def freq_config(self) -> FrequencyConfig:
        """Get frequency configuration."""
        return get_frequency_config(self.frequency)

    @property
    def is_intraday(self) -> bool:
        """Check if this alpha uses intraday frequency."""
        return is_intraday(self.frequency)

    @property
    def bars_per_day(self) -> int:
        """Get number of bars per trading day."""
        return self.freq_config.bars_per_day

    @property
    def annualization_factor(self) -> int:
        """Get annualization factor for statistics."""
        return self.freq_config.bars_per_year

    def rolling_window(self, days: int) -> int:
        """
        Convert days to rolling window size for current frequency.

        Args:
            days: Number of days

        Returns:
            Window size in bars

        Example:
            window_63d = self.rolling_window(63)  # ~2457 for 10T
        """
        return self.freq_config.bars_per_day * days

    def backtest(
        self,
        universe: str = None,
        start: int = None,
        end: int = None,
        data_handler=None,
        **kwargs
    ):
        """
        Run backtest with automatic simulator selection.

        For intraday frequencies, uses IntradaySimulator.
        For daily frequency, uses standard Simulator.

        Args:
            universe: Override universe
            start: Override start date
            end: Override end date
            data_handler: Override data handler
            **kwargs: Additional arguments for simulator

        Returns:
            Simulation result with summary statistics

        Example:
            result = alpha.backtest(start=20240101, end=20240131)
            print(result.summary)
        """
        # Update instance attributes
        if universe is not None:
            self.universe = universe
        if start is not None:
            self.start = start
        if end is not None:
            self.end = end
        if data_handler is not None:
            self.data_handler = data_handler

        # Validate required attributes
        missing_attrs = [
            attr for attr in ["start", "end", "universe"]
            if getattr(self, attr) is None
        ]
        if missing_attrs:
            raise ValueError(
                f"Missing required attributes: {', '.join(missing_attrs)}. "
                f"Please set them before calling backtest()."
            )

        # Get position
        position = self.get(self.start, self.end)

        # Select appropriate simulator
        if self.is_intraday:
            return self._backtest_intraday(position, **kwargs)
        else:
            return self._backtest_daily(position, **kwargs)

    def _backtest_intraday(self, position: pd.DataFrame, **kwargs):
        """Run intraday backtest."""
        from finter.backtest.intraday_simulator import IntradaySimulator

        simulator = IntradaySimulator(
            market_type=self.universe,
            start=self.start,
            end=self.end,
            frequency=self.frequency,
            data_handler=self.data_handler,
        )

        return simulator.run(position=position, **kwargs)

    def _backtest_daily(self, position: pd.DataFrame, **kwargs):
        """Run daily backtest (standard path)."""
        from finter.backtest.__legacy_support.main import Simulator

        simulator = Simulator(self.start, self.end, data_handler=self.data_handler)
        result = simulator.run(universe=self.universe, position=position)
        return result.summary

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"universe='{self.universe}', "
            f"frequency='{self.frequency}', "
            f"bars_per_day={self.bars_per_day})"
        )


# Convenience alias for gradual migration
class BaseAlphaV2(BaseIntradayAlpha):
    """
    Alias for BaseIntradayAlpha.

    Use this for gradual migration from BaseAlpha to BaseIntradayAlpha.
    Defaults to daily frequency for backward compatibility.
    """
    frequency = "D"  # Default to daily


# Factory function
def create_alpha_class(
    universe: str,
    frequency: AVAILABLE_FREQUENCIES = "10T",
    alpha_func=None,
):
    """
    Factory function to create alpha class dynamically.

    Args:
        universe: Universe name
        frequency: Trading frequency
        alpha_func: Function that returns position DataFrame

    Returns:
        Alpha class

    Example:
        MyAlpha = create_alpha_class(
            universe="crypto_test",
            frequency="10T",
            alpha_func=lambda self, s, e: self.get_cf(s, e).get_df("close").pct_change()
        )
        alpha = MyAlpha()
    """
    class DynamicAlpha(BaseIntradayAlpha):
        pass

    DynamicAlpha.universe = universe
    DynamicAlpha.frequency = frequency

    if alpha_func:
        DynamicAlpha.get = alpha_func

    return DynamicAlpha
