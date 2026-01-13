"""Visualization functions for fingerprint comparison results.

This module provides visualization functions for ComparisonResults, including
bar charts showing win probabilities with confidence intervals.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from lbvslitmus.comparison.baseline_comparator import ComparisonResults
from lbvslitmus.visualization.utils import plotting_context, save_plot


def _prepare_posterior_table_for_plotting(
    posterior, control_fingerprint: str | None, error_message: str = "No data available"
):
    """Prepare posterior table for plotting by extracting win probabilities vs control.

    When control_fingerprint is set, extracts probabilities for each fingerprint beating the control.
    If a row shows "A > Control" with probability p, then A's win probability vs control is p.
    If a row shows "Control > A" with probability p, then A's win probability vs control is 1-p.

    Parameters
    ----------
    posterior : pd.DataFrame
        Posterior table from comparison results with columns: pair, left_model, right_model, mean, hdi_low, hdi_high
    control_fingerprint : str | None
        Name of the control fingerprint
    error_message : str, default="No data available"
        Error message to print if table is empty

    Returns
    -------
    pd.DataFrame or None
        DataFrame with columns: fingerprint, mean, hdi_low, hdi_high, or None if preparation failed
    """
    if posterior.empty:
        print(f"{error_message}")
        return None

    # Check if we have the required columns
    required_cols = ["mean"]
    if not all(col in posterior.columns for col in required_cols):
        print(f"Missing required columns. Available: {posterior.columns.tolist()}")
        return None

    # If we have control_fingerprint, extract win probabilities vs control
    if control_fingerprint:
        if (
            "left_model" not in posterior.columns
            or "right_model" not in posterior.columns
        ):
            print(
                "Missing 'left_model' or 'right_model' columns for control comparison"
            )
            return None

        results = []
        for _, row in posterior.iterrows():
            left = str(row["left_model"])
            right = str(row["right_model"])
            mean_prob = row["mean"]

            # Determine which fingerprint is being compared and its win probability vs control
            if left == control_fingerprint:
                # Control > Other: Other's win prob vs control is 1 - mean
                fingerprint = right
                win_prob = 1 - mean_prob
                # For HDI, swap and invert: if original is [low, high], inverted is [1-high, 1-low]
                if "hdi_low" in row and "hdi_high" in row:
                    hdi_low = 1 - row["hdi_high"]
                    hdi_high = 1 - row["hdi_low"]
                else:
                    hdi_low = None
                    hdi_high = None
            elif right == control_fingerprint:
                # Other > Control: Other's win prob vs control is mean
                fingerprint = left
                win_prob = mean_prob
                hdi_low = row.get("hdi_low")
                hdi_high = row.get("hdi_high")
            else:
                # This row doesn't involve control, skip it
                continue

            result_row = {"fingerprint": fingerprint, "mean": win_prob}
            if hdi_low is not None and hdi_high is not None:
                result_row["hdi_low"] = hdi_low
                result_row["hdi_high"] = hdi_high
            results.append(result_row)

        if not results:
            print(
                f"No comparisons found involving control fingerprint '{control_fingerprint}'"
            )
            return None

        return pd.DataFrame(results)

    # No control: use index or first column as fingerprint names
    posterior = posterior.copy()
    if "fingerprint" not in posterior.columns:
        if posterior.index.name == "fingerprint":
            posterior = posterior.reset_index()
        elif len(posterior.index) > 0:
            # Try to use index values
            posterior.insert(0, "fingerprint", posterior.index.tolist())

    if "fingerprint" not in posterior.columns:
        print(
            f"Could not determine fingerprint names. Columns: {posterior.columns.tolist()}"
        )
        return None

    return posterior


def plot_win_counts(
    comparison_results: ComparisonResults,
    output_dir: str = "plots",
    style: str = "whitegrid",
    figure_dpi: int = 100,
    savefig_dpi: int = 300,
    font_size: int = 10,
) -> None:
    """Plot horizontal bar chart showing win probability for each fingerprint.

    Shows the posterior mean probability of each fingerprint beating the control,
    with error bars showing the 89% HDI (Highest Density Interval).

    Parameters
    ----------
    comparison_results : ComparisonResults
        Comparison results from BaselineComparator.compare()
    output_dir : str, default="plots"
        Directory to save the plot
    style : str, default="whitegrid"
        Seaborn style to use
    figure_dpi : int, default=100
        DPI for figure display
    savefig_dpi : int, default=300
        DPI for saved figures
    font_size : int, default=10
        Base font size for plots

    Examples
    --------
    >>> from lbvslitmus.comparison import BaselineComparator
    >>> comparator = BaselineComparator(results.to_dataframe())
    >>> comparison = comparator.compare(["ECFP4", "MACCS"], metric="AUROC")
    >>> plot_win_counts(comparison, output_dir="my_plots")
    """
    with plotting_context(style, figure_dpi, savefig_dpi, font_size):
        posterior = _prepare_posterior_table_for_plotting(
            comparison_results.posterior_table.copy(),
            comparison_results.control_fingerprint,
            error_message="No data available for win counts plot",
        )

        if posterior is None:
            return

        # Check if required columns exist
        if "mean" not in posterior.columns:
            print(f"Missing 'mean' column. Columns: {posterior.columns.tolist()}")
            return

        # Sort by mean probability (descending - best first)
        posterior_sorted = posterior.sort_values("mean", ascending=False)

        # Convert fingerprint names to strings to ensure proper display
        fingerprints = [str(fp) for fp in posterior_sorted["fingerprint"].tolist()]
        means = posterior_sorted["mean"].values

        # Calculate error bars from HDI if available
        if (
            "hdi_low" in posterior_sorted.columns
            and "hdi_high" in posterior_sorted.columns
        ):
            errors_low = means - posterior_sorted["hdi_low"].values
            errors_high = posterior_sorted["hdi_high"].values - means
            errors = [errors_low, errors_high]
        else:
            errors = None

        n_fingerprints = len(fingerprints)
        fig_height = max(6, min(12, n_fingerprints * 0.5))
        fig, ax = plt.subplots(figsize=(12, fig_height), facecolor="white")

        # Use gradient colors based on performance
        # Better color scheme: green for winners, orange for neutral, red for losers
        colors = []
        for m in means:
            if m > 0.5 + comparison_results.rope_value:
                # Strong winner - vibrant green
                colors.append("#27ae60")
            elif m > 0.5:
                # Weak winner - light green
                colors.append("#58d68d")
            elif m > 0.5 - comparison_results.rope_value:
                # In ROPE - orange
                colors.append("#f39c12")
            else:
                # Loser - red
                colors.append("#e74c3c")

        y_pos = np.arange(len(fingerprints))

        bars = ax.barh(
            y_pos,
            means,
            xerr=errors,
            capsize=4,
            color=colors,
            alpha=0.85,
            edgecolor="white",
            linewidth=2,
            height=0.7,
        )

        # Add vertical line at 0.5 (neutral point)
        neutral_line = ax.axvline(
            x=0.5,
            color="#34495e",
            linestyle="--",
            linewidth=2.5,
            alpha=0.6,
            zorder=0,
        )

        err_lows = errors[0] if errors else [0] * len(means)
        err_highs = errors[1] if errors else [0] * len(means)
        for i, (bar, mean_val, err_low, err_high) in enumerate(
            zip(bars, means, err_lows, err_highs)
        ):
            # Position label at the end of the bar
            label_x = mean_val + err_high + 0.02 if errors else mean_val + 0.02
            # If bar is too close to right edge, put label inside
            if label_x > 0.95:
                label_x = mean_val - err_low - 0.02 if errors else mean_val - 0.02
                ha = "right"
                color = "white" if mean_val > 0.3 else "#2c3e50"
            else:
                ha = "left"
                color = "#2c3e50"

            ax.text(
                label_x,
                i,
                f"{mean_val:.3f}",
                va="center",
                ha=ha,
                fontsize=11,
                fontweight="600",
                color=color,
            )

        ax.set_yticks(y_pos)
        ax.set_yticklabels(fingerprints, fontsize=12, fontweight="500")

        if comparison_results.control_fingerprint:
            xlabel_text = (
                f"Probability of Winning vs {comparison_results.control_fingerprint}"
            )
        else:
            xlabel_text = "Win Probability"
        ax.set_xlabel(
            xlabel_text,
            fontsize=14,
            fontweight="bold",
            color="#2c3e50",
            labelpad=10,
        )
        ax.set_ylabel(
            "Fingerprint",
            fontsize=14,
            fontweight="bold",
            color="#2c3e50",
            labelpad=10,
        )

        control_text = (
            f"Control: {comparison_results.control_fingerprint}"
            if comparison_results.control_fingerprint
            else "Pairwise Comparison"
        )
        ax.set_title(
            f"Fingerprint Performance Comparison\n{comparison_results.metric} • {control_text}",
            fontsize=15,
            fontweight="bold",
            pad=20,
            color="#2c3e50",
        )

        # Set limits and grid
        ax.set_xlim(0, 1.05)
        ax.grid(axis="x", alpha=0.2, linestyle="-", linewidth=0.8, color="#95a5a6")
        ax.set_axisbelow(True)

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#bdc3c7")
        ax.spines["bottom"].set_color("#bdc3c7")

        # Create informative legend
        from matplotlib.patches import Rectangle

        # Create legend elements
        legend_elements = []

        # Add color explanations
        if comparison_results.control_fingerprint:
            legend_elements.append(
                Rectangle(
                    (0, 0),
                    1,
                    1,
                    facecolor="#27ae60",
                    edgecolor="white",
                    linewidth=2,
                    label="Better than control (>0.5)",
                )
            )
            legend_elements.append(
                Rectangle(
                    (0, 0),
                    1,
                    1,
                    facecolor="#f39c12",
                    edgecolor="white",
                    linewidth=2,
                    label="Equivalent to control (ROPE)",
                )
            )
            legend_elements.append(
                Rectangle(
                    (0, 0),
                    1,
                    1,
                    facecolor="#e74c3c",
                    edgecolor="white",
                    linewidth=2,
                    label="Worse than control (<0.5)",
                )
            )
        else:
            legend_elements.append(
                Rectangle(
                    (0, 0),
                    1,
                    1,
                    facecolor="#27ae60",
                    edgecolor="white",
                    linewidth=2,
                    label="Strong performer",
                )
            )
            legend_elements.append(
                Rectangle(
                    (0, 0),
                    1,
                    1,
                    facecolor="#f39c12",
                    edgecolor="white",
                    linewidth=2,
                    label="Neutral performance",
                )
            )
            legend_elements.append(
                Rectangle(
                    (0, 0),
                    1,
                    1,
                    facecolor="#e74c3c",
                    edgecolor="white",
                    linewidth=2,
                    label="Weak performer",
                )
            )

        # Add neutral line explanation
        legend_elements.append(
            plt.Line2D(
                [0],
                [0],
                color="#34495e",
                linestyle="--",
                linewidth=2.5,
                label="Equal performance (0.5)",
            )
        )

        ax.legend(
            handles=legend_elements,
            loc="lower right",
            fontsize=10,
            framealpha=0.95,
            edgecolor="#ecf0f1",
            facecolor="white",
            title="Interpretation"
            if comparison_results.control_fingerprint
            else "Performance",
            title_fontsize=11,
        )

        plt.tight_layout()
        save_plot(output_dir, "comparison_win_probabilities.png")


def plot_all_comparisons(
    comparison_results: ComparisonResults,
    output_dir: str = "plots",
    style: str = "whitegrid",
    figure_dpi: int = 100,
    savefig_dpi: int = 300,
    font_size: int = 10,
) -> None:
    """Generate all available comparison visualizations.

    Parameters
    ----------
    comparison_results : ComparisonResults
        Comparison results from BaselineComparator.compare()
    output_dir : str, default="plots"
        Directory to save the plots
    style : str, default="whitegrid"
        Seaborn style to use
    figure_dpi : int, default=100
        DPI for figure display
    savefig_dpi : int, default=300
        DPI for saved figures
    font_size : int, default=10
        Base font size for plots

    Examples
    --------
    >>> from lbvslitmus.comparison import BaselineComparator
    >>> comparator = BaselineComparator(results.to_dataframe())
    >>> comparison = comparator.compare(["ECFP4", "MACCS"], metric="AUROC")
    >>> plot_all_comparisons(comparison, output_dir="my_plots")
    """
    plot_win_counts(
        comparison_results,
        output_dir=output_dir,
        style=style,
        figure_dpi=figure_dpi,
        savefig_dpi=savefig_dpi,
        font_size=font_size,
    )
