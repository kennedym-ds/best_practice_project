# User Guide

Complete guide to using the Data Analysis Project for data loading, cleaning, analysis, and visualization.

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [DataLoader Module](#dataloader-module)
4. [DataCleaner Module](#datacleaner-module)
5. [DataAnalyzer Module](#dataanalyzer-module)
6. [Visualizer Module](#visualizer-module)
7. [Complete Workflow Example](#complete-workflow-example)
8. [Best Practices](#best-practices)
9. [Tips and Tricks](#tips-and-tricks)

## Introduction

The Data Analysis Project provides a comprehensive toolkit for working with data in Python. It simplifies common tasks and follows best practices for data analysis workflows.

### Key Benefits

- **Easy to use**: Simple, intuitive API
- **Comprehensive**: Covers the entire analysis pipeline
- **Flexible**: Supports multiple data formats and methods
- **Well-tested**: >90% code coverage
- **Type-safe**: Full type hints for better IDE support

## Getting Started

### Installation

See the [Installation Guide](installation.md) for detailed instructions.

Quick start:

```bash
pip install -e .
```

### Basic Import

```python
from data_analysis import DataLoader, DataCleaner, DataAnalyzer, Visualizer
import pandas as pd
```

## DataLoader Module

The `DataLoader` class handles loading and saving data in multiple formats.

### Supported Formats

- CSV files (`.csv`)
- Excel files (`.xlsx`, `.xls`)
- JSON files (`.json`)

### Loading Data

#### Loading CSV Files

```python
from data_analysis import DataLoader

loader = DataLoader()

# Basic CSV loading
df = loader.load_csv('data/raw/employees.csv')

# With custom delimiter
df = loader.load_csv('data/raw/data.tsv', delimiter='\t')

# With specific data types
df = loader.load_csv(
    'data/raw/sales.csv',
    dtype={'product_id': str, 'price': float}
)

# Parse date columns
df = loader.load_csv(
    'data/raw/logs.csv',
    parse_dates=['timestamp', 'created_at']
)
```

#### Loading Excel Files

```python
# Load first sheet (default)
df = loader.load_excel('data/raw/report.xlsx')

# Load specific sheet
df = loader.load_excel('data/raw/report.xlsx', sheet_name='Sheet2')

# Load multiple sheets
dfs = loader.load_excel('data/raw/report.xlsx', sheet_name=None)
# Returns dict: {'Sheet1': df1, 'Sheet2': df2, ...}
```

#### Loading JSON Files

```python
# Load JSON array
df = loader.load_json('data/raw/records.json')

# Load nested JSON
df = loader.load_json('data/raw/nested_data.json')

# Load with specific orientation
df = loader.load_json('data/raw/data.json', orient='records')
```

### Saving Data

#### Saving CSV Files

```python
# Basic save
loader.save_csv(df, 'data/processed/cleaned_data.csv')

# Without index
loader.save_csv(df, 'data/processed/output.csv', index=False)

# With custom delimiter
loader.save_csv(df, 'data/processed/data.tsv', sep='\t')
```

#### Saving Excel Files

```python
# Basic save
loader.save_excel(df, 'data/processed/report.xlsx')

# With custom sheet name
loader.save_excel(df, 'data/processed/report.xlsx', sheet_name='Results')

# Without index
loader.save_excel(df, 'data/processed/output.xlsx', index=False)
```

#### Saving JSON Files

```python
# Basic save
loader.save_json(df, 'data/processed/output.json')

# With specific orientation
loader.save_json(df, 'data/processed/records.json', orient='records')

# With indentation for readability
loader.save_json(df, 'data/processed/data.json', indent=2)
```

## DataCleaner Module

The `DataCleaner` class provides methods for cleaning and preparing data.

### Creating a Cleaner

```python
from data_analysis import DataCleaner

# Create cleaner with DataFrame
cleaner = DataCleaner(df)
```

### Handling Missing Values

```python
# Drop rows with any missing values
cleaner.handle_missing_values(strategy='drop')

# Drop rows where all values are missing
cleaner.handle_missing_values(strategy='drop', how='all')

# Fill with constant value
cleaner.handle_missing_values(strategy='constant', fill_value=0)

# Fill with column mean
cleaner.handle_missing_values(strategy='mean', columns=['age', 'salary'])

# Fill with column median
cleaner.handle_missing_values(strategy='median')

# Forward fill (use previous value)
cleaner.handle_missing_values(strategy='forward_fill')

# Backward fill (use next value)
cleaner.handle_missing_values(strategy='backward_fill')

# Interpolate values
cleaner.handle_missing_values(strategy='interpolate')
```

### Removing Duplicates

```python
# Remove all duplicate rows
cleaner.remove_duplicates()

# Remove duplicates based on specific columns
cleaner.remove_duplicates(subset=['id', 'date'])

# Keep last occurrence instead of first
cleaner.remove_duplicates(keep='last')
```

### Converting Data Types

```python
# Convert single column
cleaner.convert_dtypes({'age': 'int64'})

# Convert multiple columns
cleaner.convert_dtypes({
    'age': 'int64',
    'salary': 'float64',
    'hire_date': 'datetime64[ns]',
    'department': 'category'
})

# Common conversions
cleaner.convert_dtypes({
    'price': 'float64',           # Numeric
    'quantity': 'int32',           # Integer
    'date': 'datetime64[ns]',      # Date/Time
    'category': 'category',        # Categorical
    'is_active': 'bool'            # Boolean
})
```

### Detecting Outliers

```python
# Detect outliers using Z-score method
outlier_indices = cleaner.detect_outliers(
    column='salary',
    method='zscore',
    threshold=3.0
)

# Detect outliers using IQR method
outlier_indices = cleaner.detect_outliers(
    column='price',
    method='iqr',
    multiplier=1.5
)

print(f"Found {len(outlier_indices)} outliers")
```

### Removing Outliers

```python
# Remove outliers using Z-score
cleaner.remove_outliers(
    column='salary',
    method='zscore',
    threshold=3.0
)

# Remove outliers using IQR
cleaner.remove_outliers(
    column='price',
    method='iqr',
    multiplier=1.5
)
```

### Method Chaining

DataCleaner supports method chaining for compact code:

```python
cleaner = DataCleaner(df)
cleaned_df = (cleaner
    .handle_missing_values(strategy='mean')
    .remove_duplicates()
    .convert_dtypes({'date': 'datetime64[ns]'})
    .remove_outliers(column='salary', method='zscore')
    .get_data()
)
```

### Getting Cleaned Data

```python
# Get cleaned DataFrame
cleaned_df = cleaner.get_data()
```

## DataAnalyzer Module

The `DataAnalyzer` class provides statistical analysis capabilities.

### Creating an Analyzer

```python
from data_analysis import DataAnalyzer

analyzer = DataAnalyzer(df)
```

### Summary Statistics

```python
# Get comprehensive summary statistics
summary = analyzer.get_summary_statistics()
# Returns: count, mean, std, min, 25%, 50%, 75%, max, skewness, kurtosis

# For specific columns only
summary = analyzer.get_summary_statistics(columns=['age', 'salary'])
```

### Missing Value Analysis

```python
# Get missing value report
missing_report = analyzer.get_missing_value_report()
# Returns DataFrame with: missing_count, missing_percentage, data_type

# Check specific columns
missing_report = analyzer.get_missing_value_report(columns=['age', 'email'])
```

### Correlation Analysis

```python
# Get correlation matrix (Pearson)
corr_matrix = analyzer.get_correlation_matrix()

# Use different methods
corr_pearson = analyzer.get_correlation_matrix(method='pearson')
corr_spearman = analyzer.get_correlation_matrix(method='spearman')
corr_kendall = analyzer.get_correlation_matrix(method='kendall')

# For specific columns only
corr_matrix = analyzer.get_correlation_matrix(columns=['age', 'salary', 'score'])
```

### Finding High Correlations

```python
# Find correlations above threshold
high_corr = analyzer.find_high_correlations(threshold=0.7)
# Returns list of tuples: [(col1, col2, correlation), ...]

# Adjust threshold
strong_corr = analyzer.find_high_correlations(threshold=0.9)
```

### Group Analysis

```python
# Analyze by single column
dept_stats = analyzer.group_analysis(
    group_column='department',
    agg_columns=['salary', 'age'],
    agg_funcs=['mean', 'median', 'std']
)

# Multiple aggregation functions
region_stats = analyzer.group_analysis(
    group_column='region',
    agg_columns=['sales', 'profit'],
    agg_funcs=['sum', 'mean', 'min', 'max', 'count']
)
```

### Linear Regression

```python
# Simple linear regression
slope, intercept, r_squared = analyzer.simple_linear_regression(
    x='age',
    y='salary'
)

print(f"Slope: {slope:.2f}")
print(f"Intercept: {intercept:.2f}")
print(f"R² Score: {r_squared:.4f}")
```

### Value Counts

```python
# Get value counts for categorical column
counts = analyzer.get_value_counts(column='department')

# As percentages
percentages = analyzer.get_value_counts(
    column='category',
    normalize=True
)

# Top N values
top_10 = analyzer.get_value_counts(
    column='product',
    top_n=10
)
```

### Anomaly Detection

```python
# Detect anomalies using Z-score method
anomaly_indices = analyzer.detect_anomalies(
    column='price',
    method='zscore',
    threshold=3.0
)

# Using IQR method
anomaly_indices = analyzer.detect_anomalies(
    column='sales',
    method='iqr'
)

# Get anomaly records
anomalies = df.loc[anomaly_indices]
```

## Visualizer Module

The `Visualizer` class creates publication-quality visualizations.

### Creating a Visualizer

```python
from data_analysis import Visualizer

viz = Visualizer(df)
```

### Histograms

```python
# Basic histogram
viz.create_histogram(column='age')

# With custom bins and KDE overlay
viz.create_histogram(
    column='salary',
    bins=20,
    kde=True,
    title='Salary Distribution',
    xlabel='Salary ($)',
    ylabel='Frequency',
    color='skyblue'
)

# Save to file
viz.create_histogram(
    column='age',
    bins=15,
    save_path='outputs/visualizations/age_dist.png'
)
```

### Box Plots

```python
# Basic box plot
viz.create_boxplot(column='salary')

# Grouped by category
viz.create_boxplot(
    column='salary',
    groupby='department',
    title='Salary by Department',
    ylabel='Salary ($)'
)

# Horizontal orientation
viz.create_boxplot(
    column='score',
    horizontal=True
)
```

### Scatter Plots

```python
# Basic scatter plot
viz.create_scatter(x='age', y='salary')

# With hue (color by category)
viz.create_scatter(
    x='age',
    y='salary',
    title='Age vs Salary by Department',
    xlabel='Age',
    ylabel='Salary ($)',
    hue='department'
)

# With size encoding
viz.create_scatter(
    x='price',
    y='sales',
    size='profit',
    hue='region'
)
```

### Correlation Heatmaps

```python
# Basic heatmap
viz.create_correlation_heatmap()

# With specific columns
viz.create_correlation_heatmap(
    columns=['age', 'salary', 'experience', 'performance'],
    title='Employee Metrics Correlation',
    annot=True,  # Show correlation values
    cmap='coolwarm'  # Color scheme
)

# Save to file
viz.create_correlation_heatmap(
    annot=True,
    save_path='outputs/visualizations/correlation.png'
)
```

### Line Plots

```python
# Basic line plot
viz.create_line_plot(x='date', y='sales')

# Multiple lines with hue
viz.create_line_plot(
    x='month',
    y='revenue',
    title='Monthly Revenue by Region',
    xlabel='Month',
    ylabel='Revenue ($)',
    hue='region'
)

# With markers
viz.create_line_plot(
    x='date',
    y='temperature',
    marker='o'
)
```

### Bar Plots

```python
# Basic bar plot
viz.create_bar_plot(x='category', y='sales')

# Grouped bar plot
viz.create_bar_plot(
    x='product',
    y='revenue',
    title='Revenue by Product and Region',
    xlabel='Product',
    ylabel='Revenue ($)',
    hue='region'
)

# Horizontal bar plot
viz.create_bar_plot(
    x='department',
    y='headcount',
    horizontal=True
)
```

### Pair Plots

```python
# Basic pair plot (all numeric columns)
viz.create_pairplot()

# With specific columns and hue
viz.create_pairplot(
    columns=['age', 'salary', 'experience'],
    hue='department',
    title='Employee Metrics Relationships'
)

# Customize diagonal plots
viz.create_pairplot(
    columns=['price', 'sales', 'profit'],
    hue='category',
    diag_kind='kde'  # or 'hist'
)
```

### Count Plots

```python
# Basic count plot
viz.create_countplot(column='department')

# Grouped count plot
viz.create_countplot(
    column='product_category',
    title='Product Distribution by Region',
    xlabel='Category',
    ylabel='Count',
    hue='region'
)

# Horizontal count plot
viz.create_countplot(
    column='status',
    horizontal=True
)
```

## Complete Workflow Example

Here's a complete example combining all modules:

```python
from data_analysis import DataLoader, DataCleaner, DataAnalyzer, Visualizer
from pathlib import Path

# 1. Load Data
print("Loading data...")
loader = DataLoader()
df = loader.load_csv('data/raw/employees.csv')
print(f"Loaded {len(df)} records")

# 2. Clean Data
print("\nCleaning data...")
cleaner = DataCleaner(df)
cleaned_df = (cleaner
    .convert_dtypes({'hire_date': 'datetime64[ns]'})
    .handle_missing_values(strategy='mean')
    .remove_duplicates()
    .remove_outliers(column='salary', method='zscore', threshold=3.0)
    .get_data()
)
print(f"After cleaning: {len(cleaned_df)} records")

# 3. Analyze Data
print("\nAnalyzing data...")
analyzer = DataAnalyzer(cleaned_df)

# Summary statistics
summary = analyzer.get_summary_statistics()
print("\nSummary Statistics:")
print(summary)

# Group analysis
dept_analysis = analyzer.group_analysis(
    group_column='department',
    agg_columns=['salary', 'age'],
    agg_funcs=['mean', 'median', 'count']
)
print("\nDepartment Analysis:")
print(dept_analysis)

# Correlation analysis
corr_matrix = analyzer.get_correlation_matrix(
    columns=['age', 'salary', 'performance_score']
)
print("\nCorrelations:")
print(corr_matrix)

# Find high correlations
high_corr = analyzer.find_high_correlations(threshold=0.7)
print(f"\nHigh correlations: {high_corr}")

# 4. Visualize Data
print("\nCreating visualizations...")
viz = Visualizer(cleaned_df)
output_dir = Path('outputs/visualizations')
output_dir.mkdir(parents=True, exist_ok=True)

# Salary distribution
viz.create_histogram(
    column='salary',
    bins=15,
    kde=True,
    title='Salary Distribution',
    save_path=output_dir / 'salary_dist.png'
)

# Salary by department
viz.create_boxplot(
    column='salary',
    groupby='department',
    title='Salary by Department',
    save_path=output_dir / 'salary_by_dept.png'
)

# Age vs Salary
viz.create_scatter(
    x='age',
    y='salary',
    hue='department',
    title='Age vs Salary by Department',
    save_path=output_dir / 'age_vs_salary.png'
)

# Correlation heatmap
viz.create_correlation_heatmap(
    columns=['age', 'salary', 'performance_score'],
    annot=True,
    title='Metrics Correlation',
    save_path=output_dir / 'correlation_heatmap.png'
)

# 5. Save Results
print("\nSaving results...")
output_data_dir = Path('data/processed')
output_data_dir.mkdir(parents=True, exist_ok=True)

loader.save_csv(cleaned_df, output_data_dir / 'employees_cleaned.csv')
loader.save_csv(dept_analysis, output_data_dir / 'department_analysis.csv')

print("\n✅ Analysis complete! Check outputs/ folder for visualizations.")
```

## Best Practices

### Data Loading

1. **Always specify data types** when possible:
   ```python
   df = loader.load_csv(
       'data.csv',
       dtype={'id': str, 'amount': float}
   )
   ```

2. **Parse dates explicitly**:
   ```python
   df = loader.load_csv('data.csv', parse_dates=['created_at', 'updated_at'])
   ```

3. **Handle large files efficiently**:
   ```python
   # Load in chunks for large files
   chunks = pd.read_csv('large_file.csv', chunksize=10000)
   for chunk in chunks:
       process_chunk(chunk)
   ```

### Data Cleaning

1. **Understand your data first**:
   ```python
   # Check data before cleaning
   print(df.info())
   print(df.describe())
   print(df.isnull().sum())
   ```

2. **Clean in the right order**:
   - Remove duplicates first
   - Handle missing values
   - Convert data types
   - Remove outliers last

3. **Document your cleaning decisions**:
   ```python
   # Good: Clear reasoning
   cleaner.handle_missing_values(strategy='median')  # Using median due to skewed distribution
   ```

### Data Analysis

1. **Check for data quality issues**:
   ```python
   # Check missing values
   missing_report = analyzer.get_missing_value_report()
   if missing_report['missing_percentage'].max() > 10:
       print("Warning: High missing value percentage")
   ```

2. **Validate correlations**:
   ```python
   # Check for multicollinearity
   high_corr = analyzer.find_high_correlations(threshold=0.9)
   if high_corr:
       print(f"Warning: High correlations found: {high_corr}")
   ```

3. **Use appropriate statistical methods**:
   ```python
   # Pearson for linear relationships
   corr_pearson = analyzer.get_correlation_matrix(method='pearson')
   
   # Spearman for monotonic relationships
   corr_spearman = analyzer.get_correlation_matrix(method='spearman')
   ```

### Visualization

1. **Choose the right plot type**:
   - Histogram: Distribution of single variable
   - Box plot: Distribution with outliers
   - Scatter: Relationship between two variables
   - Line plot: Trends over time
   - Bar plot: Comparisons between categories
   - Heatmap: Multiple correlations

2. **Always add labels and titles**:
   ```python
   viz.create_scatter(
       x='age',
       y='salary',
       title='Age vs Salary Analysis',  # Clear title
       xlabel='Age (years)',            # Units included
       ylabel='Salary ($)'              # Units included
   )
   ```

3. **Save high-resolution plots**:
   ```python
   import matplotlib.pyplot as plt
   
   viz.create_histogram(column='price')
   plt.savefig('output.png', dpi=300, bbox_inches='tight')
   ```

## Tips and Tricks

### Performance Tips

1. **Use appropriate data types**:
   ```python
   # Categorical data
   cleaner.convert_dtypes({'category': 'category'})  # Saves memory
   ```

2. **Filter early**:
   ```python
   # Filter before analysis
   df_filtered = df[df['date'] > '2023-01-01']
   analyzer = DataAnalyzer(df_filtered)
   ```

3. **Avoid copying DataFrames**:
   ```python
   # DataCleaner modifies in place by default
   cleaner = DataCleaner(df)
   cleaner.remove_duplicates()  # df is modified
   ```

### Common Patterns

1. **Creating analysis pipelines**:
   ```python
   def analyze_dataset(file_path):
       loader = DataLoader()
       df = loader.load_csv(file_path)
       
       cleaner = DataCleaner(df)
       cleaned_df = cleaner.handle_missing_values().remove_duplicates().get_data()
       
       analyzer = DataAnalyzer(cleaned_df)
       return analyzer.get_summary_statistics()
   ```

2. **Batch visualization**:
   ```python
   columns_to_plot = ['age', 'salary', 'experience']
   for col in columns_to_plot:
       viz.create_histogram(
           column=col,
           save_path=f'outputs/{col}_dist.png'
       )
   ```

3. **Comparing groups**:
   ```python
   for group in df['department'].unique():
       group_df = df[df['department'] == group]
       viz_group = Visualizer(group_df)
       viz_group.create_histogram(
           column='salary',
           title=f'Salary Distribution - {group}',
           save_path=f'outputs/salary_{group}.png'
       )
   ```

### Debugging Tips

1. **Check data at each step**:
   ```python
   print(f"Original shape: {df.shape}")
   cleaner = DataCleaner(df)
   cleaner.remove_duplicates()
   print(f"After deduplication: {cleaner.df.shape}")
   ```

2. **Inspect problematic records**:
   ```python
   # Find rows with missing values
   missing_rows = df[df.isnull().any(axis=1)]
   print(missing_rows)
   
   # Find outliers
   outliers = analyzer.detect_anomalies(column='price', method='zscore')
   print(df.loc[outliers])
   ```

3. **Validate outputs**:
   ```python
   # After cleaning
   assert cleaner.df.duplicated().sum() == 0, "Duplicates still present!"
   assert cleaner.df.isnull().sum().sum() == 0, "Missing values remain!"
   ```

---

For more examples, see the [Example Notebook](../../notebooks/example_analysis.ipynb).

For installation help, see the [Installation Guide](installation.md).

For contributing, see the [Contributing Guide](../../CONTRIBUTING.md).
