"""Data Analysis Best Practices Package.

A comprehensive Python package demonstrating best practices for data analysis projects.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .data_analyzer import DataAnalyzer
from .data_cleaner import DataCleaner
from .data_loader import DataLoader
from .visualizer import Visualizer

__all__ = [
    "DataLoader",
    "DataCleaner",
    "DataAnalyzer",
    "Visualizer",
]
