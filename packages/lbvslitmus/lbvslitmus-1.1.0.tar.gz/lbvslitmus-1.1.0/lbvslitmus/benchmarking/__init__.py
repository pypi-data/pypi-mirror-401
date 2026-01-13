"""Benchmarking module for Litmus.

This module provides tools for benchmarking molecular embedding models
and comparing results with baseline fingerprints using Bayesian statistics.
"""

from lbvslitmus.benchmarking.benchmark import Benchmark, BenchmarkResults
from lbvslitmus.comparison.baseline_comparator import (
    BaselineComparator,
    ComparisonResults,
)
from lbvslitmus.comparison.baseline_loader import AVAILABLE_BASELINES, BaselineLoader

__all__ = [
    "AVAILABLE_BASELINES",
    "BaselineComparator",
    "BaselineLoader",
    "Benchmark",
    "BenchmarkResults",
    "ComparisonResults",
]
