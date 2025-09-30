"""Data Loading Module.

This module provides utilities for loading data from various sources.
"""

import logging
from pathlib import Path
from typing import Optional, Union

import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logger = logging.getLogger(__name__)


class DataLoader:
    """
    A class for loading data from various file formats.

    This class demonstrates best practices for data loading including:
    - Type hints for better code clarity
    - Comprehensive error handling
    - Logging for debugging
    - Support for multiple file formats
    - Configurable options
    """

    def __init__(self, data_dir: Optional[Union[str, Path]] = None) -> None:
        """
        Initialize the DataLoader.

        Args:
            data_dir: Directory containing data files.
                     Defaults to 'data/raw' if not specified.
        """
        if data_dir is None:
            self.data_dir = Path("data/raw")
        else:
            self.data_dir = Path(data_dir)

        # Create the directory if it doesn't exist
        self.data_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"DataLoader initialized with data directory: {self.data_dir}")

    def load_csv(self, filename: str, **kwargs: dict) -> pd.DataFrame:
        """
        Load data from a CSV file.

        Args:
            filename: Name of the CSV file to load
            **kwargs: Additional arguments to pass to pandas.read_csv()

        Returns:
            DataFrame containing the loaded data

        Raises:
            FileNotFoundError: If the file doesn't exist
            pd.errors.ParserError: If the CSV file is malformed

        Example:
            >>> loader = DataLoader()
            >>> df = loader.load_csv('sample_data.csv')
        """
        filepath = self.data_dir / filename

        try:
            logger.info(f"Loading CSV file: {filepath}")
            df = pd.read_csv(filepath, **kwargs)
            logger.info(f"Successfully loaded {len(df)} rows and {len(df.columns)} columns")
            return df
        except FileNotFoundError:
            logger.error(f"File not found: {filepath}")
            raise
        except pd.errors.ParserError:
            logger.error(f"Error parsing CSV file: {filepath}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error loading CSV: {e}")
            raise

    def load_excel(
        self, filename: str, sheet_name: Union[str, int] = 0, **kwargs: dict
    ) -> pd.DataFrame:
        """
        Load data from an Excel file.

        Args:
            filename: Name of the Excel file to load
            sheet_name: Name or index of the sheet to load (default: 0)
            **kwargs: Additional arguments to pass to pandas.read_excel()

        Returns:
            DataFrame containing the loaded data

        Raises:
            FileNotFoundError: If the file doesn't exist
        """
        filepath = self.data_dir / filename

        try:
            logger.info(f"Loading Excel file: {filepath}, sheet: {sheet_name}")
            df = pd.read_excel(filepath, sheet_name=sheet_name, **kwargs)
            logger.info(f"Successfully loaded {len(df)} rows and {len(df.columns)} columns")
            return df
        except FileNotFoundError:
            logger.error(f"File not found: {filepath}")
            raise
        except Exception as e:
            logger.error(f"Error loading Excel file: {e}")
            raise

    def load_json(self, filename: str, **kwargs: dict) -> pd.DataFrame:
        """
        Load data from a JSON file.

        Args:
            filename: Name of the JSON file to load
            **kwargs: Additional arguments to pass to pandas.read_json()

        Returns:
            DataFrame containing the loaded data

        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the JSON file is malformed
        """
        filepath = self.data_dir / filename

        try:
            logger.info(f"Loading JSON file: {filepath}")
            df = pd.read_json(filepath, **kwargs)
            logger.info(f"Successfully loaded {len(df)} rows and {len(df.columns)} columns")
            return df
        except FileNotFoundError:
            logger.error(f"File not found: {filepath}")
            raise
        except ValueError:
            logger.error(f"Error parsing JSON file: {filepath}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error loading JSON: {e}")
            raise

    def save_csv(
        self,
        df: pd.DataFrame,
        filename: str,
        output_dir: Optional[Union[str, Path]] = None,
        **kwargs: dict,
    ) -> Path:
        """
        Save a DataFrame to a CSV file.

        Args:
            df: DataFrame to save
            filename: Name of the output file
            output_dir: Directory to save the file.
                       Defaults to 'data/processed' if not specified.
            **kwargs: Additional arguments to pass to DataFrame.to_csv()

        Returns:
            Path to the saved file

        Example:
            >>> loader = DataLoader()
            >>> path = loader.save_csv(df, 'processed_data.csv')
        """
        if output_dir is None:
            output_path = Path("data/processed")
        else:
            output_path = Path(output_dir)

        output_path.mkdir(parents=True, exist_ok=True)
        filepath = output_path / filename

        try:
            logger.info(f"Saving DataFrame to CSV: {filepath}")
            df.to_csv(filepath, index=False, **kwargs)
            logger.info(f"Successfully saved {len(df)} rows to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error saving CSV file: {e}")
            raise
