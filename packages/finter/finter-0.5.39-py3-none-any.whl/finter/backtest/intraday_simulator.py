"""
Intraday Simulator for sub-daily frequency backtesting.

Extends the standard Simulator to support intraday frequencies
(10T, 30T, 1H) with appropriate cost adjustments and output resampling.

Usage:
    from finter.backtest.intraday_simulator import IntradaySimulator

    sim = IntradaySimulator(
        market_type="crypto_test",
        start=20240101,
        end=20240131,
        frequency="10T"
    )

    result = sim.run(position=position_df)
    print(result.summary)
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union

import numpy as np
import pandas as pd

from finter.backtest.config.config import (
    AVAILABLE_FREQUENCIES,
    CostConfig,
    IntradayExecutionConfig,
)
from finter.backtest.config.frequency import (
    BARS_PER_DAY,
    FrequencyConfig,
    get_bars_per_day,
    get_frequency_config,
    is_intraday,
)
from finter.settings import logger


@dataclass
class IntradaySimulationResult:
    """
    Container for intraday simulation results.

    Attributes:
        summary: Time series DataFrame with NAV, returns, turnover
        weights: Position weights over time
        statistics: Performance statistics dict
        frequency: Simulation frequency
        config: Frequency configuration
    """
    summary: pd.DataFrame
    weights: pd.DataFrame
    statistics: dict
    frequency: str
    config: FrequencyConfig

    @property
    def nav(self) -> pd.Series:
        """Net Asset Value time series."""
        return self.summary["nav"]

    @property
    def returns(self) -> pd.Series:
        """Return time series."""
        return self.summary["return"]

    @property
    def total_return(self) -> float:
        """Total return percentage."""
        return (self.nav.iloc[-1] / self.nav.iloc[0] - 1) * 100

    @property
    def sharpe_ratio(self) -> float:
        """Annualized Sharpe ratio."""
        return self.statistics.get("sharpe_ratio", np.nan)

    @property
    def max_drawdown(self) -> float:
        """Maximum drawdown percentage."""
        return self.statistics.get("max_drawdown", np.nan)

    def __repr__(self) -> str:
        return (
            f"IntradaySimulationResult("
            f"total_return={self.total_return:.2f}%, "
            f"sharpe={self.sharpe_ratio:.2f}, "
            f"max_dd={self.max_drawdown:.2f}%)"
        )


class IntradaySimulator:
    """
    Simulator extended for intraday frequency backtesting.

    Key differences from daily Simulator:
    1. Frequency-aware date/time handling
    2. Intraday-specific cost model (scaled slippage)
    3. Extended resampling (10T -> 1H -> D)
    4. Annualization based on bars per year

    Attributes:
        market_type: Universe name
        start: Start date (YYYYMMDD)
        end: End date (YYYYMMDD)
        frequency: Trading frequency
        freq_config: Frequency-specific configuration

    Example:
        sim = IntradaySimulator("crypto_test", 20240101, 20240131, "10T")
        result = sim.run(position=position_df, initial_cash=1e8)
    """

    def __init__(
        self,
        market_type: str,
        start: int = 20150101,
        end: int = None,
        frequency: AVAILABLE_FREQUENCIES = "10T",
        data_handler=None,
    ):
        """
        Initialize IntradaySimulator.

        Args:
            market_type: Universe name (e.g., 'crypto_test')
            start: Start date in YYYYMMDD format
            end: End date (defaults to today)
            frequency: Trading frequency ('10T', '30T', '1H', 'D')
            data_handler: Optional data handler
        """
        self.market_type = market_type
        self.start = start
        self.end = end or int(datetime.now().strftime("%Y%m%d"))
        self.frequency = frequency
        self.data_handler = data_handler

        # Frequency configuration
        self.freq_config = get_frequency_config(frequency)
        self._bars_per_day = get_bars_per_day(frequency, market_type)
        self._is_intraday = is_intraday(frequency)

        # Cost configuration (will be adjusted for frequency)
        self._base_slippage = 0.0
        self._cost_adjusted = False

    def run(
        self,
        position: pd.DataFrame,
        initial_cash: float = 1e8,
        buy_fee_tax: float = 0.0,
        sell_fee_tax: float = 0.0,
        slippage: float = 0.0,
        resample_output: Optional[str] = None,
        **kwargs
    ) -> IntradaySimulationResult:
        """
        Run intraday simulation.

        Args:
            position: Position DataFrame (index=timestamp, columns=tickers)
            initial_cash: Initial portfolio value
            buy_fee_tax: Buy transaction cost (basis points)
            sell_fee_tax: Sell transaction cost (basis points)
            slippage: Slippage cost (basis points, will be scaled)
            resample_output: Optional output resampling frequency ('D', 'W')
            **kwargs: Additional arguments

        Returns:
            IntradaySimulationResult with summary and statistics
        """
        # Validate position
        if position.empty:
            raise ValueError("Position DataFrame is empty")

        # Adjust costs for intraday
        adjusted_slippage = self._adjust_slippage(slippage)

        # Load price data
        prices = self._load_prices(position)

        # Align position and prices
        position, prices = self._align_data(position, prices)

        # Calculate weights
        weights = self._calculate_weights(position)

        # Run vectorized backtest
        summary = self._run_backtest(
            prices=prices,
            weights=weights,
            initial_cash=initial_cash,
            buy_fee_tax=buy_fee_tax,
            sell_fee_tax=sell_fee_tax,
            slippage=adjusted_slippage,
        )

        # Calculate statistics
        statistics = self._calculate_statistics(summary)

        # Resample output if requested
        if resample_output:
            summary = self._resample_summary(summary, resample_output)

        return IntradaySimulationResult(
            summary=summary,
            weights=weights,
            statistics=statistics,
            frequency=self.frequency,
            config=self.freq_config,
        )

    def _adjust_slippage(self, slippage: float) -> float:
        """
        Adjust slippage for intraday frequency.

        Slippage is scaled by sqrt(bars_per_day) heuristic,
        as impact per bar is typically lower for intraday.

        Args:
            slippage: Original slippage in basis points

        Returns:
            Adjusted slippage
        """
        if not self._is_intraday or slippage == 0:
            return slippage

        # Scale slippage down for intraday
        # Heuristic: sqrt(bars_per_day) reduction
        scale_factor = np.sqrt(self._bars_per_day)
        adjusted = slippage / scale_factor

        logger.debug(
            f"Slippage adjusted for {self.frequency}: "
            f"{slippage:.2f}bp -> {adjusted:.2f}bp"
        )

        return adjusted

    def _load_prices(self, position: pd.DataFrame) -> pd.DataFrame:
        """
        Load price data for position tickers.

        Args:
            position: Position DataFrame

        Returns:
            Price DataFrame aligned with position
        """
        from finter.data.content_model.intraday_loader import IntradayContentFactory

        tickers = position.columns.tolist()

        cf = IntradayContentFactory(
            universe_name=self.market_type,
            start=self.start,
            end=self.end,
            frequency=self.frequency,
        )

        # Load close prices
        prices = cf.get_df("close")

        # Filter to position tickers
        common_tickers = [t for t in tickers if t in prices.columns]
        if not common_tickers:
            logger.warning(
                f"No common tickers between position and price data. "
                f"Position: {tickers[:5]}..., Prices: {prices.columns.tolist()[:5]}..."
            )
            # Return prices as-is, alignment will handle it
            return prices

        return prices[common_tickers]

    def _align_data(
        self,
        position: pd.DataFrame,
        prices: pd.DataFrame
    ) -> tuple:
        """
        Align position and price data.

        Args:
            position: Position DataFrame
            prices: Price DataFrame

        Returns:
            Tuple of aligned (position, prices) DataFrames
        """
        # Ensure datetime index
        if not isinstance(position.index, pd.DatetimeIndex):
            position.index = pd.to_datetime(position.index.astype(str))
        if not isinstance(prices.index, pd.DatetimeIndex):
            prices.index = pd.to_datetime(prices.index.astype(str))

        # Find common index and columns
        common_index = position.index.intersection(prices.index)
        common_cols = [c for c in position.columns if c in prices.columns]

        if len(common_index) == 0:
            raise ValueError(
                f"No common timestamps between position and prices. "
                f"Position range: {position.index[0]} - {position.index[-1]}, "
                f"Prices range: {prices.index[0]} - {prices.index[-1]}"
            )

        position = position.loc[common_index, common_cols]
        prices = prices.loc[common_index, common_cols]

        return position, prices

    def _calculate_weights(self, position: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate portfolio weights from position.

        Args:
            position: Position DataFrame (raw signals)

        Returns:
            Normalized weights DataFrame
        """
        # Normalize to sum to 1 (long-only) or handle long-short
        position_abs_sum = position.abs().sum(axis=1)
        position_abs_sum = position_abs_sum.replace(0, np.nan)

        weights = position.div(position_abs_sum, axis=0)
        weights = weights.fillna(0)

        return weights

    def _run_backtest(
        self,
        prices: pd.DataFrame,
        weights: pd.DataFrame,
        initial_cash: float,
        buy_fee_tax: float,
        sell_fee_tax: float,
        slippage: float,
    ) -> pd.DataFrame:
        """
        Run vectorized backtest.

        Args:
            prices: Price DataFrame
            weights: Weight DataFrame
            initial_cash: Initial cash
            buy_fee_tax: Buy cost (bp)
            sell_fee_tax: Sell cost (bp)
            slippage: Slippage (bp)

        Returns:
            Summary DataFrame with NAV, returns, turnover
        """
        # Calculate returns
        returns = prices.pct_change().fillna(0)

        # Calculate weight changes (turnover)
        weight_changes = weights.diff().abs().sum(axis=1)
        weight_changes.iloc[0] = weights.iloc[0].abs().sum()  # Initial investment

        # Transaction costs
        total_cost_rate = (buy_fee_tax + sell_fee_tax + slippage) / 10000
        turnover_cost = weight_changes * total_cost_rate

        # Portfolio returns
        # Shifted weights represent holdings at start of each bar
        portfolio_returns = (weights.shift(1).fillna(0) * returns).sum(axis=1)
        portfolio_returns = portfolio_returns - turnover_cost

        # NAV calculation
        nav = (1 + portfolio_returns).cumprod() * initial_cash
        nav.iloc[0] = initial_cash

        # Create summary DataFrame
        summary = pd.DataFrame({
            "nav": nav,
            "return": portfolio_returns,
            "turnover": weight_changes,
            "cost": turnover_cost,
        })

        return summary

    def _calculate_statistics(self, summary: pd.DataFrame) -> dict:
        """
        Calculate performance statistics.

        Args:
            summary: Summary DataFrame

        Returns:
            Dictionary of statistics
        """
        nav = summary["nav"]
        returns = summary["return"]

        # Annualization factor
        ann_factor = self.freq_config.bars_per_year

        # Basic statistics
        total_return = (nav.iloc[-1] / nav.iloc[0] - 1) * 100
        mean_return = returns.mean()
        std_return = returns.std()

        # Annualized returns and volatility
        ann_return = mean_return * ann_factor * 100
        ann_volatility = std_return * np.sqrt(ann_factor) * 100

        # Sharpe ratio (assuming 0 risk-free rate)
        sharpe_ratio = (mean_return / std_return * np.sqrt(ann_factor)) if std_return > 0 else 0

        # Maximum drawdown
        rolling_max = nav.cummax()
        drawdown = (nav - rolling_max) / rolling_max
        max_drawdown = drawdown.min() * 100

        # Sortino ratio (downside deviation)
        downside_returns = returns[returns < 0]
        downside_std = downside_returns.std() if len(downside_returns) > 0 else 0
        sortino_ratio = (mean_return / downside_std * np.sqrt(ann_factor)) if downside_std > 0 else 0

        # Calmar ratio
        calmar_ratio = ann_return / abs(max_drawdown) if max_drawdown != 0 else 0

        # Average turnover
        avg_turnover = summary["turnover"].mean()

        return {
            "total_return": total_return,
            "ann_return": ann_return,
            "ann_volatility": ann_volatility,
            "sharpe_ratio": sharpe_ratio,
            "sortino_ratio": sortino_ratio,
            "calmar_ratio": calmar_ratio,
            "max_drawdown": max_drawdown,
            "avg_turnover": avg_turnover,
            "frequency": self.frequency,
            "bars_per_year": ann_factor,
        }

    def _resample_summary(
        self,
        summary: pd.DataFrame,
        target_freq: str
    ) -> pd.DataFrame:
        """
        Resample summary to target frequency.

        Args:
            summary: Summary DataFrame
            target_freq: Target frequency ('D', 'W', 'M')

        Returns:
            Resampled summary
        """
        return summary.resample(target_freq).agg({
            "nav": "last",
            "return": lambda x: (1 + x).prod() - 1,  # Compound returns
            "turnover": "sum",
            "cost": "sum",
        })

    def __repr__(self) -> str:
        return (
            f"IntradaySimulator("
            f"market_type='{self.market_type}', "
            f"frequency='{self.frequency}', "
            f"start={self.start}, end={self.end}, "
            f"bars_per_day={self._bars_per_day})"
        )
