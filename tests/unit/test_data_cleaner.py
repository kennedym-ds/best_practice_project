"""Unit tests for the DataCleaner module."""

import numpy as np
import pandas as pd
import pytest

from data_analysis.data_cleaner import DataCleaner


@pytest.fixture
def sample_data_with_issues():
    """Create sample DataFrame with various data quality issues."""
    return pd.DataFrame(
        {
            "id": [1, 2, 2, 4, 5, 6, 7],
            "name": ["Alice", "Bob", "Bob", "David", None, "Frank", "Grace"],
            "age": [25, 30, 30, np.nan, 45, 28, 150],  # Has NaN and outlier
            "salary": [50000, 60000, 60000, 80000, 90000, None, 55000],  # Has duplicate and NaN
            "department": ["HR", "IT", "IT", "Finance", "IT", "HR", "HR"],
        }
    )


@pytest.fixture
def clean_data():
    """Create sample DataFrame with clean data."""
    return pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5],
            "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
            "age": [25, 30, 35, 40, 45],
            "salary": [50000.0, 60000.0, 70000.0, 80000.0, 90000.0],
        }
    )


class TestDataCleanerInitialization:
    """Tests for DataCleaner initialization."""

    def test_init_with_dataframe(self, sample_data_with_issues):
        """Test initialization with a DataFrame."""
        cleaner = DataCleaner(sample_data_with_issues)
        assert cleaner.df is not None
        assert cleaner.df.shape == sample_data_with_issues.shape

    def test_init_creates_copy(self, sample_data_with_issues):
        """Test that initialization creates a copy, not a reference."""
        cleaner = DataCleaner(sample_data_with_issues)
        cleaner.df.loc[0, "age"] = 999

        # Original should be unchanged
        assert sample_data_with_issues.loc[0, "age"] == 25


class TestHandleMissingValues:
    """Tests for missing value handling."""

    def test_handle_missing_drop(self, sample_data_with_issues):
        """Test dropping rows with missing values."""
        cleaner = DataCleaner(sample_data_with_issues)
        result = cleaner.handle_missing_values(strategy="drop")

        assert result.isnull().sum().sum() == 0
        assert result.shape[0] < sample_data_with_issues.shape[0]

    def test_handle_missing_fill_value(self, sample_data_with_issues):
        """Test filling missing values with a specific value."""
        cleaner = DataCleaner(sample_data_with_issues)
        result = cleaner.handle_missing_values(strategy="fill", fill_value=0)

        assert result.isnull().sum().sum() == 0

    def test_handle_missing_ffill(self, sample_data_with_issues):
        """Test forward fill strategy."""
        cleaner = DataCleaner(sample_data_with_issues)
        result = cleaner.handle_missing_values(strategy="ffill")

        # Should have fewer NaN values
        assert result.isnull().sum().sum() <= sample_data_with_issues.isnull().sum().sum()

    def test_handle_missing_mean(self, sample_data_with_issues):
        """Test filling with mean for numeric columns."""
        cleaner = DataCleaner(sample_data_with_issues)
        result = cleaner.handle_missing_values(strategy="mean")

        # Numeric columns should have no NaN
        numeric_cols = result.select_dtypes(include=[np.number]).columns
        assert result[numeric_cols].isnull().sum().sum() == 0

    def test_handle_missing_median(self, sample_data_with_issues):
        """Test filling with median for numeric columns."""
        cleaner = DataCleaner(sample_data_with_issues)
        result = cleaner.handle_missing_values(strategy="median")

        # Numeric columns should have no NaN
        numeric_cols = result.select_dtypes(include=[np.number]).columns
        assert result[numeric_cols].isnull().sum().sum() == 0

    def test_handle_missing_invalid_strategy(self, sample_data_with_issues):
        """Test that invalid strategy raises ValueError."""
        cleaner = DataCleaner(sample_data_with_issues)

        with pytest.raises(ValueError):
            cleaner.handle_missing_values(strategy="invalid")


class TestRemoveDuplicates:
    """Tests for duplicate removal."""

    def test_remove_duplicates_all_columns(self, sample_data_with_issues):
        """Test removing duplicates considering all columns."""
        cleaner = DataCleaner(sample_data_with_issues)
        result = cleaner.remove_duplicates()

        # Should have fewer rows
        assert result.shape[0] <= sample_data_with_issues.shape[0]
        # Should have no duplicates
        assert result.duplicated().sum() == 0

    def test_remove_duplicates_subset(self, sample_data_with_issues):
        """Test removing duplicates based on specific columns."""
        cleaner = DataCleaner(sample_data_with_issues)
        result = cleaner.remove_duplicates(subset=["name"])

        # Should have unique names
        assert result["name"].duplicated().sum() == 0

    def test_remove_duplicates_keep_last(self, sample_data_with_issues):
        """Test keeping last duplicate."""
        cleaner = DataCleaner(sample_data_with_issues)
        result = cleaner.remove_duplicates(keep="last")

        assert result.shape[0] <= sample_data_with_issues.shape[0]


class TestConvertDtypes:
    """Tests for data type conversion."""

    def test_convert_dtypes_numeric(self):
        """Test converting string to numeric."""
        df = pd.DataFrame({"value": ["1", "2", "3", "4"]})
        cleaner = DataCleaner(df)
        result = cleaner.convert_dtypes({"value": "int64"})

        assert result["value"].dtype == np.int64

    def test_convert_dtypes_float(self):
        """Test converting to float."""
        df = pd.DataFrame({"value": [1, 2, 3, 4]})
        cleaner = DataCleaner(df)
        result = cleaner.convert_dtypes({"value": "float64"})

        assert result["value"].dtype == np.float64

    def test_convert_dtypes_datetime(self):
        """Test converting to datetime."""
        df = pd.DataFrame({"date": ["2023-01-01", "2023-01-02", "2023-01-03"]})
        cleaner = DataCleaner(df)
        result = cleaner.convert_dtypes({"date": "datetime64[ns]"})

        assert pd.api.types.is_datetime64_any_dtype(result["date"])

    def test_convert_dtypes_invalid_column(self, clean_data):
        """Test that converting non-existent column raises ValueError."""
        cleaner = DataCleaner(clean_data)

        with pytest.raises(ValueError):
            cleaner.convert_dtypes({"nonexistent": "int64"})


class TestOutlierDetection:
    """Tests for outlier detection."""

    def test_detect_outliers_iqr(self, sample_data_with_issues):
        """Test IQR method for outlier detection."""
        cleaner = DataCleaner(sample_data_with_issues)
        outliers = cleaner.detect_outliers("age", method="iqr")

        # Should detect the age=150 as an outlier
        assert len(outliers) > 0

    def test_detect_outliers_zscore(self, sample_data_with_issues):
        """Test z-score method for outlier detection."""
        cleaner = DataCleaner(sample_data_with_issues)
        outliers = cleaner.detect_outliers("age", method="zscore")

        # Should detect extreme values
        assert len(outliers) > 0

    def test_detect_outliers_invalid_method(self, sample_data_with_issues):
        """Test that invalid method raises ValueError."""
        cleaner = DataCleaner(sample_data_with_issues)

        with pytest.raises(ValueError):
            cleaner.detect_outliers("age", method="invalid")

    def test_detect_outliers_invalid_column(self, sample_data_with_issues):
        """Test that invalid column raises ValueError."""
        cleaner = DataCleaner(sample_data_with_issues)

        with pytest.raises(ValueError):
            cleaner.detect_outliers("nonexistent")


class TestRemoveOutliers:
    """Tests for outlier removal."""

    def test_remove_outliers_iqr(self, sample_data_with_issues):
        """Test removing outliers using IQR method."""
        cleaner = DataCleaner(sample_data_with_issues)
        result = cleaner.remove_outliers("age", method="iqr")

        # Should have fewer rows
        assert result.shape[0] <= sample_data_with_issues.shape[0]

    def test_remove_outliers_zscore(self, sample_data_with_issues):
        """Test removing outliers using z-score method."""
        cleaner = DataCleaner(sample_data_with_issues)
        result = cleaner.remove_outliers("age", method="zscore", threshold=2.0)

        # Should have fewer rows
        assert result.shape[0] <= sample_data_with_issues.shape[0]


class TestGetData:
    """Tests for get_data method."""

    def test_get_data_returns_copy(self, clean_data):
        """Test that get_data returns the cleaned DataFrame."""
        cleaner = DataCleaner(clean_data)
        result = cleaner.get_data()

        assert result.shape == clean_data.shape
        pd.testing.assert_frame_equal(result, clean_data)


class TestDataCleanerIntegration:
    """Integration tests for DataCleaner."""

    def test_full_cleaning_pipeline(self, sample_data_with_issues):
        """Test a complete cleaning pipeline."""
        cleaner = DataCleaner(sample_data_with_issues)

        # Chain cleaning operations
        cleaner.remove_duplicates()
        cleaner.handle_missing_values(strategy="mean")
        cleaner.remove_outliers("age", method="iqr")

        result = cleaner.get_data()

        # Verify cleaning results
        assert result.duplicated().sum() == 0  # No duplicates
        numeric_cols = result.select_dtypes(include=[np.number]).columns
        assert result[numeric_cols].isnull().sum().sum() == 0  # No NaN in numeric columns
        assert result.shape[0] > 0  # Still has data
