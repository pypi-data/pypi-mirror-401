# Release Process

This guide documents the process for creating and publishing new releases of Codemode.

## Version Management

Codemode follows [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes to the public API
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

The version is defined in `pyproject.toml`:

```toml
[project]
name = "codemode"
version = "0.2.0"
```

## Pre-Release Checklist

Before creating a release, ensure:

1. All tests pass:

```bash
make test
make e2e
```

2. Code is properly formatted and linted:

```bash
make format
make lint
```

3. Documentation is updated for any API changes

4. `CHANGELOG.md` is updated with release notes

## Changelog Updates

Maintain a changelog following [Keep a Changelog](https://keepachangelog.com/) format.

### Changelog Structure

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- New feature description

### Changed
- Modified behavior description

### Deprecated
- Features to be removed in future versions

### Removed
- Removed features

### Fixed
- Bug fix description

### Security
- Security-related changes

## [0.2.0] - 2024-01-15

### Added
- Async executor support
- TLS encryption for gRPC communication

### Fixed
- Timeout handling in executor client
```

### Writing Good Changelog Entries

- Write from the user's perspective
- Include issue/PR references where applicable
- Group related changes together
- Be concise but descriptive

## Creating a Release

Codemode uses a structured branch workflow for releases:

### Branch Flow

```
develop -> main -> release-test -> release
```

| Branch | Purpose | Publishing |
|--------|---------|------------|
| `develop` | Active development | None |
| `main` | Stable, reviewed code | None |
| `release-test` | Testing releases | Test PyPI |
| `release` | Production releases | PyPI |

### 1. Update Version

Update the version in `pyproject.toml`:

```toml
[project]
version = "0.2.0"
```

### 2. Update Changelog

Move items from `[Unreleased]` to a new version section with the release date:

```markdown
## [0.2.0] - 2024-01-15
```

### 3. Merge to Main

Ensure all changes are merged from `develop` to `main`:

```bash
git checkout main
git merge develop
git push origin main
```

### 4. Test on Test PyPI

Merge to `release-test` to trigger Test PyPI publish:

```bash
git checkout release-test
git merge main
git push origin release-test
```

This automatically:
- Bumps version with `.dev<run_number>` suffix
- Builds and publishes to Test PyPI

Verify installation from Test PyPI:

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ opencodemode
```

### 5. Publish to PyPI

Once verified, merge to `release` to trigger PyPI publish:

```bash
git checkout release
git merge release-test
git push origin release
```

### 6. Create Git Tag and GitHub Release

```bash
git tag -a v0.2.0 -m "Release v0.2.0"
git push origin v0.2.0
```

Then create a GitHub Release from the tag.

## PyPI Publishing

### Automated Publishing via Branches

Publishing is automated via GitHub Actions:

| Branch | Workflow | Destination |
|--------|----------|-------------|
| `release-test` | `publish-test-pypi.yml` | Test PyPI |
| `release` | `publish.yml` | PyPI |

The Test PyPI workflow automatically bumps the version with a `.dev<run_number>` suffix to avoid conflicts.

### Manual Publishing

If needed, you can publish manually:

```bash
# Build the package
uv build

# Upload to PyPI
uv publish
```

Ensure you have PyPI credentials configured.

## Test PyPI

Use Test PyPI for validating the release process without affecting the production package index.

### Publishing to Test PyPI

The workflow `.github/workflows/publish-test-pypi.yml` publishes to Test PyPI for pre-releases.

To manually publish to Test PyPI:

```bash
uv publish --repository testpypi
```

### Installing from Test PyPI

```bash
pip install --index-url https://test.pypi.org/simple/ opencodemode
```

### Pre-Release Versions

Use pre-release version suffixes for testing:

```toml
[project]
version = "0.2.0a1"   # Alpha
version = "0.2.0b1"   # Beta
version = "0.2.0rc1"  # Release candidate
```

## Release Types

### Stable Releases

Standard releases following the version format `X.Y.Z`:

1. Create a tag matching `v*.*.*`
2. GitHub Actions publishes to PyPI

### Pre-Releases

Alpha, beta, and release candidates:

1. Use version suffix (e.g., `0.2.0a1`)
2. Tag with the full version (e.g., `v0.2.0a1`)
3. Optionally publish to Test PyPI first

### Hotfix Releases

For urgent bug fixes:

1. Create a branch from the release tag: `git checkout -b hotfix/0.2.1 v0.2.0`
2. Apply the fix
3. Update version to `0.2.1`
4. Follow standard release process

## Post-Release

After a successful release:

1. Verify the package is available on PyPI
2. Test installation: `pip install opencodemode==0.2.0`
3. Update documentation if needed
4. Announce the release (if applicable)
5. Add a new `[Unreleased]` section to `CHANGELOG.md`

## Troubleshooting

### Build Failures

If the build fails:

```bash
# Clean previous builds
make clean

# Rebuild
uv build
```

### Publishing Failures

- Verify PyPI credentials are correct
- Check that the version does not already exist on PyPI
- Ensure the package name is not taken

### Version Conflicts

PyPI does not allow re-uploading the same version. If you need to fix a release:

1. Increment the patch version
2. Create a new release

## Commands Reference

| Command | Description |
|---------|-------------|
| `make test` | Run tests before release |
| `make lint` | Verify code quality |
| `make format` | Format code |
| `make clean` | Clean build artifacts |
| `uv build` | Build the package |
| `uv publish` | Publish to PyPI |

## GitHub Actions Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `ci.yml` | Push to main/develop, PRs | Run tests and linting |
| `publish.yml` | Push to release branch | Publish to PyPI |
| `publish-test-pypi.yml` | Push to release-test branch | Publish to Test PyPI |
