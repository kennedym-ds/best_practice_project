"""
Integration tests for the complete data analysis pipeline.
"""

import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from data_analysis.data_analyzer import DataAnalyzer
from data_analysis.data_cleaner import DataCleaner
from data_analysis.data_loader import DataLoader
from data_analysis.visualizer import Visualizer


@pytest.fixture
def sample_raw_data():
    """Create sample raw data with typical data quality issues."""
    np.random.seed(42)
    return pd.DataFrame({
        'id': [1, 2, 2, 4, 5, 6, 7, 8, 9, 10],
        'name': ['Alice', 'Bob', 'Bob', 'David', None, 'Frank', 'Grace', 'Henry', 'Ivy', 'Jack'],
        'age': [25, 30, 30, np.nan, 45, 28, 150, 35, 40, 33],  # Has NaN and outlier
        'salary': [50000, 60000, 60000, 80000, 90000, None, 55000, 70000, 75000, 65000],
        'department': ['HR', 'IT', 'IT', 'Finance', 'IT', 'HR', 'HR', 'Finance', 'IT', 'Sales'],
        'years_experience': [2, 5, 5, 10, 15, 3, 12, 8, 11, 6]
    })


@pytest.fixture
def temp_workspace():
    """Create a temporary workspace directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = Path(tmpdir)
        (workspace / "raw").mkdir()
        (workspace / "processed").mkdir()
        (workspace / "visualizations").mkdir()
        yield workspace


class TestEndToEndPipeline:
    """Test the complete data analysis pipeline from loading to visualization."""
    
    def test_complete_pipeline(self, sample_raw_data, temp_workspace):
        """Test a complete end-to-end data analysis workflow."""
        # Step 1: Save raw data
        raw_data_path = temp_workspace / "raw" / "raw_data.csv"
        sample_raw_data.to_csv(raw_data_path, index=False)
        
        # Step 2: Load data
        loader = DataLoader(data_dir=str(temp_workspace / "raw"))
        df = loader.load_csv("raw_data.csv")
        assert df is not None
        assert df.shape == sample_raw_data.shape
        
        # Step 3: Clean data
        cleaner = DataCleaner(df)
        cleaner.remove_duplicates()
        cleaner.handle_missing_values(strategy='mean')
        cleaner.remove_outliers('age', method='iqr')
        cleaned_df = cleaner.get_data()
        
        # Verify cleaning
        assert cleaned_df.shape[0] < df.shape[0]  # Some rows removed
        assert cleaned_df.duplicated().sum() == 0  # No duplicates
        numeric_cols = cleaned_df.select_dtypes(include=[np.number]).columns
        assert cleaned_df[numeric_cols].isnull().sum().sum() == 0  # No NaN in numeric
        
        # Step 4: Save cleaned data
        processed_path = loader.save_csv(
            cleaned_df,
            "cleaned_data.csv",
            output_dir=str(temp_workspace / "processed")
        )
        assert processed_path.exists()
        
        # Step 5: Analyze data
        analyzer = DataAnalyzer(cleaned_df)
        
        # Get various analyses
        stats = analyzer.get_summary_statistics()
        assert stats is not None
        
        corr = analyzer.get_correlation_matrix()
        assert corr is not None
        
        dept_analysis = analyzer.group_analysis('department', 'salary', 'mean')
        assert len(dept_analysis) > 0
        
        # Step 6: Create visualizations
        viz = Visualizer(cleaned_df)
        
        hist_path = temp_workspace / "visualizations" / "age_distribution.png"
        viz.create_histogram('age', save_path=hist_path)
        assert hist_path.exists()
        
        box_path = temp_workspace / "visualizations" / "salary_by_dept.png"
        viz.create_boxplot('salary', by='department', save_path=box_path)
        assert box_path.exists()
        
        scatter_path = temp_workspace / "visualizations" / "age_vs_salary.png"
        viz.create_scatter('age', 'salary', save_path=scatter_path)
        assert scatter_path.exists()
        
        heatmap_path = temp_workspace / "visualizations" / "correlation_heatmap.png"
        viz.create_correlation_heatmap(save_path=heatmap_path)
        assert heatmap_path.exists()


class TestDataLoaderIntegration:
    """Integration tests for data loading across different formats."""
    
    def test_load_and_convert_formats(self, sample_raw_data, temp_workspace):
        """Test loading CSV and saving as different formats."""
        # Save as CSV
        csv_path = temp_workspace / "raw" / "data.csv"
        sample_raw_data.to_csv(csv_path, index=False)
        
        # Load CSV
        loader = DataLoader(data_dir=str(temp_workspace / "raw"))
        df = loader.load_csv("data.csv")
        
        # Save as different formats
        output_csv = loader.save_csv(df, "output.csv", output_dir=str(temp_workspace / "processed"))
        assert output_csv.exists()
        
        # Load and verify - create a new loader for the processed directory
        processed_loader = DataLoader(data_dir=str(temp_workspace / "processed"))
        reloaded_df = processed_loader.load_csv("output.csv")
        # Note: CSV doesn't preserve all dtypes perfectly, so we only check shape
        assert reloaded_df.shape == df.shape


class TestCleanerAnalyzerIntegration:
    """Integration tests combining data cleaning and analysis."""
    
    def test_clean_then_analyze(self, sample_raw_data):
        """Test cleaning data and then performing analysis."""
        # Clean data
        cleaner = DataCleaner(sample_raw_data)
        cleaner.remove_duplicates()
        # Use 'drop' strategy to remove all rows with missing values
        cleaner.handle_missing_values(strategy='drop')
        cleaned_df = cleaner.get_data()
        
        # Analyze cleaned data
        analyzer = DataAnalyzer(cleaned_df)
        
        # Should be able to perform all analyses without errors
        stats = analyzer.get_summary_statistics()
        assert stats is not None
        
        missing_report = analyzer.get_missing_value_report()
        # Should have no missing values after cleaning with 'drop' strategy
        assert len(missing_report) == 0 or all(missing_report['missing_count'] == 0)
        
        corr = analyzer.get_correlation_matrix()
        assert corr is not None
        
        # Test group analysis
        dept_stats = analyzer.group_analysis('department', 'salary', 'mean')
        assert len(dept_stats) > 0


class TestAnalyzerVisualizerIntegration:
    """Integration tests combining analysis and visualization."""
    
    def test_analyze_then_visualize(self, sample_raw_data, temp_workspace):
        """Test analyzing data and then creating visualizations."""
        # Clean data first
        cleaner = DataCleaner(sample_raw_data)
        cleaner.remove_duplicates()
        cleaner.handle_missing_values(strategy='mean')
        cleaner.remove_outliers('age', method='iqr')
        cleaned_df = cleaner.get_data()
        
        # Analyze
        analyzer = DataAnalyzer(cleaned_df)
        corr = analyzer.get_correlation_matrix()
        
        # Find high correlations
        high_corr = analyzer.find_high_correlations(threshold=0.3)
        
        # Visualize correlations
        viz = Visualizer(cleaned_df)
        
        # Create correlation heatmap
        heatmap_path = temp_workspace / "visualizations" / "correlation.png"
        viz.create_correlation_heatmap(save_path=heatmap_path)
        assert heatmap_path.exists()
        
        # Create scatter plots for highly correlated features
        if high_corr:
            for feature1, feature2, corr_val in high_corr[:2]:  # First 2 pairs
                scatter_path = temp_workspace / "visualizations" / f"{feature1}_vs_{feature2}.png"
                viz.create_scatter(feature1, feature2, save_path=scatter_path)
                assert scatter_path.exists()


class TestFullPipelineWithExcelData:
    """Test pipeline with Excel data format."""
    
    def test_excel_pipeline(self, sample_raw_data, temp_workspace):
        """Test complete pipeline using Excel format."""
        # Save as Excel
        excel_path = temp_workspace / "raw" / "data.xlsx"
        sample_raw_data.to_excel(excel_path, index=False)
        
        # Load Excel
        loader = DataLoader(data_dir=str(temp_workspace / "raw"))
        df = loader.load_excel("data.xlsx")
        
        # Process
        cleaner = DataCleaner(df)
        cleaner.handle_missing_values(strategy='mean')
        cleaned_df = cleaner.get_data()
        
        # Analyze
        analyzer = DataAnalyzer(cleaned_df)
        stats = analyzer.get_summary_statistics()
        
        assert stats is not None
        assert cleaned_df is not None


class TestFullPipelineWithJSONData:
    """Test pipeline with JSON data format."""
    
    def test_json_pipeline(self, sample_raw_data, temp_workspace):
        """Test complete pipeline using JSON format."""
        # Save as JSON
        json_path = temp_workspace / "raw" / "data.json"
        sample_raw_data.to_json(json_path, orient='records')
        
        # Load JSON
        loader = DataLoader(data_dir=str(temp_workspace / "raw"))
        df = loader.load_json("data.json")
        
        # Process
        cleaner = DataCleaner(df)
        cleaner.handle_missing_values(strategy='median')
        cleaned_df = cleaner.get_data()
        
        # Analyze
        analyzer = DataAnalyzer(cleaned_df)
        dept_analysis = analyzer.group_analysis('department', 'salary', 'sum')
        
        assert dept_analysis is not None
        assert len(dept_analysis) > 0


class TestRobustness:
    """Test pipeline robustness with edge cases."""
    
    def test_empty_dataframe_handling(self):
        """Test how pipeline handles empty DataFrame."""
        df = pd.DataFrame()
        
        # Cleaner should handle empty df
        cleaner = DataCleaner(df)
        result = cleaner.get_data()
        assert len(result) == 0
    
    def test_single_row_dataframe(self):
        """Test pipeline with single row."""
        df = pd.DataFrame({
            'id': [1],
            'value': [100]
        })
        
        cleaner = DataCleaner(df)
        result = cleaner.get_data()
        assert len(result) == 1
        
        analyzer = DataAnalyzer(df)
        stats = analyzer.get_summary_statistics()
        assert stats is not None
    
    def test_all_missing_column(self):
        """Test handling of column with all missing values."""
        df = pd.DataFrame({
            'a': [1, 2, 3],
            'b': [None, None, None]
        })
        
        cleaner = DataCleaner(df)
        result = cleaner.handle_missing_values(strategy='drop')
        
        # Should still have column 'a'
        assert 'a' in result.columns
