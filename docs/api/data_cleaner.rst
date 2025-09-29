DataCleaner Module
==================

.. automodule:: data_analysis.data_cleaner
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

Class Overview
--------------

The ``DataCleaner`` class provides methods for cleaning and preparing data.

Features
--------

* Handle missing values with multiple strategies
* Remove duplicate records
* Convert data types
* Detect and remove outliers
* Method chaining support

Examples
--------

Basic Cleaning
~~~~~~~~~~~~~~

.. code-block:: python

    from data_analysis import DataCleaner

    cleaner = DataCleaner(df)
    cleaner.handle_missing_values(strategy='mean')
    cleaner.remove_duplicates()
    cleaned_df = cleaner.get_data()

Method Chaining
~~~~~~~~~~~~~~~

.. code-block:: python

    cleaner = DataCleaner(df)
    cleaned_df = (cleaner
        .handle_missing_values(strategy='mean')
        .remove_duplicates()
        .convert_dtypes({'date': 'datetime64[ns]'})
        .remove_outliers(column='salary', method='zscore')
        .get_data()
    )

Missing Value Strategies
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Drop rows with missing values
    cleaner.handle_missing_values(strategy='drop')

    # Fill with mean
    cleaner.handle_missing_values(strategy='mean')

    # Fill with constant
    cleaner.handle_missing_values(strategy='constant', fill_value=0)

    # Forward fill
    cleaner.handle_missing_values(strategy='forward_fill')

Outlier Detection
~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Detect outliers using Z-score
    outlier_indices = cleaner.detect_outliers(
        column='price',
        method='zscore',
        threshold=3.0
    )

    # Remove outliers using IQR
    cleaner.remove_outliers(column='price', method='iqr')

API Documentation
-----------------

.. autoclass:: data_analysis.data_cleaner.DataCleaner
   :members:
   :undoc-members:
   :show-inheritance:
