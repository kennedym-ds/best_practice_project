"""
Unit tests for the DataAnalyzer module.
"""

import numpy as np
import pandas as pd
import pytest

from data_analysis.data_analyzer import DataAnalyzer


@pytest.fixture
def sample_data():
    """Create sample DataFrame for testing."""
    np.random.seed(42)
    return pd.DataFrame({
        'id': range(1, 101),
        'age': np.random.randint(20, 65, 100),
        'salary': np.random.randint(30000, 150000, 100),
        'years_experience': np.random.randint(0, 40, 100),
        'department': np.random.choice(['HR', 'IT', 'Finance', 'Sales'], 100),
        'performance_score': np.random.uniform(1.0, 5.0, 100)
    })


@pytest.fixture
def data_with_correlations():
    """Create DataFrame with known correlations."""
    np.random.seed(42)
    x = np.random.randn(100)
    return pd.DataFrame({
        'x': x,
        'y_strong': 2 * x + np.random.randn(100) * 0.1,  # Strong correlation
        'y_weak': x + np.random.randn(100) * 5,  # Weak correlation
        'z': np.random.randn(100)  # No correlation with x
    })


class TestDataAnalyzerInitialization:
    """Tests for DataAnalyzer initialization."""
    
    def test_init_with_dataframe(self, sample_data):
        """Test initialization with a DataFrame."""
        analyzer = DataAnalyzer(sample_data)
        assert analyzer.df is not None
        assert analyzer.df.shape == sample_data.shape
    
    def test_init_creates_copy(self, sample_data):
        """Test that initialization creates a copy."""
        analyzer = DataAnalyzer(sample_data)
        analyzer.df.loc[0, 'age'] = 999
        
        # Original should be unchanged
        assert sample_data.loc[0, 'age'] != 999


class TestSummaryStatistics:
    """Tests for summary statistics."""
    
    def test_get_summary_statistics(self, sample_data):
        """Test getting summary statistics."""
        analyzer = DataAnalyzer(sample_data)
        stats = analyzer.get_summary_statistics()
        
        # Should have standard stats
        assert 'mean' in stats.index
        assert 'std' in stats.index
        assert 'min' in stats.index
        assert 'max' in stats.index
        
        # Should have additional stats
        assert 'skewness' in stats.index
        assert 'kurtosis' in stats.index
    
    def test_summary_statistics_numeric_only(self, sample_data):
        """Test that summary statistics only includes numeric columns."""
        analyzer = DataAnalyzer(sample_data)
        stats = analyzer.get_summary_statistics()
        
        # Should not include 'department' (categorical)
        assert 'department' not in stats.columns


class TestMissingValueReport:
    """Tests for missing value reporting."""
    
    def test_missing_value_report_no_missing(self, sample_data):
        """Test report when there are no missing values."""
        analyzer = DataAnalyzer(sample_data)
        report = analyzer.get_missing_value_report()
        
        # Should be empty
        assert len(report) == 0
    
    def test_missing_value_report_with_missing(self):
        """Test report with missing values."""
        df = pd.DataFrame({
            'a': [1, 2, None, 4, 5],
            'b': [1, None, None, 4, 5],
            'c': [1, 2, 3, 4, 5]
        })
        analyzer = DataAnalyzer(df)
        report = analyzer.get_missing_value_report()
        
        # Should have 2 rows (a and b)
        assert len(report) == 2
        assert 'missing_count' in report.columns
        assert 'missing_percentage' in report.columns
        
        # b should have more missing values than a
        assert report.loc['b', 'missing_count'] > report.loc['a', 'missing_count']


class TestCorrelationAnalysis:
    """Tests for correlation analysis."""
    
    def test_get_correlation_matrix_default(self, data_with_correlations):
        """Test correlation matrix with default settings."""
        analyzer = DataAnalyzer(data_with_correlations)
        corr = analyzer.get_correlation_matrix()
        
        # Should be square matrix
        assert corr.shape[0] == corr.shape[1]
        
        # Diagonal should be 1
        assert all(corr.values.diagonal() == 1.0)
    
    def test_get_correlation_matrix_spearman(self, data_with_correlations):
        """Test correlation matrix with Spearman method."""
        analyzer = DataAnalyzer(data_with_correlations)
        corr = analyzer.get_correlation_matrix(method='spearman')
        
        assert corr is not None
        assert corr.shape[0] == corr.shape[1]
    
    def test_get_correlation_matrix_subset(self, data_with_correlations):
        """Test correlation matrix with column subset."""
        analyzer = DataAnalyzer(data_with_correlations)
        corr = analyzer.get_correlation_matrix(columns=['x', 'y_strong'])
        
        assert corr.shape == (2, 2)
        assert 'x' in corr.columns
        assert 'y_strong' in corr.columns
    
    def test_find_high_correlations(self, data_with_correlations):
        """Test finding high correlations."""
        analyzer = DataAnalyzer(data_with_correlations)
        high_corr = analyzer.find_high_correlations(threshold=0.8)
        
        # Should find strong correlation between x and y_strong
        assert len(high_corr) > 0
        
        # Results should be tuples
        assert all(len(item) == 3 for item in high_corr)
    
    def test_find_high_correlations_threshold(self, data_with_correlations):
        """Test that threshold works correctly."""
        analyzer = DataAnalyzer(data_with_correlations)
        
        high_threshold = analyzer.find_high_correlations(threshold=0.95)
        low_threshold = analyzer.find_high_correlations(threshold=0.3)
        
        # Lower threshold should find more correlations
        assert len(low_threshold) >= len(high_threshold)


class TestGroupAnalysis:
    """Tests for group-based analysis."""
    
    def test_group_analysis_mean(self, sample_data):
        """Test group analysis with mean aggregation."""
        analyzer = DataAnalyzer(sample_data)
        result = analyzer.group_analysis('department', 'salary', 'mean')
        
        # Should have one row per department
        assert len(result) <= sample_data['department'].nunique()
        assert 'salary' in result.columns
    
    def test_group_analysis_sum(self, sample_data):
        """Test group analysis with sum aggregation."""
        analyzer = DataAnalyzer(sample_data)
        result = analyzer.group_analysis('department', 'salary', 'sum')
        
        assert len(result) > 0
    
    def test_group_analysis_invalid_column(self, sample_data):
        """Test that invalid column raises ValueError."""
        analyzer = DataAnalyzer(sample_data)
        
        with pytest.raises(ValueError):
            analyzer.group_analysis('nonexistent', 'salary', 'mean')
        
        with pytest.raises(ValueError):
            analyzer.group_analysis('department', 'nonexistent', 'mean')


class TestLinearRegression:
    """Tests for linear regression analysis."""
    
    def test_simple_linear_regression(self, data_with_correlations):
        """Test simple linear regression."""
        analyzer = DataAnalyzer(data_with_correlations)
        results = analyzer.simple_linear_regression('x', 'y_strong')
        
        # Should return dict with required keys
        assert 'slope' in results
        assert 'intercept' in results
        assert 'r_squared' in results
        
        # R-squared should be high for strong correlation
        assert results['r_squared'] > 0.8
    
    def test_linear_regression_weak_correlation(self, data_with_correlations):
        """Test linear regression with weak correlation."""
        analyzer = DataAnalyzer(data_with_correlations)
        results = analyzer.simple_linear_regression('x', 'y_weak')
        
        # R-squared should be lower
        assert results['r_squared'] < 0.8
    
    def test_linear_regression_with_nan(self):
        """Test linear regression handles NaN values."""
        df = pd.DataFrame({
            'x': [1, 2, 3, None, 5],
            'y': [2, 4, 6, 8, None]
        })
        analyzer = DataAnalyzer(df)
        results = analyzer.simple_linear_regression('x', 'y')
        
        # Should still work by removing NaN
        assert 'slope' in results
        assert results['slope'] is not None


class TestValueCounts:
    """Tests for value counting."""
    
    def test_get_value_counts(self, sample_data):
        """Test getting value counts."""
        analyzer = DataAnalyzer(sample_data)
        counts = analyzer.get_value_counts('department')
        
        assert len(counts) > 0
        assert counts.sum() == len(sample_data)
    
    def test_get_value_counts_normalized(self, sample_data):
        """Test getting normalized value counts."""
        analyzer = DataAnalyzer(sample_data)
        counts = analyzer.get_value_counts('department', normalize=True)
        
        # Should sum to 1
        assert abs(counts.sum() - 1.0) < 0.01
    
    def test_get_value_counts_top_n(self, sample_data):
        """Test getting top N values."""
        analyzer = DataAnalyzer(sample_data)
        counts = analyzer.get_value_counts('department', top_n=2)
        
        assert len(counts) == 2
    
    def test_get_value_counts_invalid_column(self, sample_data):
        """Test that invalid column raises ValueError."""
        analyzer = DataAnalyzer(sample_data)
        
        with pytest.raises(ValueError):
            analyzer.get_value_counts('nonexistent')


class TestAnomalyDetection:
    """Tests for anomaly detection."""
    
    def test_detect_anomalies_zscore(self):
        """Test z-score anomaly detection."""
        df = pd.DataFrame({
            'value': [1, 2, 3, 4, 5, 100]  # 100 is an outlier
        })
        analyzer = DataAnalyzer(df)
        anomalies = analyzer.detect_anomalies('value', method='zscore', threshold=2.0)
        
        # Should detect the outlier
        assert len(anomalies) > 0
        assert 100 in anomalies['value'].values
    
    def test_detect_anomalies_iqr(self):
        """Test IQR anomaly detection."""
        df = pd.DataFrame({
            'value': list(range(1, 21)) + [100]  # 100 is an outlier
        })
        analyzer = DataAnalyzer(df)
        anomalies = analyzer.detect_anomalies('value', method='iqr', threshold=1.5)
        
        # Should detect the outlier
        assert len(anomalies) > 0
    
    def test_detect_anomalies_invalid_method(self, sample_data):
        """Test that invalid method raises ValueError."""
        analyzer = DataAnalyzer(sample_data)
        
        with pytest.raises(ValueError):
            analyzer.detect_anomalies('age', method='invalid')
    
    def test_detect_anomalies_invalid_column(self, sample_data):
        """Test that invalid column raises ValueError."""
        analyzer = DataAnalyzer(sample_data)
        
        with pytest.raises(ValueError):
            analyzer.detect_anomalies('nonexistent')
    
    def test_detect_anomalies_non_numeric(self, sample_data):
        """Test that non-numeric column raises ValueError."""
        analyzer = DataAnalyzer(sample_data)
        
        with pytest.raises(ValueError):
            analyzer.detect_anomalies('department')


class TestDataAnalyzerIntegration:
    """Integration tests for DataAnalyzer."""
    
    def test_full_analysis_pipeline(self, sample_data):
        """Test a complete analysis pipeline."""
        analyzer = DataAnalyzer(sample_data)
        
        # Get multiple analyses
        stats = analyzer.get_summary_statistics()
        missing_report = analyzer.get_missing_value_report()
        corr = analyzer.get_correlation_matrix()
        dept_analysis = analyzer.group_analysis('department', 'salary', 'mean')
        
        # All should return valid results
        assert stats is not None
        assert missing_report is not None
        assert corr is not None
        assert dept_analysis is not None
