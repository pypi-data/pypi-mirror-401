"""Baseline results management for statistical comparisons.

This module provides functionality for loading and managing baseline benchmark
results used in Bayesian statistical comparisons. Baselines are pre-computed
benchmark results for standard fingerprints (ECFP4, MACCS, etc.) that can be
used as reference points when evaluating new models.

All baselines are hosted on HuggingFace Hub and are automatically downloaded
and cached on first use.
"""

import pathlib
import shutil
from typing import List, Optional, Union

import pandas as pd
from huggingface_hub import hf_hub_download
from sklearn.datasets import get_data_home

# Available baseline fingerprints
AVAILABLE_BASELINES: List[str] = [
    "AtomPair",
    "ECFP4",
    "ECFP4_Count",
    "ECFP6",
    "ECFP6_Count",
    "ECFP8",
    "ECFP8_Count",
    "MACCS",
    "PubChem",
    "TopologicalTorsion",
]

# HuggingFace repository configuration
HF_REPO: str = "scikit-fingerprints/litmus"
HF_BASELINES_DIR: str = "baselines"


class BaselineLoader:
    """Loader for baseline benchmark results from HuggingFace.

    This class handles downloading, caching, and loading baseline results
    for standard molecular fingerprints. Baselines are used as reference
    points for Bayesian statistical comparisons with new models.

    Parameters
    ----------
    cache_dir : Optional[Union[str, pathlib.Path]], default=None
        Directory to store downloaded baselines. If None, uses
        sklearn's data home directory.

    Examples
    --------
    >>> loader = BaselineLoader()
    >>> baseline_df = loader.load("ECFP4")
    >>> print(baseline_df.head())

    >>> # Load multiple baselines
    >>> baselines = loader.load_multiple(["ECFP4", "MACCS"])
    """

    def __init__(self, cache_dir: Optional[Union[str, pathlib.Path]] = None):
        """Initialize the baseline loader."""
        if cache_dir is None:
            cache_dir = pathlib.Path(get_data_home()) / "litmus" / "baselines"
        self.cache_dir = pathlib.Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_baseline_path(self, fingerprint: str) -> pathlib.Path:
        """Get the local cache path for a baseline.

        Parameters
        ----------
        fingerprint : str
            Name of the fingerprint baseline.

        Returns
        -------
        pathlib.Path
            Path to the cached baseline file.
        """
        return self.cache_dir / f"{fingerprint}.csv"

    def is_downloaded(self, fingerprint: str) -> bool:
        """Check if a baseline is already downloaded.

        Parameters
        ----------
        fingerprint : str
            Name of the fingerprint baseline.

        Returns
        -------
        bool
            True if the baseline exists in cache.
        """
        return self._get_baseline_path(fingerprint).exists()

    def download(self, fingerprint: str, force: bool = False) -> pathlib.Path:
        """Download a baseline from HuggingFace Hub.

        Parameters
        ----------
        fingerprint : str
            Name of the fingerprint baseline to download.
        force : bool, default=False
            If True, re-download even if already cached.

        Returns
        -------
        pathlib.Path
            Path to the downloaded baseline file.

        Raises
        ------
        ValueError
            If the fingerprint is not in the list of available baselines.
        """
        if fingerprint not in AVAILABLE_BASELINES:
            raise ValueError(
                f"Unknown baseline '{fingerprint}'. "
                f"Available baselines: {AVAILABLE_BASELINES}"
            )

        local_path = self._get_baseline_path(fingerprint)

        if not force and local_path.exists():
            return local_path

        # Download from HuggingFace
        hf_filename = f"{HF_BASELINES_DIR}/{fingerprint}.csv"
        downloaded_path = hf_hub_download(
            repo_id=HF_REPO,
            filename=hf_filename,
            repo_type="dataset",
            force_download=force,
            local_dir=self.cache_dir / "hf_cache",
        )

        # Copy to standard cache location
        shutil.copy2(downloaded_path, local_path)

        return local_path

    def load(self, fingerprint: str, force_download: bool = False) -> pd.DataFrame:
        """Load a baseline as a DataFrame.

        Downloads the baseline if not already cached.

        Parameters
        ----------
        fingerprint : str
            Name of the fingerprint baseline to load.
        force_download : bool, default=False
            If True, re-download even if already cached.

        Returns
        -------
        pd.DataFrame
            Baseline results with columns:
            benchmark, model, target, metric, score, seed

        Raises
        ------
        ValueError
            If the fingerprint is not in the list of available baselines.

        Examples
        --------
        >>> loader = BaselineLoader()
        >>> df = loader.load("ECFP4")
        >>> print(df["metric"].unique())
        """
        self.download(fingerprint, force=force_download)
        local_path = self._get_baseline_path(fingerprint)
        df = pd.read_csv(local_path)

        # Add fingerprint column for identification when merging multiple baselines
        df["fingerprint"] = fingerprint

        return df

    def load_multiple(
        self, fingerprints: List[str], force_download: bool = False
    ) -> pd.DataFrame:
        """Load multiple baselines and concatenate them.

        Parameters
        ----------
        fingerprints : List[str]
            List of fingerprint baseline names to load.
        force_download : bool, default=False
            If True, re-download even if already cached.

        Returns
        -------
        pd.DataFrame
            Combined baseline results from all fingerprints.

        Examples
        --------
        >>> loader = BaselineLoader()
        >>> df = loader.load_multiple(["ECFP4", "MACCS", "AtomPair"])
        """
        dfs = [self.load(fp, force_download=force_download) for fp in fingerprints]
        return pd.concat(dfs, ignore_index=True)

    @staticmethod
    def list_available() -> List[str]:
        """List all available baseline fingerprints.

        Returns
        -------
        List[str]
            List of available baseline names.

        Examples
        --------
        >>> BaselineLoader.list_available()
        ['AtomPair', 'ECFP4', 'ECFP4_Count', 'ECFP6', 'ECFP6_Count', ...]
        """
        return AVAILABLE_BASELINES.copy()
