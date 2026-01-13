# CI/CD Setup Checklist

Follow this checklist to complete the CI/CD setup for your project.

## ✅ Initial Setup

### 1. GitHub Repository Configuration

- [ ] **Enable GitHub Actions**
  - Go to `Settings → Actions → General`
  - Select "Allow all actions and reusable workflows"
  - Select "Read and write permissions"
  - Check "Allow GitHub Actions to create and approve pull requests"

- [ ] **Configure Branch Protection** (Recommended for `main` branch)
  - Go to `Settings → Branches → Add rule`
  - Branch name pattern: `main`
  - Enable:
    - ✅ Require a pull request before merging
    - ✅ Require approvals: 1
    - ✅ Require status checks to pass before merging
    - ✅ Require branches to be up to date before merging
  - Add required status checks:
    - `Code Quality (lint, type, security)`
    - `Test on Python 3.13`
    - `Build Distribution`

### 2. PyPI Setup

- [ ] **Create/Login to PyPI Account**
  - Visit [https://pypi.org/](https://pypi.org/)
  - Create account or log in
  - Enable 2FA (required for publishing)

- [ ] **Generate API Token**
  - Go to `Account settings → API tokens`
  - Click "Add API token"
  - Name: `GitHub Actions`
  - Scope: `Entire account` (initially - can narrow after first upload)
  - Copy the token (starts with `pypi-`) - you'll only see it once!

- [ ] **Consider Trusted Publishing** (Recommended for better security)
  - Alternative to API tokens
  - See [PyPI Trusted Publishers Guide](https://docs.pypi.org/trusted-publishers/)
  - Allows GitHub Actions to publish without storing tokens

### 3. GitHub Secrets Configuration

- [ ] **Add PyPI Secret**
  - Go to `Settings → Secrets and variables → Actions`
  - Click "New repository secret"
  - Add this secret:

    | Name | Value | Example |
    |------|-------|---------|
    | `PYPI_API_TOKEN` | Your PyPI API token | `pypi-abc123def456...` |

### 4. Verify Workflows

- [ ] **Check Workflow Files Exist**
  ```bash
  ls -la .github/workflows/
  # Should show:
  # - ci.yml
  # - publish.yml
  # - security.yml
  # - pr-checks.yml
  ```

- [ ] **Commit and Push Workflows**
  ```bash
  git add .github/
  git commit -m "ci: add GitHub Actions workflows"
  git push origin main
  ```

- [ ] **Verify CI Workflow Runs**
  - Go to `Actions` tab
  - Should see "CI" workflow running/completed
  - All jobs should pass ✅

### 5. Test the Setup

- [ ] **Test CI Workflow**
  ```bash
  # Create test branch
  git checkout -b test/ci-setup

  # Make a small change
  echo "# Test" >> README.md

  # Push to trigger CI
  git add README.md
  git commit -m "test: verify CI workflow"
  git push origin test/ci-setup

  # Check Actions tab - CI should run
  ```

- [ ] **Test PR Workflow**
  ```bash
  # Create PR from test branch
  gh pr create --title "test: verify PR checks" --body "Testing CI/CD setup"

  # Check PR - should see status checks
  ```

- [ ] **Clean up test**
  ```bash
  # Close PR and delete branch
  gh pr close
  git checkout main
  git branch -D test/ci-setup
  ```

### 6. Test Publishing (Optional)

- [ ] **Test Publish Workflow** (Optional - creates real release)
  ```bash
  # Update version in pyproject.toml to test version
  # version = "0.0.1-test"

  # Create test tag
  git add pyproject.toml
  git commit -m "test: publish workflow"
  git tag v0.0.1-test
  git push origin v0.0.1-test

  # Check Actions - Publish workflow should run
  # Verify package appears on PyPI
  ```

  **⚠️ Warning**: This creates a real package version. You may want to delete it from PyPI after testing.

## 🔧 Optional Enhancements

### Security Scanning

- [ ] **Enable Dependabot Alerts**
  - Go to `Settings → Security → Code security and analysis`
  - Enable "Dependabot alerts"
  - Enable "Dependabot security updates"

- [ ] **Enable Secret Scanning**
  - Same location as above
  - Enable "Secret scanning"
  - Enable "Push protection"

- [ ] **Enable CodeQL**
  - Go to `Settings → Security → Code security and analysis`
  - Enable "CodeQL analysis"
  - Workflow already included in `security.yml`

### Notifications

- [ ] **Configure Workflow Notifications**
  - Go to `Settings → Notifications`
  - Choose notification preferences for Actions
  - Recommended: Enable notifications for failed workflows

- [ ] **Slack/Discord Integration** (Optional)
  - Install GitHub app for your team chat
  - Subscribe to repository notifications
  - Example for Slack: `/github subscribe owner/repo workflows`

### Labels

- [ ] **Create PR Size Labels**
  - Go to `Issues → Labels`
  - Create labels (already auto-created by pr-checks workflow):
    - `size/xs` - Very small PR
    - `size/s` - Small PR
    - `size/m` - Medium PR
    - `size/l` - Large PR
    - `size/xl` - Very large PR

- [ ] **Create Type Labels**
  - `bug` - Bug reports
  - `enhancement` - Feature requests
  - `documentation` - Documentation improvements
  - `dependencies` - Dependency updates
  - `good first issue` - Good for newcomers

### README Updates

- [ ] **Update README.md**
  - Add CI/CD section from `.github/README_CICD_SECTION.md`
  - Add status badges
  - Update installation instructions with Gemfury URL

- [ ] **Replace Placeholders**
  - Search for `YOUR_USERNAME` and replace with actual username
  - Search for `YOUR_ACCOUNT` and replace with Gemfury account name
  - Update repository URLs

## 📊 Verification

After completing setup, verify everything works:

### ✅ Checklist

- [ ] CI workflow runs on push
- [ ] CI workflow runs on pull requests
- [ ] All CI checks pass
- [ ] PR checks validate title format
- [ ] PR gets size label automatically
- [ ] Security workflow runs weekly
- [ ] Dependabot creates update PRs
- [ ] Publish workflow triggers on version tags
- [ ] Package successfully uploads to PyPI
- [ ] GitHub release created automatically
- [ ] Package can be installed from PyPI

### Test Commands

```bash
# Verify package on PyPI
pip index versions synteles-platform-mcp

# Test installation
pip install synteles-platform-mcp

# Verify installation
python -c "from synteles_platform_mcp import __version__; print(__version__)"
```

## 🎉 You're Done!

If all items are checked, your CI/CD pipeline is fully configured!

### Next Steps

1. **Create your first release**: Follow [QUICK_REFERENCE.md](.github/QUICK_REFERENCE.md)
2. **Invite collaborators**: Add team members to the repository
3. **Set up local development**: Follow development setup in README
4. **Start contributing**: Check open issues or create new features

## 📚 Additional Resources

- [CI/CD Setup Guide](.github/CICD_SETUP.md) - Detailed documentation
- [Quick Reference](.github/QUICK_REFERENCE.md) - Common commands
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [PyPI Docs](https://docs.pypi.org/)

## 🆘 Troubleshooting

If something doesn't work:

1. Check workflow logs in Actions tab
2. Review [CICD_SETUP.md → Troubleshooting](.github/CICD_SETUP.md#troubleshooting)
3. Verify all secrets are set correctly
4. Check branch protection rules
5. Create an issue with error details

---

**Questions?** Contact: emin.askerov@synteles.com
