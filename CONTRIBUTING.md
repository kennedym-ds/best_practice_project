# Contributing to Data Analysis Project

Thank you for your interest in contributing to the Data Analysis Project! This document provides guidelines and instructions for contributing.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)

## 🤝 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for everyone. We expect all contributors to:

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/best_practice_project.git
cd best_practice_project

# Add the upstream repository
git remote add upstream https://github.com/ORIGINAL_OWNER/best_practice_project.git
```

### 2. Set Up Development Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Unix/MacOS:
source venv/bin/activate

# Install development dependencies
pip install -e ".[dev,docs,test]"

# Install pre-commit hooks
pre-commit install
```

### 3. Verify Installation

```bash
# Run tests to ensure everything works
pytest

# Run linters
make lint

# Check types
make type-check
```

## 🔄 Development Workflow

### 1. Create a Branch

Always create a new branch for your work:

```bash
# Update your main branch
git checkout main
git pull upstream main

# Create a new feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

### Branch Naming Conventions

- `feature/feature-name` - New features
- `fix/bug-description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring
- `test/description` - Test additions or modifications
- `chore/description` - Maintenance tasks

### 2. Make Changes

- Write clean, readable code
- Follow the coding standards (see below)
- Add tests for new functionality
- Update documentation as needed
- Keep commits focused and atomic

### 3. Test Your Changes

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_data_loader.py

# Run with coverage
pytest --cov=src/data_analysis --cov-report=html

# View coverage report
# Open htmlcov/index.html in your browser
```

### 4. Commit Your Changes

```bash
# Stage your changes
git add .

# Commit with a descriptive message
git commit -m "feat: add new data validation feature"

# Push to your fork
git push origin feature/your-feature-name
```

## 📏 Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some modifications:

- **Line Length**: Maximum 100 characters (configured in `pyproject.toml`)
- **Formatter**: Use Black for automatic formatting
- **Import Sorting**: Use isort with Black-compatible profile
- **Type Hints**: Required for all functions and methods
- **Docstrings**: Required for all public functions, classes, and methods (Google style)

### Code Formatting

```bash
# Format code with Black
black src/ tests/

# Sort imports with isort
isort src/ tests/

# Or use the Makefile
make format
```

### Type Hints

All functions must include type hints:

```python
from typing import Optional, List, Dict, Any
import pandas as pd

def process_data(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
    threshold: float = 0.5
) -> Dict[str, Any]:
    """
    Process data with specified parameters.

    Args:
        df: Input DataFrame to process
        columns: Optional list of columns to include
        threshold: Threshold value for processing

    Returns:
        Dictionary containing processed results

    Raises:
        ValueError: If DataFrame is empty
    """
    if df.empty:
        raise ValueError("DataFrame cannot be empty")
    # Implementation here
    return {"status": "success"}
```

### Docstring Style

Use Google-style docstrings:

```python
def example_function(param1: str, param2: int = 10) -> bool:
    """
    Brief description of the function.

    More detailed explanation if needed. This can span multiple
    lines and explain the function's behavior in detail.

    Args:
        param1: Description of param1
        param2: Description of param2 with default value

    Returns:
        Description of return value

    Raises:
        ValueError: When param1 is empty
        TypeError: When param2 is negative

    Examples:
        >>> example_function("test", 5)
        True
    """
    pass
```

## 🧪 Testing Guidelines

### Test Organization

- **Unit Tests**: Test individual functions/methods in isolation
  - Located in `tests/unit/`
  - Mock external dependencies
  - Fast execution

- **Integration Tests**: Test component interactions
  - Located in `tests/integration/`
  - Test real workflows
  - May be slower

### Writing Tests

```python
import pytest
import pandas as pd
from data_analysis import DataLoader

class TestDataLoader:
    """Test suite for DataLoader class."""

    @pytest.fixture
    def sample_df(self) -> pd.DataFrame:
        """Create sample DataFrame for testing."""
        return pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': ['a', 'b', 'c']
        })

    def test_load_csv_success(self, tmp_path, sample_df):
        """Test successful CSV loading."""
        # Arrange
        csv_file = tmp_path / "test.csv"
        sample_df.to_csv(csv_file, index=False)
        loader = DataLoader()

        # Act
        result = loader.load_csv(csv_file)

        # Assert
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 3
        assert list(result.columns) == ['col1', 'col2']

    def test_load_csv_file_not_found(self):
        """Test CSV loading with non-existent file."""
        loader = DataLoader()
        
        with pytest.raises(FileNotFoundError):
            loader.load_csv("nonexistent.csv")
```

### Test Coverage

- Maintain >90% test coverage
- Test both success and failure cases
- Test edge cases and boundary conditions
- Use parametrized tests for multiple scenarios

```python
@pytest.mark.parametrize("strategy,expected", [
    ("drop", 8),
    ("mean", 10),
    ("median", 10),
    ("forward_fill", 10),
])
def test_handle_missing_values(strategy, expected):
    """Test different missing value strategies."""
    # Test implementation
    pass
```

## 📚 Documentation

### Documentation Types

1. **Code Documentation**: Docstrings for all public APIs
2. **User Guides**: Step-by-step tutorials in `docs/guides/`
3. **API Reference**: Auto-generated from docstrings
4. **README**: Project overview and quick start

### Building Documentation

```bash
# Build HTML documentation
cd docs
make html

# View documentation
# Open docs/_build/html/index.html in browser

# Or use Makefile from root
make docs
```

### Documentation Standards

- Write clear, concise explanations
- Include code examples
- Add diagrams where helpful
- Keep documentation up-to-date with code changes

## 📝 Commit Messages

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks, dependency updates

### Examples

```bash
# Feature
feat(data_loader): add support for Parquet files

Implemented load_parquet and save_parquet methods with
automatic compression detection.

Closes #123

# Bug fix
fix(data_cleaner): correct outlier detection threshold

Changed IQR multiplier from 1.5 to 1.0 to match documentation.

Fixes #456

# Documentation
docs(readme): update installation instructions

Added section on virtual environment setup for Windows users.
```

### Best Practices

- Use present tense ("add" not "added")
- Keep subject line under 50 characters
- Capitalize first letter
- No period at the end of subject
- Separate subject from body with blank line
- Wrap body at 72 characters
- Explain *what* and *why*, not *how*

## 🔀 Pull Request Process

### Before Submitting

1. **Update your branch**:
   ```bash
   git checkout main
   git pull upstream main
   git checkout your-feature-branch
   git rebase main
   ```

2. **Run all checks**:
   ```bash
   make all  # Runs format, lint, type-check, and test
   ```

3. **Update documentation**: If your changes affect usage

4. **Add tests**: Ensure new code is tested

5. **Update CHANGELOG**: Add entry for notable changes

### Submitting Pull Request

1. Push to your fork:
   ```bash
   git push origin your-feature-branch
   ```

2. Go to GitHub and create a Pull Request

3. Fill out the PR template completely:
   - Description of changes
   - Related issues
   - Testing performed
   - Screenshots (if applicable)

4. Request review from maintainers

### PR Title Format

Use the same format as commit messages:

```
feat(module): add new feature
fix(module): resolve bug
docs: update user guide
```

### Review Process

- Maintainers will review your PR
- Address feedback and push updates
- Keep the conversation professional and constructive
- Once approved, a maintainer will merge your PR

### After Merge

- Delete your feature branch
- Update your main branch
- Celebrate! 🎉

## 🐛 Issue Reporting

### Before Creating an Issue

1. Search existing issues to avoid duplicates
2. Verify the issue in the latest version
3. Gather relevant information

### Creating a Good Issue

**Bug Reports** should include:
- Clear, descriptive title
- Steps to reproduce
- Expected vs actual behavior
- Error messages/stack traces
- Environment info (OS, Python version)
- Code samples (minimal reproducible example)

**Feature Requests** should include:
- Clear description of the feature
- Use cases and motivation
- Proposed implementation (if applicable)
- Examples of similar features elsewhere

### Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Documentation improvements
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention needed
- `question`: Further information requested

## 🎯 Areas for Contribution

### Good First Issues

- Documentation improvements
- Adding tests
- Fixing typos
- Adding examples

### Advanced Contributions

- New data sources (SQL, APIs, etc.)
- Performance optimizations
- Advanced statistical methods
- Interactive visualizations

## 💡 Tips for Success

1. **Start Small**: Begin with small contributions to familiarize yourself
2. **Ask Questions**: Don't hesitate to ask for clarification
3. **Be Patient**: Reviews may take time
4. **Stay Engaged**: Respond to feedback promptly
5. **Learn**: Use this as an opportunity to improve your skills

## 📞 Getting Help

- **Documentation**: Check the [User Guide](docs/guides/user_guide.md)
- **Discussions**: Use [GitHub Discussions](https://github.com/yourusername/best_practice_project/discussions)
- **Issues**: Search [existing issues](https://github.com/yourusername/best_practice_project/issues)

## 🙏 Thank You

Thank you for contributing to the Data Analysis Project! Your efforts help make this project better for everyone.

---

*This contributing guide is adapted from open source best practices.*
