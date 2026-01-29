#!/bin/bash
# Test installation script for codemode package from Test PyPI
# This script tests both pip and uv installation methods

set -e  # Exit on error

PACKAGE_NAME="codemode"
TEST_PYPI_URL="https://test.pypi.org/simple/"
PYPI_URL="https://pypi.org/simple/"

echo "=========================================="
echo "Testing Installation Methods for ${PACKAGE_NAME}"
echo "=========================================="
echo ""

# Function to cleanup virtual environments
cleanup() {
    echo "Cleaning up test environments..."
    rm -rf test_pip_env test_uv_env
    echo "Cleanup complete."
}

# Set trap to cleanup on exit
trap cleanup EXIT

# Test 1: pip install
echo "=========================================="
echo "Test 1: Testing pip install"
echo "=========================================="
python -m venv test_pip_env
source test_pip_env/bin/activate

echo "Installing ${PACKAGE_NAME} with pip..."
pip install --index-url ${TEST_PYPI_URL} --extra-index-url ${PYPI_URL} ${PACKAGE_NAME}

echo ""
echo "Verifying installation..."
pip show ${PACKAGE_NAME}

echo ""
echo "Testing import..."
python -c "import codemode; print(f'Successfully imported codemode version: {codemode.__version__}')"

echo ""
echo "Testing CLI..."
codemode --help

deactivate
echo ""
echo "✅ pip install test PASSED"
echo ""

# Test 2: uv installation
echo "=========================================="
echo "Test 2: Testing uv pip install"
echo "=========================================="

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

python -m venv test_uv_env
source test_uv_env/bin/activate

echo "Installing ${PACKAGE_NAME} with uv pip..."
uv pip install --index-url ${TEST_PYPI_URL} --extra-index-url ${PYPI_URL} ${PACKAGE_NAME}

echo ""
echo "Verifying installation..."
uv pip show ${PACKAGE_NAME}

echo ""
echo "Testing import..."
python -c "import codemode; print(f'Successfully imported codemode version: {codemode.__version__}')"

echo ""
echo "Testing CLI..."
codemode --help

deactivate
echo ""
echo "✅ uv pip install test PASSED"
echo ""

# Test 3: uv add (requires a test project)
echo "=========================================="
echo "Test 3: Testing uv add in a new project"
echo "=========================================="

mkdir -p test_uv_project
cd test_uv_project

cat > pyproject.toml <<EOF
[project]
name = "test-codemode-installation"
version = "0.1.0"
dependencies = []

[[tool.uv.index]]
name = "testpypi"
url = "${TEST_PYPI_URL}"
default = true

[[tool.uv.index]]
name = "pypi"
url = "${PYPI_URL}"
explicit = true
EOF

echo "Adding ${PACKAGE_NAME} with uv add..."
uv add ${PACKAGE_NAME}

echo ""
echo "Verifying installation..."
uv pip show ${PACKAGE_NAME}

echo ""
echo "Testing import..."
uv run python -c "import codemode; print(f'Successfully imported codemode version: {codemode.__version__}')"

echo ""
echo "Testing CLI..."
uv run codemode --help

cd ..
rm -rf test_uv_project

echo ""
echo "✅ uv add test PASSED"
echo ""

echo "=========================================="
echo "All installation tests completed successfully! ✅"
echo "=========================================="
