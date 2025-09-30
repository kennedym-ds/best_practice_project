# Git and GitHub Guide for Beginners

A comprehensive guide to version control with Git and GitHub, designed for complete beginners.

## Table of Contents

1. [Introduction](#introduction)
2. [Understanding Version Control](#understanding-version-control)
3. [Installing Git](#installing-git)

4. [Git Basics](#git-basics)
5. [Working with Branches](#working-with-branches)
6. [GitHub Fundamentals](#github-fundamentals)
7. [Collaboration Workflow](#collaboration-workflow)
8. [Best Practices](#best-practices)
9. [Common Scenarios](#common-scenarios)
10. [Troubleshooting](#troubleshooting)
11. [Additional Resources](#additional-resources)

## Introduction

### What is Git?

**Git** is a distributed version control system that tracks changes in your code over time. Think of it as a time machine for your code - you can:

- Save snapshots of your work at any point
- Go back to previous versions
- See what changed and when
- Work on multiple features simultaneously
- Collaborate with others without conflicts

### What is GitHub?

**GitHub** is a web-based platform that hosts Git repositories online. It provides:

- A place to store your code in the cloud
- Tools for collaboration (pull requests, issues, reviews)
- Project management features
- A portfolio of your work
- Integration with many development tools

### Why Use Version Control?

Version control is essential for:

- **Safety**: Never lose your work
- **History**: Track all changes with context
- **Collaboration**: Work with others efficiently
- **Experimentation**: Try new ideas without risk
- **Professional workflow**: Industry standard practice

## Understanding Version Control

### Key Concepts

#### Repository (Repo)

A repository is a folder that Git tracks. It contains:

- Your project files
- A hidden `.git` folder with all version history
- Metadata about your project

#### Commit

A commit is a snapshot of your project at a specific point in time. Each commit:

- Records what changed
- Includes a message describing the change
- Has a unique ID (SHA hash)
- Links to the previous commit

#### Branch

A branch is an independent line of development. Branches let you:

- Work on features without affecting the main code
- Experiment safely
- Develop multiple features simultaneously
- Review changes before merging

#### Remote

A remote is a version of your repository hosted elsewhere (like GitHub). It allows:

- Backup of your code
- Collaboration with others
- Access from multiple computers

### How Git Works

```text
Working Directory  →  Staging Area  →  Repository
(Your files)          (Ready to commit)  (Committed history)

1. Edit files         2. Stage changes   3. Commit changes

   (modify code)         (git add)          (git commit)

```

**Working Directory**: Where you edit files
**Staging Area (Index)**: Where you prepare changes for commit
**Repository**: Where Git stores committed history

## Installing Git

### Windows

#### Option 1: Official Installer (Recommended)

1. Download Git from [git-scm.com](https://git-scm.com/download/win)
2. Run the installer
3. Use recommended settings (default options are fine)

4. Verify installation:

```powershell

git --version

```

#### Option 2: Using Winget

```powershell

winget install --id Git.Git -e --source winget

```

### macOS

#### Option 1: Using Homebrew (Recommended)

```bash

# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Git
brew install git

```

#### Option 2: Official Installer

1. Download from [git-scm.com](https://git-scm.com/download/mac)
2. Run the installer

#### Option 3: Xcode Command Line Tools

```bash

xcode-select --install

```

Verify installation:

```bash

git --version

```

### Linux

#### Ubuntu/Debian

```bash

sudo apt update
sudo apt install git

```

#### Fedora/CentOS

```bash

sudo dnf install git

```

#### Arch Linux

```bash

sudo pacman -S git

```

Verify installation:

```bash

git --version

```

### Initial Configuration

After installing Git, configure your identity:

```bash

# Set your name
git config --global user.name "Your Name"

# Set your email
git config --global user.email "your.email@example.com"

# Set default branch name
git config --global init.defaultBranch main

# Set default editor (optional)
git config --global core.editor "code --wait"  # VS Code
# or
git config --global core.editor "nano"  # Nano editor

# View your configuration
git config --list

```

## Git Basics

### Creating a Repository

#### Starting a new project

```bash

# Create a new directory
mkdir my-project
cd my-project

# Initialize Git repository
git init

# Your project is now a Git repository!
```

#### Cloning an existing repository

```bash

# Clone from GitHub
git clone https://github.com/username/repository.git

# Clone into a specific folder
git clone https://github.com/username/repository.git my-folder

```

### Checking Repository Status

```bash

# See current status
git status

# Shows:
# - Which branch you're on
# - Which files have changes
# - Which files are staged
# - Which files are untracked
```

### The Basic Workflow

#### 1. Make changes to your files

Edit files in your favorite editor.

#### 2. Check what changed

```bash

# See which files changed
git status

# See specific changes
git diff

# See changes for a specific file
git diff filename.py

```

#### 3. Stage your changes

```bash

# Stage a specific file
git add filename.py

# Stage all changed files
git add .

# Stage multiple specific files
git add file1.py file2.py

# Stage all files of a certain type
git add *.py

```

#### 4. Commit your changes

```bash

# Commit with message
git commit -m "Add new feature"

# Commit with detailed message
git commit -m "Add user authentication

- Add login form
- Add password validation
- Add session management"

# Stage and commit in one step (only for tracked files)
git commit -am "Fix typo in README"

```

### Viewing History

```bash

# View commit history
git log

# View compact history
git log --oneline

# View history with graph
git log --graph --oneline --all

# View history for specific file
git log filename.py

# View changes in each commit
git log -p

# View last N commits
git log -5  # Last 5 commits

```

### Viewing Commit Details

```bash

# Show details of latest commit
git show

# Show specific commit
git show abc123

# Show changes in specific file from commit
git show abc123:path/to/file.py

```

### Undoing Changes

#### Discard changes in working directory

```bash

# Discard changes in specific file
git checkout -- filename.py

# Discard all changes
git checkout -- .

# Modern syntax (Git 2.23+)
git restore filename.py
git restore .

```

#### Unstage files

```bash

# Unstage specific file
git reset HEAD filename.py

# Unstage all files
git reset HEAD

# Modern syntax (Git 2.23+)
git restore --staged filename.py

```

#### Amend last commit

```bash

# Fix last commit message
git commit --amend -m "Corrected message"

# Add forgotten files to last commit
git add forgotten_file.py
git commit --amend --no-edit

```

## Working with Branches

### Why Use Branches?

Branches allow you to:

- Develop features independently
- Keep main code stable
- Experiment without risk
- Work on multiple features simultaneously

### Creating and Switching Branches

```bash

# Create a new branch
git branch feature-login

# Switch to branch
git checkout feature-login

# Create and switch in one command
git checkout -b feature-login

# Modern syntax (Git 2.23+)
git switch feature-login           # Switch to existing branch
git switch -c feature-login        # Create and switch to new branch

```

### Viewing Branches

```bash

# List local branches
git branch

# List all branches (including remote)
git branch -a

# List branches with latest commit
git branch -v

# See which branches are merged
git branch --merged
git branch --no-merged

```

### Merging Branches

```bash

# Switch to target branch (usually main)
git checkout main

# Merge feature branch into current branch
git merge feature-login

# Merge with no fast-forward (creates merge commit)
git merge --no-ff feature-login

```

### Deleting Branches

```bash

# Delete merged branch
git branch -d feature-login

# Force delete unmerged branch
git branch -D feature-login

# Delete remote branch
git push origin --delete feature-login

```

### Handling Merge Conflicts

When Git can't automatically merge changes, you'll get a conflict:

```bash

# 1. Git will tell you there's a conflict
git merge feature-branch
# Auto-merging file.py
# CONFLICT (content): Merge conflict in file.py

# 2. Check which files have conflicts
git status

# 3. Open the conflicted file
# You'll see markers like this:
# <<<<<<< HEAD
# Your current changes
# =======
# Incoming changes
# >>>>>>> feature-branch

# 4. Edit the file to resolve conflicts
# Remove the markers and keep the correct code

# 5. Stage the resolved file
git add file.py

# 6. Complete the merge
git commit -m "Resolve merge conflict"

```

## GitHub Fundamentals

### Creating a GitHub Account

1. Go to [github.com](https://github.com)
2. Click "Sign up"
3. Follow the registration process

4. Verify your email address

### Creating a Repository on GitHub

#### Web Interface

1. Click the "+" icon in top right
2. Select "New repository"
3. Fill in details:

   - Repository name

   - Description (optional)

   - Public or Private

   - Initialize with README (optional)

4. Click "Create repository"

#### From Command Line

```bash
# Create repository on GitHub using GitHub CLI
gh repo create my-project --public

# Or push existing local repository
git remote add origin https://github.com/username/my-project.git
git push -u origin main

```

### Connecting Local and Remote Repositories

```bash

# Add remote
git remote add origin https://github.com/username/repository.git

# View remotes
git remote -v

# Change remote URL
git remote set-url origin https://github.com/username/new-repository.git

# Remove remote
git remote remove origin

```

### Pushing to GitHub

```bash

# Push to remote repository
git push origin main

# Push and set upstream (first time)
git push -u origin main

# After setting upstream, just use
git push

# Push all branches
git push --all origin

# Push with tags
git push --tags

```

### Pulling from GitHub

```bash

# Fetch and merge changes
git pull origin main

# After setting upstream
git pull

# Fetch without merging
git fetch origin

# View fetched changes
git log origin/main

```

### Cloning Repositories

```bash

# Clone repository
git clone https://github.com/username/repository.git

# Clone specific branch
git clone -b branch-name https://github.com/username/repository.git

# Clone with different name
git clone https://github.com/username/repository.git my-folder

```

## Collaboration Workflow

### Forking a Repository

**Forking** creates your own copy of someone else's repository.

1. Go to the repository on GitHub
2. Click "Fork" button (top right)
3. GitHub creates a copy in your account

4. Clone your fork:

```bash

git clone https://github.com/YOUR-USERNAME/repository.git
cd repository

```

5. Add original repository as upstream:

```bash

git remote add upstream https://github.com/ORIGINAL-OWNER/repository.git

```

### Keeping Your Fork Updated

```bash

# Fetch changes from upstream
git fetch upstream

# Switch to main branch
git checkout main

# Merge upstream changes
git merge upstream/main

# Push to your fork
git push origin main

```

### Creating Pull Requests

**Pull Requests (PRs)** propose changes to a repository.

#### Process

1. **Create a branch for your changes**:

```bash

git checkout -b fix-typo

```

2. **Make your changes and commit**:

```bash

git add README.md
git commit -m "Fix typo in README"

```

3. **Push to your fork**:

```bash

git push origin fix-typo

```

4. **Create PR on GitHub**:

   - Go to your fork on GitHub

   - Click "Pull requests" tab

   - Click "New pull request"

   - Select your branch

   - Fill in title and description

   - Click "Create pull request"

#### Good PR Practices

- **Clear title**: "Fix typo in README" not "Update file"
- **Detailed description**: Explain what and why
- **Small changes**: Easier to review
- **One concern per PR**: Don't mix unrelated changes
- **Tests**: Include tests for new features
- **Documentation**: Update docs if needed

### Reviewing Pull Requests

As a reviewer:

1. Read the description
2. Check the "Files changed" tab
3. Add comments on specific lines

4. Test the changes locally if needed:

```bash
# Fetch PR to local branch
git fetch origin pull/123/head:pr-123
git checkout pr-123

```

5. Approve or request changes
6. Merge if approved

### Issues

**Issues** track bugs, features, and tasks.

#### Creating an Issue

1. Go to repository on GitHub
2. Click "Issues" tab
3. Click "New issue"

4. Fill in:

   - Title (clear and concise)

   - Description (what, why, how to reproduce)

   - Labels (bug, feature, documentation, etc.)

5. Click "Submit new issue"

#### Good Issue Examples

**Bug Report**:

```text
Title: Login button not working on mobile

Description:
When clicking the login button on mobile devices, nothing happens.

Steps to reproduce:

1. Open app on mobile browser
2. Navigate to login page
3. Click login button

Expected: Login form submits
Actual: Nothing happens

Browser: Chrome Mobile 120
OS: Android 13

```

**Feature Request**:

```text

Title: Add dark mode support

Description:
Add a dark mode theme option to reduce eye strain in low-light conditions.

Proposed solution:

- Add theme toggle in settings
- Save preference in localStorage
- Use CSS variables for colors

```

## Best Practices

### Commit Messages

#### Format

```text

<type>: <subject>

<body>

<footer>

```

#### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code formatting (no logic change)
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance tasks

#### Good Examples

```bash

# Simple commit
git commit -m "feat: add user login form"

# Detailed commit
git commit -m "fix: resolve database connection timeout

The connection pool was exhausted under heavy load.
Increased pool size from 10 to 50 connections.

Fixes #123"

# Breaking change
git commit -m "refactor: change API response format

BREAKING CHANGE: Response now returns data in 'payload' field
instead of root level. Update client code accordingly."

```

#### Commit Message Tips

- Use imperative mood: "add feature" not "added feature"
- Keep first line under 50 characters
- Separate subject from body with blank line
- Wrap body at 72 characters
- Explain what and why, not how
- Reference issues: "Fixes #123" or "Closes #456"

### When to Commit

**Commit often**:

- After completing a logical unit of work
- Before taking a break
- After fixing a bug
- After adding a feature

**Don't commit**:

- Broken code (unless work-in-progress marker)
- Generated files
- Sensitive data (passwords, API keys)
- Large binary files (use Git LFS)

### Branching Strategy

#### Feature Branch Workflow

```bash
main                 o---o---o---o---o
                          \         /
feature-login              o---o---o

```

1. Create branch from `main`
2. Develop feature
3. Merge back to `main`

#### Naming Conventions

- `feature/user-authentication`
- `fix/database-connection`
- `docs/api-reference`
- `refactor/payment-system`
- `hotfix/security-vulnerability`

### What to Commit

#### .gitignore File

Create a `.gitignore` file to exclude files:

```gitignore

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
*.egg-info/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# Environment
.env
.env.local

# OS
.DS_Store
Thumbs.db

# Project specific
outputs/
*.log
data/raw/

```

#### Commit

- Source code
- Configuration files
- Documentation
- Tests
- Build scripts

#### Don't commit

- Dependencies (`node_modules/`, `venv/`)
- Build artifacts (`dist/`, `build/`)
- Environment variables (`.env`)
- IDE settings (`.vscode/`, `.idea/`)
- Log files
- Temporary files
- Large data files

### Collaboration Etiquette

- **Pull before push**: Always pull latest changes before pushing
- **Review your changes**: Check `git diff` before committing
- **Write tests**: Include tests for new code
- **Update documentation**: Keep docs in sync with code
- **Be responsive**: Respond to PR comments promptly
- **Be respectful**: Constructive feedback only
- **Keep PRs small**: Easier to review
- **Don't force push**: To shared branches

## Common Scenarios

### Starting a New Project

```bash
# 1. Create directory
mkdir my-project
cd my-project

# 2. Initialize Git
git init

# 3. Create initial files
echo "# My Project" > README.md
echo "*.pyc" > .gitignore

# 4. Initial commit
git add .
git commit -m "Initial commit"

# 5. Create GitHub repository (using GitHub CLI or web interface)
gh repo create my-project --public

# 6. Push to GitHub
git remote add origin https://github.com/username/my-project.git
git push -u origin main

```

### Contributing to an Open Source Project

```bash

# 1. Fork repository on GitHub (click Fork button)

# 2. Clone your fork
git clone https://github.com/YOUR-USERNAME/project.git
cd project

# 3. Add upstream remote
git remote add upstream https://github.com/ORIGINAL-OWNER/project.git

# 4. Create feature branch
git checkout -b fix-bug

# 5. Make changes
# ... edit files ...

# 6. Commit changes
git add .
git commit -m "fix: resolve issue with login"

# 7. Push to your fork
git push origin fix-bug

# 8. Create Pull Request on GitHub

# 9. Keep fork updated
git fetch upstream
git checkout main
git merge upstream/main
git push origin main

```

### Fixing a Mistake

#### Wrong commit message

```bash

# Fix last commit message
git commit --amend -m "Correct message"

```

#### Forgot to add files

```bash

# Add files to last commit
git add forgotten_file.py
git commit --amend --no-edit

```

#### Committed to wrong branch

```bash

# On wrong branch
git log  # Copy commit hash (abc123)

# Switch to correct branch
git checkout correct-branch
git cherry-pick abc123

# Go back and remove from wrong branch
git checkout wrong-branch
git reset --hard HEAD~1

```

#### Want to undo last commit

```bash

# Undo commit, keep changes
git reset HEAD~1

# Undo commit, discard changes
git reset --hard HEAD~1

```

### Working with Multiple Remotes

```bash

# Add multiple remotes
git remote add origin https://github.com/you/project.git
git remote add upstream https://github.com/original/project.git
git remote add colleague https://github.com/colleague/project.git

# Push to specific remote
git push origin main
git push colleague feature-branch

# Fetch from specific remote
git fetch upstream
git fetch colleague

```

## Troubleshooting

### Common Errors and Solutions

#### "Permission denied (publickey)"

**Problem**: SSH key not set up

**Solution**:

```bash

# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Start SSH agent
eval "$(ssh-agent -s)"

# Add key to agent
ssh-add ~/.ssh/id_ed25519

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub: Settings → SSH and GPG keys → New SSH key
```

#### "fatal: refusing to merge unrelated histories"

**Problem**: Repositories have no common history

**Solution**:

```bash

git pull origin main --allow-unrelated-histories

```

#### "Your branch and 'origin/main' have diverged"

**Problem**: Local and remote have different commits

**Solution 1** (if local changes should be kept):

```bash

git pull --rebase origin main
git push

```

**Solution 2** (if remote should be kept):

```bash

git fetch origin
git reset --hard origin/main

```

#### Merge conflicts

**Problem**: Git can't automatically merge

**Solution**:

```bash

# 1. See conflicted files
git status

# 2. Open and edit each file
# Remove conflict markers and keep desired code

# 3. Stage resolved files
git add conflicted_file.py

# 4. Complete merge
git commit

```

#### Accidentally committed sensitive data

**Problem**: Pushed password/API key to GitHub

**Solution**:

```bash

# Remove file from history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/file" \
  --prune-empty --tag-name-filter cat -- --all

# Force push
git push origin --force --all

# IMPORTANT: Rotate the compromised credentials immediately!
```

#### Can't push: "Updates were rejected"

**Problem**: Remote has changes you don't have

**Solution**:

```bash

# Pull first
git pull origin main

# Resolve any conflicts

# Then push
git push origin main

```

### Getting Help

```bash

# General help
git help

# Help for specific command
git help commit
git help branch

# Quick help
git commit --help
git branch -h

```

### Checking Git Configuration

```bash

# View all configuration
git config --list

# View specific setting
git config user.name
git config user.email

# View configuration with file locations
git config --list --show-origin

```

## Additional Resources

### Official Documentation

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Documentation](https://docs.github.com)
- [Pro Git Book](https://git-scm.com/book/en/v2) (Free online)

### Interactive Learning

- [Learn Git Branching](https://learngitbranching.js.org/) - Interactive tutorial
- [GitHub Skills](https://skills.github.com/) - Hands-on GitHub courses
- [Git Immersion](https://gitimmersion.com/) - Step-by-step tutorial

### Cheat Sheets

- [GitHub Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [Atlassian Git Cheat Sheet](https://www.atlassian.com/git/tutorials/atlassian-git-cheatsheet)

### GUI Tools

- [GitHub Desktop](https://desktop.github.com/) - Official GitHub GUI
- [GitKraken](https://www.gitkraken.com/) - Cross-platform Git client
- [Sourcetree](https://www.sourcetreeapp.com/) - Free Git GUI
- Built-in Git support in IDEs (VS Code, PyCharm, etc.)

### Video Tutorials

- [Git and GitHub for Beginners - Crash Course](https://www.youtube.com/watch?v=RGOj5yH7evk) (freeCodeCamp)
- [Git Tutorial for Beginners](https://www.youtube.com/watch?v=8JJ101D3knE) (Programming with Mosh)

### Community

- [GitHub Community Forum](https://github.community/)
- [Stack Overflow - Git Tag](https://stackoverflow.com/questions/tagged/git)
- [r/git on Reddit](https://www.reddit.com/r/git/)

---

## Quick Reference

### Essential Commands

```bash
# Setup
git config --global user.name "Your Name"
git config --global user.email "email@example.com"

# Starting
git init                          # Initialize repository
git clone <url>                   # Clone repository

# Basic workflow
git status                        # Check status
git add <file>                    # Stage file
git add .                         # Stage all files
git commit -m "message"           # Commit changes
git push                          # Push to remote
git pull                          # Pull from remote

# Branching
git branch                        # List branches
git branch <name>                 # Create branch
git checkout <name>               # Switch branch
git checkout -b <name>            # Create and switch
git merge <branch>                # Merge branch
git branch -d <name>              # Delete branch

# History
git log                           # View history
git log --oneline                 # Compact history
git diff                          # View changes
git show <commit>                 # Show commit details

# Undoing
git restore <file>                # Discard changes
git restore --staged <file>       # Unstage file
git reset HEAD~1                  # Undo last commit
git revert <commit>               # Revert commit

# Remote
git remote add origin <url>       # Add remote
git remote -v                     # View remotes
git fetch                         # Fetch changes
git push origin <branch>          # Push branch

```

---

**Congratulations!** You now have a solid foundation in Git and GitHub. Remember, the best way to learn is by doing. Start using Git for your projects and don't be afraid to experiment!

For project-specific workflows, see the [Contributing Guide](../../CONTRIBUTING.md).
