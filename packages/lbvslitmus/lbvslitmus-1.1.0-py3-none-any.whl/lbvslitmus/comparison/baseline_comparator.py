"""Baseline comparison functionality for statistical fingerprint evaluation.

This module provides functionality for comparing benchmark results with baseline
fingerprints using Bayesian Bradley-Terry statistical tests. Results are aggregated
across all ML models to compare the quality of molecular representations.
"""

from dataclasses import dataclass
from typing import Any, List, Optional, Union

import pandas as pd
from bbttest import PyBBT, TieSolver

from lbvslitmus.comparison.baseline_loader import BaselineLoader


@dataclass
class ComparisonResults:
    """Results from Bayesian Bradley-Terry comparison of fingerprints.

    This class stores the posterior table from the statistical comparison
    and provides methods for accessing and visualizing the results.

    Parameters
    ----------
    posterior_table : pd.DataFrame
        Posterior table with comparison results. Columns include:
        - mean: posterior mean probability of winning vs control
        - hdi_low/hdi_high: Highest Density Interval bounds
        - delta: difference from 0.5
        - above_50: probability > 0.5
        - in_rope: probability within ROPE
        - weak_interpretation: "better", "equivalent", or "worse"
    metric : str
        The metric used for comparison (e.g., "AUROC", "AUPRC").
    fingerprint_name : str
        Name of the fingerprint being compared.
    control_fingerprint : Optional[str]
        Name of the control fingerprint used in comparison.
    rope_value : float
        Region of Practical Equivalence threshold used.

    Examples
    --------
    >>> comparator = BaselineComparator(results.to_dataframe())
    >>> comparison = comparator.compare("MACCS", metric="AUROC")
    >>> print(comparison.posterior_table)
    >>> comparison.plot()  # Future visualization method
    """

    posterior_table: pd.DataFrame
    metric: str
    fingerprint_name: str
    control_fingerprint: Optional[str]
    rope_value: float

    def to_dataframe(self) -> pd.DataFrame:
        """Convert results to pandas DataFrame.

        Returns
        -------
        pd.DataFrame
            Posterior table with comparison results.
        """
        return self.posterior_table.copy()

    def __str__(self) -> str:
        """Return string representation of comparison results."""
        if self.posterior_table.empty:
            return "No comparison results available."

        lines = [
            f"Comparison Results for {self.fingerprint_name}",
            f"Metric: {self.metric}",
            f"ROPE value: {self.rope_value}",
        ]
        if self.control_fingerprint:
            lines.append(f"Control fingerprint: {self.control_fingerprint}")
        lines.append("")
        lines.append(str(self.posterior_table))
        return "\n".join(lines)

    def __repr__(self) -> str:
        """Return detailed string representation."""
        return (
            f"ComparisonResults(metric={self.metric!r}, "
            f"fingerprint_name={self.fingerprint_name!r}, "
            f"control_fingerprint={self.control_fingerprint!r}, "
            f"rope_value={self.rope_value})"
        )

    def plot(self, output_dir: str = "plots") -> None:
        """Generate visualization plots from comparison results.

        Creates heatmap and win count visualizations for the comparison results.

        Parameters
        ----------
        output_dir : str, default="plots"
            Directory to save plots

        Examples
        --------
        >>> comparison = comparator.compare("MACCS", metric="AUROC")
        >>> comparison.plot(output_dir="my_plots")
        """
        from lbvslitmus.comparison.comparison_visualization import plot_all_comparisons

        plot_all_comparisons(self, output_dir=output_dir)


class BaselineComparator:
    """Compare benchmark results with baseline fingerprints using Bayesian statistics.

    This class performs Bayesian statistical comparisons between your fingerprint
    results and baseline fingerprints. Results are aggregated across all ML models
    (RandomForest, LogisticRegression, SimilaritySearch) to compare the quality
    of molecular representations.

    Parameters
    ----------
    results_df : pd.DataFrame
        Benchmark results DataFrame with columns:
        benchmark, model, target, metric, score, and optionally seed.

    Examples
    --------
    >>> from lbvslitmus.benchmarking import BenchmarkResults, BaselineComparator
    >>> results = benchmark.run()
    >>> comparator = BaselineComparator(results.to_dataframe())
    >>> comparison = comparator.compare(
    ...     baseline="MACCS",
    ...     metric="AUROC",
    ...     fingerprint_name="MyECFP4",
    ...     control_fingerprint="MyECFP4"
    ... )
    >>> print(comparison.posterior_table)
    """

    def __init__(self, results_df: pd.DataFrame):
        """Initialize the baseline comparator with benchmark results.

        Parameters
        ----------
        results_df : pd.DataFrame
            Benchmark results DataFrame. Must have columns:
            benchmark, model, target, metric, score, and optionally seed.
        """
        if results_df.empty:
            raise ValueError("Results DataFrame cannot be empty.")
        self.results_df = results_df.copy()

    def compare(
        self,
        baseline: Union[str, List[str], pd.DataFrame],
        metric: str = "AUROC",
        rope_value: float = 0.01,
        fingerprint_name: str = "new",
        control_fingerprint: Optional[str] = None,
        **pymc_kwargs: Any,
    ) -> pd.DataFrame:
        """Compare your fingerprint with baselines using Bayesian Bradley-Terry test.

        This method performs a Bayesian statistical comparison between your
        fingerprint and baseline fingerprints. Results are aggregated across
        all ML models (RandomForest, LogisticRegression, SimilaritySearch) to
        compare the quality of molecular representations.

        Parameters
        ----------
        baseline : str, List[str], or pd.DataFrame
            Baseline fingerprint(s) to compare against. Can be:
            - A fingerprint name (e.g., "ECFP4") to load from HuggingFace
            - A list of fingerprint names (e.g., ["ECFP4", "MACCS"])
            - A DataFrame with baseline results (must have columns:
              benchmark, model, target, metric, score, fingerprint)
        metric : str, default="AUROC"
            The metric to use for comparison. Must be present in both
            the benchmark results and baseline results.
        rope_value : float, default=0.01
            Region of Practical Equivalence threshold. Differences smaller
            than this are considered ties.
        fingerprint_name : str, default="new"
            Name for your fingerprint in the comparison results.
        control_fingerprint : str, optional
            Name of the fingerprint to use as control/reference for comparison.
            If provided, the posterior table will show probabilities of
            each fingerprint beating the control. Use your fingerprint name
            to see how baselines compare against yours.
        **pymc_kwargs
            Additional keyword arguments passed to the PyMC sampler.
            Common options include:
            - draws: int, number of samples (default: 1000)
            - chains: int, number of chains (default: 4)
            - cores: int, number of CPU cores to use

        Returns
        -------
        ComparisonResults
            ComparisonResults object containing:
            - posterior_table: DataFrame with comparison results. Columns include:
              - mean: posterior mean probability of winning vs control
              - hdi_low/hdi_high: Highest Density Interval bounds
              - delta: difference from 0.5
              - above_50: probability > 0.5
              - in_rope: probability within ROPE
              - weak_interpretation: "better", "equivalent", or "worse"
            - metric: The metric used for comparison
            - fingerprint_name: Name of the fingerprint being compared
            - control_fingerprint: Name of the control fingerprint
            - rope_value: ROPE threshold used

        Raises
        ------
        ValueError
            If no results are available, if the metric is not found,
            or if there's no overlap between benchmark and baseline datasets.

        Examples
        --------
        >>> comparator = BaselineComparator(results.to_dataframe())
        >>> # Compare your fingerprint with MACCS baseline
        >>> comparison = comparator.compare(
        ...     "MACCS",
        ...     metric="AUROC",
        ...     fingerprint_name="MyECFP4",
        ...     control_fingerprint="MyECFP4"
        ... )
        >>> print(comparison.posterior_table)
        >>> # Or convert to DataFrame
        >>> df = comparison.to_dataframe()

        >>> # Compare with multiple baselines
        >>> comparison = comparator.compare(
        ...     ["ECFP4", "MACCS", "AtomPair"],
        ...     metric="AUROC",
        ...     fingerprint_name="MyFingerprint",
        ...     control_fingerprint="MyFingerprint"
        ... )
        >>> print(comparison)

        Notes
        -----
        The Bradley-Terry model is a probabilistic model for pairwise comparisons.
        Results are aggregated across all ML models to compare fingerprint quality.

        When using control_fingerprint, the interpretation is:
        - If baseline's mean < 0.5: your fingerprint is better
        - If baseline's mean > 0.5: baseline fingerprint is better
        - If in_rope is True: fingerprints are practically equivalent

        References
        ----------
        .. [1] Wainer, J. "A Bayesian Bradley-Terry model to compare multiple ML
               algorithms on multiple data sets." JMLR 24 (2023): 1-34.
        """
        # Load baseline data
        baseline_df = self._load_baseline_data(baseline)

        # Prepare data for BBT (aggregated by fingerprint)
        bbt_data = self._prepare_bbt_data(
            baseline_df=baseline_df,
            metric=metric,
            fingerprint_name=fingerprint_name,
        )

        if bbt_data.empty:
            raise ValueError(
                f"No overlapping datasets found for metric '{metric}'. "
                "Check that baseline and your results cover the same benchmarks."
            )

        # Fit BBT model
        model = PyBBT(local_rope_value=rope_value, tie_solver=TieSolver.SPREAD)
        model.fit(bbt_data, dataset_col="dataset", **pymc_kwargs)

        # Get posterior table
        posterior = model.posterior_table(control_model=control_fingerprint)

        return ComparisonResults(
            posterior_table=posterior,
            metric=metric,
            fingerprint_name=fingerprint_name,
            control_fingerprint=control_fingerprint,
            rope_value=rope_value,
        )

    def _load_baseline_data(
        self, baseline: Union[str, List[str], pd.DataFrame]
    ) -> pd.DataFrame:
        """Load baseline data from various sources.

        Parameters
        ----------
        baseline : str, List[str], or pd.DataFrame
            Baseline specification.

        Returns
        -------
        pd.DataFrame
            Combined baseline data.
        """
        if isinstance(baseline, pd.DataFrame):
            return baseline

        loader = BaselineLoader()

        if isinstance(baseline, str):
            return loader.load(baseline)

        # List of fingerprints
        return loader.load_multiple(baseline)

    def _prepare_bbt_data(
        self,
        baseline_df: pd.DataFrame,
        metric: str,
        fingerprint_name: str,
    ) -> pd.DataFrame:
        """Prepare data in format required by BBT.

        Transforms long-format results into wide format where each column
        is a fingerprint (aggregated across ML models) and each row is a dataset.

        Parameters
        ----------
        baseline_df : pd.DataFrame
            Baseline results DataFrame.
        metric : str
            Metric to filter on.
        fingerprint_name : str
            Name for the new fingerprint being tested.

        Returns
        -------
        pd.DataFrame
            Wide-format DataFrame ready for BBT.
        """
        # Filter by metric
        results_filtered = self.results_df[self.results_df["metric"] == metric].copy()
        baseline_filtered = baseline_df[baseline_df["metric"] == metric].copy()

        if results_filtered.empty:
            raise ValueError(
                f"Metric '{metric}' not found in benchmark results. "
                f"Available metrics: {self.results_df['metric'].unique().tolist()}"
            )

        if baseline_filtered.empty:
            raise ValueError(
                f"Metric '{metric}' not found in baseline results. "
                f"Available metrics: {baseline_df['metric'].unique().tolist()}"
            )

        # Create dataset identifier (benchmark + target)
        results_filtered["dataset"] = (
            results_filtered["benchmark"] + "_" + results_filtered["target"]
        )
        baseline_filtered["dataset"] = (
            baseline_filtered["benchmark"] + "_" + baseline_filtered["target"]
        )

        # Aggregate new results by dataset (mean across all ML models)
        # This gives one score per dataset for the new fingerprint
        results_agg = results_filtered.groupby("dataset")["score"].mean().reset_index()
        results_agg["fingerprint"] = fingerprint_name

        # Aggregate baseline results by dataset and fingerprint (mean across ML models)
        if "fingerprint" not in baseline_filtered.columns:
            raise ValueError(
                "Baseline DataFrame must have 'fingerprint' column. "
                "Use BaselineLoader to load baselines properly."
            )

        baseline_agg = (
            baseline_filtered.groupby(["dataset", "fingerprint"])["score"]
            .mean()
            .reset_index()
        )

        # Combine new and baseline results
        combined = pd.concat([results_agg, baseline_agg], ignore_index=True)

        # Pivot to wide format: rows = datasets, columns = fingerprints
        pivot = combined.pivot_table(
            index="dataset",
            columns="fingerprint",
            values="score",
            aggfunc="mean",
        )

        # Drop rows with any NaN (datasets that don't have all fingerprints)
        pivot = pivot.dropna()

        # Reset index to make dataset a column
        pivot = pivot.reset_index()

        return pivot
