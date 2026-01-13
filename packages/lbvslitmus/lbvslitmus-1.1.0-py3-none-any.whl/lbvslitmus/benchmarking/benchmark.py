from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

import numpy as np
import pandas as pd
from skfp.metrics import (
    bedroc_score,
    enrichment_factor,
    multioutput_auprc_score,
    multioutput_matthews_corr_coef,
)
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from tqdm import tqdm

from lbvslitmus.comparison.baseline_comparator import BaselineComparator
from lbvslitmus.datasets.registry import registry as dataset_registry
from lbvslitmus.datasets.welqrate import WelQrateDownloader
from lbvslitmus.models.registry import ModelRegistry
from lbvslitmus.models.similarity_search import SimilaritySearch


@dataclass
class BenchmarkResults:
    """
    Class to store the results of the benchmarking.
    """

    used_benchmarks: List[str]
    results: List[Dict[str, Any]]  # Any because results can have optional 'seed' field

    @property
    def summary(self) -> str:
        """Return a comprehensive summary of benchmark results.

        For WelQrate, shows both per-seed results and averaged results.
        """
        if not self.results:
            return "No results available."

        df = pd.DataFrame(self.results)
        summary_parts = [
            f"Datasets tested: {len(self.used_benchmarks)}",
            f"Total evaluations: {len(self.results)}",
            "",
        ]

        # Separate WelQrate results (with seeds) from other results
        has_seed = "seed" in df.columns
        if has_seed:
            welqrate_df = df[df["benchmark"] == "WELQRATE"]
            # Results with seeds have non-null seed values
            welqrate_with_seeds = welqrate_df[welqrate_df["seed"].notna()]
            # Averaged results have null seed values (they were added without seed field)
            welqrate_averaged = welqrate_df[welqrate_df["seed"].isna()]
            other_results = df[df["benchmark"] != "WELQRATE"]
        else:
            welqrate_with_seeds = pd.DataFrame()
            welqrate_averaged = pd.DataFrame()
            other_results = df

        # Group by metric for cleaner display (excluding seed-specific results)
        display_df = (
            pd.concat([welqrate_averaged, other_results], ignore_index=True)
            if has_seed
            else df
        )
        for metric in display_df["metric"].unique():
            metric_data = display_df.loc[display_df["metric"] == metric, "score"]
            summary_parts.extend(
                [
                    f"{metric} results:",
                    f"  Mean: {metric_data.mean():.4f}",
                    f"  Std:  {metric_data.std():.4f}",
                    f"  Min:  {metric_data.min():.4f}",
                    f"  Max:  {metric_data.max():.4f}",
                    "",
                ]
            )

        # Per-benchmark breakdown (using averaged results)
        summary_parts.append("Per-benchmark performance (averaged):")
        benchmark_summary = (
            display_df.groupby(
                [
                    "benchmark",
                    "model",
                    "metric",
                ]
            )["score"]
            .mean()
            .unstack(fill_value=0)
        )
        for benchmark, model in benchmark_summary.index:
            line = f"  {benchmark} | {model}:"
            for metric in benchmark_summary.columns:
                value = benchmark_summary.loc[(benchmark, model), metric]
                line += f" {metric}={value:.3f}"
            summary_parts.append(line)

        # Per-target breakdown (using averaged results)
        summary_parts.append("Per-target performance (averaged):")
        benchmark_summary = (
            display_df.groupby(
                [
                    "benchmark",
                    "target",
                    "model",
                    "metric",
                ]
            )["score"]
            .mean()
            .unstack(fill_value=0)
        )
        for benchmark, target, model in benchmark_summary.index:
            line = f"  {benchmark}| {target} | {model}:"
            for metric in benchmark_summary.columns:
                value = benchmark_summary.loc[(benchmark, target, model), metric]
                if value > 0:
                    line += f" {metric}={value:.3f}"
            summary_parts.append(line)

        # WelQrate per-seed breakdown
        if has_seed and not welqrate_with_seeds.empty:
            summary_parts.append("")
            summary_parts.append("WelQrate per-seed performance:")
            seed_summary = (
                welqrate_with_seeds.groupby(
                    [
                        "benchmark",
                        "target",
                        "model",
                        "metric",
                        "seed",
                    ]
                )["score"]
                .mean()
                .reset_index()
            )

            # Group by target and model for cleaner display
            for target, model in (
                seed_summary[["target", "model"]].drop_duplicates().values
            ):
                target_data = seed_summary[
                    (seed_summary["target"] == target)
                    & (seed_summary["model"] == model)
                ]
                line = f"  WELQRATE | {target} | {model}:"
                for metric in target_data["metric"].unique():
                    metric_scores = target_data[target_data["metric"] == metric][
                        "score"
                    ].values
                    mean_score = metric_scores.mean()
                    std_score = metric_scores.std()
                    line += f" {metric}={mean_score:.3f}±{std_score:.3f}"
                summary_parts.append(line)

        return "\n".join(summary_parts)

    def to_dataframe(self) -> pd.DataFrame:
        """Convert results to pandas DataFrame for easy analysis."""
        return pd.DataFrame(self.results)

    def save_to_csv(self, filepath: str) -> None:
        """Save results to CSV file."""
        df = self.to_dataframe()
        df.to_csv(filepath, index=False)
        print(f"Results saved to {filepath}")

    def plot(self, output_dir: str = "plots") -> None:
        """
        Generate visualization plots from benchmark results.

        Parameters
        ----------
        output_dir : str, default="plots"
            Directory to save plots

        Examples
        --------
        >>> results = benchmark.run()
        >>> results.plot(output_dir="my_plots")
        """
        from lbvslitmus.visualization import plot_all

        plot_all(self, output_dir=output_dir)

    def __str__(self) -> str:
        """Return the summary as a string representation."""
        return self.summary

    def compare_with_baseline(
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
        >>> results = benchmark.run()
        >>> # Compare your fingerprint with MACCS baseline
        >>> comparison = results.compare_with_baseline(
        ...     "MACCS",
        ...     metric="AUROC",
        ...     fingerprint_name="MyECFP4",
        ...     control_fingerprint="MyECFP4"
        ... )
        >>> print(comparison.posterior_table)
        >>> # Or convert to DataFrame
        >>> df = comparison.to_dataframe()

        >>> # Compare with multiple baselines
        >>> comparison = results.compare_with_baseline(
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
        if not self.results:
            raise ValueError("No results available for comparison.")

        comparator = BaselineComparator(self.to_dataframe())
        return comparator.compare(
            baseline=baseline,
            metric=metric,
            rope_value=rope_value,
            fingerprint_name=fingerprint_name,
            control_fingerprint=control_fingerprint,
            **pymc_kwargs,
        )


class Benchmark:
    """
    Class for benchmarking the performance of the molecular embedding models.
    """

    def __init__(self, pipeline: Pipeline, benchmarks: Optional[List[str]] = None):
        self.pipeline = pipeline
        self.results = []
        self.model_registry = ModelRegistry()

        # Register models
        self.model_registry.register(
            RandomForestClassifier,
            "RandomForestClassifier",
            {"n_jobs": -1, "verbose": 0, "random_state": 0},
        )
        self.model_registry.register(SimilaritySearch, "SimilaritySearch")
        self.model_registry.register(
            LogisticRegressionCV,
            "LogisticRegressionCV",
            {
                "cv": 5,  # Number of folds for cross-validation during hyperparameter tuning
                "scoring": "roc_auc",
                "max_iter": 1000,
                "random_state": 0,
                "n_jobs": -1,
            },
        )
        if benchmarks is None:
            self.benchmarks = dataset_registry.list_datasets()
        else:
            self.benchmarks = benchmarks

    def _evaluate(
        self,
        y_test: pd.Series,
        y_score: np.ndarray,
        y_pred: Optional[np.ndarray] = None,
    ) -> Dict[str, float]:
        results = {
            "AUROC": roc_auc_score(y_test, y_score),
            "BEDROC": bedroc_score(y_test, y_score),
            "Enrichment factor 1%": enrichment_factor(y_test, y_score, fraction=0.01),
            "Enrichment factor 5%": enrichment_factor(y_test, y_score, fraction=0.05),
            "AUPRC": multioutput_auprc_score(y_test, y_score),
        }

        if y_pred is not None:
            results["accuracy"] = accuracy_score(y_test, y_pred)
            results["F1 score"] = f1_score(y_test, y_pred)
            results["recall"] = recall_score(y_test, y_pred)
            results["precision"] = precision_score(y_test, y_pred, zero_division=0)
            results["MCC"] = multioutput_matthews_corr_coef(y_test, y_pred)

        return results

    def _process_target(
        self,
        benchmark: str,
        target: str,
        pipeline: Pipeline,
        seed: Optional[int] = None,
    ) -> List[Dict[str, float]]:
        """Process a single target and return evaluation results.

        Parameters
        ----------
        benchmark : str
            Name of the benchmark dataset
        target : str
            Name of the target
        pipeline : Pipeline
            Pipeline for transforming SMILES to features
        seed : Optional[int], default=None
            Seed number for datasets with multiple seeds (e.g., WelQrate).
            If None, uses default split.

        Returns
        -------
        List[Dict[str, float]]
            List of result dictionaries containing benchmark, model, target,
            metric, score, and optionally seed information.
        """
        downloader = dataset_registry.get_downloader(benchmark)
        df = downloader.load(target=target)
        splits = downloader.get_splits(target, seed=seed)
        results = []

        train_df = df.iloc[splits["train"]]
        test_df = df.iloc[splits["test"]]

        X_train = pipeline.fit_transform(train_df["SMILES"])
        y_train = train_df[target]
        X_test = pipeline.transform(test_df["SMILES"])
        y_test = test_df[target]

        for name in self.model_registry.models:
            instance = self.model_registry.create_model_instance(name)
            instance.fit(X_train, y_train)

            y_test_pred = instance.predict(X_test)
            try:
                y_test_pred_proba = instance.predict_proba(X_test)
                y_test_pred_proba = y_test_pred_proba[:, 1]
            except NotImplementedError:  # SimilaritySearch
                y_test_pred_proba = instance.score_samples(X_test)
                y_test_pred = None  # we do not want to calculate this when `predict_proba` is not implemented

            results_metric = self._evaluate(y_test, y_test_pred_proba, y_test_pred)

            for metric_name, metric_score in results_metric.items():
                result_dict = {
                    "benchmark": benchmark,
                    "model": name,
                    "target": target,
                    "metric": metric_name,
                    "score": metric_score,
                }
                # Add seed information if available
                if seed is not None:
                    result_dict["seed"] = seed
                results.append(result_dict)

        return results

    def run(self) -> BenchmarkResults:
        """
        Run benchmark.

        For WelQrate dataset, this will run cross-validation across all 5 seeds
        and include both per-seed results and averaged results.

        Returns
        -------
        BenchmarkResults
            BenchmarkResults object containing the results of the benchmark.
        """
        if not self.pipeline:
            raise ValueError(
                "You must first set the pipeline with your embedding model"
            )
        if not self.benchmarks or self.benchmarks == []:
            raise ValueError("List of benchmarks cannot be empty")

        for benchmark in tqdm(self.benchmarks, desc="Downloading"):
            downloader = dataset_registry.get_downloader(benchmark)
            downloader.download()

        # Build tasks list
        tasks = []
        for benchmark in self.benchmarks:
            downloader = dataset_registry.get_downloader(benchmark)
            # Check if this is WelQrate which has multiple seeds
            if isinstance(downloader, WelQrateDownloader):
                seeds = downloader.get_available_seeds()
                for target in downloader.metadata.available_targets:
                    for seed in seeds:
                        tasks.append((benchmark, target, self.pipeline, seed))
            else:
                # Regular datasets without seeds
                for target in downloader.metadata.available_targets:
                    tasks.append((benchmark, target, self.pipeline, None))

        # Process all tasks
        results = []
        for task in tqdm(tasks, desc="Benchmarking"):
            benchmark, target, pipeline, seed = task
            task_results = self._process_target(benchmark, target, pipeline, seed=seed)
            results.extend(task_results)

        # For WelQrate, compute averaged results across seeds
        welqrate_results = [
            r for r in results if r.get("benchmark") == "WELQRATE" and "seed" in r
        ]
        if welqrate_results:
            # Group by benchmark, target, model, metric
            welqrate_df = pd.DataFrame(welqrate_results)
            averaged = (
                welqrate_df.groupby(["benchmark", "target", "model", "metric"])["score"]
                .mean()
                .reset_index()
            )

            # Add averaged results (without seed column)
            for _, row in averaged.iterrows():
                results.append(
                    {
                        "benchmark": row["benchmark"],
                        "model": row["model"],
                        "target": row["target"],
                        "metric": row["metric"],
                        "score": row["score"],
                        # No seed field for averaged results
                    }
                )

        self.results = results

        return BenchmarkResults(
            results=self.results,
            used_benchmarks=self.benchmarks,
        )
