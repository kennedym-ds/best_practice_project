# Data Analysis Project

[![CI/CD](https://github.com/yourusername/best_practice_project/workflows/CI/CD/badge.svg)](https://github.com/yourusername/best_practice_project/actions)
[![codecov](https://codecov.io/gh/yourusername/best_practice_project/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/best_practice_project)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive Python data analysis project demonstrating best practices in software engineering, testing, documentation, and CI/CD workflows.

## ✨ Features

- **🔄 Data Loading**: Support for multiple formats (CSV, Excel, JSON)
- **🧹 Data Cleaning**: Handle missing values, duplicates, and outliers
- **📊 Statistical Analysis**: Summary statistics, correlations, regression analysis
- **📈 Visualization**: Create publication-quality charts and plots
- **🧪 Comprehensive Testing**: Unit and integration tests with >90% coverage
- **🔒 Type Safety**: Full type hints with mypy strict checking
- **📚 Documentation**: Detailed guides and API documentation
- **🚀 CI/CD Pipeline**: Automated testing, linting, and deployment

## 🎯 Quick Start

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/best_practice_project.git
   cd best_practice_project
   ```

2. **Create and activate a virtual environment**:

   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Unix/MacOS
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install the package**:

   ```bash
   # For users
   pip install -e .

   # For developers (includes testing and documentation tools)
   pip install -e ".[dev,docs,test]"
   ```

### Basic Usage

```python
from data_analysis import DataLoader, DataCleaner, DataAnalyzer, Visualizer

# Load data
loader = DataLoader()
df = loader.load_csv('data/raw/employees.csv')

# Clean data
cleaner = DataCleaner(df)
cleaner.handle_missing_values(strategy='drop')
cleaner.remove_duplicates()
clean_df = cleaner.get_data()

# Analyze data
analyzer = DataAnalyzer(clean_df)
summary = analyzer.get_summary_statistics()
correlations = analyzer.get_correlation_matrix()

# Visualize data
visualizer = Visualizer(clean_df)
visualizer.create_histogram('salary', bins=10, kde=True)
visualizer.create_correlation_heatmap()
```

## 📖 Documentation

### User Guides

- [Installation Guide](docs/guides/installation.md) - Detailed setup instructions
- [User Guide](docs/guides/user_guide.md) - Complete usage documentation
- [Git & GitHub Guide](docs/guides/git_github_guide.md) - Version control for beginners
- [Configuration Files Guide](docs/guides/configuration_files.md) - In-depth guide to all project configuration files

### Developer Guides

- [Contributing Guide](CONTRIBUTING.md) - How to contribute to this project
- [API Reference](docs/api/index.html) - Full API documentation

### Examples

- [Example Notebook](notebooks/example_analysis.ipynb) - Complete analysis workflow

## 🏗️ Project Structure

```text
best_practice_project/
├── .github/
│   └── workflows/
│       └── ci.yml              # CI/CD pipeline configuration
├── data/
│   ├── raw/                    # Raw data files
│   └── processed/              # Processed data files
├── docs/
│   ├── api/                    # API documentation
│   └── guides/                 # User and developer guides
├── notebooks/
│   └── example_analysis.ipynb  # Example Jupyter notebook
├── outputs/
│   └── visualizations/         # Generated plots and charts
├── src/
│   └── data_analysis/          # Main package
│       ├── __init__.py
│       ├── data_loader.py      # Data loading utilities
│       ├── data_cleaner.py     # Data cleaning functions
│       ├── data_analyzer.py    # Statistical analysis
│       └── visualizer.py       # Visualization tools
├── tests/
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   └── conftest.py             # Shared test fixtures
├── .editorconfig               # Editor configuration
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
├── .pre-commit-config.yaml     # Pre-commit hooks
├── LICENSE                     # MIT License
├── Makefile                    # Common development commands
├── pyproject.toml              # Project configuration
├── README.md                   # This file
├── requirements.txt            # Production dependencies
└── requirements-dev.txt        # Development dependencies
```

## 🔧 Development

### Setting Up Development Environment

```bash
# Install development dependencies
pip install -e ".[dev,docs,test]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/data_analysis --cov-report=html

# Run specific test file
pytest tests/unit/test_data_loader.py

# Run with verbose output
pytest -v
```

### Code Quality

```text
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
flake8 src/ tests/

# Type check
mypy src/data_analysis/

# Run all checks
make all
```

### Documentation Linting

Markdown documentation is linted using `markdownlint-cli2`:

```bash
# Install markdownlint globally (one-time setup)
npm install -g markdownlint-cli2

# Lint all project documentation
markdownlint-cli2 "*.md" "docs/**/*.md"

# Lint specific file
markdownlint-cli2 README.md
```

Configuration is in `.markdownlint.json` with rules for:

- Line length (400 chars for documentation)
- Code block language specification
- Consistent list and emphasis styles
- Proper spacing around headings and lists

### Using Makefile

The project includes a `Makefile` for common tasks:

```text
make help           # Show all available commands
make install        # Install package
make install-dev    # Install with dev dependencies
make test           # Run tests
make coverage       # Run tests with coverage
make lint           # Run all linters
make format         # Format code
make type-check     # Run type checker
make docs           # Build documentation
make clean          # Clean generated files
make all            # Run format, lint, type-check, and test
```

## 🧪 Testing Strategy

This project maintains high code quality through comprehensive testing:

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions and workflows
- **Coverage Target**: >90% code coverage
- **Continuous Testing**: Automated tests on every push via GitHub Actions

### Test Structure

```text
tests/
├── unit/
│   ├── test_data_loader.py     # DataLoader tests
│   ├── test_data_cleaner.py    # DataCleaner tests
│   ├── test_data_analyzer.py   # DataAnalyzer tests
│   └── test_visualizer.py      # Visualizer tests
├── integration/
│   └── test_pipeline.py        # End-to-end pipeline tests
└── conftest.py                 # Shared fixtures and configuration
```

## 🚀 CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment:

- **Multi-OS Testing**: Ubuntu, Windows, macOS
- **Multi-Python Testing**: Python 3.9, 3.10, 3.11, 3.12
- **Quality Checks**: Linting, type checking, security scanning
- **Code Coverage**: Automatic coverage reporting with Codecov
- **Documentation**: Automated documentation builds
- **Package Building**: Verify package can be built and distributed

## 📊 Modules Overview

### DataLoader

Load data from various file formats:

- CSV files with customizable parsing options
- Excel files with sheet selection
- JSON files with nested data support
- Automatic data type inference

### DataCleaner

Clean and prepare data for analysis:

- Handle missing values (drop, fill, interpolate)
- Remove duplicate records
- Convert data types
- Detect and remove outliers (Z-score, IQR methods)

### DataAnalyzer

Perform statistical analysis:

- Summary statistics with skewness and kurtosis
- Missing value reports
- Correlation analysis (Pearson, Spearman, Kendall)
- Group-based analysis with aggregations
- Simple linear regression
- Anomaly detection

### Visualizer

Create publication-quality visualizations:

- Histograms with KDE overlays
- Box plots with grouping
- Scatter plots with hue and size encoding
- Correlation heatmaps
- Line plots for time series
- Bar plots for categorical comparisons
- Pair plots for multivariate analysis
- Count plots for categorical distributions

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:

- Setting up your development environment
- Our coding standards and guidelines
- The pull request process
- Running tests and quality checks

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/), and [Matplotlib](https://matplotlib.org/)
- Testing with [pytest](https://pytest.org/)
- Documentation with [Sphinx](https://www.sphinx-doc.org/)
- CI/CD with [GitHub Actions](https://github.com/features/actions)

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/best_practice_project/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/best_practice_project/discussions)
- **Documentation**: [Read the Docs](https://best-practice-project.readthedocs.io)

## 🗺️ Roadmap

- [ ] Add support for SQL databases
- [ ] Implement advanced ML models
- [ ] Add interactive visualizations with Plotly
- [ ] Create web dashboard with Streamlit
- [ ] Add data validation with Pydantic
- [ ] Support for big data with Dask

---

Made with ❤️ by the Data Analysis Project Team
