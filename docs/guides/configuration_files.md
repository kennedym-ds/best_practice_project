# Configuration Files Guide

## Overview

Configuration files are essential for maintaining consistency, automating workflows, and ensuring best practices across your Python project. This guide explains each configuration file in detail, why it's needed, and how to use it effectively.

---

## Table of Contents

1. [.gitignore](#gitignore)
2. [.env and .env.example](#env-and-envexample)
3. [.editorconfig](#editorconfig)
4. [pyproject.toml](#pyprojecttoml)
5. [requirements.txt and requirements-dev.txt](#requirementstxt-and-requirements-devtxt)
6. [.pre-commit-config.yaml](#pre-commit-configyaml)
7. [Makefile](#makefile)
8. [.github/workflows/ci.yml](#githubworkflowsciyml)
9. [LICENSE](#license)

---

## .gitignore

### What It Is

The `.gitignore` file tells Git which files and directories to ignore and not track in version control.

### Why It's Important

**Best Practice Reasons:**

1. **Security**: Prevents accidentally committing sensitive data (API keys, passwords, tokens)
2. **Repository Size**: Keeps repository lean by excluding generated files and dependencies
3. **Collaboration**: Avoids conflicts from developer-specific files (IDE settings, OS files)

4. **Cleanliness**: Focuses repository on source code, not build artifacts or temporary files

### How It Works

Git reads `.gitignore` and excludes matching files from:

- `git add` operations
- `git status` output
- `git commit` operations

### Common Patterns in Our Project

```gitignore
# Python bytecode and cache
__pycache__/
*.py[cod]
*$py.class
*.so

# Virtual environments
venv/
env/
ENV/
.venv/

# IDE settings
.vscode/
.idea/
*.swp
*.swo

# Environment variables (CRITICAL for security)
.env
.env.local

# Test and coverage
.coverage
htmlcov/
.pytest_cache/

# Build artifacts
dist/
build/
*.egg-info/

# OS files
.DS_Store
Thumbs.db

```text

### Pattern Syntax

| Pattern | Matches | Example |
|---------|---------|---------|
| `*.txt` | All .txt files | `notes.txt`, `data.txt` |
| `temp/` | Directory and contents | `temp/file.py` |
| `**/logs` | logs dir anywhere | `src/logs/`, `tests/logs/` |
| `!important.log` | Exception (don't ignore) | Keeps `important.log` |
| `data/*.csv` | Files in data/ only | `data/test.csv` (not `data/raw/test.csv`) |
| `data/**/*.csv` | CSV files anywhere in data/ | `data/raw/test.csv`, `data/processed/output.csv` |

### Best Practices

1. **Start Early**: Create `.gitignore` before first commit
2. **Use Templates**: Start with [gitignore.io](https://gitignore.io) templates for Python
3. **Be Specific**: Prefer explicit patterns over wildcards when possible

4. **Document Unusual Patterns**: Add comments explaining non-obvious exclusions
5. **Never Commit Then Ignore**: If already committed, you must remove from history:

   ```bash
   git rm --cached <file>  # Remove from Git, keep local copy

```bash

### Example: Why We Ignore Each Category

```gitignore

# Python bytecode - regenerated automatically, platform-specific
__pycache__/
*.pyc

# Virtual environments - everyone uses different paths/tools
venv/
.venv/

# Secrets - NEVER commit these!
.env
*.key
*.pem

# IDE files - personal preference, not project requirement
.vscode/
.idea/

# Generated files - can be rebuilt from source
dist/
build/
*.egg-info/

# Test outputs - generated during testing
.coverage
htmlcov/
.pytest_cache/

# OS files - not relevant to project
.DS_Store     # macOS
Thumbs.db     # Windows

```python

### Security Tip

**Already committed secrets?** Don't just delete and commit again - the secret is still in Git history!

**Solutions:**

1. **Immediate**: Rotate the secret (change API key, password, etc.)
2. **Clean History**: Use `git filter-repo` or BFG Repo-Cleaner
3. **Prevention**: Use pre-commit hooks to scan for secrets (see `.pre-commit-config.yaml` section)

---

## .env and .env.example

### What They Are

- **.env**: Contains actual environment variables (API keys, database URLs, secrets)
- **.env.example**: Template showing required variables without actual values

### Why They're Important

**Best Practice Reasons:**

1. **Security**: Keeps secrets out of source code and version control
2. **Flexibility**: Easy to change configuration without code changes
3. **Environment Separation**: Different values for dev, staging, production

4. **Team Onboarding**: `.env.example` shows what's needed
5. **12-Factor App**: Follows [12-factor methodology](https://12factor.net/config) for modern applications

### How They Work

```python
# Without .env (BAD - secrets in code)
API_KEY = "sk_live_abc123xyz"  # ❌ Hardcoded secret
DATABASE_URL = "postgresql://user:pass@localhost/db"

# With .env (GOOD - externalized config)
from dotenv import load_dotenv
import os

load_dotenv()  # Loads variables from .env file

API_KEY = os.getenv("API_KEY")  # ✅ Loaded from environment
DATABASE_URL = os.getenv("DATABASE_URL")

```text

### Our Project Structure

**.env** (NEVER commit - listed in .gitignore):

```env

# API Keys
OPENAI_API_KEY=sk-proj-abc123xyz789...
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/mydb

# Application Settings
DEBUG=True
LOG_LEVEL=DEBUG
MAX_WORKERS=4

# Feature Flags
ENABLE_CACHING=true
ENABLE_ANALYTICS=false

```text

**.env.example** (Committed to Git):

```env

# API Keys
OPENAI_API_KEY=your_openai_api_key_here
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Application Settings
DEBUG=False
LOG_LEVEL=INFO
MAX_WORKERS=4

# Feature Flags
ENABLE_CACHING=true
ENABLE_ANALYTICS=false

```text

### Best Practices

#### 1. **Always Use .env.example**

```bash

# New team member setup
cp .env.example .env
# Edit .env with actual values
nano .env

```bash

#### 2. **Document Each Variable**

```env

# OpenAI API key for GPT-4 access
# Get it from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_key_here

# PostgreSQL connection string format:
# postgresql://username:password@host:port/database
DATABASE_URL=postgresql://user:pass@localhost:5432/mydb

# Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL=INFO

```text

#### 3. **Use Type-Appropriate Defaults**

```python

import os
from distutils.util import strtobool

# String with default
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Integer with default
MAX_WORKERS = int(os.getenv("MAX_WORKERS", "4"))

# Boolean with proper parsing
DEBUG = bool(strtobool(os.getenv("DEBUG", "False")))

# Required variable (no default)
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable is required")

```text

#### 4. **Organize by Category**

```env

# ============================================
# External Services
# ============================================
OPENAI_API_KEY=...
STRIPE_API_KEY=...
SENDGRID_API_KEY=...

# ============================================
# Database Configuration
# ============================================
DATABASE_URL=...
REDIS_URL=...

# ============================================
# Application Settings
# ============================================
DEBUG=False
LOG_LEVEL=INFO
SECRET_KEY=...

# ============================================
# Feature Flags
# ============================================
ENABLE_CACHING=true
ENABLE_RATE_LIMITING=true

```text

#### 5. **Different Environments**

Many teams use multiple `.env` files:

```bash

.env                # Local development (gitignored)
.env.example        # Template (committed)
.env.test          # Test environment (gitignored)
.env.staging       # Staging (server only, not in Git)
.env.production    # Production (server only, not in Git)

```text

Load the appropriate one:

```python

import os
from dotenv import load_dotenv

# Load environment-specific file
env = os.getenv("ENVIRONMENT", "development")
load_dotenv(f".env.{env}")

```text

### Security Best Practices

#### ✅ DO

- Use `.env` for ALL secrets and sensitive configuration
- Add `.env` to `.gitignore` immediately
- Use strong, unique values for each environment
- Rotate secrets regularly
- Use secret management tools in production (AWS Secrets Manager, HashiCorp Vault)
- Validate required variables at application startup

#### ❌ DON'T

- Commit `.env` files to Git (use `.env.example` instead)
- Email or Slack `.env` files (use secure sharing tools)
- Use production credentials in development
- Reuse the same secret across multiple services
- Store `.env` in shared folders or cloud storage

### Common Pitfalls

**Problem**: Forgot to load `.env` before accessing variables

```python
# ❌ This will be None if .env not loaded
API_KEY = os.getenv("API_KEY")

# ✅ Load first
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("API_KEY")

```text

**Problem**: `.env` not in same directory as script

```python

# ✅ Load from specific path
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

```text

**Problem**: Variables not updating after changing `.env`

```bash

# Restart your application/server after editing .env
# Or use auto-reload in development (e.g., Flask debug mode)
```bash

---

## .editorconfig

### What It Is

`.editorconfig` is a configuration file that defines coding styles and ensures consistency across different editors and IDEs.

### Why It's Important

**Best Practice Reasons:**

1. **Consistency**: Everyone on the team uses the same indentation, line endings, etc.
2. **Editor-Agnostic**: Works with VS Code, PyCharm, Sublime Text, Vim, etc.
3. **Automatic**: No manual configuration needed

4. **Prevents Issues**: Avoids mixed line endings, tab/space conflicts
5. **Professional**: Shows attention to detail and code quality

### How It Works

When you open a file, your editor checks for `.editorconfig` and automatically applies the settings. Most modern editors support it natively or via plugins.

### Our Project Configuration

```ini
# EditorConfig is awesome: https://EditorConfig.org

# Top-most EditorConfig file
root = true

# Default settings for all files
[*]
charset = utf-8                    # Use UTF-8 encoding
end_of_line = lf                   # Unix-style line endings
insert_final_newline = true        # End files with newline
trim_trailing_whitespace = true    # Remove trailing spaces
indent_style = space              # Use spaces, not tabs

# Python files
[*.py]
indent_size = 4                   # PEP 8 standard
max_line_length = 88              # Black formatter default

# YAML files (CI config, docker-compose, etc.)
[*.{yml,yaml}]
indent_size = 2                   # YAML convention

# JSON files
[*.json]
indent_size = 2                   # Common JSON convention

# Markdown files
[*.md]
max_line_length = off             # Don't enforce line length
trim_trailing_whitespace = false  # Preserve 2-space line breaks

# Makefile (requires tabs)
[Makefile]
indent_style = tab                # Makefiles must use tabs

```makefile

### Property Reference

| Property | Values | Description |
|----------|--------|-------------|
| `indent_style` | `space`, `tab` | Type of indentation |
| `indent_size` | number | Number of spaces per indent |
| `end_of_line` | `lf`, `cr`, `crlf` | Line ending format |
| `charset` | `utf-8`, `latin1`, etc. | File character encoding |
| `trim_trailing_whitespace` | `true`, `false` | Remove trailing spaces |
| `insert_final_newline` | `true`, `false` | Ensure file ends with newline |
| `max_line_length` | number, `off` | Maximum line length |

### Line Endings Explained

**Why `end_of_line = lf` matters:**

- **LF** (`\n`): Unix/Linux/Mac line endings
- **CRLF** (`\r\n`): Windows line endings
- **CR** (`\r`): Old Mac line endings (pre-OS X)

**Problem without .editorconfig:**

```text
Alice (Mac): Edits file, saves with LF
Bob (Windows): Opens file, Git shows every line changed due to CRLF conversion
Conflicts and confusion ensue

```text

**Solution with .editorconfig:**

```text

Everyone uses LF (Unix-style) regardless of OS
Git is configured to convert on checkout (if needed)
No false conflicts!

```text

### Best Practices

#### 1. **Place at Project Root**

```text

project/
├── .editorconfig      # ✅ Here (applies to whole project)
├── src/
├── tests/
└── docs/

```text

#### 2. **Use Pattern Matching**

```ini

# Multiple extensions
[*.{js,ts,jsx,tsx}]
indent_size = 2

# Specific files
[package.json]
indent_size = 2

# All files in directory
[tests/**]
indent_size = 4

# Match any depth
[**/migrations/*.py]
max_line_length = off

```python

#### 3. **Align with Language Conventions**

```ini

# Python - PEP 8
[*.py]
indent_size = 4
max_line_length = 88  # Black default (or 79 for strict PEP 8)

# JavaScript - Common convention
[*.{js,ts}]
indent_size = 2

# Go - Must use tabs
[*.go]
indent_style = tab

# YAML - 2 spaces is standard
[*.{yml,yaml}]
indent_size = 2

```yaml

#### 4. **Match Your Formatters**

If using Black for Python:

```ini

[*.py]
max_line_length = 88  # Match Black's default
indent_size = 4

```python

If using Prettier for JavaScript:

```ini

[*.{js,json,yml}]
indent_size = 2  # Match Prettier's default

```json

### Editor Support

Most editors support `.editorconfig` automatically:

| Editor | Support |
|--------|---------|
| **VS Code** | Built-in (install EditorConfig extension for full support) |
| **PyCharm/IntelliJ** | Built-in |
| **Sublime Text** | Plugin required |
| **Vim** | Plugin required |
| **Emacs** | Plugin required |
| **Atom** | Built-in |

**VS Code**: Install "EditorConfig for VS Code" extension

### Testing Your Configuration

```bash

# Create test file
echo "test  " > test.py  # Note trailing spaces

# Open in editor with .editorconfig support
# Save file
# Trailing spaces should be removed automatically
```python

### Common Issues

**Problem**: Settings not applying

```text


1. Check editor has EditorConfig support
2. Ensure .editorconfig is at project root
3. Restart editor

4. Check for syntax errors in .editorconfig

```text

**Problem**: Conflicts with editor settings

```text

.editorconfig should override editor defaults
If not working, check editor documentation for precedence

```text

**Problem**: Git showing changes after setup

```bash

# EditorConfig may cause one-time reformatting
# Commit these changes:
git add -A
git commit -m "Apply EditorConfig formatting"

```bash

---

## pyproject.toml

### What It Is

`pyproject.toml` is the modern, standardized configuration file for Python projects. It replaces multiple configuration files (`setup.py`, `setup.cfg`, `MANIFEST.in`, etc.) with a single, unified TOML format.

### Why It's Important

**Best Practice Reasons:**

1. **Single Source of Truth**: All project metadata and tool configs in one place
2. **PEP 518 Standard**: Official Python standard for build system configuration
3. **Modern**: Replaces legacy `setup.py` with declarative configuration

4. **Tool Integration**: Most modern Python tools support it
5. **Reproducible Builds**: Specifies exact build dependencies

### How It Works

`pyproject.toml` uses TOML (Tom's Obvious, Minimal Language) format - simple key-value pairs:

```toml
[section]
key = "value"
number = 42
list = ["item1", "item2"]

[section.subsection]
nested_key = "nested_value"

```text

### File Structure Overview

Our `pyproject.toml` has several sections:

```toml

[build-system]              # How to build the package
[tool.hatch.build]          # Build backend configuration
[project]                   # Project metadata
[project.optional-dependencies]  # Optional dependency groups
[project.urls]              # Project links
[tool.pytest.ini_options]   # pytest configuration
[tool.coverage]             # Coverage.py configuration
[tool.black]                # Black formatter configuration
[tool.isort]                # isort import sorter configuration
[tool.mypy]                 # mypy type checker configuration

```python

---

### Section 1: [build-system]

**Purpose**: Specifies how to build your package

```toml

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

```toml

**Explanation:**

- `requires`: Build dependencies needed to build the package
- `build-backend`: Which build tool to use

**Common Build Backends:**

| Backend | When to Use | Package Size |
|---------|-------------|--------------|
| `hatchling` | Modern projects, simple ✅ | Lightweight |
| `setuptools` | Legacy support, complex builds | Feature-rich |
| `flit_core` | Pure Python, minimal config | Minimal |
| `poetry.core` | Poetry users | Poetry ecosystem |

**Why We Use Hatchling:**

- Modern and fast
- Simple configuration
- Works great with `src` layout
- Follows latest Python packaging standards

---

### Section 2: [tool.hatch.build.targets.wheel]

**Purpose**: Tells the build backend where to find source code

```toml
[tool.hatch.build.targets.wheel]
packages = ["src/data_analysis"]

```toml

**Why This Matters:**

- Python packages can be in project root or `src/` directory
- Build tools need to know where to look
- We use `src` layout (best practice) so we must specify it

**Without this section:**

```bash

$ python -m build
ERROR: Unable to determine which files to ship inside the wheel

```bash

---

### Section 3: [project]

**Purpose**: Core project metadata (name, version, dependencies, etc.)

```toml

[project]
name = "data-analysis-best-practices"
version = "0.1.0"
description = "A comprehensive Python data analysis project demonstrating best practices"
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
readme = "README.md"
requires-python = ">=3.9"
license = {text = "MIT"}
keywords = ["data-analysis", "best-practices", "python", "pandas", "numpy"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

dependencies = [
    "pandas>=2.0.0",
    "numpy>=1.24.0",
    "matplotlib>=3.7.0",
    "seaborn>=0.12.0",
    "scikit-learn>=1.3.0",
    "openpyxl>=3.1.0",
    "python-dotenv>=1.0.0",
]

```python

**Field Explanations:**

| Field | Purpose | Example |
|-------|---------|---------|
| `name` | Package name (PyPI identifier) | `data-analysis-best-practices` |
| `version` | Current version (semver) | `0.1.0` |
| `description` | One-line summary | "A comprehensive..." |
| `authors` | Package maintainers | `[{name = "...", email = "..."}]` |
| `readme` | Path to README file | `"README.md"` |
| `requires-python` | Minimum Python version | `">=3.9"` |
| `license` | License type | `{text = "MIT"}` |
| `keywords` | Search keywords (PyPI) | `["data-analysis", "pandas"]` |
| `classifiers` | PyPI classifiers | Status, audience, license |
| `dependencies` | Required packages | `["pandas>=2.0.0"]` |

**Version Specifiers:**

```toml

dependencies = [
    "pandas>=2.0.0",        # Minimum version (recommended)
    "numpy==1.24.0",        # Exact version (rare)
    "matplotlib>=3.7,<4",   # Version range
    "requests>=2.28.0,!=2.29.0",  # Exclude specific version
]

```text

**Best Practices:**

- Use `>=` for minimum versions (allows upgrades)
- Avoid `==` unless absolutely necessary (prevents upgrades)
- Use `<major+1` to prevent breaking changes (e.g., `pandas>=2.0,<3`)

**PyPI Classifiers:**

Browse full list at: <https://pypi.org/classifiers/>

```toml

classifiers = [
    # Development status
    "Development Status :: 3 - Alpha",        # Planning: 1, Pre-Alpha: 2, Alpha: 3, Beta: 4, Stable: 5

    # Target audience
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",

    # License
    "License :: OSI Approved :: MIT License",

    # Python versions supported
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",

    # Topics
    "Topic :: Scientific/Engineering :: Information Analysis",
]

```python

---

### Section 4: [project.optional-dependencies]

**Purpose**: Optional dependency groups for different use cases

```toml

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "black>=23.7.0",
    "flake8>=6.1.0",
    "mypy>=1.5.0",
]
docs = [
    "sphinx>=7.1.0",
    "sphinx-rtd-theme>=1.3.0",
    "myst-parser>=2.0.0",
]

```text

**Installation:**

```bash

# Install just the package
pip install data-analysis-best-practices

# Install with dev tools
pip install data-analysis-best-practices[dev]

# Install with docs tools
pip install data-analysis-best-practices[docs]

# Install multiple groups
pip install data-analysis-best-practices[dev,docs]

# Install from local directory with dev dependencies
pip install -e .[dev]

```text

**Common Dependency Groups:**

| Group | Purpose | Typical Packages |
|-------|---------|------------------|
| `dev` | Development tools | pytest, black, mypy, flake8 |
| `docs` | Documentation | sphinx, sphinx-rtd-theme |
| `test` | Testing only | pytest, pytest-cov, pytest-mock |
| `lint` | Linting/formatting | black, flake8, pylint, isort |
| `typing` | Type checking | mypy, types-* packages |
| `jupyter` | Jupyter notebooks | jupyter, ipykernel, nbconvert |
| `viz` | Extra visualizations | plotly, bokeh, altair |

**Why Use Optional Dependencies:**

- Users can install minimal package without dev tools
- Reduces installation size and time for end users
- Clear separation of concerns
- CI can install only what it needs

---

### Section 5: [project.urls]

**Purpose**: Links to project resources

```toml
[project.urls]
Homepage = "https://github.com/yourusername/data-analysis-best-practices"
Documentation = "https://data-analysis-best-practices.readthedocs.io"
Repository = "https://github.com/yourusername/data-analysis-best-practices"
Issues = "https://github.com/yourusername/data-analysis-best-practices/issues"

```text

**These appear on PyPI package page!**

**Common URLs:**

- `Homepage`: Main project website or repository
- `Documentation`: Docs hosted on Read the Docs, GitHub Pages, etc.
- `Repository`: Source code (GitHub, GitLab, etc.)
- `Issues`: Bug tracker
- `Changelog`: CHANGELOG.md or GitHub releases
- `Funding`: Sponsor page (GitHub Sponsors, Patreon, etc.)

---

### Section 6: [tool.pytest.ini_options]

**Purpose**: Configure pytest behavior

```toml

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test__.py", "__test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--verbose",
    "--cov=src",
    "--cov-report=html",
    "--cov-report=term-missing",
    "--cov-branch",
    "--import-mode=importlib",
]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
]

```text

**Key Options:**

| Option | Purpose | Example |
|--------|---------|---------|
| `testpaths` | Where to find tests | `["tests"]` |
| `python_files` | Test file patterns | `["test_*.py"]` |
| `python_classes` | Test class patterns | `["Test*"]` |
| `python_functions` | Test function patterns | `["test_*"]` |
| `addopts` | Default CLI arguments | `["--verbose", "--cov=src"]` |
| `markers` | Custom test markers | `["slow", "integration"]` |

**Using Custom Markers:**

```python

import pytest

@pytest.mark.slow
def test_large_dataset():
    # This test takes a long time
    pass

@pytest.mark.integration
def test_end_to_end_pipeline():
    # This test requires database, external APIs, etc.
    pass

```text

```bash

# Run only fast tests (skip slow)
pytest -m "not slow"

# Run only integration tests
pytest -m integration

# Run unit tests only
pytest -m unit

```text

---

### Section 7: [tool.coverage]

**Purpose**: Configure coverage.py (test coverage measurement)

```toml

[tool.coverage.run]
source = ["src"]
omit = ["_/tests/_", "_/test__.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
]

```text

**Explanation:**

- `source`: Which directories to measure coverage for
- `omit`: Files/patterns to exclude from coverage
- `exclude_lines`: Code lines to ignore (e.g., debug code, type checking)

**Using `pragma: no cover`:**

```python

def some_function():
    try:
        result = risky_operation()
    except Exception:  # pragma: no cover
        # This is defensive code that's hard to test
        log_error()
        raise

```text

---

### Section 8: [tool.black]

**Purpose**: Configure Black code formatter

```toml

[tool.black]
line-length = 88
target-version = ['py39', 'py310', 'py311', 'py312']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''

```text

**Key Options:**

| Option | Purpose | Default |
|--------|---------|---------|
| `line-length` | Maximum line length | 88 |
| `target-version` | Python versions to target | Current Python |
| `include` | File patterns to format | `.py` files |
| `exclude` | Directories/files to skip | `venv`, `build`, etc. |

**Why 88 Characters?**

- Black's default is 88 (not PEP 8's 79)
- 10% over 79 = ~10% fewer lines
- Still readable on modern displays
- Compromise between strict 79 and unlimited

**Running Black:**

```bash

# Format all files
black .

# Check without modifying
black --check .

# Show what would change
black --diff .

```text

---

### Section 9: [tool.isort]

**Purpose**: Configure isort (import statement sorter)

```toml

[tool.isort]
profile = "black"
line_length = 88
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true

```text

**Key Options:**

| Option | Purpose |
|--------|---------|
| `profile = "black"` | Make compatible with Black |
| `line_length = 88` | Match Black's line length |
| `multi_line_output = 3` | Vertical hanging indent style |

**Import Sorting Example:**

Before isort:

```python

from my_lib import Object
import os
from my_lib import Object3
from my_lib import Object2
import sys
from third_party import lib15, lib1, lib2, lib3

```text

After isort:

```python

import os
import sys

from third_party import lib1, lib2, lib3, lib15

from my_lib import Object, Object2, Object3

```text

**Import Order:**

1. Standard library imports
2. Third-party imports
3. Local/application imports

---

### Section 10: [tool.mypy]

**Purpose**: Configure mypy static type checker

```toml

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = false
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
follow_imports = "normal"
ignore_missing_imports = true

```text

**Key Options Explained:**

| Option | Purpose | Effect |
|--------|---------|--------|
| `disallow_untyped_defs` | Require type hints on functions | ✅ Enforces type hints |
| `disallow_incomplete_defs` | All arguments must be typed | ✅ Prevents partial hints |
| `check_untyped_defs` | Check bodies of untyped functions | ✅ More thorough |
| `ignore_missing_imports` | Don't error on missing stubs | ✅ Allows third-party libs |
| `warn_return_any` | Warn when returning `Any` | ⚠️ Encourages specific types |
| `warn_unused_ignores` | Warn about unnecessary `# type: ignore` | 🧹 Keeps codebase clean |

**Example Code with Type Hints:**

```python

from typing import List, Optional

def process_data(
    data: List[str],
    threshold: int = 10,
    normalize: bool = True
) -> Optional[List[float]]:
    """Process data with proper type hints."""
    if not data:
        return None

    results: List[float] = []
    for item in data:
        value = float(item)
        if normalize:
            value /= threshold
        results.append(value)

    return results

```text

**Running mypy:**

```bash

# Check entire project
mypy src/

# Check specific file
mypy src/data_analysis/data_loader.py

# Ignore errors from third-party packages
mypy --ignore-missing-imports src/

```python

---

## Best Practices for pyproject.toml

### 1. Use Version Ranges, Not Exact Versions

```toml

# ✅ GOOD - Allows bug fixes and improvements
dependencies = [
    "pandas>=2.0.0",
    "numpy>=1.24.0",
]

# ❌ BAD - Prevents updates, causes dependency conflicts
dependencies = [
    "pandas==2.0.3",
    "numpy==1.24.2",
]

```text

### 2. Organize Dependencies by Category

```toml

dependencies = [
    # Core data processing
    "pandas>=2.0.0",
    "numpy>=1.24.0",

    # Visualization
    "matplotlib>=3.7.0",
    "seaborn>=0.12.0",

    # Machine learning
    "scikit-learn>=1.3.0",

    # Utilities
    "python-dotenv>=1.0.0",
]

```python

### 3. Keep Tool Configs in pyproject.toml

**Instead of:**

- `pytest.ini`
- `setup.cfg`
- `.coveragerc`
- `.flake8`
- `mypy.ini`

**Use:**

- All in `pyproject.toml` under `[tool.name]` sections

### 4. Version Semantic Versioning

```toml

MAJOR.MINOR.PATCH

0.1.0 - Initial development
0.2.0 - Added new feature (backward compatible)
0.2.1 - Fixed bug (backward compatible)
1.0.0 - First stable release
1.1.0 - New feature (backward compatible)
2.0.0 - Breaking changes

```text

### 5. Add All Necessary Classifiers

Helps users find your package on PyPI:

```toml

classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Scientific/Engineering",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Typing :: Typed",
]

```python

---

## Common Issues and Solutions

### Issue 1: Package Not Found After Installing

**Problem:**

```bash

pip install .
python -c "import data_analysis"  # ModuleNotFoundError

```bash

**Solution:**

```toml

# Add this section to specify package location
[tool.hatch.build.targets.wheel]
packages = ["src/data_analysis"]

```toml

### Issue 2: Build Fails with "No module named 'hatchling'"

**Problem:**

```bash

python -m build
# ERROR: No module named 'hatchling'
```bash

**Solution:**

```bash

# Install build tool and backend
pip install build hatchling

```bash

### Issue 3: pytest Not Finding Tests

**Problem:**

```bash

pytest
# collected 0 items
```bash

**Solution:**

```toml

[tool.pytest.ini_options]
testpaths = ["tests"]  # Make sure this points to your test directory
python_files = ["test_*.py"]  # Make sure your test files match this pattern

```makefile

### Issue 4: mypy Complains About Missing Imports

**Problem:**

```bash

mypy src/
# error: Cannot find implementation or library stub for module named 'pandas'
```bash

**Solution:**

```toml

[tool.mypy]
ignore_missing_imports = true  # Or install type stubs: pip install types-pandas

```toml

---

## Summary

These three configuration files form the foundation of a well-organized Python project:

1. **`.gitignore`**: Keeps repository clean and secure
2. **`.env` / `.env.example`**: Manages secrets and configuration
3. **`.editorconfig`**: Ensures consistent code formatting

4. **`pyproject.toml`**: Modern Python project configuration (⭐ **Most Important**)

### Quick Setup Checklist

- [ ] Create `.gitignore` using [gitignore.io](https://gitignore.io/?templates=python)
- [ ] Add `.env` to `.gitignore`
- [ ] Create `.env.example` with template variables
- [ ] Create `.env` from `.env.example`
- [ ] Add `.editorconfig` matching your team's style guide
- [ ] Install EditorConfig plugin for your editor
- [ ] Create `pyproject.toml` with all necessary sections
- [ ] Configure all tools in `[tool.*]` sections
- [ ] Test that package builds: `python -m build`

### Next Steps

Continue reading about other configuration files:

- [requirements.txt](#requirementstxt-and-requirements-devtxt) - Dependency management
- [.pre-commit-config.yaml](#pre-commit-configyaml) - Automated code quality
- [Makefile](#makefile) - Common tasks automation
- [CI/CD workflows](#githubworkflowsciyml) - Automated testing and deployment

---

_This guide is part of the Data Analysis Best Practices project documentation._

---

## requirements.txt and requirements-dev.txt

### What They Are

`requirements.txt` files are simple text files listing Python package dependencies. They're the traditional way to specify what packages your project needs.

**Two Common Files:**

- **`requirements.txt`**: Production dependencies (needed to run the application)
- **`requirements-dev.txt`**: Development dependencies (needed for development/testing)

### Why They're Important

**Best Practice Reasons:**

1. **Reproducibility**: Anyone can install exact same dependencies
2. **Simplicity**: Plain text format, universally understood
3. **Version Control**: Track dependency changes over time

4. **CI/CD**: Automated systems can easily install dependencies
5. **Virtual Environments**: Isolate project dependencies

### How They Work

```bash
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Install both
pip install -r requirements.txt -r requirements-dev.txt

```text

---

### Our requirements.txt (Production)

```txt

# Core dependencies
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
scikit-learn>=1.3.0
openpyxl>=3.1.0
python-dotenv>=1.0.0

```python

**Purpose:** Only packages needed to **run** the application.

**These are:**

- Data processing: `pandas`, `numpy`
- Visualization: `matplotlib`, `seaborn`
- Machine learning: `scikit-learn`
- File handling: `openpyxl` (Excel files)
- Configuration: `python-dotenv` (environment variables)

---

### Our requirements-dev.txt (Development)

```txt

# Development dependencies
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-mock>=3.11.0
black>=23.7.0
flake8>=6.1.0
flake8-pytest-style>=1.7.0
mypy>=1.5.0
isort>=5.12.0
pre-commit>=3.3.0

# Documentation dependencies
sphinx>=7.1.0
sphinx-rtd-theme>=1.3.0
myst-parser>=2.0.0

```text

**Purpose:** Packages needed for **development and testing only**.

**Categories:**

1. **Testing**: `pytest`, `pytest-cov`, `pytest-mock`
2. **Code Quality**: `black`, `flake8`, `mypy`, `isort`, `pre-commit`
3. **Documentation**: `sphinx`, `sphinx-rtd-theme`, `myst-parser`

**Why Separate?**

- Users installing your package don't need pytest or black
- Keeps production installations lightweight
- Clear separation of concerns
- Faster CI/CD for different stages

---

## Version Specifiers Explained

### Common Patterns

| Specifier | Meaning | Example | When to Use |
|-----------|---------|---------|-------------|
| `==` | Exact version | `pandas==2.0.3` | Rare (only for compatibility issues) |
| `>=` | Minimum version | `pandas>=2.0.0` | **Most common** (allows upgrades) |
| `<=` | Maximum version | `pandas<=2.1.0` | Rare (prevent breaking changes) |
| `~=` | Compatible release | `pandas~=2.0.0` | Allows `2.0.x` but not `2.1.0` |
| `>=,<` | Version range | `pandas>=2.0,<3` | Prevent major version bumps |
| `!=` | Exclude version | `pandas>=2.0,!=2.0.1` | Skip broken version |

### Examples

```txt
# ✅ GOOD - Recommended approach
pandas>=2.0.0              # Minimum version, allows 2.1.0, 2.2.0, etc.
numpy>=1.24.0,<2           # Allow 1.x updates but not 2.0 (breaking)

# ⚠️ USE WITH CAUTION
pandas~=2.0.0              # Allows 2.0.1, 2.0.2 but not 2.1.0
                           # Good for conservative updates

# ❌ AVOID (unless necessary)
pandas==2.0.3              # Exact version - prevents security updates
                           # Can cause dependency conflicts

```text

### Real-World Scenario

```txt

# A new pandas version has a security fix
pandas>=2.0.0              # ✅ Gets the fix automatically
pandas==2.0.3              # ❌ Stuck on vulnerable version

```text

---

## requirements.txt vs pyproject.toml

### Which One to Use?

| Aspect | requirements.txt | pyproject.toml |
|--------|------------------|----------------|
| **Best For** | Applications, scripts | Libraries, packages |
| **Simplicity** | ✅ Very simple | More complex |
| **Tooling** | Universal (pip) | Modern Python tools |
| **Standards** | De facto standard | PEP 517/518 standard |
| **Version Lock** | Can pin exact versions | Usually ranges |
| **Our Project** | ✅ We use both | ✅ We use both |

### Our Strategy

We use **BOTH** because:

```toml
# pyproject.toml - Library dependencies (abstract)
[project]
dependencies = [
    "pandas>=2.0.0",        # Wide range for compatibility
    "numpy>=1.24.0",
]

```text

```txt

# requirements.txt - Exact working versions (concrete)
pandas==2.0.3               # Specific version that works
numpy==1.24.3

```text

**Workflow:**

1. **Development**: Install from `requirements.txt` (exact versions)
2. **Package Building**: `pyproject.toml` declares flexible ranges
3. **Testing**: Test against multiple versions (CI matrix)

---

## Advanced: pip-tools Workflow

### Problem: Manual Dependency Management is Hard

```txt

# You specify:
pandas>=2.0.0

# But pandas requires:
numpy>=1.21.0
python-dateutil>=2.8.2
pytz>=2020.1
# ... and many more

# How do you lock ALL transitive dependencies?
```python

### Solution: pip-tools

**Install:**

```bash

pip install pip-tools

```bash

**Workflow:**

**Step 1: Create `requirements.in` (abstract)**

```txt

# requirements.in - What YOU need
pandas>=2.0.0
matplotlib>=3.7.0
scikit-learn>=1.3.0

```text

**Step 2: Compile to `requirements.txt` (concrete)**

```bash

pip-compile requirements.in

# Creates requirements.txt with ALL dependencies pinned:
# pandas==2.0.3
# numpy==1.24.3
# matplotlib==3.7.2
# ... (50+ transitive dependencies, all pinned)
```text

**Step 3: Install exact versions**

```bash

pip-sync requirements.txt

```bash

**Benefits:**

- Reproducible builds (exact versions)
- Fast installation (no dependency resolution)
- Track what YOU added vs. what's transitive
- Easy updates: `pip-compile --upgrade`

**Our Project:**
We could adopt this workflow for better reproducibility.

---

## Best Practices

### 1. Organize with Comments

```txt

# Core data processing
pandas>=2.0.0
numpy>=1.24.0

# Visualization
matplotlib>=3.7.0
seaborn>=0.12.0

# Machine learning
scikit-learn>=1.3.0

# File I/O
openpyxl>=3.1.0           # Excel support

# Configuration
python-dotenv>=1.0.0      # Environment variables

```python

### 2. Use Minimum Versions, Not Exact

```txt

# ✅ GOOD - Flexible, allows security updates
pandas>=2.0.0

# ❌ BAD - Rigid, prevents updates
pandas==2.0.3

```text

**Exception:** If you encounter a bug in a specific version:

```txt

pandas>=2.0.0,!=2.0.1     # Skip broken version 2.0.1

```text

### 3. Keep Development Separate

```txt

# requirements.txt - ONLY production dependencies
pandas>=2.0.0
numpy>=1.24.0

# requirements-dev.txt - Everything else
-r requirements.txt       # Include production deps
pytest>=7.4.0
black>=23.7.0

```text

**Includes Production:**

```txt

# requirements-dev.txt
-r requirements.txt       # This line includes requirements.txt
pytest>=7.4.0             # Then adds dev tools

```text

### 4. Document Why You Need Each Package

```txt

pandas>=2.0.0             # DataFrame operations
numpy>=1.24.0             # Numerical computations
matplotlib>=3.7.0         # Plotting
openpyxl>=3.1.0          # Excel file support (required for .xlsx)
python-dotenv>=1.0.0     # Load .env files

```python

### 5. Use Platform Markers for OS-Specific Dependencies

```txt

# Only install on Windows
pywin32>=305 ; sys_platform == 'win32'

# Only on macOS
pyobjc-framework-Cocoa>=9.0 ; sys_platform == 'darwin'

# Only on Linux
python-dbus>=1.3.0 ; sys_platform == 'linux'

```python

### 6. Specify Python Version Requirement

```txt

# At the top of requirements.txt
# Requires Python 3.9+

pandas>=2.0.0

```python

Or use `requires-python` in `pyproject.toml`:

```toml

[project]
requires-python = ">=3.9"

```python

---

## Common Workflows

### Fresh Install (New Developer)

```bash

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install production dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Verify installation
pip list

```text

### Adding a New Dependency

```bash

# Install the package
pip install some-new-package

# Add to requirements.txt (manually)
echo "some-new-package>=1.0.0" >> requirements.txt

# Or use pip freeze (with caution)
pip freeze | grep some-new-package >> requirements.txt

```text

⚠️ **Warning:** Don't use `pip freeze > requirements.txt` blindly - it includes ALL packages including transitive dependencies!

### Updating Dependencies

```bash

# Update all packages to latest compatible versions
pip install --upgrade -r requirements.txt

# Update specific package
pip install --upgrade pandas

# Save new versions (if using pip-tools)
pip-compile --upgrade requirements.in

```text

### Checking for Outdated Packages

```bash

# List outdated packages
pip list --outdated

# Example output:
# Package    Version  Latest
# ---------- -------- ------
# pandas     2.0.3    2.1.0
# numpy      1.24.3   1.25.1
```text

---

## Common Issues and Solutions

### Issue 1: Dependency Conflicts

**Problem:**

```bash

pip install -r requirements.txt
ERROR: Cannot install package-a==1.0 and package-b==2.0 because they have conflicting dependencies

```bash

**Solution:**

```txt

# Use version ranges instead of exact versions
package-a>=1.0,<2
package-b>=2.0,<3

```text

Or create a fresh virtual environment:

```bash

# Delete old venv
rm -rf venv

# Create new venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```python

### Issue 2: "Package not found" in requirements.txt

**Problem:**

```bash

pip install -r requirements.txt
ERROR: Could not find a version that satisfies the requirement some-package

```bash

**Solution:**

1. Check spelling and case
2. Check if package exists: <https://pypi.org>
3. Check Python version compatibility

4. Update pip: `pip install --upgrade pip`

### Issue 3: Slow Installation

**Problem:**

```bash

pip install -r requirements.txt
# Takes 10+ minutes to resolve dependencies
```bash

**Solution:**

```bash

# Use pip-tools to pre-resolve dependencies
pip install pip-tools
pip-compile requirements.in  # Generates requirements.txt with pinned versions
pip-sync requirements.txt    # Fast installation, no resolution

```bash

### Issue 4: Different Versions on Different Machines

**Problem:**

- Developer A has pandas 2.0.3
- Developer B has pandas 2.1.0
- Code works on A, breaks on B

**Solution:**

```txt

# Use exact versions for critical packages
pandas==2.0.3

# Or use pip-tools for full dependency locking
pip-compile requirements.in > requirements.txt

```text

---

## Requirements vs Poetry vs Pipenv

### Comparison

| Tool | Pros | Cons |
|------|------|------|
| **requirements.txt** | Simple, universal, no extra tools | No automatic dependency resolution |
| **Poetry** | Modern, handles everything, lock files | Opinionated, learning curve |
| **Pipenv** | Lock files, manages venv | Slow, less popular now |
| **pip-tools** | Best of both worlds | Requires two files (.in and .txt) |

### Our Choice: requirements.txt + pyproject.toml

**Why:**

- ✅ Simple and universal
- ✅ Works with all tools
- ✅ No additional dependencies
- ✅ Easy for beginners
- ✅ Compatible with Docker, CI/CD
- ✅ Can upgrade to pip-tools later if needed

---

## Summary

**requirements.txt Files:**

- ✅ List all Python package dependencies
- ✅ Use `>=` for flexible versioning
- ✅ Separate production (`requirements.txt`) and dev (`requirements-dev.txt`)
- ✅ Organize with comments
- ✅ Document why each package is needed
- ✅ Consider pip-tools for large projects

**Quick Setup:**

```bash
# Create requirements.txt
echo "pandas>=2.0.0" > requirements.txt
echo "numpy>=1.24.0" >> requirements.txt

# Create requirements-dev.txt
echo "-r requirements.txt" > requirements-dev.txt
echo "pytest>=7.4.0" >> requirements-dev.txt

# Install
pip install -r requirements-dev.txt

```text

---

_This guide is part of the Data Analysis Best Practices project documentation._

---

## .pre-commit-config.yaml

### What It Is

`.pre-commit-config.yaml` configures the **pre-commit** framework, which automatically runs code quality checks **before** you commit code to Git.

**Key Concept:** Git hooks that run automatically when you type `git commit`.

### Why It's Important

**Best Practice Reasons:**

1. **Catch Issues Early**: Find problems before they reach the repository
2. **Enforce Standards**: Automatically format code to team standards
3. **Save Time**: No manual linting/formatting before commits

4. **Prevent Bad Commits**: Block commits with syntax errors or security issues
5. **Team Consistency**: Everyone runs the same checks automatically

### How It Works

```text
Developer types: git commit -m "Add feature"
                     ↓
Pre-commit runs:
  ✓ Check trailing whitespace
  ✓ Format code with Black
  ✓ Sort imports with isort
  ✓ Run linter (flake8)
  ✓ Type check (mypy)
  ✓ Security scan (bandit)
                     ↓
All checks pass? → Commit succeeds ✅
Any check fails? → Commit blocked ❌ (with error messages)

```text

**Installation:**

```bash

# Install pre-commit
pip install pre-commit

# Install git hooks (one-time setup)
pre-commit install

# Now all commits automatically run checks!
```text

---

### File Structure Overview

Our `.pre-commit-config.yaml` has 8 hook repositories:

```yaml

repos:

  - repo: pre-commit/pre-commit-hooks      # 1. General file cleanup

  - repo: psf/black                        # 2. Code formatting

  - repo: PyCQA/isort                      # 3. Import sorting

  - repo: PyCQA/flake8                     # 4. Code linting

  - repo: pre-commit/mirrors-mypy          # 5. Type checking

  - repo: PyCQA/bandit                     # 6. Security scanning

  - repo: igorshubovych/markdownlint-cli   # 7. Markdown linting

  - repo: adrienverge/yamllint             # 8. YAML linting

```yaml

---

### Hook 1: General File Cleanup

```yaml


- repo: https://github.com/pre-commit/pre-commit-hooks

  rev: v4.5.0
  hooks:

    - id: trailing-whitespace              # Remove trailing spaces

      args: [--markdown-linebreak-ext=md]

    - id: end-of-file-fixer               # Add newline at end of files

    - id: check-yaml                       # Validate YAML syntax

    - id: check-json                       # Validate JSON syntax

    - id: check-toml                       # Validate TOML syntax

    - id: check-added-large-files         # Prevent committing large files

      args: ['--maxkb=1000']              # Max 1MB

    - id: check-merge-conflict            # Detect merge conflict markers

    - id: check-case-conflict             # Detect case-sensitive filename conflicts

    - id: mixed-line-ending               # Normalize line endings

      args: ['--fix=lf']                  # Use LF (Unix)

    - id: debug-statements                # Find leftover debug prints

```text

**What These Do:**

| Hook | Purpose | Example |
|------|---------|---------|
| `trailing-whitespace` | Removes spaces at end of lines | `"hello "` → `"hello"` |
| `end-of-file-fixer` | Adds newline at EOF (POSIX standard) | Fixes missing final newline |
| `check-yaml` | Validates YAML files | Catches syntax errors |
| `check-json` | Validates JSON files | Catches syntax errors |
| `check-toml` | Validates TOML files | Catches syntax errors |
| `check-added-large-files` | Prevents commits >1MB | Blocks `data.csv` (10MB) |
| `check-merge-conflict` | Finds `<<<<<<<` markers | Detects unresolved merges |
| `check-case-conflict` | Prevents `file.py` + `File.py` | Windows/Mac compatibility |
| `mixed-line-ending` | Normalizes CRLF/LF | Forces LF (Unix style) |
| `debug-statements` | Finds `breakpoint()`, `pdb.set_trace()` | Prevents debug code in commits |

**Why `--fix=lf`?**

- Git stores files with LF endings
- Windows uses CRLF
- This normalizes everything to LF

---

### Hook 2: Black (Code Formatting)

```yaml

- repo: https://github.com/psf/black

  rev: 23.12.1
  hooks:

    - id: black

      language_version: python3.9
      args: ['--line-length=100']

```python

**What It Does:**

- Automatically formats Python code
- Ensures consistent style across entire project
- No more debates about formatting!

**Example:**

Before Black:

```python

def my_function(x,y,z):
    result=x+y+z
    return result

```python

After Black:

```python

def my_function(x, y, z):
    result = x + y + z
    return result

```python

**Configuration:**

- `--line-length=100`: Max 100 characters per line (project standard)
- `language_version: python3.9`: Target Python 3.9+

---

### Hook 3: isort (Import Sorting)

```yaml


- repo: https://github.com/PyCQA/isort

  rev: 5.13.2
  hooks:

    - id: isort

      args: ['--profile=black', '--line-length=100']

```text

**What It Does:**

- Sorts and organizes import statements
- Groups: stdlib → third-party → local

**Example:**

Before isort:

```python

from my_lib import Object
import os
from my_lib import Object3
from my_lib import Object2
import sys
from third_party import lib15, lib1, lib2, lib3

```text

After isort:

```python

import os
import sys

from third_party import lib1, lib2, lib3, lib15

from my_lib import Object, Object2, Object3

```text

**Configuration:**

- `--profile=black`: Compatible with Black formatting
- `--line-length=100`: Match Black's line length

---

### Hook 4: flake8 (Linting)

```yaml


- repo: https://github.com/PyCQA/flake8

  rev: 7.0.0
  hooks:

    - id: flake8

      args: ['--max-line-length=100', '--extend-ignore=E203,W503']
      additional_dependencies:

        - flake8-docstrings          # Check docstring presence

        - flake8-bugbear             # Find likely bugs

        - flake8-comprehensions      # Improve list/dict comprehensions

        - flake8-simplify            # Suggest simpler code

```text

**What It Does:**

- Checks code quality (PEP 8 compliance)
- Finds common bugs and anti-patterns
- Enforces docstring presence

**Common Issues Caught:**

```python

# Missing docstring
def my_function():  # flake8: D103 missing docstring
    pass

# Unused import
import pandas as pd  # flake8: F401 imported but unused

# Undefined variable
print(undefined_var)  # flake8: F821 undefined name

# Line too long
really_long_variable_name = "this line is way over 100 characters..."  # flake8: E501

```text

**Configuration:**

- `--max-line-length=100`: Match Black
- `--extend-ignore=E203,W503`: Ignore Black-incompatible rules

**Plugins:**

- `flake8-docstrings`: Enforces Google/NumPy style docstrings
- `flake8-bugbear`: Catches bugs like mutable default arguments
- `flake8-comprehensions`: Suggests better comprehensions
- `flake8-simplify`: Suggests simpler code patterns

---

### Hook 5: mypy (Type Checking)

```yaml


- repo: https://github.com/pre-commit/mirrors-mypy

  rev: v1.8.0
  hooks:

    - id: mypy

      additional_dependencies:

        - types-requests           # Type stubs for requests

        - pandas-stubs            # Type stubs for pandas

      args: ['--ignore-missing-imports', '--strict']
      exclude: '^tests/'          # Don't type-check tests

```text

**What It Does:**

- Static type checking (catches type errors before runtime)
- Ensures type hints are correct

**Example:**

```python

def add_numbers(a: int, b: int) -> int:
    return a + b

# This will fail mypy check:
result: str = add_numbers(1, 2)  # Error: Incompatible types (int vs str)

```text

**Configuration:**

- `--ignore-missing-imports`: Don't fail on packages without type stubs
- `--strict`: Enable all optional checks (maximum type safety)
- `exclude: '^tests/'`: Skip tests (often have dynamic typing)

**Additional Dependencies:**

- Type stubs provide type information for third-party libraries
- Without stubs, mypy treats everything as `Any`

---

### Hook 6: bandit (Security Scanning)

```yaml


- repo: https://github.com/PyCQA/bandit

  rev: 1.7.6
  hooks:

    - id: bandit

      args: ['-c', 'pyproject.toml']
      additional_dependencies: ['bandit[toml]']
      exclude: '^tests/'          # Don't scan tests

```toml

**What It Does:**

- Scans code for common security issues
- Finds hardcoded passwords, SQL injection risks, etc.

**Common Issues Caught:**

```python

# Hardcoded password (B105)
password = "admin123"  # ❌ Security risk!

# SQL injection risk (B608)
query = f"SELECT * FROM users WHERE id = {user_id}"  # ❌ Use parameterized queries

# Using pickle (B301)
import pickle
data = pickle.loads(untrusted_data)  # ❌ Arbitrary code execution risk

# Using shell=True (B602)
subprocess.call(f"ls {user_input}", shell=True)  # ❌ Command injection risk

```bash

**Configuration:**

- `-c pyproject.toml`: Read config from pyproject.toml
- `additional_dependencies: ['bandit[toml]']`: Support TOML config
- `exclude: '^tests/'`: Skip tests (often have intentional security issues)

---

### Hook 7: markdownlint (Markdown Linting)

```yaml


- repo: https://github.com/igorshubovych/markdownlint-cli

  rev: v0.38.0
  hooks:

    - id: markdownlint

      args: ['--fix']

```markdown

**What It Does:**

- Enforces consistent Markdown formatting
- Auto-fixes common issues

**Common Issues:**

```markdown

# Missing blank lines around headers
Some text
## Header  ← Missing blank line before

# Inconsistent list markers
- Item 1
* Item 2  ← Mix of - and *

# Trailing spaces
Line with spaces at end

# Multiple blank lines


← Too many blank lines

```text

**Configuration:**

- `--fix`: Automatically fix issues when possible

---

### Hook 8: yamllint (YAML Linting)

```yaml


- repo: https://github.com/adrienverge/yamllint

  rev: v1.33.0
  hooks:

    - id: yamllint

      args: ['-d', '{extends: default, rules: {line-length: {max: 120}}}']

```yaml

**What It Does:**

- Validates YAML syntax and style
- Enforces consistent YAML formatting

**Common Issues:**

```yaml

# Inconsistent indentation
key:
    value  ← 4 spaces
  other: value  ← 2 spaces (inconsistent)

# Too long lines
very_long_key: "This line has way too many characters and exceeds the 120 character limit"

# Missing spaces
key:value  ← Should be "key: value"

# Trailing spaces
key: value   ← Spaces at end

```text

**Configuration:**

- `line-length: {max: 120}`: Allow up to 120 characters

---

## Common Pre-commit Workflows

### Initial Setup

```bash

# 1. Install pre-commit
pip install pre-commit

# 2. Install git hooks
pre-commit install

# 3. (Optional) Run on all files
pre-commit run --all-files

# Now every commit automatically runs checks!
```text

### Daily Development

```bash

# Make changes
vim src/my_module.py

# Try to commit
git add src/my_module.py
git commit -m "Add feature"

# Pre-commit runs automatically:
# - Formats code with Black
# - Sorts imports with isort
# - Runs flake8 linting
# - Type checks with mypy
# - Security scans with bandit
# - Fixes markdown/yaml issues

# If all pass: commit succeeds ✅
# If any fail: commit blocked, see error messages ❌
```yaml

### Fixing Failed Checks

```bash

# Pre-commit failed, what now?

# Option 1: Auto-fix (Black, isort, markdownlint fix automatically)
# Just re-stage and commit:
git add .
git commit -m "Add feature"

# Option 2: Manual fix (flake8, mypy, bandit require manual fixes)
# Fix the issues in your editor
vim src/my_module.py
git add src/my_module.py
git commit -m "Add feature"

# Option 3: Skip hooks (use sparingly!)
git commit -m "Add feature" --no-verify

```python

### Running Manually

```bash

# Run on all files
pre-commit run --all-files

# Run on specific files
pre-commit run --files src/my_module.py

# Run specific hook
pre-commit run black --all-files
pre-commit run flake8 --all-files
pre-commit run mypy --all-files

```text

### Updating Hooks

```bash

# Update all hooks to latest versions
pre-commit autoupdate

# Updates .pre-commit-config.yaml versions
# Example: rev: v4.5.0 → rev: v4.6.0
```yaml

---

## Best Practices

### 1. Install Pre-commit Hooks Immediately

```bash

# First thing after cloning repository:
git clone <repo>
cd <repo>
pip install -r requirements-dev.txt
pre-commit install  # ← Critical step!

```text

### 2. Run on All Files Initially

```bash

# Before first commit, clean up existing code:
pre-commit run --all-files

# This may find many issues in existing code
# Fix them all before proceeding
```text

### 3. Keep Hooks Updated

```bash

# Monthly or quarterly:
pre-commit autoupdate
git add .pre-commit-config.yaml
git commit -m "Update pre-commit hooks"

```yaml

### 4. Document How to Skip (For Emergencies)

Sometimes you need to commit even with failing checks:

```bash

# Skip all hooks (use rarely!)
git commit -m "WIP: Work in progress" --no-verify

# Better: Fix the issues before committing
```bash

### 5. Configure Hooks Consistently

Make sure hook configs match tool configs:

```yaml

# .pre-commit-config.yaml
- repo: https://github.com/psf/black

  hooks:

    - id: black

      args: ['--line-length=100']  # ← Match pyproject.toml

```yaml

```toml

# pyproject.toml
[tool.black]
line-length = 100  # ← Same as pre-commit args

```toml

### 6. Exclude Generated Files

```yaml

# Don't check auto-generated files
- repo: https://github.com/pre-commit/mirrors-mypy

  hooks:

    - id: mypy

      exclude: '^(tests/|migrations/|.*_pb2\.py$)'

```python

### 7. Use `--fix` Where Possible

```yaml

# Auto-fix issues instead of just reporting
- repo: https://github.com/psf/black

  hooks:

    - id: black  # Automatically formats

- repo: https://github.com/PyCQA/isort

  hooks:

    - id: isort  # Automatically sorts imports

- repo: https://github.com/igorshubovych/markdownlint-cli

  hooks:

    - id: markdownlint

      args: ['--fix']  # Automatically fixes markdown

```markdown

---

## Common Issues and Solutions

### Issue 1: Pre-commit Not Running

**Problem:**

```bash

git commit -m "Test"
# Hooks don't run
```bash

**Solution:**

```bash

# Install the git hooks
pre-commit install

# Verify installation
ls .git/hooks/pre-commit  # Should exist

```text

### Issue 2: Hooks Fail on CI but Not Locally

**Problem:**

- Pre-commit passes locally
- CI fails with pre-commit errors

**Solution:**

```bash

# Make sure you have the latest hooks locally
pre-commit autoupdate

# Run exactly what CI runs
pre-commit run --all-files

# Some hooks may behave differently on different OS
# Check Python version, tool versions
```python

### Issue 3: Too Slow

**Problem:**

```bash

# Pre-commit takes 30+ seconds every commit
```bash

**Solution:**

```yaml

# Option 1: Disable slow hooks for commits, run in CI instead
- repo: https://github.com/pre-commit/mirrors-mypy

  hooks:

    - id: mypy

      stages: [manual]  # Only run when explicitly called

# Then in CI:
# pre-commit run --all-files --hook-stage manual
```text

```yaml

# Option 2: Limit file scope
- repo: https://github.com/PyCQA/bandit

  hooks:

    - id: bandit

      files: '^src/'  # Only check src/, not tests/

```text

### Issue 4: Conflicts Between Tools

**Problem:**

```text

Black formats line one way
flake8 complains about Black's formatting

```text

**Solution:**

```yaml

# Configure flake8 to be compatible with Black
- repo: https://github.com/PyCQA/flake8

  hooks:

    - id: flake8

      args: [
        '--max-line-length=100',
        '--extend-ignore=E203,W503,E501'  # ← Ignore Black-incompatible rules
      ]

```text

### Issue 5: Failing on First Run with Many Errors

**Problem:**

```bash

pre-commit run --all-files
# 500+ errors from existing code
```bash

**Solution:**

```bash

# Approach 1: Fix incrementally
pre-commit run black --all-files      # Auto-fix formatting
pre-commit run isort --all-files      # Auto-fix imports
pre-commit run --all-files            # Now manually fix remaining

# Approach 2: Exclude existing code temporarily
```text

```yaml


- repo: https://github.com/PyCQA/flake8

  hooks:

    - id: flake8

      exclude: '^(old_code/|legacy/)'  # Exclude problematic directories

```yaml

---

## Pre-commit in CI/CD

Run pre-commit in GitHub Actions to ensure everyone follows rules:

```yaml

# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  pre-commit:
    runs-on: ubuntu-latest
    steps:

      - uses: actions/checkout@v3

      - uses: actions/setup-python@v4

        with:
          python-version: '3.11'

      - name: Run pre-commit

        uses: pre-commit/action@v3.0.0

```python

**Benefits:**

- Catches issues even if developers skip local hooks
- Enforces standards on all PRs
- Fast feedback (fails quickly if code doesn't meet standards)

---

## Summary

**Pre-commit Hooks:**

- ✅ Automatically run code quality checks before commits
- ✅ Catch issues early (before they reach the repository)
- ✅ Enforce consistent coding standards across team
- ✅ Auto-fix formatting issues (Black, isort, markdownlint)
- ✅ Prevent security issues, bugs, and style violations

**Our Configuration:**

1. **File cleanup**: Trailing whitespace, line endings, etc.
2. **Black**: Code formatting
3. **isort**: Import sorting

4. **flake8**: Linting
5. **mypy**: Type checking
6. **bandit**: Security scanning
7. **markdownlint**: Markdown formatting
8. **yamllint**: YAML validation

**Quick Setup:**

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files  # Initial cleanup

```bash

**Daily Use:**

```bash

# Just commit normally - hooks run automatically!
git commit -m "Add feature"

# If hooks fail, fix issues and recommit
```bash

---

## Makefile

### What It Is

A `Makefile` is a build automation file originally from C/C++ projects. In Python projects, it's used to **standardize common development tasks** with simple commands.

**Key Concept:** Type `make test` instead of remembering `pytest --cov=src --cov-report=term-missing tests/`

### Why It's Important

**Best Practice Reasons:**

1. **Standardization**: Everyone uses the same commands (`make test`, `make lint`)
2. **Documentation**: Self-documenting list of available tasks
3. **Simplicity**: Short commands instead of long CLI invocations

4. **Onboarding**: New developers see all tasks with `make help`
5. **Consistency**: Same commands work across all projects

### How It Works

```bash
# Developer types simple command
make test

# Make runs the configured command
pytest --cov=src/data_analysis --cov-report=term-missing tests/

```makefile

**Basic Syntax:**

```makefile

target: dependencies  ## Description
    command to run
    another command

```makefile

---

### Our Makefile Targets

#### Help and Discovery

```makefile

help:  ## Show this help message
 @echo "Available commands:"
 @grep -E '^[a-zA-Z_-]+:._?## ._$$' $(MAKEFILE_LIST) | sort | \
   awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

```makefile

**Usage:**

```bash

make help
# Shows all available commands with descriptions
```makefile

**Why:**

- ✅ Self-documenting Makefile
- ✅ New developers discover all tasks
- ✅ No need to read the Makefile source

---

#### Installation

```makefile

install:  ## Install package and dependencies
 pip install -e .

install-dev:  ## Install package with development dependencies
 pip install -e ".[dev,docs,test]"

```text

**Usage:**

```bash

# Production installation
make install

# Development installation (includes pytest, black, sphinx, etc.)
make install-dev

```makefile

**Why Two Targets?**

- `install`: Minimal install for using the package
- `install-dev`: Full install for development work

---

#### Testing

```makefile

test:  ## Run tests
 pytest tests/

test-verbose:  ## Run tests with verbose output
 pytest -v tests/

coverage:  ## Run tests with coverage report
 pytest --cov=src/data_analysis --cov-report=term-missing --cov-report=html tests/

```text

**Usage:**

```bash

# Quick test run
make test

# See detailed test output
make test-verbose

# Check code coverage
make coverage
# Opens htmlcov/index.html for detailed coverage report
```makefile

**Why:**

- ✅ Short commands instead of remembering pytest flags
- ✅ Consistent coverage configuration across team
- ✅ Easy to run comprehensive checks

---

#### Code Quality

```makefile

lint:  ## Run all linters (black check, isort check, flake8)
 black --check --diff src/ tests/
 isort --check-only --diff src/ tests/
 flake8 src/ tests/

format:  ## Format code with black and isort
 black src/ tests/
 isort src/ tests/

type-check:  ## Run type checker (mypy)
 mypy src/data_analysis/

security:  ## Run security checks (bandit and safety)
 bandit -r src/
 safety check

```text

**Usage:**

```bash

# Check code formatting (doesn't change files)
make lint

# Auto-format code
make format

# Check type hints
make type-check

# Security scan
make security

```makefile

**Why:**

- ✅ `lint` checks everything at once (Black, isort, flake8)
- ✅ `format` fixes formatting issues automatically
- ✅ Consistent quality checks across team
- ✅ Easy to run before committing

---

#### Documentation

```makefile

docs:  ## Build documentation
 cd docs && make html

docs-serve:  ## Build and serve documentation locally
 cd docs && make html && python -m http.server --directory _build/html 8000

```makefile

**Usage:**

```bash

# Build HTML documentation
make docs
# Output in docs/_build/html/

# Build and serve on http://localhost:8000
make docs-serve

```makefile

**Why:**

- ✅ Simplifies Sphinx build process
- ✅ `docs-serve` lets you preview docs in browser
- ✅ No need to remember Sphinx commands

---

#### Cleanup

```makefile

clean:  ## Clean up generated files
 rm -rf build/
 rm -rf dist/
 rm -rf *.egg-info
 rm -rf .pytest_cache/
 rm -rf .mypy_cache/
 rm -rf .coverage
 rm -rf htmlcov/
 rm -rf docs/_build/
 find . -type d -name __pycache__ -exec rm -rf {} +
 find . -type f -name "*.pyc" -delete

```python

**Usage:**

```bash

make clean

```makefile

**What It Removes:**

- Build artifacts (`build/`, `dist/`, `*.egg-info`)
- Test caches (`.pytest_cache/`, `.coverage`, `htmlcov/`)
- Type checker cache (`.mypy_cache/`)
- Python bytecode (`__pycache__/`, `*.pyc`)
- Documentation build (`docs/_build/`)

**Why:**

- ✅ Fresh start when troubleshooting
- ✅ Reduces repository size
- ✅ Removes stale artifacts

---

#### Building

```makefile

build:  ## Build package
 python -m build

```makefile

**Usage:**

```bash

make build
# Creates wheel and source distribution in dist/
```makefile

**Why:**

- ✅ Standardizes package building
- ✅ Prepares for PyPI upload
- ✅ Uses modern `build` tool (PEP 517)

---

#### Pre-commit

```makefile

pre-commit-install:  ## Install pre-commit hooks
 pre-commit install

pre-commit-run:  ## Run pre-commit hooks on all files
 pre-commit run --all-files

```text

**Usage:**

```bash

# One-time setup after cloning
make pre-commit-install

# Run all hooks manually
make pre-commit-run

```makefile

**Why:**

- ✅ Easy setup for new developers
- ✅ Convenient manual hook execution

---

#### Virtual Environment

```makefile

venv:  ## Create virtual environment
 python -m venv venv
 @echo "Virtual environment created. Activate with:"
 @echo "  Windows: .\\venv\\Scripts\\activate"
 @echo "  Unix/Mac: source venv/bin/activate"

```python

**Usage:**

```bash

make venv
# Creates venv/ directory
# Shows activation command for your OS
```makefile

**Why:**

- ✅ Consistent venv creation
- ✅ Reminds developers how to activate
- ✅ Cross-platform instructions

---

#### Composite Target

```makefile

all: format lint type-check test  ## Run format, lint, type-check, and test

```makefile

**Usage:**

```bash

make all
# Runs: format → lint → type-check → test
```makefile

**Why:**

- ✅ Run all quality checks before pushing
- ✅ One command for comprehensive validation
- ✅ CI/CD equivalent locally

---

## Makefile Syntax Basics

### Targets and Dependencies

```makefile

target: dependency1 dependency2
    command to run

```makefile

**Example:**

```makefile

test: install-dev  ## Run tests (requires dev dependencies)
    pytest tests/

```makefile

**Means:** "To run `test`, first run `install-dev`, then run pytest"

### .PHONY Declaration

```makefile

.PHONY: test lint clean

```makefile

**Why:**

- Tells Make these are **commands**, not **files**
- Without `.PHONY`, Make checks if file named "test" exists
- With `.PHONY`, Make always runs the command

### Variables

```makefile

PYTHON := python3
SRC_DIR := src/

test:
    $(PYTHON) -m pytest $(SRC_DIR)

```python

**Benefits:**

- Change Python version in one place
- Reuse paths across targets
- Make Makefile configurable

### Comments and Help Text

```makefile

target:  ## This appears in help output
    # This is a regular comment
    command

```makefile

- `##` after target: Shown in `make help`
- `#` on its own line: Internal comment

---

## Platform Considerations

### Unix/Linux/Mac

```bash

# Make is pre-installed
make test

```makefile

### Windows

**Option 1: Install Make**

```powershell

# Using Chocolatey
choco install make

# Using Scoop
scoop install make

```makefile

**Option 2: Use PowerShell Scripts**

Create `scripts/test.ps1`:

```powershell

pytest tests/

```bash

Run with:

```powershell

.\scripts\test.ps1

```bash

**Option 3: Use Cross-Platform Task Runners**

- **invoke**: Python-based task runner
- **poetry scripts**: Built into Poetry
- **nox**: Test automation tool

**Our Approach:**
We use Makefile because:

- ✅ Universal on Unix systems (Linux, Mac, WSL)
- ✅ Well-known standard
- ✅ Simple syntax
- ✅ Easy to install on Windows

---

## Best Practices

### 1. Always Use .PHONY

```makefile
.PHONY: test lint clean  # ✅ GOOD

# Without .PHONY:
# If file named "test" exists, Make won't run command
```makefile

### 2. Provide Help Target

```makefile

help:  ## Show available commands
 @grep -E '^[a-zA-Z_-]+:._?## ._$$' $(MAKEFILE_LIST) | \
   awk 'BEGIN {FS = ":.*?## "}; {printf "%-20s %s\n", $$1, $$2}'

# Developers run: make help
```makefile

### 3. Make Help the Default Target

```makefile

.DEFAULT_GOAL := help

help:  ## Show available commands
    ...

```makefile

**Why:**

- Typing just `make` shows help
- Great for onboarding

### 4. Use Composite Targets

```makefile

all: format lint type-check test  ## Run all checks

ci: lint type-check test  ## CI pipeline (no formatting)

```makefile

**Benefits:**

- `make all`: Local comprehensive check
- `make ci`: Same as CI runs

### 5. Keep Commands Cross-Platform

```makefile

# ❌ BAD: Unix-specific
clean:
    rm -rf build/

# ✅ BETTER: Still Unix-specific but documented
clean:  ## Clean generated files (requires Unix shell)
    rm -rf build/

# ✅ BEST: Provide alternative
clean:  ## Clean generated files
 python scripts/clean.py  # Works everywhere

```python

### 6. Document Each Target

```makefile

# ❌ BAD
test:
    pytest

# ✅ GOOD
test:  ## Run test suite with pytest
    pytest tests/

```text

### 7. Use Consistent Naming

**Common Patterns:**

- `install`, `install-dev`: Installation
- `test`, `test-verbose`, `coverage`: Testing
- `lint`, `format`, `type-check`: Quality
- `docs`, `docs-serve`: Documentation
- `build`, `publish`: Packaging
- `clean`: Cleanup

---

## Common Makefile Patterns

### Pattern 1: Environment Setup

```makefile

setup: venv install-dev pre-commit-install  ## Complete development setup
 @echo "✅ Development environment ready!"
 @echo "Run 'make help' to see available commands"

```makefile

**Usage:**

```bash

# New developer setup
make setup
# Creates venv, installs deps, installs hooks
```makefile

### Pattern 2: Watch Mode

```makefile

watch-test:  ## Run tests on file changes
 pytest-watch tests/

```makefile

### Pattern 3: Docker Integration

```makefile

docker-build:  ## Build Docker image
 docker build -t myproject:latest .

docker-test:  ## Run tests in Docker
 docker run myproject:latest pytest

```text

### Pattern 4: CI Simulation

```makefile

ci: lint type-check test  ## Run CI checks locally
 @echo "✅ All CI checks passed!"

```makefile

---

## Alternatives to Makefiles

### Option 1: Python Scripts

**scripts/run.py:**

```python

import sys

def test():
    """Run tests"""
    import subprocess
    subprocess.run(["pytest", "tests/"])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/run.py [test|lint|format]")
    elif sys.argv[1] == "test":
        test()

```python

**Pros:**

- ✅ Pure Python (no Make dependency)
- ✅ Works on all platforms

**Cons:**

- ❌ More verbose
- ❌ Not industry standard

### Option 2: invoke

```python

# tasks.py
from invoke import task

@task
def test(c):
    """Run tests"""
    c.run("pytest tests/")

@task
def lint(c):
    """Run linters"""
    c.run("black --check src/")

```text

**Usage:**

```bash

invoke test
invoke lint

```bash

**Pros:**

- ✅ Python-based
- ✅ Cross-platform
- ✅ Rich features

**Cons:**

- ❌ Additional dependency
- ❌ Less familiar than Make

### Option 3: Poetry Scripts

```toml

# pyproject.toml
[tool.poetry.scripts]
test = "pytest:main"

[tool.poetry.dev-dependencies]
pytest = "^7.4.0"

```text

**Usage:**

```bash

poetry run test

```bash

**Pros:**

- ✅ Built into Poetry
- ✅ No extra files

**Cons:**

- ❌ Only works with Poetry
- ❌ Limited to Python commands

### Option 4: Just

```just

# justfile
test:
    pytest tests/

lint:
    black --check src/

```text

**Usage:**

```bash

just test
just lint

```bash

**Pros:**

- ✅ Make-like syntax
- ✅ Modern features
- ✅ Cross-platform

**Cons:**

- ❌ Less common
- ❌ Additional installation

### Our Choice: Makefile

**Why:**

- ✅ Industry standard (developers know Make)
- ✅ Simple and readable
- ✅ No runtime dependencies (just Make)
- ✅ Works on all Unix systems
- ✅ Easy to install on Windows
- ✅ Perfect for command standardization

---

## Common Issues

### Issue 1: "make: command not found" on Windows

**Solution:**

```powershell
# Install Make with Chocolatey
choco install make

# Or use WSL (Windows Subsystem for Linux)
wsl
make test

```makefile

### Issue 2: Tabs vs Spaces

**Problem:**

```makefile

test:  ## Run tests
    pytest tests/  ← Must be tab, not spaces

```makefile

**Error:**

```makefile

Makefile:2: *** missing separator. Stop.

```makefile

**Solution:**

- Makefile commands **MUST** be indented with **tabs**
- Configure editor to use tabs in Makefiles
- In VS Code: File → Preferences → Settings → "Insert Spaces" → disable for Makefiles

### Issue 3: Target Not Running

**Problem:**

```bash

make test
# make: 'test' is up to date.
```makefile

**Cause:**
File named "test" exists in directory

**Solution:**

```makefile

.PHONY: test  # ← Add this

```makefile

### Issue 4: Variables Not Expanding

**Problem:**

```makefile

TEST_DIR = tests/
test:
    pytest $TEST_DIR  # ❌ Doesn't work

```makefile

**Solution:**

```makefile

TEST_DIR := tests/
test:
    pytest $(TEST_DIR)  # ✅ Works

```makefile

---

## Summary

**Makefiles for Python:**

- ✅ Standardize common tasks with short commands
- ✅ Self-documenting with `make help`
- ✅ Simplify onboarding for new developers
- ✅ Consistent across projects and teams
- ✅ Industry-standard build automation

**Our Targets:**

- **Installation**: `install`, `install-dev`, `venv`
- **Testing**: `test`, `test-verbose`, `coverage`
- **Quality**: `lint`, `format`, `type-check`, `security`
- **Documentation**: `docs`, `docs-serve`
- **Maintenance**: `clean`, `build`
- **Utilities**: `help`, `pre-commit-install`, `all`

**Quick Start:**

```bash
# See all available commands
make help

# Development setup
make venv
source venv/bin/activate  # Unix
# or: .\venv\Scripts\activate  # Windows
make install-dev
make pre-commit-install

# Daily workflow
make format  # Format code
make all     # Run all checks
make test    # Run tests

# Before pushing
make all     # Ensure everything passes

```makefile

**Remember:**

- Use tabs (not spaces) for command indentation
- Always declare `.PHONY` targets
- Provide `help` target with `##` comments
- Keep commands simple and well-documented

---

## .github/workflows/ci.yml

### What It Is

`.github/workflows/ci.yml` defines a **GitHub Actions CI/CD pipeline** that automatically runs tests, checks code quality, builds documentation, and packages your project whenever code is pushed or pull requests are created.

**Key Concept:** Automated quality gates that run on GitHub's servers every time you push code.

### Why It's Important

**Best Practice Reasons:**

1. **Automated Testing**: Tests run automatically on every change
2. **Multi-Environment**: Test on Linux, Windows, and macOS simultaneously
3. **Quality Gates**: Block merges if tests fail

4. **Catch Issues Early**: Find problems before they reach main branch
5. **Documentation**: Always have up-to-date docs
6. **Transparency**: Everyone sees test results

### How It Works

```text
Developer pushes code → GitHub receives push
                            ↓
GitHub Actions triggered (on: push)
                            ↓
Parallel job execution:
  ├─ Lint (Black, isort, flake8, mypy)
  ├─ Test (12 combinations: 3 OS × 4 Python versions)
  ├─ Security (bandit, safety)
  └─ Docs (Sphinx build)
                            ↓
Sequential jobs (after tests pass):
  ├─ Coverage (collect coverage reports)
  └─ Build (create package)
                            ↓
Notify (report results)
                            ↓
✅ All pass: Green checkmark on commit
❌ Any fail: Red X + detailed error logs

```text

---

### Workflow Triggers

```yaml

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
  workflow_dispatch:

```text

**What Triggers Our Workflow:**

1. **`push` to main/develop**: Every commit to these branches runs CI
2. **`pull_request` to main/develop**: All PRs run CI before merge
3. **`workflow_dispatch`**: Manual trigger from GitHub UI

**Why These Triggers:**

- ✅ `push`: Ensure main/develop always passes tests
- ✅ `pull_request`: Prevent broken code from merging
- ✅ `workflow_dispatch`: Allow manual reruns

---

### Job 1: Lint (Code Quality Checks)

```yaml

lint:
  name: Code Quality Checks
  runs-on: ubuntu-latest

```yaml

**What It Does:**

- Runs formatting checks (Black)
- Checks import sorting (isort)
- Lints code (flake8)
- Type checks (mypy)

**Steps:**

1. **Checkout code**: `actions/checkout@v4`
2. **Set up Python 3.11**: `actions/setup-python@v5`
3. **Install dependencies**: Install from requirements.txt

4. **Run checks**:

   ```bash
   black --check src/ tests/
   isort --check-only src/ tests/
   flake8 src/ tests/ --max-line-length=100
   mypy src/ --ignore-missing-imports

```bash

**Why `continue-on-error: true`:**

- Allows all checks to run (doesn't stop at first failure)
- See all issues at once

**Why Run on `ubuntu-latest`:**

- Linting is OS-independent
- Linux is fastest/cheapest GitHub Actions runner

---

### Job 2: Test (Test Suite with Matrix)

```yaml

test:
  name: Test Suite
  runs-on: ${{ matrix.os }}
  strategy:
    fail-fast: false
    matrix:
      os: [ubuntu-latest, windows-latest, macos-latest]
      python-version: ['3.9', '3.10', '3.11', '3.12']

```python

**What It Does:**

- Runs tests on **12 combinations**:

  - 3 Operating Systems (Ubuntu, Windows, macOS)

  - 4 Python Versions (3.9, 3.10, 3.11, 3.12)
- Tests both unit and integration tests

**Matrix Strategy:**

| OS | Python 3.9 | Python 3.10 | Python 3.11 | Python 3.12 |
|----|-----------|-------------|-------------|-------------|
| Ubuntu | ✅ Job 1 | ✅ Job 2 | ✅ Job 3 | ✅ Job 4 |
| Windows | ✅ Job 5 | ✅ Job 6 | ✅ Job 7 | ✅ Job 8 |
| macOS | ✅ Job 9 | ✅ Job 10 | ✅ Job 11 | ✅ Job 12 |

**Why Matrix Testing:**

- ✅ **Cross-platform compatibility**: Ensures code works on Windows, Mac, Linux
- ✅ **Python version support**: Confirms support for all claimed Python versions
- ✅ **Find OS-specific bugs**: Path separators, line endings, etc.
- ✅ **Python version bugs**: API changes between versions

**Why `fail-fast: false`:**

```yaml
strategy:
  fail-fast: false

```yaml

- Runs ALL 12 combinations even if one fails
- See which specific OS/Python combos have issues
- Without this: first failure cancels remaining jobs

**Steps:**

1. **Checkout code**: `actions/checkout@v4`
2. **Set up Python**: `actions/setup-python@v5` with matrix version
3. **Cache pip**: `cache: 'pip'` speeds up dependency installation

4. **Install dependencies**
5. **Run unit tests**: `pytest tests/unit/ -v`
6. **Run integration tests**: `pytest tests/integration/ -v`

---

### Job 3: Coverage (Code Coverage Report)

```yaml

coverage:
  name: Code Coverage
  runs-on: ubuntu-latest
  needs: test

```yaml

**What It Does:**

- Runs tests with coverage measurement
- Uploads coverage report to Codecov
- Stores HTML coverage report as artifact

**Why `needs: test`:**

- Runs **after** test job completes
- No point measuring coverage if tests fail

**Steps:**

1. **Run tests with coverage**:

   ```bash
   pytest --cov=src/data_analysis \
          --cov-report=xml \
          --cov-report=html \
          --cov-report=term

```bash

2. **Upload to Codecov**:

   ```yaml

   - uses: codecov/codecov-action@v4

     with:
       file: ./coverage.xml
       fail_ci_if_error: false

```yaml

   - Codecov shows coverage trends over time

   - `fail_ci_if_error: false`: Don't fail if upload fails

3. **Upload HTML report**:

   ```yaml

   - uses: actions/upload-artifact@v4

     with:
       name: coverage-report
       path: htmlcov/

```yaml

   - Download from GitHub Actions UI

   - View detailed coverage locally

**Why Run Coverage Separately:**

- Coverage slows down tests (~20-30%)
- Only need one coverage report (not 12 from matrix)

---

### Job 4: Security (Security Scanning)

```yaml

security:
  name: Security Scan
  runs-on: ubuntu-latest

```yaml

**What It Does:**

- **Safety**: Checks for known vulnerabilities in dependencies
- **Bandit**: Scans code for security issues

**Steps:**

1. **Safety check**:

   ```bash
   safety check --json

```bash

   - Checks requirements.txt against vulnerability database

   - Finds: CVEs in pandas, numpy, requests, etc.

2. **Bandit check**:

   ```bash
   bandit -r src/ -f json

```bash

   - Scans Python code for security issues

   - Finds: hardcoded passwords, SQL injection, pickle usage

**Why `continue-on-error: true`:**

- Reports issues but doesn't fail CI
- Security warnings shouldn't block development
- Review warnings and fix when appropriate

**Example Issues Found:**

```text

Safety:
  → requests==2.25.0 has vulnerability CVE-2021-33503

Bandit:
  → src/auth.py:42: Hardcoded password detected (B105)
  → src/db.py:18: SQL injection risk (B608)

```python

---

### Job 5: Docs (Documentation Build)

```yaml

docs:
  name: Documentation Build
  runs-on: ubuntu-latest

```yaml

**What It Does:**

- Builds Sphinx documentation
- Verifies no build errors
- Uploads HTML documentation as artifact

**Steps:**

1. **Build docs**:

   ```bash
   cd docs
   make html

```makefile

2. **Upload documentation**:

   ```yaml

   - uses: actions/upload-artifact@v4

     with:
       name: documentation
       path: docs/_build/html/

```yaml

**Why Build Docs in CI:**

- ✅ Catch Sphinx errors early
- ✅ Broken links, missing references
- ✅ Always have latest docs available
- ✅ Preview docs before merge

**Accessing Built Docs:**

1. Go to GitHub Actions run
2. Scroll to "Artifacts" section
3. Download "documentation" artifact

4. Open `index.html` in browser

---

### Job 6: Build (Package Building)

```yaml

build:
  name: Build Package
  runs-on: ubuntu-latest
  needs: [lint, test]

```yaml

**What It Does:**

- Builds Python package (wheel + source distribution)
- Validates package with twine
- Uploads artifacts

**Why `needs: [lint, test]`:**

- Only build if code passes quality checks
- Don't waste time building broken code

**Steps:**

1. **Build package**:

   ```bash
   python -m build

```bash

   - Creates: `dist/data_analysis-0.1.0-py3-none-any.whl`

   - Creates: `dist/data_analysis-0.1.0.tar.gz`

2. **Check package**:

   ```bash
   twine check dist/*

```bash

   - Validates PyPI requirements

   - Checks README rendering

   - Validates metadata

3. **Upload artifacts**:

   ```yaml

   - uses: actions/upload-artifact@v4

     with:
       name: dist-packages
       path: dist/

```yaml

**Why Build in CI:**

- ✅ Ensure package builds successfully
- ✅ Validate before PyPI upload
- ✅ Test installation from built package

---

### Job 7: Notify (Status Notification)

```yaml

notify:
  name: Notification
  runs-on: ubuntu-latest
  needs: [lint, test, coverage, security, docs, build]
  if: always()

```text

**What It Does:**

- Runs **after all other jobs**
- Reports status of each job
- Always runs (even if jobs fail)

**Why `if: always()`:**

- Runs even when previous jobs fail
- Ensures notification happens

**Output Example:**

```text

Lint: success
Test: success
Coverage: success
Security: success
Docs: success
Build: success

```text

**Future Enhancements:**

- Send Slack notification
- Post PR comment
- Update status badge

---

## GitHub Actions Concepts

### Actions vs Workflows vs Jobs vs Steps

```text

Workflow (ci.yml)
├─ Job 1: lint
│  ├─ Step 1: Checkout code (uses action)
│  ├─ Step 2: Setup Python (uses action)
│  └─ Step 3: Run linter (run command)
├─ Job 2: test
│  └─ ...
└─ Job 3: build
   └─ ...

```bash

**Definitions:**

- **Workflow**: The entire CI/CD pipeline (ci.yml file)
- **Job**: A set of steps that run on the same runner
- **Step**: Individual task within a job
- **Action**: Reusable step (from marketplace or custom)

### Job Dependencies

```yaml

# Jobs run in parallel by default
lint:       # Runs immediately
  ...
test:       # Runs immediately (parallel with lint)
  ...

# Sequential execution with needs
coverage:
  needs: test    # Waits for test to complete
  ...

build:
  needs: [lint, test]  # Waits for BOTH lint and test
  ...

```text

**Our Dependency Graph:**

```text

                  ┌─────┐
                  │Start│
                  └──┬──┘
                     │
      ┌──────────────┼──────────────┐
      │              │              │
   ┌──▼──┐      ┌───▼───┐     ┌───▼────┐
   │Lint │      │ Test  │     │Security│
   └──┬──┘      └───┬───┘     └────────┘
      │             │
      │      ┌──────▼──────┐
      │      │  Coverage   │
      │      └─────────────┘
      │             │
      └──────┬──────┘
             │
        ┌────▼────┐       ┌──────┐
        │  Build  │       │ Docs │
        └────┬────┘       └──────┘
             │                │
             └────────┬───────┘
                      │
                 ┌────▼─────┐
                 │  Notify  │
                 └──────────┘

```text

### Caching

```yaml


- name: Set up Python

  uses: actions/setup-python@v5
  with:
    python-version: '3.11'
    cache: 'pip'  # ← Caches pip dependencies

```python

**What Gets Cached:**

- Pip packages from `requirements.txt`
- Cache key based on file hash
- Invalidates when requirements change

**Benefits:**

- ⏱️ Faster installs (30s → 5s)
- 💰 Reduced bandwidth
- 🚀 Faster feedback

**Cache Locations:**

- Pip: `~/.cache/pip`
- Pre-commit: `~/.cache/pre-commit`

### Matrix Strategies

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    python-version: ['3.9', '3.10', '3.11', '3.12']

```yaml

**Creates 12 Jobs:**

- Each combination runs independently
- Parallelized (runs simultaneously)
- GitHub shows results in matrix view

**Advanced Matrix:**

```yaml

strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    python-version: ['3.9', '3.11']
    include:

      - os: macos-latest

        python-version: '3.11'  # Only test Python 3.11 on macOS
    exclude:

      - os: windows-latest

        python-version: '3.9'   # Skip Windows + Python 3.9

```python

**Use Cases:**

- Test multiple Python versions
- Test multiple databases (postgres, mysql, sqlite)
- Test multiple dependency versions

---

## Secrets and Environment Variables

### Using Secrets

```yaml

steps:

  - name: Deploy to PyPI

    env:
      PYPI_TOKEN: ${{ secrets.PYPI_TOKEN }}
    run: |
      twine upload dist/* --username __token__ --password $PYPI_TOKEN

```python

**Setting Secrets:**

1. Go to GitHub repo → Settings → Secrets
2. Click "New repository secret"
3. Name: `PYPI_TOKEN`

4. Value: `pypi-AgEIcHlwaS5vcmcC...`

**Why Use Secrets:**

- 🔒 Never committed to repository
- 🔒 Encrypted in GitHub
- 🔒 Masked in logs
- 🔒 Only accessible during workflow

### Environment Variables

```yaml

env:
  PYTHON_VERSION: '3.11'
  DATABASE_URL: 'sqlite:///test.db'

jobs:
  test:
    env:
      TEST_ENV: 'ci'
    steps:

      - run: echo "Python: $PYTHON_VERSION"

      - run: echo "Test Env: $TEST_ENV"

```python

**Scopes:**

- **Workflow-level**: Available in all jobs
- **Job-level**: Available in all steps of that job
- **Step-level**: Available only in that step

---

## Artifacts

### Uploading Artifacts

```yaml


- name: Upload coverage report

  uses: actions/upload-artifact@v4
  with:
    name: coverage-report
    path: htmlcov/
    retention-days: 30

```text

**What Are Artifacts:**

- Files generated during workflow
- Available for download after run completes
- Examples: coverage reports, logs, built packages

**Our Artifacts:**

1. **coverage-report**: HTML coverage report
2. **documentation**: Built Sphinx docs
3. **dist-packages**: Python wheels and source distributions

### Downloading Artifacts

**From GitHub UI:**

1. Go to Actions tab
2. Click on workflow run
3. Scroll to "Artifacts" section

4. Click artifact name to download

**In Other Jobs:**

```yaml
jobs:
  build:
    steps:

      - name: Build package

        run: python -m build

      - name: Upload package

        uses: actions/upload-artifact@v4
        with:
          name: my-package
          path: dist/

  publish:
    needs: build
    steps:

      - name: Download package

        uses: actions/download-artifact@v4
        with:
          name: my-package
          path: dist/

      - name: Publish to PyPI

        run: twine upload dist/*

```text

---

## Best Practices

### 1. Use Caching

```yaml


- name: Set up Python

  uses: actions/setup-python@v5
  with:
    python-version: '3.11'
    cache: 'pip'  # ✅ Enables pip caching

```python

**Benefits:**

- ⏱️ 5-10x faster dependency installation
- 💰 Reduces GitHub Actions minutes usage

### 2. Pin Action Versions

```yaml

# ❌ BAD: Uses latest (can break unexpectedly)
- uses: actions/checkout@v4

# ✅ GOOD: Pin to specific version
- uses: actions/checkout@v4.1.1

# ✅ ALSO GOOD: Pin to major version (gets patches)
- uses: actions/checkout@v4

```text

**Why Pin:**

- Prevents unexpected breaking changes
- Reproducible builds
- Security (review before upgrading)

### 3. Use fail-fast Appropriately

```yaml

strategy:
  fail-fast: false  # ✅ For test matrix (see all failures)

jobs:
  validate:
    steps:

      - run: black --check

      - run: flake8

        continue-on-error: false  # ✅ Fail immediately on lint errors

```text

**Guidelines:**

- `fail-fast: false` for matrix testing (see all OS/Python issues)
- `fail-fast: true` (default) for sequential pipelines

### 4. Separate Fast and Slow Jobs

```yaml

jobs:
  quick-checks:  # Runs in 30 seconds
    steps:

      - run: black --check

      - run: flake8

  slow-tests:    # Runs in 5 minutes
    needs: quick-checks  # Only run if quick checks pass
    steps:

      - run: pytest

```text

**Benefits:**

- Fast feedback (know about lint errors in 30s)
- Don't waste time running slow tests if quick checks fail

### 5. Use Job Dependencies Wisely

```yaml

jobs:
  lint:
    # No dependencies - runs immediately

  test:
    # No dependencies - runs in parallel with lint

  build:
    needs: [lint, test]  # Waits for both

  deploy:
    needs: build  # Sequential deployment

```text

**Guidelines:**

- Run independent jobs in parallel (faster)
- Use `needs` for logical dependencies
- Don't over-use `needs` (causes unnecessary waiting)

### 6. Keep Workflows DRY

**Use Composite Actions:**

```yaml

# .github/actions/setup-python/action.yml
name: 'Setup Python Environment'
runs:
  using: 'composite'
  steps:

    - uses: actions/setup-python@v5

      with:
        python-version: '3.11'
        cache: 'pip'

    - run: pip install -r requirements.txt

      shell: bash

```bash

**Use in Workflows:**

```yaml

jobs:
  test:
    steps:

      - uses: ./.github/actions/setup-python

      - run: pytest

```python

### 7. Add Status Badges

```markdown

# README.md
![CI](https://github.com/username/repo/workflows/CI%2FCD%20Pipeline/badge.svg)

```markdown

**Benefits:**

- Shows build status on README
- Quickly see if main branch is passing
- Builds confidence in project quality

---

## Common Patterns

### Pattern 1: Multi-Stage Pipeline

```yaml

jobs:
  test:
    # Stage 1: Test

  build:
    needs: test
    # Stage 2: Build (only if tests pass)

  deploy-staging:
    needs: build
    if: github.ref == 'refs/heads/develop'
    # Stage 3: Deploy to staging

  deploy-production:
    needs: build
    if: github.ref == 'refs/heads/main'
    # Stage 3: Deploy to production

```text

### Pattern 2: Conditional Execution

```yaml

jobs:
  deploy:
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    # Only deploy on push to main

```yaml

**Common Conditions:**

- `github.ref == 'refs/heads/main'`: Only main branch
- `github.event_name == 'pull_request'`: Only PRs
- `github.actor != 'dependabot[bot]'`: Exclude Dependabot
- `startsWith(github.ref, 'refs/tags/')`: Only tags

### Pattern 3: Manual Approval

```yaml

deploy:
  environment:
    name: production
    url: https://example.com
  steps:

    - run: ./deploy.sh

```text

**Setup:**

1. Go to Settings → Environments → production
2. Enable "Required reviewers"
3. Add team members

**Workflow:**

- Job waits at deployment step
- Reviewer clicks "Approve" in GitHub UI
- Deployment proceeds

---

## Common Issues

### Issue 1: Tests Pass Locally, Fail in CI

**Possible Causes:**

1. **Different Python versions**

   ```yaml
   # Solution: Match local version

   - uses: actions/setup-python@v5

     with:
       python-version: '3.11'  # Same as local

```yaml

2. **Missing dependencies**

   ```bash
   # Solution: Verify requirements.txt is complete
   pip freeze > requirements.txt

```bash

3. **Environment-specific code**

   ```python
   # Bad: Assumes specific paths
   with open('/home/user/data.csv') as f:

   # Good: Use relative paths
   with open('data/data.csv') as f:

```text

### Issue 2: Slow CI Runs

**Solutions:**

1. **Enable caching**

   ```yaml

   - uses: actions/setup-python@v5

     with:
       cache: 'pip'

```yaml

2. **Reduce matrix size**

   ```yaml
   # Before: 12 jobs (3 OS × 4 Python)
   matrix:
     os: [ubuntu-latest, windows-latest, macos-latest]
     python-version: ['3.9', '3.10', '3.11', '3.12']

   # After: 4 jobs
   matrix:
     os: [ubuntu-latest]
     python-version: ['3.9', '3.12']  # Only test min and max

```python

3. **Parallelize better**

   ```yaml
   # Run lint, test, docs in parallel (not sequential)

```yaml

### Issue 3: Secrets Not Working

**Problem:**

```yaml

env:
  API_KEY: ${{ secrets.API_KEY }}  # Empty/not found

```yaml

**Solutions:**

1. **Check secret name matches exactly**

   - Secrets are case-sensitive

   - `API_KEY` ≠ `api_key`

2. **Verify secret is set**

   - Settings → Secrets → Check if listed

3. **Check scope**

   - Repository secrets: Available in that repo only

   - Organization secrets: Available in all repos

   - Environment secrets: Only in specific environment

---

## Summary

**GitHub Actions CI/CD:**

- ✅ Automated testing on every push/PR
- ✅ Multi-platform testing (Linux, Windows, macOS)
- ✅ Multi-version testing (Python 3.9-3.12)
- ✅ Quality gates (linting, type checking, security)
- ✅ Artifact generation (coverage, docs, packages)
- ✅ Parallel execution for speed

**Our Workflow (7 Jobs):**

1. **Lint**: Code quality checks (Black, isort, flake8, mypy)
2. **Test**: 12-job matrix (3 OS × 4 Python versions)
3. **Coverage**: Coverage reporting to Codecov

4. **Security**: Vulnerability scanning (safety, bandit)
5. **Docs**: Sphinx documentation build
6. **Build**: Package building and validation
7. **Notify**: Status reporting

**Key Features:**

- **Matrix testing**: 12 combinations tested in parallel
- **Caching**: Faster runs with pip cache
- **Artifacts**: Coverage reports, docs, packages available for download
- **Job dependencies**: Logical execution order
- **Fail-fast**: See all failures at once

**Quick Reference:**

```yaml
# Trigger workflow
on: [push, pull_request]

# Matrix testing
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    python-version: ['3.9', '3.11']

# Caching
- uses: actions/setup-python@v5

  with:
    cache: 'pip'

# Job dependencies
needs: [lint, test]

# Upload artifacts
- uses: actions/upload-artifact@v4

  with:
    name: my-artifact
    path: dist/

```text

---

## LICENSE

### What It Is

The `LICENSE` file contains the **software license** that legally defines how others can use, modify, and distribute your code.

**Key Concept:** Without a license, your code is under exclusive copyright by default—nobody can legally use it!

### Why It's Important

**Legal and Practical Reasons:**

1. **Clarifies Permissions**: Explicitly states what others can/cannot do
2. **Protects Contributors**: Limits liability for bugs or issues
3. **Enables Collaboration**: People know they can safely use/contribute

4. **Required for Distribution**: PyPI, npm require license specification
5. **Open Source Compliance**: GitHub shows license badge
6. **Professional Standards**: Expected in all public repositories

**Without a License:**

- ❌ All rights reserved (default copyright)
- ❌ Nobody can legally use your code
- ❌ Cannot include in other projects
- ❌ Risky for companies to use

**With a License:**

- ✅ Clear legal framework
- ✅ Encourages contributions
- ✅ Reduces legal risk
- ✅ Shows professionalism

### Our License: MIT License

We use the **MIT License**—one of the most permissive open-source licenses.

**Full License Text:**

```text
MIT License

Copyright (c) 2024 Data Analysis Project Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```text

### Understanding the MIT License

**What the MIT License Allows:**

1. ✅ **Commercial use**: Use in commercial products
2. ✅ **Modification**: Change the code however you want
3. ✅ **Distribution**: Share modified or unmodified copies

4. ✅ **Private use**: Use in private projects
5. ✅ **Sublicense**: Include in projects with different licenses

**What the MIT License Requires:**

1. ⚠️ **Include copyright notice**: Must include the MIT License text
2. ⚠️ **Include license**: Must include this license in all copies

**What the MIT License Does NOT Allow:**

1. ❌ **Liability**: Authors are not liable for damages
2. ❌ **Warranty**: No warranty—software provided "as-is"

### Why We Chose MIT

**MIT License Benefits:**

1. **Simplicity**: Short, easy to understand
2. **Permissive**: Very few restrictions
3. **Popular**: Used by jQuery, Node.js, Rails, React

4. **Business-friendly**: Companies comfortable using MIT-licensed code
5. **Compatible**: Works with almost any other license
6. **No copyleft**: Users don't have to open-source their modifications

**MIT vs Other Licenses:**

| Aspect | MIT | Apache 2.0 | GPL v3 | BSD |
|--------|-----|------------|--------|-----|
| **Permissiveness** | Very high | High | Low (copyleft) | Very high |
| **Patent protection** | No | Yes | Yes | No |
| **Requires attribution** | Yes | Yes | Yes | Yes |
| **Copyleft** | No | No | Yes | No |
| **Length** | ~200 words | ~10,000 words | ~5,000 words | ~150 words |
| **Business-friendly** | ✅ Yes | ✅ Yes | ⚠️ Sometimes | ✅ Yes |

---

## Common Open Source Licenses

### 1. MIT License (Our Choice)

**Best For:** Most projects wanting maximum adoption

**Characteristics:**

- ✅ Very permissive
- ✅ Simple and short
- ✅ Business-friendly
- ❌ No patent protection

**Used By:** jQuery, Node.js, Rails, React, Angular, Vue.js

**When to Choose:**

- You want maximum code reuse
- You don't care if others commercialize your code
- You want simplicity

### 2. Apache License 2.0

**Best For:** Projects concerned about patents

**Characteristics:**

- ✅ Permissive
- ✅ Explicit patent grant
- ✅ Business-friendly
- ⚠️ Longer/more complex

**Used By:** Android, Apache projects, Kubernetes, TensorFlow

**When to Choose:**

- Patent protection is important
- You want permissive license with more legal clarity
- Corporate contributions likely

**Key Difference from MIT:**

```text
Apache 2.0 includes explicit patent grant:
"If you sue anyone for patent infringement related to this software,
your license terminates."

```text

### 3. GNU General Public License (GPL) v3

**Best For:** Projects requiring derivative works to be open-source

**Characteristics:**

- ⚠️ Strong copyleft
- ✅ Patent protection
- ⚠️ Requires derivatives to be GPL
- ❌ Complex (~5,000 words)

**Used By:** Linux kernel (v2), Git, GIMP, WordPress

**When to Choose:**

- You want all derivatives to remain open-source
- You want to prevent proprietary forks
- You're building on GPL code

**Copyleft Requirement:**

```text
If you modify GPL code and distribute it:
→ You MUST release source code
→ You MUST use GPL license
→ Users MUST have same freedoms

```text

**Business Implications:**

- ❌ Many companies avoid GPL dependencies
- ❌ Cannot use in proprietary software
- ✅ Ensures community benefits from improvements

### 4. BSD Licenses (2-Clause and 3-Clause)

**Best For:** Projects wanting maximum freedom

**Characteristics:**

- ✅ Extremely permissive
- ✅ Very short
- ✅ No copyleft
- ❌ No patent protection

**Used By:** FreeBSD, Python (in part), Django

**Difference from MIT:**

- Very similar to MIT
- Slightly different wording
- 3-Clause BSD has non-endorsement clause

### 5. Mozilla Public License (MPL) 2.0

**Best For:** File-level copyleft

**Characteristics:**

- ⚠️ Weak copyleft (file-level)
- ✅ Can mix with proprietary code
- ✅ Patent grant
- ⚠️ More complex

**Used By:** Firefox, Thunderbird, LibreOffice

**When to Choose:**

- You want copyleft on YOUR files only
- Allow proprietary additions
- Middle ground between MIT and GPL

### 6. Unlicense / Public Domain

**Best For:** Maximum freedom (no restrictions at all)

**Characteristics:**

- ✅ No restrictions whatsoever
- ✅ No attribution required
- ⚠️ Public domain may not exist in all jurisdictions

**Used By:** Small utilities, SQLite

**When to Choose:**

- You want absolutely no restrictions
- You don't care about attribution
- Educational/reference code

---

## Choosing a License

### Decision Tree

```text
Do you want derivatives to be open-source?
├─ YES → Use copyleft license
│         ├─ Strong copyleft → GPL v3
│         ├─ Weak copyleft → MPL 2.0
│         └─ Network copyleft → AGPL v3
│
└─ NO → Use permissive license
          ├─ Need patent protection → Apache 2.0
          ├─ Want simplicity → MIT or BSD
          └─ No restrictions at all → Unlicense

```text

### Quick Guide

**Choose MIT if:**

- ✅ You want maximum adoption
- ✅ You want simplicity
- ✅ You're okay with commercial use without giving back

**Choose Apache 2.0 if:**

- ✅ Patent protection matters
- ✅ You expect corporate contributions
- ✅ You want explicit patent grant

**Choose GPL v3 if:**

- ✅ You want derivatives to be open-source
- ✅ You're building on GPL code
- ✅ You want to prevent proprietary forks

**Choose BSD if:**

- ✅ You want maximum permissiveness
- ✅ You prefer BSD wording over MIT

**Choose MPL 2.0 if:**

- ✅ You want file-level copyleft
- ✅ You want to allow proprietary additions
- ✅ Middle ground between MIT and GPL

---

## How to Add a License

### Step 1: Choose Your License

Visit [choosealicense.com](https://choosealicense.com/) for guidance.

### Step 2: Create LICENSE File

```bash
# Create LICENSE file in project root
touch LICENSE

```bash

### Step 3: Add License Text

**For MIT License:**

```text

MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```text

**Replace:**

- `[year]` → Current year (e.g., `2024`)
- `[fullname]` → Your name or organization (e.g., `Data Analysis Project Contributors`)

### Step 4: Specify in pyproject.toml

```toml

[project]
name = "data-analysis"
license = {text = "MIT"}
# Or if you have LICENSE file:
# license = {file = "LICENSE"}
```text

### Step 5: Add to setup.py (if using)

```python

setup(
    name="data-analysis",
    license="MIT",
    # ...
)

```text

### Step 6: Mention in README

```markdown

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```markdown

---

## License Compatibility

### Can You Combine Code from Different Licenses?

**General Rules:**

1. **MIT + MIT** → ✅ Yes, use MIT
2. **MIT + Apache 2.0** → ✅ Yes, use Apache 2.0
3. **MIT + GPL** → ⚠️ Yes, but result must be GPL

4. **Apache 2.0 + GPL v3** → ✅ Yes, result must be GPL v3
5. **GPL v2 + GPL v3** → ❌ No (incompatible)

### Permissive → Copyleft (One-Way Street)

```text

MIT/Apache → GPL v3  ✅ Allowed
GPL v3 → MIT/Apache  ❌ Not allowed

(Copyleft "infects" the combined work)

```text

### Multiple Licenses in One Project

**Option 1: Dual License**

```text

This project is dual-licensed under:

- MIT License (for permissive use)
- GPL v3 (for copyleft use)

Users can choose which license to follow.

```text

**Example:** SQLite (public domain OR proprietary license)

**Option 2: Different Licenses for Different Files**

```text

src/core/       → MIT License
src/gpl_module/ → GPL v3 License
(Entire project becomes GPL because of copyleft)

```text

---

## License Headers in Source Files

### Should You Add License Headers?

**Short Answer:** Optional for MIT, recommended for Apache/GPL.

**MIT License:**

```python

# Copyright (c) 2024 Data Analysis Project Contributors
# SPDX-License-Identifier: MIT
```python

**Apache License 2.0:**

```python

# Copyright 2024 Data Analysis Project Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
```text

**GPL v3:**

```python

# Copyright (C) 2024  Data Analysis Project Contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
```text

### SPDX License Identifiers

**Modern Best Practice:** Use SPDX identifiers

```python

# SPDX-License-Identifier: MIT
```python

**Benefits:**

- ✅ Machine-readable
- ✅ Short (one line)
- ✅ Standardized
- ✅ Supported by GitHub

---

## Common Questions

### Q1: Can I change the license later?

**Answer:** Yes, but complicated.

- ✅ You can relicense YOUR code
- ❌ You cannot relicense contributors' code without permission
- ✅ You can dual-license going forward

**Best Practice:**

- Include Contributor License Agreement (CLA) if you might relicense
- Get agreement from ALL contributors
- Or use permissive license from start

### Q2: What if I don't add a license?

**Answer:** All rights reserved (default copyright)

- ❌ Nobody can legally use your code
- ❌ Nobody can fork your repository
- ❌ Nobody can contribute safely

**Exception:** GitHub public repos have implicit right to view/fork, but NOT to use.

### Q3: Can I use MIT-licensed code in my proprietary product?

**Answer:** Yes!

- ✅ You can use MIT code commercially
- ✅ You can keep your modifications private
- ⚠️ You MUST include the MIT License notice

**Example:**

```text
MyProduct/
├── src/
│   └── mycode.py          (Your proprietary code)
├── vendor/
│   └── mitlibrary/        (MIT-licensed)
│       └── LICENSE        (Must include this)
└── NOTICES.txt            (List all third-party licenses)

```python

### Q4: Do I need a lawyer?

**Answer:** Usually no for standard licenses.

- ✅ MIT, Apache, GPL are well-established
- ✅ No legal review needed for standard use
- ⚠️ Consult lawyer for:

  - Custom licenses

  - License changes

  - Combining incompatible licenses

  - Commercial concerns

---

## Best Practices

### 1. Always Include a License

```bash

# Every repository should have:
LICENSE           # ← License text
README.md         # ← Link to license
pyproject.toml    # ← License identifier

```bash

### 2. Use Standard Licenses

**❌ Don't:**

- Write your own license
- Modify standard licenses
- Mix license fragments

**✅ Do:**

- Use well-known licenses (MIT, Apache, GPL)
- Use exact license text
- Reference by name

### 3. Specify License in Multiple Places

**Checklist:**

- [ ] `LICENSE` file in root
- [ ] `license` in `pyproject.toml`
- [ ] License badge in `README.md`
- [ ] License mention in documentation

### 4. Check Dependencies' Licenses

```bash
# Check licenses of your dependencies
pip-licenses

```bash

**Example Output:**

```bash

 Name       Version  License
 pandas     2.2.0    BSD 3-Clause
 numpy      1.26.3   BSD 3-Clause
 requests   2.31.0   Apache 2.0

```bash

**Watch Out For:**

- ❌ GPL dependencies (if you're MIT)
- ❌ Proprietary licenses
- ❌ Unknown/missing licenses

### 5. Document License Exceptions

**Example:**

```markdown

# Licenses

This project is licensed under the MIT License.

## Exceptions

- `src/vendored/gpl_module/` is licensed under GPL v3
- `data/` content is licensed under CC BY 4.0

```text

---

## License Badges

### Adding License Badge to README

**MIT License:**

```markdown

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

```markdown

**Apache 2.0:**

```markdown

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

```markdown

**GPL v3:**

```markdown

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

```markdown

**Result:**
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## Summary

**The LICENSE File:**

- ✅ Legally defines usage rights
- ✅ Required for all public repositories
- ✅ Essential for open-source projects
- ✅ Protects authors from liability

**Our Choice (MIT License):**

- ✅ Very permissive
- ✅ Simple and short
- ✅ Business-friendly
- ✅ Maximum adoption

**Key Licenses:**

1. **MIT**: Permissive, simple (our choice)
2. **Apache 2.0**: Permissive + patent protection
3. **GPL v3**: Copyleft (requires derivatives to be open-source)

4. **BSD**: Very permissive, similar to MIT
5. **MPL 2.0**: Weak copyleft (file-level)

**Choosing a License:**

- Want max adoption → MIT
- Need patent protection → Apache 2.0
- Want derivatives open → GPL v3
- Want file-level copyleft → MPL 2.0

**Remember:**

- Always include a LICENSE file
- Use standard licenses (don't write your own)
- Check dependency licenses
- Specify license in pyproject.toml
- Add license badge to README

---

_This guide is part of the Data Analysis Best Practices project documentation._
