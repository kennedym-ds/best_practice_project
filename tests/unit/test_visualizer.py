"""Unit tests for the Visualizer module."""

import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from data_analysis.visualizer import Visualizer


@pytest.fixture
def sample_data():
    """Create sample DataFrame for testing."""
    np.random.seed(42)
    return pd.DataFrame(
        {
            "age": np.random.randint(20, 65, 100),
            "salary": np.random.randint(30000, 150000, 100),
            "years_experience": np.random.randint(0, 40, 100),
            "department": np.random.choice(["HR", "IT", "Finance", "Sales"], 100),
            "performance_score": np.random.uniform(1.0, 5.0, 100),
        }
    )


@pytest.fixture
def temp_output_dir():
    """Create a temporary directory for output files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


class TestVisualizerInitialization:
    """Tests for Visualizer initialization."""

    def test_init_with_dataframe(self, sample_data):
        """Test initialization with a DataFrame."""
        viz = Visualizer(sample_data)
        assert viz.df is not None
        assert viz.df.shape == sample_data.shape

    def test_init_creates_copy(self, sample_data):
        """Test that initialization creates a copy."""
        viz = Visualizer(sample_data)
        viz.df.loc[0, "age"] = 999

        # Original should be unchanged
        assert sample_data.loc[0, "age"] != 999

    def test_init_with_custom_style(self, sample_data):
        """Test initialization with custom style."""
        # Should not raise an error
        viz = Visualizer(sample_data, style="whitegrid", palette="muted")
        assert viz is not None


class TestHistogram:
    """Tests for histogram creation."""

    def test_create_histogram_basic(self, sample_data):
        """Test basic histogram creation."""
        viz = Visualizer(sample_data)
        fig = viz.create_histogram("age")

        assert fig is not None
        assert len(fig.axes) == 1

    def test_create_histogram_with_kde(self, sample_data):
        """Test histogram with KDE overlay."""
        viz = Visualizer(sample_data)
        fig = viz.create_histogram("age", kde=True)

        assert fig is not None

    def test_create_histogram_custom_bins(self, sample_data):
        """Test histogram with custom number of bins."""
        viz = Visualizer(sample_data)
        fig = viz.create_histogram("age", bins=20)

        assert fig is not None

    def test_create_histogram_with_title(self, sample_data):
        """Test histogram with custom title."""
        viz = Visualizer(sample_data)
        fig = viz.create_histogram("age", title="Age Distribution")

        assert "Age Distribution" in fig.axes[0].get_title()

    def test_create_histogram_save(self, sample_data, temp_output_dir):
        """Test saving histogram to file."""
        viz = Visualizer(sample_data)
        save_path = temp_output_dir / "histogram.png"
        viz.create_histogram("age", save_path=save_path)

        assert save_path.exists()

    def test_create_histogram_invalid_column(self, sample_data):
        """Test that invalid column raises ValueError."""
        viz = Visualizer(sample_data)

        with pytest.raises(ValueError):
            viz.create_histogram("nonexistent")


class TestBoxplot:
    """Tests for boxplot creation."""

    def test_create_boxplot_basic(self, sample_data):
        """Test basic boxplot creation."""
        viz = Visualizer(sample_data)
        fig = viz.create_boxplot("salary")

        assert fig is not None

    def test_create_boxplot_grouped(self, sample_data):
        """Test boxplot grouped by category."""
        viz = Visualizer(sample_data)
        fig = viz.create_boxplot("salary", by="department")

        assert fig is not None

    def test_create_boxplot_save(self, sample_data, temp_output_dir):
        """Test saving boxplot to file."""
        viz = Visualizer(sample_data)
        save_path = temp_output_dir / "boxplot.png"
        viz.create_boxplot("salary", save_path=save_path)

        assert save_path.exists()

    def test_create_boxplot_invalid_column(self, sample_data):
        """Test that invalid column raises ValueError."""
        viz = Visualizer(sample_data)

        with pytest.raises(ValueError):
            viz.create_boxplot("nonexistent")


class TestScatterPlot:
    """Tests for scatter plot creation."""

    def test_create_scatter_basic(self, sample_data):
        """Test basic scatter plot creation."""
        viz = Visualizer(sample_data)
        fig = viz.create_scatter("age", "salary")

        assert fig is not None

    def test_create_scatter_with_hue(self, sample_data):
        """Test scatter plot with color coding."""
        viz = Visualizer(sample_data)
        fig = viz.create_scatter("age", "salary", hue="department")

        assert fig is not None

    def test_create_scatter_with_size(self, sample_data):
        """Test scatter plot with size coding."""
        viz = Visualizer(sample_data)
        fig = viz.create_scatter("age", "salary", size="years_experience")

        assert fig is not None

    def test_create_scatter_save(self, sample_data, temp_output_dir):
        """Test saving scatter plot to file."""
        viz = Visualizer(sample_data)
        save_path = temp_output_dir / "scatter.png"
        viz.create_scatter("age", "salary", save_path=save_path)

        assert save_path.exists()


class TestCorrelationHeatmap:
    """Tests for correlation heatmap creation."""

    def test_create_correlation_heatmap_basic(self, sample_data):
        """Test basic correlation heatmap creation."""
        viz = Visualizer(sample_data)
        fig = viz.create_correlation_heatmap()

        assert fig is not None

    def test_create_correlation_heatmap_subset(self, sample_data):
        """Test heatmap with column subset."""
        viz = Visualizer(sample_data)
        fig = viz.create_correlation_heatmap(columns=["age", "salary"])

        assert fig is not None

    def test_create_correlation_heatmap_spearman(self, sample_data):
        """Test heatmap with Spearman correlation."""
        viz = Visualizer(sample_data)
        fig = viz.create_correlation_heatmap(method="spearman")

        assert fig is not None

    def test_create_correlation_heatmap_no_annot(self, sample_data):
        """Test heatmap without annotations."""
        viz = Visualizer(sample_data)
        fig = viz.create_correlation_heatmap(annot=False)

        assert fig is not None

    def test_create_correlation_heatmap_save(self, sample_data, temp_output_dir):
        """Test saving heatmap to file."""
        viz = Visualizer(sample_data)
        save_path = temp_output_dir / "heatmap.png"
        viz.create_correlation_heatmap(save_path=save_path)

        assert save_path.exists()


class TestLinePlot:
    """Tests for line plot creation."""

    def test_create_line_plot_single(self, sample_data):
        """Test line plot with single series."""
        viz = Visualizer(sample_data)
        fig = viz.create_line_plot("age", ["salary"])

        assert fig is not None

    def test_create_line_plot_multiple(self, sample_data):
        """Test line plot with multiple series."""
        viz = Visualizer(sample_data)
        fig = viz.create_line_plot("age", ["salary", "years_experience"])

        assert fig is not None

    def test_create_line_plot_save(self, sample_data, temp_output_dir):
        """Test saving line plot to file."""
        viz = Visualizer(sample_data)
        save_path = temp_output_dir / "lineplot.png"
        viz.create_line_plot("age", ["salary"], save_path=save_path)

        assert save_path.exists()


class TestBarPlot:
    """Tests for bar plot creation."""

    def test_create_bar_plot_basic(self, sample_data):
        """Test basic bar plot creation."""
        # Create aggregated data for bar plot
        df_agg = sample_data.groupby("department")["salary"].mean().reset_index()
        viz = Visualizer(df_agg)
        fig = viz.create_bar_plot("department", "salary")

        assert fig is not None

    def test_create_bar_plot_horizontal(self, sample_data):
        """Test horizontal bar plot."""
        df_agg = sample_data.groupby("department")["salary"].mean().reset_index()
        viz = Visualizer(df_agg)
        fig = viz.create_bar_plot("department", "salary", horizontal=True)

        assert fig is not None

    def test_create_bar_plot_save(self, sample_data, temp_output_dir):
        """Test saving bar plot to file."""
        df_agg = sample_data.groupby("department")["salary"].mean().reset_index()
        viz = Visualizer(df_agg)
        save_path = temp_output_dir / "barplot.png"
        viz.create_bar_plot("department", "salary", save_path=save_path)

        assert save_path.exists()


class TestPairplot:
    """Tests for pairplot creation."""

    def test_create_pairplot_basic(self, sample_data):
        """Test basic pairplot creation."""
        viz = Visualizer(sample_data)
        grid = viz.create_pairplot(columns=["age", "salary", "years_experience"])

        assert grid is not None

    def test_create_pairplot_with_hue(self, sample_data):
        """Test pairplot with color coding."""
        viz = Visualizer(sample_data)
        grid = viz.create_pairplot(columns=["age", "salary"], hue="department")

        assert grid is not None

    def test_create_pairplot_kde(self, sample_data):
        """Test pairplot with KDE on diagonal."""
        viz = Visualizer(sample_data)
        grid = viz.create_pairplot(columns=["age", "salary"], diag_kind="kde")

        assert grid is not None

    def test_create_pairplot_save(self, sample_data, temp_output_dir):
        """Test saving pairplot to file."""
        viz = Visualizer(sample_data)
        save_path = temp_output_dir / "pairplot.png"
        viz.create_pairplot(columns=["age", "salary"], save_path=save_path)

        assert save_path.exists()


class TestCountplot:
    """Tests for countplot creation."""

    def test_create_countplot_basic(self, sample_data):
        """Test basic countplot creation."""
        viz = Visualizer(sample_data)
        fig = viz.create_countplot("department")

        assert fig is not None

    def test_create_countplot_with_hue(self, sample_data):
        """Test countplot with grouping."""
        # Add a categorical column for testing
        sample_data["level"] = np.random.choice(["Junior", "Senior"], len(sample_data))
        viz = Visualizer(sample_data)
        fig = viz.create_countplot("department", hue="level")

        assert fig is not None

    def test_create_countplot_save(self, sample_data, temp_output_dir):
        """Test saving countplot to file."""
        viz = Visualizer(sample_data)
        save_path = temp_output_dir / "countplot.png"
        viz.create_countplot("department", save_path=save_path)

        assert save_path.exists()


class TestVisualizerIntegration:
    """Integration tests for Visualizer."""

    def test_multiple_plots(self, sample_data, temp_output_dir):
        """Test creating multiple plots in sequence."""
        viz = Visualizer(sample_data)

        # Create multiple plots
        hist_path = temp_output_dir / "hist.png"
        box_path = temp_output_dir / "box.png"
        scatter_path = temp_output_dir / "scatter.png"

        viz.create_histogram("age", save_path=hist_path)
        viz.create_boxplot("salary", save_path=box_path)
        viz.create_scatter("age", "salary", save_path=scatter_path)

        # All files should exist
        assert hist_path.exists()
        assert box_path.exists()
        assert scatter_path.exists()
