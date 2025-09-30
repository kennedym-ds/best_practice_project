"""Data Visualization Module.

This module provides utilities for creating visualizations from data.
"""

import logging
from pathlib import Path
from typing import List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

logger = logging.getLogger(__name__)


class Visualizer:
    """
    A class for creating data visualizations.

    This class demonstrates best practices for data visualization including:
    - Distribution plots
    - Correlation visualizations
    - Time series plots
    - Categorical analysis
    """

    def __init__(self, df: pd.DataFrame, style: str = "darkgrid", palette: str = "deep") -> None:
        """
        Initialize the Visualizer with a DataFrame.

        Args:
            df: The DataFrame to visualize
            style: Seaborn style ('darkgrid', 'whitegrid', 'dark', 'white', 'ticks')
            palette: Color palette to use
        """
        self.df = df.copy()
        sns.set_style(style)
        sns.set_palette(palette)
        logger.info(f"Visualizer initialized with DataFrame shape: {self.df.shape}")

    def create_histogram(
        self,
        column: str,
        bins: int = 30,
        kde: bool = True,
        figsize: Tuple[int, int] = (10, 6),
        title: Optional[str] = None,
        save_path: Optional[Path] = None,
    ) -> plt.Figure:
        """
        Create a histogram for a numeric column.

        Args:
            column: Column name to plot
            bins: Number of bins for the histogram
            kde: Whether to overlay a kernel density estimate
            figsize: Figure size (width, height)
            title: Plot title
            save_path: Path to save the figure

        Returns:
            Matplotlib Figure object

        Example:
            >>> viz = Visualizer(df)
            >>> fig = viz.create_histogram('age', bins=20)
        """
        logger.info(f"Creating histogram for column '{column}'")

        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found")

        fig, ax = plt.subplots(figsize=figsize)

        sns.histplot(data=self.df, x=column, bins=bins, kde=kde, ax=ax)

        ax.set_title(title or f"Distribution of {column}")
        ax.set_xlabel(column)
        ax.set_ylabel("Frequency")

        plt.tight_layout()

        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches="tight")
            logger.info(f"Histogram saved to {save_path}")

        return fig

    def create_boxplot(
        self,
        column: str,
        by: Optional[str] = None,
        figsize: Tuple[int, int] = (10, 6),
        title: Optional[str] = None,
        save_path: Optional[Path] = None,
    ) -> plt.Figure:
        """
        Create a boxplot for a numeric column.

        Args:
            column: Column name to plot
            by: Optional column to group by
            figsize: Figure size (width, height)
            title: Plot title
            save_path: Path to save the figure

        Returns:
            Matplotlib Figure object

        Example:
            >>> viz = Visualizer(df)
            >>> fig = viz.create_boxplot('salary', by='department')
        """
        logger.info(f"Creating boxplot for column '{column}'")

        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found")

        fig, ax = plt.subplots(figsize=figsize)

        if by:
            sns.boxplot(data=self.df, x=by, y=column, ax=ax)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
        else:
            sns.boxplot(data=self.df, y=column, ax=ax)

        ax.set_title(title or f"Boxplot of {column}")

        plt.tight_layout()

        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches="tight")
            logger.info(f"Boxplot saved to {save_path}")

        return fig

    def create_scatter(
        self,
        x_column: str,
        y_column: str,
        hue: Optional[str] = None,
        size: Optional[str] = None,
        figsize: Tuple[int, int] = (10, 6),
        title: Optional[str] = None,
        save_path: Optional[Path] = None,
    ) -> plt.Figure:
        """
        Create a scatter plot.

        Args:
            x_column: Column for x-axis
            y_column: Column for y-axis
            hue: Column for color coding
            size: Column for size coding
            figsize: Figure size (width, height)
            title: Plot title
            save_path: Path to save the figure

        Returns:
            Matplotlib Figure object

        Example:
            >>> viz = Visualizer(df)
            >>> fig = viz.create_scatter('age', 'income', hue='gender')
        """
        logger.info(f"Creating scatter plot: {x_column} vs {y_column}")

        fig, ax = plt.subplots(figsize=figsize)

        sns.scatterplot(data=self.df, x=x_column, y=y_column, hue=hue, size=size, ax=ax, alpha=0.6)

        ax.set_title(title or f"{y_column} vs {x_column}")
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)

        plt.tight_layout()

        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches="tight")
            logger.info(f"Scatter plot saved to {save_path}")

        return fig

    def create_correlation_heatmap(
        self,
        columns: Optional[List[str]] = None,
        method: str = "pearson",
        figsize: Tuple[int, int] = (12, 10),
        annot: bool = True,
        cmap: str = "coolwarm",
        title: Optional[str] = None,
        save_path: Optional[Path] = None,
    ) -> plt.Figure:
        """
        Create a correlation heatmap.

        Args:
            columns: List of columns to include. If None, uses all numeric columns.
            method: Correlation method ('pearson', 'spearman', 'kendall')
            figsize: Figure size (width, height)
            annot: Whether to annotate cells with values
            cmap: Color map to use
            title: Plot title
            save_path: Path to save the figure

        Returns:
            Matplotlib Figure object

        Example:
            >>> viz = Visualizer(df)
            >>> fig = viz.create_correlation_heatmap(method='spearman')
        """
        logger.info(f"Creating correlation heatmap using {method} method")

        if columns is None:
            numeric_df = self.df.select_dtypes(include=[np.number])
        else:
            numeric_df = self.df[columns]

        corr_matrix = numeric_df.corr(method=method)

        fig, ax = plt.subplots(figsize=figsize)

        sns.heatmap(
            corr_matrix,
            annot=annot,
            cmap=cmap,
            center=0,
            square=True,
            linewidths=1,
            cbar_kws={"shrink": 0.8},
            ax=ax,
            fmt=".2f",
        )

        ax.set_title(title or f"{method.capitalize()} Correlation Heatmap")

        plt.tight_layout()

        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches="tight")
            logger.info(f"Heatmap saved to {save_path}")

        return fig

    def create_line_plot(
        self,
        x_column: str,
        y_columns: List[str],
        figsize: Tuple[int, int] = (12, 6),
        title: Optional[str] = None,
        save_path: Optional[Path] = None,
    ) -> plt.Figure:
        """
        Create a line plot for time series or sequential data.

        Args:
            x_column: Column for x-axis (typically time)
            y_columns: List of columns to plot on y-axis
            figsize: Figure size (width, height)
            title: Plot title
            save_path: Path to save the figure

        Returns:
            Matplotlib Figure object

        Example:
            >>> viz = Visualizer(df)
            >>> fig = viz.create_line_plot('date', ['sales', 'revenue'])
        """
        logger.info(f"Creating line plot with {len(y_columns)} series")

        fig, ax = plt.subplots(figsize=figsize)

        for y_col in y_columns:
            ax.plot(self.df[x_column], self.df[y_col], label=y_col, marker="o", alpha=0.7)

        ax.set_xlabel(x_column)
        ax.set_ylabel("Value")
        ax.set_title(title or "Time Series Plot")
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches="tight")
            logger.info(f"Line plot saved to {save_path}")

        return fig

    def create_bar_plot(
        self,
        x_column: str,
        y_column: str,
        figsize: Tuple[int, int] = (10, 6),
        horizontal: bool = False,
        title: Optional[str] = None,
        save_path: Optional[Path] = None,
    ) -> plt.Figure:
        """
        Create a bar plot.

        Args:
            x_column: Column for x-axis (categories)
            y_column: Column for y-axis (values)
            figsize: Figure size (width, height)
            horizontal: Whether to create horizontal bars
            title: Plot title
            save_path: Path to save the figure

        Returns:
            Matplotlib Figure object

        Example:
            >>> viz = Visualizer(df)
            >>> fig = viz.create_bar_plot('category', 'count')
        """
        logger.info(f"Creating bar plot: {x_column} vs {y_column}")

        fig, ax = plt.subplots(figsize=figsize)

        if horizontal:
            sns.barplot(data=self.df, y=x_column, x=y_column, ax=ax)
        else:
            sns.barplot(data=self.df, x=x_column, y=y_column, ax=ax)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")

        ax.set_title(title or f"{y_column} by {x_column}")

        plt.tight_layout()

        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches="tight")
            logger.info(f"Bar plot saved to {save_path}")

        return fig

    def create_pairplot(
        self,
        columns: Optional[List[str]] = None,
        hue: Optional[str] = None,
        diag_kind: str = "hist",
        save_path: Optional[Path] = None,
    ) -> sns.PairGrid:
        """
        Create a pairplot to show relationships between variables.

        Args:
            columns: List of columns to include
            hue: Column for color coding
            diag_kind: Kind of plot for diagonal ('hist' or 'kde')
            save_path: Path to save the figure

        Returns:
            Seaborn PairGrid object

        Example:
            >>> viz = Visualizer(df)
            >>> grid = viz.create_pairplot(['age', 'income', 'score'])
        """
        logger.info("Creating pairplot")

        if columns:
            plot_df = self.df[columns + ([hue] if hue and hue not in columns else [])]
        else:
            plot_df = self.df.select_dtypes(include=[np.number])

        grid = sns.pairplot(plot_df, hue=hue, diag_kind=diag_kind)

        if save_path:
            grid.savefig(save_path, dpi=300, bbox_inches="tight")
            logger.info(f"Pairplot saved to {save_path}")

        return grid

    def create_countplot(
        self,
        column: str,
        hue: Optional[str] = None,
        figsize: Tuple[int, int] = (10, 6),
        title: Optional[str] = None,
        save_path: Optional[Path] = None,
    ) -> plt.Figure:
        """
        Create a count plot for categorical data.

        Args:
            column: Column to count
            hue: Optional column for grouped counting
            figsize: Figure size (width, height)
            title: Plot title
            save_path: Path to save the figure

        Returns:
            Matplotlib Figure object

        Example:
            >>> viz = Visualizer(df)
            >>> fig = viz.create_countplot('category', hue='status')
        """
        logger.info(f"Creating count plot for column '{column}'")

        fig, ax = plt.subplots(figsize=figsize)

        sns.countplot(data=self.df, x=column, hue=hue, ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
        ax.set_title(title or f"Count Plot of {column}")

        plt.tight_layout()

        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches="tight")
            logger.info(f"Count plot saved to {save_path}")

        return fig
