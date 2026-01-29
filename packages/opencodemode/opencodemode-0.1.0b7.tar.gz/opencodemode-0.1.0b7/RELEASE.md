# PyPI Release Plan for Codemode

## Current Status ✅

- **Package Name**: `codemode`
- **Version**: `0.1.0`
- **License**: MIT
- **Python Support**: 3.9, 3.10, 3.11, 3.12
- **Build System**: Hatchling
- **Tests**: 55/59 passing (93%) ✅
- **Build**: Successfully generates wheel and sdist ✅

## Installation Methods

Once published to PyPI, users will be able to install via:

### Using pip
```bash
# Basic installation
pip install opencodemode

# With CrewAI support
pip install opencodemode[crewai]

# With all integrations
pip install opencodemode[all]

# Development installation
pip install opencodemode[dev]
```

### Using uv (recommended)
```bash
# Basic installation
uv pip install opencodemode

# With CrewAI support
uv add opencodemode[crewai]

# Development installation
uv pip install opencodemode[dev]
```

## Pre-Release Checklist

### 1. Fix Remaining Issues
- [ ] Fix 4 failing tests in `tests/unit/`:
  - `test_registry.py::test_init` (AttributeError)
  - `test_registry.py::test_register_crew`
  - `test_registry.py::test_get_component_names`
  - `test_security.py::test_validate_safe_requests_usage`
- [ ] Fix Pydantic deprecation warnings (migrate from `class Config` to `ConfigDict`)
- [ ] Add missing CLI module (`codemode.cli.main:cli`)

### 2. Documentation Updates
- [ ] Update GitHub URLs in README badges
- [ ] Add installation instructions
- [ ] Create CHANGELOG.md
- [ ] Add API documentation
- [ ] Create migration guides

### 3. PyPI Setup
- [ ] Create PyPI account at https://pypi.org/account/register/
- [ ] Set up trusted publishing on PyPI:
  1. Go to https://pypi.org/manage/account/publishing/
  2. Add publisher for `mldlwizard/code_mode` repository
  3. Set workflow name to `publish.yml`
  4. Set environment to `release` (optional)

### 4. GitHub Setup
- [ ] Create a `main` or `master` branch for releases
- [ ] Set up branch protection rules
- [ ] Add CODECOV_TOKEN secret (optional)
- [ ] Enable GitHub Actions

## Release Process

### Step 1: Prepare Release
```bash
# Ensure you're on the main branch
git checkout main
git pull origin main

# Update version in pyproject.toml
# Update CHANGELOG.md with release notes

# Run tests
python -m pytest tests/ -v -o addopts=""

# Build locally to verify
python -m build

# Verify package
twine check dist/*
```

### Step 2: Test on TestPyPI (Optional)
```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ opencodemode
```

### Step 3: Create GitHub Release
```bash
# Create and push tag
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0

# Create release on GitHub
# This will trigger the publish.yml workflow
```

Or use GitHub CLI:
```bash
gh release create v0.1.0 \
  --title "v0.1.0 - Initial Release" \
  --notes "First public release of Codemode" \
  dist/*
```

### Step 4: Verify Publication
```bash
# Wait for GitHub Action to complete
# Then verify on PyPI
pip install opencodemode

# Test basic import
python -c "import codemode; print(codemode.__version__)"
```

## Automated Release via GitHub Actions

The `.github/workflows/publish.yml` workflow will:
1. Trigger on GitHub release creation
2. Build the package
3. Publish to PyPI using trusted publishing (no token needed)

### Manual Trigger for TestPyPI
```bash
# Use workflow_dispatch to test publishing
gh workflow run publish.yml
```

## Version Management Strategy

### Semantic Versioning
- **Major** (1.0.0): Breaking changes
- **Minor** (0.1.0): New features, backward compatible
- **Patch** (0.1.1): Bug fixes

### Release Cycle
- **Alpha** (0.1.0-alpha.1): Early development
- **Beta** (0.1.0-beta.1): Feature complete, testing
- **RC** (0.1.0-rc.1): Release candidate
- **Stable** (0.1.0): Production ready

## Distribution Files

After build, the following files are created:
- `dist/codemode-0.1.0-py3-none-any.whl` (45KB) - Wheel distribution
- `dist/codemode-0.1.0.tar.gz` (82KB) - Source distribution

Both include:
- Python source code
- Documentation (`.claude/`, `docs/`)
- Examples
- Tests
- License and README

## Post-Release

### 1. Announce Release
- [ ] Post on GitHub Discussions
- [ ] Update documentation site
- [ ] Share on social media
- [ ] Update relevant project listings

### 2. Monitor
- [ ] Check PyPI download stats
- [ ] Monitor GitHub issues
- [ ] Track user feedback
- [ ] Update documentation based on questions

### 3. Plan Next Release
- [ ] Review roadmap
- [ ] Prioritize issues
- [ ] Plan features for next version

## Troubleshooting

### Build Fails
```bash
# Clean build artifacts
rm -rf dist/ build/ *.egg-info

# Rebuild
python -m build
```

### Publishing Fails
```bash
# Check package
twine check dist/*

# Verify credentials
twine upload --repository testpypi dist/*
```

### Import Errors After Install
```bash
# Verify installation
pip show codemode
pip list | grep codemode

# Check for conflicts
pip check
```

## Alternative: Manual Publishing

If trusted publishing is not set up:

```bash
# Install twine
pip install twine

# Upload to PyPI (requires API token)
twine upload dist/*
```

Set up API token:
1. Go to https://pypi.org/manage/account/token/
2. Create token with scope limited to `codemode` project
3. Add to GitHub Secrets as `PYPI_API_TOKEN`
4. Update workflow to use token instead of trusted publishing

## Resources

- **PyPI Project**: https://pypi.org/project/codemode/ (after first release)
- **PyPI Help**: https://packaging.python.org/
- **Trusted Publishing**: https://docs.pypi.org/trusted-publishers/
- **GitHub Actions**: https://github.com/pypa/gh-action-pypi-publish
- **Hatchling Docs**: https://hatch.pypa.io/

---

**Ready to release?** Follow the checklist above and create your first GitHub release!
