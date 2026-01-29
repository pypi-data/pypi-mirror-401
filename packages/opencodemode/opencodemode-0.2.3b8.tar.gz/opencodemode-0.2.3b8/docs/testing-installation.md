# Testing Package Installation from Test PyPI

This guide explains how to test your package installation using both `pip` and `uv` after publishing to Test PyPI.

## Quick Test

Use the automated test script:

```bash
bash scripts/test_installation.sh
```

This script will automatically test:
1. `pip install` from Test PyPI
2. `uv pip install` from Test PyPI
3. `uv add` in a new project

## Manual Testing Methods

### Method 1: Testing with pip

Create a clean virtual environment and install:

```bash
# Create and activate virtual environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ opencodemode

# Verify installation
pip show opencodemode

# Test import
python -c "import codemode; print(codemode.__version__)"

# Test CLI
codemode --help

# Cleanup
deactivate
rm -rf test_env
```

### Method 2: Testing with uv pip

Install uv if not already installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then test:

```bash
# Create and activate virtual environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install from Test PyPI using uv
uv pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ opencodemode

# Verify installation
uv pip show opencodemode

# Test import
python -c "import codemode; print(codemode.__version__)"

# Test CLI
codemode --help

# Cleanup
deactivate
rm -rf test_env
```

### Method 3: Testing with uv add

This method tests `uv add` in a new project, which is how users would typically add your package:

```bash
# Create a test project
mkdir test-project
cd test-project

# Initialize a new project with pyproject.toml
cat > pyproject.toml <<EOF
[project]
name = "test-codemode"
version = "0.1.0"
dependencies = []

[[tool.uv.index]]
name = "testpypi"
url = "https://test.pypi.org/simple/"
default = true

[[tool.uv.index]]
name = "pypi"
url = "https://pypi.org/simple/"
explicit = true
EOF

# Add the package
uv add opencodemode

# Verify it was added to pyproject.toml
cat pyproject.toml

# Test with uv run
uv run python -c "import codemode; print(codemode.__version__)"
uv run codemode --help

# Cleanup
cd ..
rm -rf test-project
```

## Verification Checklist

After installation, verify the following:

- [ ] Package installs without errors
- [ ] `pip show codemode` / `uv pip show codemode` displays correct version and metadata
- [ ] Python can import the module: `import codemode`
- [ ] Version is accessible: `codemode.__version__`
- [ ] CLI command works: `codemode --help`
- [ ] All dependencies are installed correctly
- [ ] No import errors when using main features

## Testing Different Features

### Test Basic Import
```python
import codemode
from codemode import CodeMode, ExecutorClient
from codemode.integrations.crewai import CrewAICodeModeTool

print(f"Version: {codemode.__version__}")
```

### Test CLI Commands
```bash
# Show help
codemode --help

# Other CLI commands (adjust based on your actual CLI)
codemode --version
```

### Test in a Real Project

Create a minimal test script:

```python
# test_codemode.py
from codemode import CodeMode

# Add your basic usage test here
cm = CodeMode()
print("CodeMode initialized successfully!")
```

Run it:
```bash
python test_codemode.py
```

## Common Issues and Solutions

### Issue: Dependencies not found

**Problem**: Installation fails because Test PyPI doesn't have all dependencies.

**Solution**: Always use `--extra-index-url https://pypi.org/simple/` to fetch dependencies from main PyPI.

### Issue: "File already exists" error when publishing

**Problem**: Trying to upload a version that already exists on Test PyPI.

**Solution**: Bump the version number in `pyproject.toml` before publishing.

### Issue: uv not found

**Problem**: `uv` command not recognized.

**Solution**: Install uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or on Windows with PowerShell:
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Issue: Import errors after installation

**Problem**: Package installs but imports fail.

**Solution**:
1. Check that `__init__.py` files exist in all package directories
2. Verify package structure in `pyproject.toml` matches actual structure
3. Test build locally: `python -m build && pip install dist/*.whl`

## Testing on Different Platforms

### Linux/macOS
```bash
bash scripts/test_installation.sh
```

### Windows (PowerShell)
```powershell
# Manual testing required - adapt the bash script commands
python -m venv test_env
.\test_env\Scripts\Activate.ps1
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ opencodemode
```

## Testing Workflow

1. **Update version** in `pyproject.toml`
2. **Push to release-test branch** (triggers auto-publish)
3. **Wait for GitHub Action** to complete
4. **Run test script**: `bash scripts/test_installation.sh`
5. **Verify on Test PyPI**: https://test.pypi.org/project/opencodemode/
6. **If tests pass**, ready for production PyPI!

## Next Steps After Successful Testing

Once all tests pass with Test PyPI:

1. Update version to production version (e.g., `0.1.0` or `1.0.0`)
2. Create a release on GitHub
3. Publish to production PyPI
4. Users can then use:
   ```bash
   pip install opencodemode
   # or
   uv add opencodemode
   ```

## Resources

- Test PyPI: https://test.pypi.org/project/opencodemode/
- Production PyPI: https://pypi.org/project/opencodemode/
- uv documentation: https://github.com/astral-sh/uv
- Python Packaging Guide: https://packaging.python.org/
