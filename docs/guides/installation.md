# Installation Guide

This guide provides detailed instructions for installing the Data Analysis Project on different operating systems and environments.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Installation](#quick-installation)
- [Detailed Installation Steps](#detailed-installation-steps)

  - [Windows Installation](#windows-installation)

  - [macOS Installation](#macos-installation)

  - [Linux Installation](#linux-installation)
- [Verifying Installation](#verifying-installation)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)

## Prerequisites

Before installing, ensure you have:

1. **Python 3.9 or higher** installed

   - Check version: `python --version` or `python3 --version`

   - Download from: [python.org](https://www.python.org/downloads/)

2. **pip** (Python package installer)

   - Usually included with Python

   - Check version: `pip --version` or `pip3 --version`

3. **Git** (for cloning the repository)

   - Check version: `git --version`

   - Download from: [git-scm.com](https://git-scm.com/downloads)

   - See our [Git & GitHub Guide](git_github_guide.md) if you're new to Git

4. **Basic command-line knowledge**

   - Navigating directories

   - Running commands

   - Setting environment variables

## Quick Installation

For experienced users, here's the quick version:

```bash
# Clone repository
git clone https://github.com/yourusername/best_practice_project.git
cd best_practice_project

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows: .\venv\Scripts\activate
# Unix/macOS: source venv/bin/activate

# Install package
pip install -e .

# Or with development tools
pip install -e ".[dev,docs,test]"

```bash

## Detailed Installation Steps

### Windows Installation

#### Step 1: Install Python

1. Download Python from [python.org](https://www.python.org/downloads/windows/)
2. Run the installer
3. **Important**: Check "Add Python to PATH" during installation

4. Click "Install Now"
5. Verify installation:

   ```powershell
   python --version

```text

#### Step 2: Install Git

1. Download Git from [git-scm.com](https://git-scm.com/download/win)
2. Run the installer with default settings
3. Verify installation:

   ```powershell
   git --version

```text

#### Step 3: Clone the Repository

```powershell

# Open PowerShell or Command Prompt
# Navigate to your desired directory
cd C:\Users\YourUsername\Projects

# Clone the repository
git clone https://github.com/yourusername/best_practice_project.git

# Navigate into the project
cd best_practice_project

```text

#### Step 4: Create Virtual Environment

```powershell

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# You should see (venv) in your prompt
```text

#### Step 5: Install the Package

```powershell

# For regular use
pip install -e .

# For development (includes testing, linting, documentation tools)
pip install -e ".[dev,docs,test]"

```text

#### Step 6: Verify Installation

```powershell

# Test import
python -c "from data_analysis import DataLoader; print('Success!')"

# Run tests
pytest

# Check installed packages
pip list

```text

### macOS Installation

#### Step 1: Install Homebrew (if not installed)

```bash

# Open Terminal
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

```bash

#### Step 2: Install Python

```bash

# Install Python using Homebrew
brew install python@3.9

# Verify installation
python3 --version

```text

#### Step 3: Install Git

```bash

# Git is usually pre-installed on macOS
# If not, install with Homebrew
brew install git

# Verify installation
git --version

```text

#### Step 4: Clone the Repository

```bash

# Navigate to your projects directory
cd ~/Projects

# Clone the repository
git clone https://github.com/yourusername/best_practice_project.git

# Navigate into the project
cd best_practice_project

```text

#### Step 5: Create Virtual Environment

```bash

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your prompt
```text

#### Step 6: Install the Package

```bash

# For regular use
pip install -e .

# For development
pip install -e ".[dev,docs,test]"

```text

#### Step 7: Verify Installation

```bash

# Test import
python -c "from data_analysis import DataLoader; print('Success!')"

# Run tests
pytest

# Check installed packages
pip list

```bash

### Linux Installation

#### Step 1: Install Python and pip

##### Ubuntu/Debian

```bash

# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3.9 python3.9-venv python3-pip

# Verify installation
python3 --version
pip3 --version

```text

##### Fedora/CentOS

```bash

# Install Python and pip
sudo dnf install python39 python3-pip

# Verify installation
python3 --version
pip3 --version

```text

##### Arch Linux

```bash

# Install Python and pip
sudo pacman -S python python-pip

# Verify installation
python --version
pip --version

```text

#### Step 2: Install Git

```bash

# Ubuntu/Debian
sudo apt install git

# Fedora/CentOS
sudo dnf install git

# Arch Linux
sudo pacman -S git

# Verify installation
git --version

```text

#### Step 3: Clone the Repository

```bash

# Navigate to your projects directory
cd ~/projects

# Clone the repository
git clone https://github.com/yourusername/best_practice_project.git

# Navigate into the project
cd best_practice_project

```text

#### Step 4: Create Virtual Environment

```bash

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your prompt
```text

#### Step 5: Install the Package

```bash

# For regular use
pip install -e .

# For development
pip install -e ".[dev,docs,test]"

```text

#### Step 6: Verify Installation

```bash

# Test import
python -c "from data_analysis import DataLoader; print('Success!')"

# Run tests
pytest

# Check installed packages
pip list

```bash

## Verifying Installation

After installation, verify everything works correctly:

### 1. Check Python Package

```python

# Start Python interactive shell
python

# Try importing the package
>>> from data_analysis import DataLoader, DataCleaner, DataAnalyzer, Visualizer
>>> print("All modules imported successfully!")
>>> exit()

```text

### 2. Run Tests

```bash

# Run all tests
pytest

# You should see all tests passing
# Example output:
# ==================== test session starts ====================
# collected 47 items
#
# tests/unit/test_data_loader.py ........        [ 17%]
# tests/unit/test_data_cleaner.py ..........     [ 38%]
# tests/unit/test_data_analyzer.py ..........    [ 60%]
# tests/unit/test_visualizer.py ..........       [ 81%]
# tests/integration/test_pipeline.py ........    [100%]
#
# ==================== 47 passed in 5.23s ====================
```text

### 3. Check Installed Packages

```bash

pip list | grep data-analysis
# Should show: data-analysis 0.1.0
```text

### 4. Test Basic Functionality

Create a test script `test_install.py`:

```python

from data_analysis import DataLoader
import pandas as pd

# Create sample data
data = {'name': ['Alice', 'Bob'], 'age': [25, 30]}
df = pd.DataFrame(data)

# Test DataLoader
loader = DataLoader()
loader.save_csv(df, 'test_output.csv')
loaded_df = loader.load_csv('test_output.csv')

print(f"Original shape: {df.shape}")
print(f"Loaded shape: {loaded_df.shape}")
print("Installation verified successfully!")

# Cleanup
import os
os.remove('test_output.csv')

```text

Run the test:

```bash

python test_install.py

```bash

## Troubleshooting

### Common Issues

#### Issue: "Python is not recognized"

**Solution:**

- Windows: Add Python to PATH environment variable

  1. Search for "Environment Variables" in Windows

  2. Edit "Path" in System Variables

  3. Add Python installation directory

  4. Restart terminal

#### Issue: "pip is not recognized"

**Solution:**

```bash

# Windows
python -m pip --version

# Unix/macOS
python3 -m pip --version

# If pip is missing, install it:
python -m ensurepip --upgrade

```text

#### Issue: "No module named 'data_analysis'"

**Solution:**

- Ensure virtual environment is activated (you should see `(venv)` in prompt)
- Try reinstalling:

  ```bash
  pip install -e .

```text

- Check if you're in the correct directory (project root)

#### Issue: "Permission denied" (Unix/macOS)

**Solution:**

```bash

# Don't use sudo! Instead use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -e .

```text

#### Issue: Tests fail with "ModuleNotFoundError"

**Solution:**

```bash

# Install with test dependencies
pip install -e ".[test]"

# Or install pytest manually
pip install pytest pytest-cov pytest-mock

```text

#### Issue: "SSL Certificate Error"

**Solution:**

```bash

# Upgrade pip
pip install --upgrade pip

# Or temporarily disable SSL verification (not recommended)
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -e .

```text

#### Issue: Slow installation on Windows

**Solution:**

- Disable Windows Defender real-time protection temporarily
- Use a faster mirror:

  ```bash
  pip install -e . -i https://pypi.tuna.tsinghua.edu.cn/simple

```bash

### Getting Help

If you encounter issues not covered here:

1. **Check existing issues**: [GitHub Issues](https://github.com/yourusername/best_practice_project/issues)
2. **Search discussions**: [GitHub Discussions](https://github.com/yourusername/best_practice_project/discussions)
3. **Create a new issue**: Include error messages, OS, Python version

4. **Read the FAQ**: [docs/FAQ.md](FAQ.md)

## Next Steps

After successful installation:

1. **Read the User Guide**: [user_guide.md](user_guide.md)
2. **Explore Examples**: Check `notebooks/example_analysis.ipynb`
3. **Learn Git/GitHub**: [git_github_guide.md](git_github_guide.md) (if contributing)

4. **Try the Quick Start**: Run examples from README

### For Contributors

If you plan to contribute to the project:

```bash
# Install development dependencies
pip install -e ".[dev,docs,test]"

# Install pre-commit hooks
pre-commit install

# Read the contributing guide
# See CONTRIBUTING.md
```text

### For Users

If you just want to use the package:

```bash

# Install minimal dependencies
pip install -e .

# Or install from PyPI (when published)
pip install data-analysis

```bash

## Understanding Virtual Environments

### What is a Virtual Environment?

A virtual environment is an isolated Python environment that:

- Keeps project dependencies separate
- Prevents conflicts between projects
- Makes projects portable

### Managing Virtual Environments

```bash

# Create virtual environment
python -m venv venv

# Activate
# Windows:
.\venv\Scripts\activate
# Unix/macOS:
source venv/bin/activate

# Deactivate (when done)
deactivate

# Delete virtual environment (just delete the folder)
# Windows:
rmdir /s venv
# Unix/macOS:
rm -rf venv

```bash

### When to Use Virtual Environments

**Always!** Benefits include:

- Reproducible environments
- Clean dependency management
- Easy project sharing
- No system pollution

## Installation Checklist

Use this checklist to ensure proper installation:

- [ ] Python 3.9+ installed and in PATH
- [ ] pip installed and working
- [ ] Git installed (if cloning repository)
- [ ] Repository cloned or downloaded
- [ ] Virtual environment created
- [ ] Virtual environment activated
- [ ] Package installed (`pip install -e .`)
- [ ] Test imports work (`from data_analysis import ...`)
- [ ] Tests pass (`pytest`)
- [ ] Example notebook runs (optional)

---

**Congratulations!** You've successfully installed the Data Analysis Project. Happy analyzing! 🎉
