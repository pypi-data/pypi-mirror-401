"""
High-frequency data processing module.

This module provides high-performance data processing utilities
for intraday quantitative analysis using a hybrid approach:
- Polars for data manipulation (columnar, lazy evaluation)
- NumPy for intermediate computations
- Numba for CPU-intensive operations

Example:
    from finter.processing import HighFreqProcessor

    processor = HighFreqProcessor(frequency="10T")
    zscore = processor.rolling_zscore(df, window=39*5)  # 5-day window for 10T
"""

from finter.processing.high_freq import HighFreqProcessor

__all__ = ["HighFreqProcessor"]
