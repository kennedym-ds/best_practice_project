Welcome to Data Analysis Project Documentation
==============================================

A comprehensive Python toolkit for data analysis following best practices.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   guides/installation
   guides/user_guide
   guides/git_github_guide
   guides/configuration_files
   api/modules

Overview
--------

The Data Analysis Project provides a complete solution for:

* **Data Loading**: Read CSV, Excel, and JSON files
* **Data Cleaning**: Handle missing values, duplicates, and outliers
* **Data Analysis**: Statistical analysis and correlation studies
* **Visualization**: Create publication-quality plots

Features
--------

✨ Easy-to-use API with comprehensive documentation
🧪 >90% test coverage with unit and integration tests
🔄 CI/CD pipeline with GitHub Actions
📊 Multiple visualization types for data exploration
🔧 Flexible data cleaning strategies
📈 Statistical analysis capabilities
🎯 Type hints throughout for better IDE support
📝 Comprehensive guides and examples

Quick Start
-----------

Installation::

    pip install -e .

Basic Usage:

.. code-block:: python

    from data_analysis import DataLoader, DataCleaner, DataAnalyzer, Visualizer

    # Load data
    loader = DataLoader()
    df = loader.load_csv('data/raw/data.csv')

    # Clean data
    cleaner = DataCleaner(df)
    cleaned_df = cleaner.handle_missing_values().remove_duplicates().get_data()

    # Analyze data
    analyzer = DataAnalyzer(cleaned_df)
    summary = analyzer.get_summary_statistics()

    # Visualize data
    viz = Visualizer(cleaned_df)
    viz.create_histogram(column='age')

Guides
------

* :doc:`guides/installation` - Installation instructions for all platforms
* :doc:`guides/user_guide` - Comprehensive usage guide
* :doc:`guides/git_github_guide` - Git and GitHub tutorial for beginners
* :doc:`guides/configuration_files` - Detailed explanation of all configuration files

API Reference
-------------

* :doc:`api/modules` - Complete API documentation

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
