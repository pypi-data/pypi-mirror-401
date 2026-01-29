# Test PyPI Automated Publishing Setup

This document describes the automated publishing workflow for Test PyPI.

## Overview

The project is configured to automatically publish to Test PyPI whenever you push to the `release-test` branch.

## Prerequisites

You need to configure a GitHub secret with your Test PyPI API token.

## Setting Up the GitHub Secret

1. Go to your GitHub repository: https://github.com/mldlwizard/code_mode

2. Navigate to **Settings** → **Secrets and variables** → **Actions**

3. Click **New repository secret**

4. Configure the secret:
   - **Name**: `TEST_PYPI_API_TOKEN`
   - **Value**:
     ```
     pypi-AgENdGVzdC5weXBpLm9yZwIkYThjMjI5M2YtYjk1OS00ZjE0LWFlNzctYmU4OWQ0Y2RmOWUzAAIqWzMsImY2ZGM0Y2I0LWY2ZGQtNDJlZi1hY2I1LWM1M2FjMzZiNGU5MCJdAAAGIFknvBG0MTAdyVz7Dn44HYx1WuUyrtFA_E6an72wxJIL
     ```

5. Click **Add secret**

## How It Works

The workflow (`.github/workflows/publish-test-pypi.yml`) automatically:

1. Triggers when you push to the `release-test` branch
2. Checks out the code
3. Sets up Python 3.11
4. Installs build dependencies (build, twine)
5. Builds the package using `python -m build`
6. Uploads to Test PyPI using twine with the configured API token

## Usage

### Publishing a New Version

1. **Update the version** in `pyproject.toml`:
   ```toml
   [project]
   name = "opencodemode"
   version = "0.1.1"  # Update this version
   ```

2. **Commit your changes**:
   ```bash
   git add pyproject.toml
   git commit -m "Bump version to 0.1.1"
   ```

3. **Push to the release-test branch**:
   ```bash
   git push origin release-test
   ```

4. The GitHub Action will automatically build and publish to Test PyPI.

5. **Monitor the workflow** at: https://github.com/mldlwizard/code_mode/actions

## Testing the Package

After publishing to Test PyPI, you can install it using:

### Using pip:
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ opencodemode
```

### Using uv:
```bash
uv pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ opencodemode
```

**Note**: The `--extra-index-url https://pypi.org/simple/` is needed because Test PyPI doesn't host dependencies, so they need to be fetched from the main PyPI.

## Verifying the Package

You can view the package on Test PyPI at:
https://test.pypi.org/project/opencodemode/

## Important Notes

- **Version conflicts**: Test PyPI won't accept re-uploads of the same version. Always bump the version number before publishing.
- **Dependencies**: Test PyPI doesn't have all packages, so when installing from Test PyPI, dependencies will be fetched from the main PyPI.
- **Token security**: Never commit the API token to the repository. Always use GitHub Secrets.

## Troubleshooting

### Build Fails

- Check that `pyproject.toml` is properly configured
- Ensure all required files are included in the repository
- Review the GitHub Actions log for specific errors

### Upload Fails with "File already exists"

- You're trying to upload a version that already exists on Test PyPI
- Bump the version number in `pyproject.toml`

### Authentication Error

- Verify the `TEST_PYPI_API_TOKEN` secret is correctly configured in GitHub
- Ensure the token hasn't expired or been revoked

## Workflow File Location

The workflow is defined in: `.github/workflows/publish-test-pypi.yml`
