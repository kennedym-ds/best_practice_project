"""Data Cleaning Module.

This module provides utilities for cleaning and preprocessing data.
"""

import logging
from typing import List, Optional, Union

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class DataCleaner:
    """
    A class for cleaning and preprocessing data.

    This class demonstrates best practices for data cleaning including:
    - Handling missing values
    - Removing duplicates
    - Data type conversions
    - Outlier detection and handling
    - Feature engineering basics
    """

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Initialize the DataCleaner with a DataFrame.

        Args:
            df: The DataFrame to clean
        """
        self.df = df.copy()  # Create a copy to avoid modifying original
        logger.info(f"DataCleaner initialized with DataFrame shape: {self.df.shape}")

    def handle_missing_values(
        self,
        strategy: str = "drop",
        columns: Optional[List[str]] = None,
        fill_value: Optional[Union[str, int, float]] = None,
    ) -> pd.DataFrame:
        """
        Handle missing values in the DataFrame.

        Args:
            strategy: Strategy for handling missing values
                     ('drop', 'fill', 'ffill', 'bfill', 'mean', 'median')
            columns: List of columns to apply the strategy to.
                    If None, applies to all columns.
            fill_value: Value to use when strategy is 'fill'

        Returns:
            DataFrame with missing values handled

        Raises:
            ValueError: If an invalid strategy is provided

        Example:
            >>> cleaner = DataCleaner(df)
            >>> df_clean = cleaner.handle_missing_values(strategy='mean')
        """
        df = self.df.copy()

        if columns is None:
            columns = df.columns.tolist()

        initial_nulls = df[columns].isnull().sum().sum()
        logger.info(f"Found {initial_nulls} missing values in specified columns")

        if strategy == "drop":
            df = df.dropna(subset=columns)
        elif strategy == "fill":
            if fill_value is None:
                raise ValueError("fill_value must be provided when strategy is 'fill'")
            df[columns] = df[columns].fillna(fill_value)
        elif strategy == "ffill":
            df[columns] = df[columns].fillna(method="ffill")
        elif strategy == "bfill":
            df[columns] = df[columns].fillna(method="bfill")
        elif strategy == "mean":
            for col in columns:
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = df[col].fillna(df[col].mean())
                else:
                    logger.info(f"Skipping non-numeric column '{col}' for mean strategy")
        elif strategy == "median":
            for col in columns:
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = df[col].fillna(df[col].median())
                else:
                    logger.info(f"Skipping non-numeric column '{col}' for median strategy")
        else:
            raise ValueError(
                f"Invalid strategy: {strategy}. "
                "Choose from 'drop', 'fill', 'ffill', 'bfill', 'mean', 'median'"
            )

        final_nulls = df[columns].isnull().sum().sum()
        logger.info(f"Missing values reduced to {final_nulls}")

        self.df = df
        return self.df

    def remove_duplicates(
        self, subset: Optional[List[str]] = None, keep: str = "first"
    ) -> pd.DataFrame:
        """
        Remove duplicate rows from the DataFrame.

        Args:
            subset: List of columns to consider when identifying duplicates.
                   If None, uses all columns.
            keep: Which duplicates to keep ('first', 'last', False)

        Returns:
            DataFrame with duplicates removed

        Example:
            >>> cleaner = DataCleaner(df)
            >>> df_clean = cleaner.remove_duplicates()
        """
        initial_rows = len(self.df)
        self.df = self.df.drop_duplicates(subset=subset, keep=keep)
        removed_rows = initial_rows - len(self.df)

        logger.info(f"Removed {removed_rows} duplicate rows")
        return self.df

    def convert_dtypes(self, column_types: dict) -> pd.DataFrame:
        """
        Convert columns to specified data types.

        Args:
            column_types: Dictionary mapping column names to target dtypes

        Returns:
            DataFrame with converted dtypes

        Example:
            >>> cleaner = DataCleaner(df)
            >>> df_clean = cleaner.convert_dtypes({
            ...     'age': 'int64',
            ...     'price': 'float64',
            ...     'date': 'datetime64'
            ... })
        """
        for col, dtype in column_types.items():
            if col in self.df.columns:
                try:
                    if dtype == "datetime64":
                        self.df[col] = pd.to_datetime(self.df[col])
                    else:
                        self.df[col] = self.df[col].astype(dtype)
                    logger.info(f"Converted column '{col}' to {dtype}")
                except Exception as e:
                    logger.warning(f"Failed to convert column '{col}' to {dtype}: {e}")
            else:
                raise ValueError(f"Column '{col}' not found in DataFrame")

        return self.df

    def detect_outliers(
        self, column: str, method: str = "iqr", threshold: float = 1.5
    ) -> pd.Series:
        """
        Detect outliers in a numeric column.

        Args:
            column: Name of the column to check for outliers
            method: Method to use ('iqr' or 'zscore')
            threshold: Threshold for outlier detection
                      For IQR: multiplier of IQR (default 1.5)
                      For Z-score: number of standard deviations (default 3.0)

        Returns:
            Boolean Series indicating outlier rows

        Example:
            >>> cleaner = DataCleaner(df)
            >>> outliers = cleaner.detect_outliers('price', method='iqr')
        """
        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found in DataFrame")

        if not pd.api.types.is_numeric_dtype(self.df[column]):
            raise ValueError(f"Column '{column}' must be numeric")

        if method == "iqr":
            Q1 = self.df[column].quantile(0.25)
            Q3 = self.df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            outliers = (self.df[column] < lower_bound) | (self.df[column] > upper_bound)
        elif method == "zscore":
            z_scores = np.abs((self.df[column] - self.df[column].mean()) / self.df[column].std())
            outliers = z_scores > threshold
        else:
            raise ValueError(f"Invalid method: {method}. Choose 'iqr' or 'zscore'")

        outlier_count = outliers.sum()
        logger.info(f"Found {outlier_count} outliers in column '{column}' using {method} method")

        return outliers

    def remove_outliers(
        self, column: str, method: str = "iqr", threshold: float = 1.5
    ) -> pd.DataFrame:
        """
        Remove outliers from the DataFrame.

        Args:
            column: Name of the column to check for outliers
            method: Method to use ('iqr' or 'zscore')
            threshold: Threshold for outlier detection

        Returns:
            DataFrame with outliers removed

        Example:
            >>> cleaner = DataCleaner(df)
            >>> df_clean = cleaner.remove_outliers('price')
        """
        outliers = self.detect_outliers(column, method, threshold)
        initial_rows = len(self.df)
        self.df = self.df[~outliers]
        removed_rows = initial_rows - len(self.df)

        logger.info(f"Removed {removed_rows} outlier rows")
        return self.df

    def get_data(self) -> pd.DataFrame:
        """
        Get the current state of the DataFrame.

        Returns:
            The cleaned DataFrame
        """
        return self.df
