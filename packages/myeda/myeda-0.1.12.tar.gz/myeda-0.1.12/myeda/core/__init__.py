from __future__ import annotations

# Version
__version__ = "0.1.12"

# Overview
from myeda.core.overview import dataset_overview

# Missing values
from myeda.core.missing import missing_overview, missing_summary

# Statistics
from myeda.core.statistics import numeric_summary, categorical_summary

# Visualization
from myeda.viz.visualization import (
    plot_numeric_distribution,
    plot_boxplot,
    plot_categorical_counts,
    plot_correlation_heatmap,
)

# Report orchestrator
from myeda.report import EDAReport

__all__ = [
    "__version__",
    "dataset_overview",
    "missing_overview",
    "missing_summary",
    "numeric_summary",
    "categorical_summary",
    "plot_numeric_distribution",
    "plot_boxplot",
    "plot_categorical_counts",
    "plot_correlation_heatmap",
    "EDAReport",
]
