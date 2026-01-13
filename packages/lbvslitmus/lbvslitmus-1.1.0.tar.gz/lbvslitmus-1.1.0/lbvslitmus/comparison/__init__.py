"""Comparison module for Litmus.

This module provides functionality for comparing benchmark results with
baseline fingerprints using Bayesian statistical methods.
"""

from lbvslitmus.comparison.baseline_comparator import (
    BaselineComparator,
    ComparisonResults,
)
from lbvslitmus.comparison.baseline_loader import AVAILABLE_BASELINES, BaselineLoader
from lbvslitmus.comparison.comparison_visualization import (
    plot_all_comparisons,
    plot_win_counts,
)

__all__ = [
    "AVAILABLE_BASELINES",
    "BaselineComparator",
    "BaselineLoader",
    "ComparisonResults",
    "plot_all_comparisons",
    "plot_win_counts",
]
