"""
Shared pytest configuration and fixtures.
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for tests

import pytest

# Add src directory to path so tests can import modules
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture(autouse=True)
def reset_matplotlib():
    """Reset matplotlib settings between tests to avoid interference."""
    import matplotlib.pyplot as plt
    
    yield
    
    # Close all figures after each test
    plt.close('all')


@pytest.fixture
def suppress_logging():
    """Suppress logging output during tests."""
    import logging
    
    # Store original level
    original_level = logging.root.level
    
    # Suppress logging
    logging.root.setLevel(logging.CRITICAL)
    
    yield
    
    # Restore original level
    logging.root.setLevel(original_level)
