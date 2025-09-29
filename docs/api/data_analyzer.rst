DataAnalyzer Module
===================

.. automodule:: data_analysis.data_analyzer
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

Class Overview
--------------

The ``DataAnalyzer`` class provides statistical analysis capabilities.

Features
--------

* Summary statistics with extended metrics
* Missing value analysis
* Correlation analysis (Pearson, Spearman, Kendall)
* Group-by analysis
* Linear regression
* Anomaly detection
* Value counts and distributions

Examples
--------

Summary Statistics
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from data_analysis import DataAnalyzer

    analyzer = DataAnalyzer(df)
    summary = analyzer.get_summary_statistics()
    print(summary)

Correlation Analysis
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Get correlation matrix
    corr_matrix = analyzer.get_correlation_matrix(method='pearson')

    # Find high correlations
    high_corr = analyzer.find_high_correlations(threshold=0.7)

Group Analysis
~~~~~~~~~~~~~~

.. code-block:: python

    # Analyze by department
    dept_stats = analyzer.group_analysis(
        group_column='department',
        agg_columns=['salary', 'age'],
        agg_funcs=['mean', 'median', 'std']
    )

Linear Regression
~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Perform simple linear regression
    slope, intercept, r_squared = analyzer.simple_linear_regression(
        x='age',
        y='salary'
    )
    print(f"R² Score: {r_squared:.4f}")

Anomaly Detection
~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Detect anomalies using Z-score
    anomaly_indices = analyzer.detect_anomalies(
        column='price',
        method='zscore',
        threshold=3.0
    )

    # Get anomaly records
    anomalies = df.loc[anomaly_indices]

API Documentation
-----------------

.. autoclass:: data_analysis.data_analyzer.DataAnalyzer
   :members:
   :undoc-members:
   :show-inheritance:
