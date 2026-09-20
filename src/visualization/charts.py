
from pathlib import Path
from typing import Optional

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend so charts can be saved
# from any environment, including one without a display (e.g. this pipeline).
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from src.utils.logger import get_logger

logger = get_logger(__name__)

# Consistent, professional visual style applied to every chart in the project.
sns.set_theme(style="whitegrid")
PALETTE = "viridis"


def _save_or_show(fig, save_path: Optional[str]):
    if save_path:
        path = Path(save_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, dpi=150, bbox_inches="tight")
        logger.info(f"Saved chart to {path}")
        plt.close(fig)
    return fig


def plot_histogram(df: pd.DataFrame, column: str, bins: int = 30,
                    title: Optional[str] = None, save_path: Optional[str] = None):

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df[column], bins=bins, kde=True, color="#2E86AB", ax=ax)
    ax.set_title(title or f"Distribution of {column}", fontsize=13, weight="bold")
    ax.set_xlabel(column)
    ax.set_ylabel("Frequency")
    fig.tight_layout()
    return _save_or_show(fig, save_path)


def plot_boxplot(df: pd.DataFrame, column: str, by: Optional[str] = None,
                  title: Optional[str] = None, save_path: Optional[str] = None):

    fig, ax = plt.subplots(figsize=(7, 5))
    if by:
        sns.boxplot(data=df, x=by, y=column, hue=by, palette=PALETTE, legend=False, ax=ax)
        ax.set_xlabel(by)
    else:
        sns.boxplot(y=df[column], color="#2E86AB", ax=ax)
    ax.set_title(title or f"Boxplot of {column}" + (f" by {by}" if by else ""), fontsize=13, weight="bold")
    ax.set_ylabel(column)
    fig.tight_layout()
    return _save_or_show(fig, save_path)


def plot_correlation_heatmap(df: pd.DataFrame, title: str = "Correlation Heatmap",
                              save_path: Optional[str] = None):

    corr = df.select_dtypes(include="number").corr()
    fig, ax = plt.subplots(figsize=(11, 9))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0,
                square=True, linewidths=0.5, cbar_kws={"shrink": 0.8}, ax=ax)
    ax.set_title(title, fontsize=14, weight="bold")
    fig.tight_layout()
    return _save_or_show(fig, save_path)


def plot_bar(x_labels, y_values, title: str, xlabel: str, ylabel: str,
             save_path: Optional[str] = None, horizontal: bool = False):

    fig, ax = plt.subplots(figsize=(9, 5.5))
    if horizontal:
        ax.barh([str(x) for x in x_labels], y_values, color="#2E86AB")
        ax.set_xlabel(ylabel)
        ax.set_ylabel(xlabel)
    else:
        ax.bar([str(x) for x in x_labels], y_values, color="#2E86AB")
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    ax.set_title(title, fontsize=13, weight="bold")
    fig.tight_layout()
    return _save_or_show(fig, save_path)


def plot_line(x_values, y_values, title: str, xlabel: str, ylabel: str,
              save_path: Optional[str] = None):

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot([str(x) for x in x_values], y_values, marker="o", color="#2E86AB", linewidth=2)
    ax.set_title(title, fontsize=13, weight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    fig.tight_layout()
    return _save_or_show(fig, save_path)
