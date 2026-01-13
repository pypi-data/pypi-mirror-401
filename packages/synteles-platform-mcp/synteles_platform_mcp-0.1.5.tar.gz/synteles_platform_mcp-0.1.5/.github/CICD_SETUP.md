# CI/CD Setup Guide

This document explains the GitHub Actions CI/CD automation setup for the Synteles Platform MCP Server.

## 📋 Table of Contents

- [Overview](#overview)
- [Workflows](#workflows)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)

## 🔍 Overview

The project uses GitHub Actions for automated:
- **Continuous Integration (CI)**: Code quality checks, testing, and building
- **Continuous Deployment (CD)**: Publishing to PyPI
- **Security**: Dependency scanning and secret detection
- **Quality**: PR validation and automated reviews

## 📦 Workflows

### 1. CI Workflow (`ci.yml`)

**Triggers:** Push to `main`, `feature/**` branches and all pull requests

**Jobs:**
- **Code Quality**: Runs `make check` (lint, type checking, security, dependency check)
  - Ruff linting
  - Mypy type checking
  - Bandit security scan
  - Deptry dependency check
  - Vulture unused code detection
  - Ruff format check
- **Test**: Runs `make test` on Python 3.13
- **Build**: Creates wheel distribution
- **Install Test**: Verifies package can be installed

**Status Badge:**
```markdown
![CI](https://github.com/YOUR_USERNAME/platform-mcp-server/workflows/CI/badge.svg)
```

### 2. Publish Workflow (`publish.yml`)

**Triggers:** Git tags matching `v*.*.*` pattern (e.g., `v0.1.0`), or manual workflow dispatch

**Jobs:**
- **Validate**: Ensures tag matches version in `pyproject.toml`
- **Quality Check**: Runs `make check` and `make test` before publishing (quality gate)
- **Publish**: Builds and uploads to PyPI using trusted publishing
- **Create Release**: Creates GitHub release with changelog and distribution artifacts

**Required Secrets:**
- `PYPI_API_TOKEN`: Your PyPI API token for publishing packages

### 3. Security Workflow (`security.yml`)

**Triggers:** Push, pull requests, and weekly schedule (Mondays 10:00 UTC)

**Jobs:**
- **Dependency Scan**: Runs `make security` (bandit) plus safety and pip-audit
- **Secret Scan**: Detects leaked secrets (TruffleHog)
- **CodeQL**: Static code analysis for security issues

### 4. PR Checks Workflow (`pr-checks.yml`)

**Triggers:** Pull request events

**Jobs:**
- **PR Title**: Validates conventional commit format
- **Size Label**: Auto-labels PR by size
- **Validate Files**: Checks for sensitive files and Python syntax
- **Spell Check**: Detects typos in documentation

## ⚙️ Setup Instructions

### 1. Configure GitHub Secrets

Go to **Settings → Secrets and variables → Actions** and add:

```bash
# Required for publishing to PyPI
PYPI_API_TOKEN=<your-pypi-api-token>
```

#### Getting PyPI API Token:

1. Login to [PyPI](https://pypi.org/) or [TestPyPI](https://test.pypi.org/)
2. Go to **Account settings → API tokens**
3. Click **Add API token**
4. Set the token name (e.g., "GitHub Actions")
5. Choose scope: **Entire account** (or limit to specific project after first upload)
6. Copy the token (starts with `pypi-`) and add it to GitHub secrets

**Note:** For enhanced security, consider using [Trusted Publishing](https://docs.pypi.org/trusted-publishers/) instead of API tokens.

### 2. Enable GitHub Actions

1. Go to **Settings → Actions → General**
2. Under **Actions permissions**, select "Allow all actions and reusable workflows"
3. Under **Workflow permissions**, select "Read and write permissions"
4. Check "Allow GitHub Actions to create and approve pull requests"

### 3. Enable Dependabot

Dependabot configuration is already set up in `.github/dependabot.yml`. It will:
- Check for Python dependency updates weekly
- Check for GitHub Actions updates weekly
- Create PRs automatically for updates

### 4. Enable Branch Protection (Recommended)

For `main` branch:
1. Go to **Settings → Branches**
2. Add rule for `main` branch
3. Enable:
   - ✅ Require a pull request before merging
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
   - Status checks: `Code Quality (lint, type, security)`, `Test on Python 3.13`, `Build Distribution`

## 🚀 Usage

### Developing and Testing

```bash
# Setup development environment
uv sync

# Create feature branch
git checkout -b feature/my-new-feature

# Make changes
# ...

# Run quality checks before pushing
make check  # Runs all quality checks
make test   # Runs all tests

# Push - this triggers CI workflow
git push origin feature/my-new-feature

# Create PR - triggers PR checks
gh pr create
```

### Releasing a New Version

```bash
# 1. Update version in pyproject.toml
# version = "0.2.0"

# 2. Commit changes
git add pyproject.toml
git commit -m "chore: bump version to 0.2.0"

# 3. Create and push tag
git tag v0.2.0
git push origin v0.2.0

# 4. Publish workflow runs automatically
# - Validates version
# - Builds wheel
# - Publishes to Gemfury
# - Creates GitHub release
```

### Manual Publish (Emergency)

If automatic publishing fails, you can trigger it manually:

1. Go to **Actions → Publish to PyPI**
2. Click **Run workflow**
3. Select branch/tag
4. Click **Run workflow**

### Installing Published Package

```bash
# Install from PyPI
pip install synteles-platform-mcp

# Or with uv (recommended)
uv pip install synteles-platform-mcp
```

## 🐛 Troubleshooting

### CI Workflow Fails

**Quality check errors:**
```bash
# Run all quality checks locally
make check

# Or run individual checks
make lint       # Ruff linting
make typed      # Mypy type checking
make security   # Bandit security scan
make depcheck   # Dependency check
make format     # Auto-format code
```

**Test failures:**
```bash
# Run tests locally
make test
```

**Build failures:**
```bash
# Test build locally
python -m build
```

### Publish Workflow Fails

**Version mismatch:**
```bash
# Ensure tag matches pyproject.toml version
git tag v0.2.0  # Must match version = "0.2.0"
```

**Authentication error:**
- Verify `PYPI_API_TOKEN` secret is set correctly
- Check token has not expired
- Ensure token has upload permissions for the package

**Upload error:**
- Check PyPI account is active
- Verify token scope includes the package name
- Check if version already exists (can't re-upload same version)
- For first upload, ensure token has "Entire account" scope

### Security Workflow Issues

**False positives in secret scanning:**
- Add patterns to `.gitignore` or `.trufflehogignore`

**Dependency vulnerabilities:**
- Review the vulnerability report
- Update affected dependencies
- Or add exception if false positive

## 📊 Monitoring

### Workflow Status

Check workflow runs:
```bash
# Using GitHub CLI
gh run list

# View specific workflow
gh run view <run-id>

# Watch latest run
gh run watch
```

### Build Artifacts

Download build artifacts:
```bash
# List artifacts
gh run list --workflow=ci.yml

# Download artifacts from specific run
gh run download <run-id>
```

## 🔒 Security Best Practices

1. **Never commit secrets**: Use GitHub Secrets for all sensitive data
2. **Review Dependabot PRs**: Don't auto-merge dependency updates
3. **Check security alerts**: Monitor the Security tab regularly
4. **Rotate tokens**: Update PyPI tokens periodically, or use Trusted Publishing
5. **Pin actions versions**: Use specific versions (e.g., `@v4`) not `@main`
6. **Use Trusted Publishing**: Consider configuring PyPI Trusted Publishing for better security

## 📈 Metrics and Insights

View workflow metrics:
1. Go to **Actions**
2. Click on a workflow name
3. View success rate, duration trends, and resource usage

## 🔄 Workflow Badges

Add these to your `README.md`:

```markdown
![CI](https://github.com/YOUR_USERNAME/platform-mcp-server/workflows/CI/badge.svg)
![Security](https://github.com/YOUR_USERNAME/platform-mcp-server/workflows/Security/badge.svg)
![Publish](https://github.com/YOUR_USERNAME/platform-mcp-server/workflows/Publish%20to%20PyPI/badge.svg)
```

## 📝 Customization

### Adding More Python Versions

Edit `.github/workflows/ci.yml`:

```yaml
strategy:
  matrix:
    python-version: ["3.13", "3.14"]  # Add more versions
```

### Changing Publish Trigger

Edit `.github/workflows/publish.yml`:

```yaml
on:
  push:
    branches: ["release"]  # Publish on push to release branch
  # OR
  release:
    types: [published]     # Publish on GitHub release creation
```

### Adding Pre-release Support

Add to `publish.yml`:

```yaml
- name: Determine if pre-release
  id: prerelease
  run: |
    if [[ ${{ github.ref_name }} =~ ^v.*-(alpha|beta|rc) ]]; then
      echo "prerelease=true" >> $GITHUB_OUTPUT
    else
      echo "prerelease=false" >> $GITHUB_OUTPUT
    fi

- name: Create Release
  uses: softprops/action-gh-release@v1
  with:
    prerelease: ${{ steps.prerelease.outputs.prerelease }}
```

## 🆘 Support

If you encounter issues:
1. Check [GitHub Actions documentation](https://docs.github.com/en/actions)
2. Review [PyPI documentation](https://docs.pypi.org/)
3. Check [Trusted Publishing guide](https://docs.pypi.org/trusted-publishers/)
4. Check workflow logs in Actions tab
5. Create an issue with workflow run ID and error details
