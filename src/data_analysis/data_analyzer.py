"""
Data Analysis Module

This module provides utilities for analyzing data and generating statistics.
"""

import logging
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)


class DataAnalyzer:
    """
    A class for performing data analysis tasks.
    
    This class demonstrates best practices for data analysis including:
    - Descriptive statistics
    - Correlation analysis
    - Basic statistical tests
    - Simple modeling
    """
    
    def __init__(self, df: pd.DataFrame) -> None:
        """
        Initialize the DataAnalyzer with a DataFrame.
        
        Args:
            df: The DataFrame to analyze
        """
        self.df = df.copy()
        logger.info(f"DataAnalyzer initialized with DataFrame shape: {self.df.shape}")
    
    def get_summary_statistics(self) -> pd.DataFrame:
        """
        Get summary statistics for numeric columns.
        
        Returns:
            DataFrame containing descriptive statistics
        
        Example:
            >>> analyzer = DataAnalyzer(df)
            >>> stats = analyzer.get_summary_statistics()
        """
        logger.info("Generating summary statistics")
        stats = self.df.describe()
        
        # Add additional statistics
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        additional_stats = pd.DataFrame({
            'skewness': self.df[numeric_cols].skew(),
            'kurtosis': self.df[numeric_cols].kurtosis()
        }).T
        
        stats = pd.concat([stats, additional_stats])
        
        return stats
    
    def get_missing_value_report(self) -> pd.DataFrame:
        """
        Generate a report of missing values.
        
        Returns:
            DataFrame with missing value counts and percentages
        
        Example:
            >>> analyzer = DataAnalyzer(df)
            >>> missing_report = analyzer.get_missing_value_report()
        """
        logger.info("Generating missing value report")
        
        missing_count = self.df.isnull().sum()
        missing_percent = 100 * missing_count / len(self.df)
        
        report = pd.DataFrame({
            'missing_count': missing_count,
            'missing_percentage': missing_percent
        })
        
        report = report[report['missing_count'] > 0].sort_values(
            'missing_count', ascending=False
        )
        
        return report
    
    def get_correlation_matrix(
        self,
        method: str = "pearson",
        columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Calculate correlation matrix for numeric columns.
        
        Args:
            method: Correlation method ('pearson', 'spearman', 'kendall')
            columns: List of columns to include. If None, uses all numeric columns.
        
        Returns:
            Correlation matrix DataFrame
        
        Example:
            >>> analyzer = DataAnalyzer(df)
            >>> corr = analyzer.get_correlation_matrix(method='pearson')
        """
        logger.info(f"Calculating {method} correlation matrix")
        
        if columns is None:
            numeric_df = self.df.select_dtypes(include=[np.number])
        else:
            numeric_df = self.df[columns]
        
        corr_matrix = numeric_df.corr(method=method)
        
        return corr_matrix
    
    def find_high_correlations(
        self,
        threshold: float = 0.7,
        method: str = "pearson"
    ) -> List[Tuple[str, str, float]]:
        """
        Find pairs of features with high correlation.
        
        Args:
            threshold: Correlation threshold (absolute value)
            method: Correlation method ('pearson', 'spearman', 'kendall')
        
        Returns:
            List of tuples (feature1, feature2, correlation)
        
        Example:
            >>> analyzer = DataAnalyzer(df)
            >>> high_corr = analyzer.find_high_correlations(threshold=0.8)
        """
        logger.info(f"Finding correlations above {threshold}")
        
        corr_matrix = self.get_correlation_matrix(method=method)
        
        # Get upper triangle of correlation matrix
        upper_tri = corr_matrix.where(
            np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
        )
        
        # Find features with correlation above threshold
        high_corr = []
        for column in upper_tri.columns:
            for index in upper_tri.index:
                corr_val = upper_tri.loc[index, column]
                if abs(corr_val) > threshold:
                    high_corr.append((index, column, corr_val))
        
        # Sort by absolute correlation
        high_corr.sort(key=lambda x: abs(x[2]), reverse=True)
        
        logger.info(f"Found {len(high_corr)} feature pairs with correlation above {threshold}")
        
        return high_corr
    
    def group_analysis(
        self,
        group_by: str,
        agg_column: str,
        agg_func: str = "mean"
    ) -> pd.DataFrame:
        """
        Perform group-based analysis.
        
        Args:
            group_by: Column to group by
            agg_column: Column to aggregate
            agg_func: Aggregation function ('mean', 'sum', 'count', 'median', 'std')
        
        Returns:
            DataFrame with grouped results
        
        Example:
            >>> analyzer = DataAnalyzer(df)
            >>> grouped = analyzer.group_analysis('category', 'sales', 'mean')
        """
        logger.info(f"Performing group analysis: {group_by} by {agg_func}({agg_column})")
        
        if group_by not in self.df.columns:
            raise ValueError(f"Column '{group_by}' not found")
        if agg_column not in self.df.columns:
            raise ValueError(f"Column '{agg_column}' not found")
        
        grouped = self.df.groupby(group_by)[agg_column].agg(agg_func)
        
        return grouped.to_frame()
    
    def simple_linear_regression(
        self,
        x_column: str,
        y_column: str
    ) -> Dict[str, float]:
        """
        Perform simple linear regression.
        
        Args:
            x_column: Independent variable column name
            y_column: Dependent variable column name
        
        Returns:
            Dictionary with regression results (slope, intercept, r_squared)
        
        Example:
            >>> analyzer = DataAnalyzer(df)
            >>> results = analyzer.simple_linear_regression('x', 'y')
        """
        logger.info(f"Performing linear regression: {y_column} ~ {x_column}")
        
        # Prepare data
        X = self.df[[x_column]].values
        y = self.df[y_column].values
        
        # Remove NaN values
        mask = ~np.isnan(X.flatten()) & ~np.isnan(y)
        X = X[mask].reshape(-1, 1)
        y = y[mask]
        
        # Fit model
        model = LinearRegression()
        model.fit(X, y)
        
        # Calculate R-squared
        r_squared = model.score(X, y)
        
        results = {
            'slope': float(model.coef_[0]),
            'intercept': float(model.intercept_),
            'r_squared': float(r_squared)
        }
        
        logger.info(f"Regression results: R² = {r_squared:.4f}")
        
        return results
    
    def get_value_counts(
        self,
        column: str,
        normalize: bool = False,
        top_n: Optional[int] = None
    ) -> pd.Series:
        """
        Get value counts for a categorical column.
        
        Args:
            column: Column name
            normalize: If True, return proportions instead of counts
            top_n: Return only top N values
        
        Returns:
            Series with value counts
        
        Example:
            >>> analyzer = DataAnalyzer(df)
            >>> counts = analyzer.get_value_counts('category', top_n=10)
        """
        logger.info(f"Getting value counts for column '{column}'")
        
        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found")
        
        counts = self.df[column].value_counts(normalize=normalize)
        
        if top_n is not None:
            counts = counts.head(top_n)
        
        return counts
    
    def detect_anomalies(
        self,
        column: str,
        method: str = "zscore",
        threshold: float = 3.0
    ) -> pd.DataFrame:
        """
        Detect anomalies in a numeric column.
        
        Args:
            column: Column to check for anomalies
            method: Detection method ('zscore' or 'iqr')
            threshold: Threshold for anomaly detection
        
        Returns:
            DataFrame containing only anomalous rows
        
        Example:
            >>> analyzer = DataAnalyzer(df)
            >>> anomalies = analyzer.detect_anomalies('value', method='zscore')
        """
        logger.info(f"Detecting anomalies in column '{column}' using {method}")
        
        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found")
        
        if not pd.api.types.is_numeric_dtype(self.df[column]):
            raise ValueError(f"Column '{column}' must be numeric")
        
        if method == "zscore":
            z_scores = np.abs((self.df[column] - self.df[column].mean()) / self.df[column].std())
            anomalies = self.df[z_scores > threshold]
        elif method == "iqr":
            Q1 = self.df[column].quantile(0.25)
            Q3 = self.df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            anomalies = self.df[(self.df[column] < lower_bound) | (self.df[column] > upper_bound)]
        else:
            raise ValueError(f"Invalid method: {method}. Choose 'zscore' or 'iqr'")
        
        logger.info(f"Found {len(anomalies)} anomalies")
        
        return anomalies
