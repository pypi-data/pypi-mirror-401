# CI/CD Quick Reference

## 🚀 Quick Commands

### Development
```bash
# Setup (installs all dependencies including dev tools)
uv sync

# Before commit - Run all quality checks
make check      # Runs: lint, typed, security, depcheck, unusedcode
make format     # Format code with ruff
make test       # Run all unit tests

# Individual checks (if needed)
make lint       # Ruff linting
make typed      # Mypy type checking
make security   # Bandit security scan
make depcheck   # Deptry dependency check
make unusedcode # Vulture unused code detection

# Build locally
python -m build
```

### Release Process
```bash
# 1. Update version
# Edit pyproject.toml: version = "0.2.0"

# 2. Commit and tag
git add pyproject.toml
git commit -m "chore: bump version to 0.2.0"
git tag v0.2.0

# 3. Push (triggers publish workflow)
git push origin main
git push origin v0.2.0
```

### Manual PyPI Upload
```bash
# If workflow fails, upload manually
python -m build
python -m twine upload dist/*
# You'll be prompted for your PyPI username and password
# Or set TWINE_USERNAME and TWINE_PASSWORD environment variables
```

## 📊 Workflow Overview

| Workflow | Trigger | Purpose | Duration |
|----------|---------|---------|----------|
| **CI** | Push, PR | Quality checks (`make check`), tests, build | ~2-3 min |
| **Publish** | Tag `v*.*.*` | Quality gate + deploy to PyPI | ~3-4 min |
| **Security** | Push, PR, Weekly | Bandit, safety, pip-audit, secrets | ~3-5 min |
| **PR Checks** | PR | Validate PR format, size, files | ~1 min |

## 🔑 Required Secrets

| Secret | Purpose | Where to Get |
|--------|---------|--------------|
| `PYPI_API_TOKEN` | Upload to PyPI | [PyPI Account Settings → API tokens](https://pypi.org/manage/account/) |

## ✅ Pre-commit Checklist

- [ ] All quality checks pass: `make check`
- [ ] Code is formatted: `make format`
- [ ] Tests pass: `make test`
- [ ] Documentation updated
- [ ] PR title follows conventional commits
- [ ] No sensitive data in code

**Quick validation:**
```bash
make check && make format && make test
```

## 🏷️ Conventional Commit Types

```bash
feat:     New feature
fix:      Bug fix
docs:     Documentation only
style:    Code style/formatting
refactor: Code refactoring
perf:     Performance improvement
test:     Adding/updating tests
build:    Build system changes
ci:       CI configuration changes
chore:    Other changes
```

## 🎯 Status Checks

All PRs must pass:
- ✅ Code Quality (lint, type, security) - `make check`
- ✅ Test on Python 3.13 - `make test`
- ✅ Build Distribution
- ✅ Install Test
- ✅ PR Title Validation
- ✅ Security Scans (bandit, safety, pip-audit)

## 🔍 Monitoring Commands

```bash
# List workflow runs
gh run list

# View specific run
gh run view <run-id> --log

# Download artifacts
gh run download <run-id>

# Cancel workflow
gh run cancel <run-id>

# Re-run failed jobs
gh run rerun <run-id> --failed
```

## 🐛 Common Issues

### "Version tag doesn't match pyproject.toml"
- Ensure tag `v0.2.0` matches `version = "0.2.0"`

### "PyPI authentication failed"
- Check `PYPI_API_TOKEN` secret
- Verify token hasn't expired
- Ensure token has upload permissions for the package

### "Quality checks failed"
```bash
make format  # Auto-fix formatting
make check   # Run all quality checks
make lint    # Check linting only
make typed   # Check types only
```

### "Tests failed"
```bash
make test  # Run all tests locally
```

## 📦 Installation URLs

```bash
# Install from PyPI
pip install synteles-platform-mcp

# With uv (recommended)
uv pip install synteles-platform-mcp

# Development install (local - installs all dev dependencies)
uv sync
```

## 🔗 Useful Links

- **Workflows**: `.github/workflows/`
- **Setup Guide**: `.github/CICD_SETUP.md`
- **Actions**: `https://github.com/YOUR_USERNAME/platform-mcp-server/actions`
- **Releases**: `https://github.com/YOUR_USERNAME/platform-mcp-server/releases`
- **PyPI Package**: `https://pypi.org/project/synteles-platform-mcp/`

## 📝 PR Title Examples

```
✅ feat: add support for OAuth token refresh
✅ fix: resolve port binding issue after logout
✅ docs: update API documentation
✅ refactor: improve error handling in auth client
✅ test: add unit tests for token storage

❌ Added new feature
❌ fixes bug
❌ Update documentation
```

## 🎨 Labels

Auto-applied labels:
- `size/xs`, `size/s`, `size/m`, `size/l`, `size/xl` - PR size
- `dependencies` - Dependabot updates
- `python` - Python dependency updates
- `github-actions` - Workflow updates

Manual labels:
- `bug` - Bug reports
- `enhancement` - Feature requests
- `documentation` - Documentation improvements
- `good first issue` - Good for newcomers
- `help wanted` - Need community help

## 🚦 Release Channels

```bash
# Stable releases
git tag v1.0.0

# Pre-releases (optional)
git tag v1.0.0-beta.1  # Beta
git tag v1.0.0-rc.1    # Release candidate
git tag v1.0.0-alpha.1 # Alpha
```

## 📞 Support

1. Check [CICD_SETUP.md](.github/CICD_SETUP.md) for detailed docs
2. Review workflow logs in Actions tab
3. Create issue with workflow run ID and logs
4. Contact: emin.askerov@synteles.com
