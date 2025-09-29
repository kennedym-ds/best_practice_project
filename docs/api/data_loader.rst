DataLoader Module
================

.. automodule:: data_analysis.data_loader
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

Class Overview
--------------

The ``DataLoader`` class provides methods for loading and saving data in multiple formats.

Supported Formats
-----------------

* CSV files (``.csv``)
* Excel files (``.xlsx``, ``.xls``)
* JSON files (``.json``)

Examples
--------

Loading CSV Files
~~~~~~~~~~~~~~~~~

.. code-block:: python

    from data_analysis import DataLoader

    loader = DataLoader()
    df = loader.load_csv('data/raw/data.csv')

Loading Excel Files
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    loader = DataLoader()
    df = loader.load_excel('data/raw/report.xlsx', sheet_name='Sheet1')

Loading JSON Files
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    loader = DataLoader()
    df = loader.load_json('data/raw/records.json')

Saving Data
~~~~~~~~~~~

.. code-block:: python

    loader = DataLoader()
    loader.save_csv(df, 'data/processed/cleaned_data.csv')
    loader.save_excel(df, 'data/processed/report.xlsx')
    loader.save_json(df, 'data/processed/data.json')

API Documentation
-----------------

.. autoclass:: data_analysis.data_loader.DataLoader
   :members:
   :undoc-members:
   :show-inheritance:
