Visualizer Module
=================

.. automodule:: data_analysis.visualizer
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

Class Overview
--------------

The ``Visualizer`` class creates publication-quality visualizations.

Features
--------

* Histograms with KDE overlays
* Box plots (grouped and ungrouped)
* Scatter plots with hue and size encoding
* Correlation heatmaps
* Line plots
* Bar plots (vertical and horizontal)
* Pair plots
* Count plots

Examples
--------

Creating Histograms
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from data_analysis import Visualizer

    viz = Visualizer(df)
    viz.create_histogram(
        column='age',
        bins=15,
        kde=True,
        title='Age Distribution'
    )

Creating Box Plots
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Grouped box plot
    viz.create_boxplot(
        column='salary',
        groupby='department',
        title='Salary by Department'
    )

Creating Scatter Plots
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Scatter with hue
    viz.create_scatter(
        x='age',
        y='salary',
        hue='department',
        title='Age vs Salary by Department'
    )

Creating Correlation Heatmaps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Correlation heatmap
    viz.create_correlation_heatmap(
        columns=['age', 'salary', 'experience'],
        annot=True,
        cmap='coolwarm'
    )

Creating Line Plots
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Line plot with multiple series
    viz.create_line_plot(
        x='date',
        y='sales',
        hue='region',
        title='Sales Over Time by Region'
    )

Creating Bar Plots
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Grouped bar plot
    viz.create_bar_plot(
        x='category',
        y='revenue',
        hue='region',
        title='Revenue by Category and Region'
    )

Creating Pair Plots
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Pair plot for multiple variables
    viz.create_pairplot(
        columns=['age', 'salary', 'experience'],
        hue='department'
    )

Saving Visualizations
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Save to file
    viz.create_histogram(
        column='age',
        save_path='outputs/visualizations/age_dist.png'
    )

API Documentation
-----------------

.. autoclass:: data_analysis.visualizer.Visualizer
   :members:
   :undoc-members:
   :show-inheritance:
