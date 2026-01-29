# Publishing nutaan-erp to PyPI

This guide will help you publish the Nutaan ERP SDK to PyPI.

## Prerequisites

1. **PyPI Account**
   - Create account at https://pypi.org/account/register/
   - Create account at https://test.pypi.org/account/register/ (for testing)

2. **Install Build Tools**
   ```bash
   pip install --upgrade pip setuptools wheel twine build
   ```

3. **API Tokens** (Recommended over password)
   - Go to https://pypi.org/manage/account/token/
   - Create new API token
   - Save it securely (you won't see it again)

## Step 1: Test Build Locally

```bash
cd /home/tecosys/ERP-agent/sdk

# Clean previous builds
rm -rf build/ dist/ *.egg-info/

# Build the package
python -m build

# This creates:
# - dist/nutaan-erp-1.0.0.tar.gz (source distribution)
# - dist/nutaan_erp-1.0.0-py3-none-any.whl (wheel)
```

## Step 2: Test on Test PyPI (Optional but Recommended)

```bash
# Upload to Test PyPI
python -m twine upload --repository testpypi dist/*

# When prompted:
# Username: __token__
# Password: <your-test-pypi-token>

# Test installation
pip install --index-url https://test.pypi.org/simple/ nutaan-erp

# Test it works
python -c "from nutaan_erp import AgentManager; print('Success!')"
```

## Step 3: Upload to Production PyPI

```bash
cd /home/tecosys/ERP-agent/sdk

# Upload to PyPI
python -m twine upload dist/*

# When prompted:
# Username: __token__
# Password: <your-pypi-token>
```

## Step 4: Verify Installation

```bash
# In a new environment
pip install nutaan-erp

# Test import
python -c "from nutaan_erp import AgentManager, AgentConfig; print('Success!')"
```

## Using .pypirc for Easier Uploads

Create `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-<your-token-here>

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-<your-test-token-here>
```

Then you can upload without entering credentials:

```bash
python -m twine upload dist/*
```

## Complete Workflow Script

```bash
#!/bin/bash
# publish.sh - Complete PyPI publish workflow

set -e

echo "🧹 Cleaning old builds..."
rm -rf build/ dist/ *.egg-info/

echo "📦 Building package..."
python -m build

echo "🔍 Checking package..."
python -m twine check dist/*

echo "📤 Uploading to PyPI..."
python -m twine upload dist/*

echo "✅ Done! Package published to PyPI"
echo "📥 Install with: pip install nutaan-erp"
```

Make it executable:
```bash
chmod +x publish.sh
./publish.sh
```

## Version Updates

When releasing new versions:

1. Update version in `sdk/nutaan_erp/__init__.py`
2. Update version in `sdk/setup.py`
3. Clean and rebuild:
   ```bash
   rm -rf build/ dist/ *.egg-info/
   python -m build
   python -m twine upload dist/*
   ```

## Troubleshooting

### Error: File already exists
- You cannot re-upload the same version
- Increment version number in `__init__.py` and `setup.py`

### Error: Invalid credentials
- Make sure you're using `__token__` as username
- Check your API token is correct
- Token should start with `pypi-`

### Import Error After Install
- Make sure package name in code is `nutaan_erp`
- PyPI package name is `nutaan-erp` (with hyphen)
- Users install with: `pip install nutaan-erp`
- Users import with: `from nutaan_erp import AgentManager`

### Testing Before Upload
```bash
# Check package structure
python -m build
tar -tzf dist/nutaan-erp-1.0.0.tar.gz

# Verify all files included
unzip -l dist/nutaan_erp-1.0.0-py3-none-any.whl
```

## Security Best Practices

1. **Never commit tokens to git**
2. Use API tokens instead of passwords
3. Use separate tokens for test and production PyPI
4. Rotate tokens periodically
5. Use `.pypirc` with restricted permissions:
   ```bash
   chmod 600 ~/.pypirc
   ```

## Package Information

- **PyPI Name**: `nutaan-erp`
- **Import Name**: `nutaan_erp`
- **Install Command**: `pip install nutaan-erp`
- **Usage**: `from nutaan_erp import AgentManager`

## Next Steps After Publishing

1. Update main README.md with PyPI installation instructions
2. Update Frappe integration requirements.txt:
   ```
   nutaan-erp>=1.0.0
   ```
3. Test installation in fresh ERPNext environment
4. Announce release!

## Useful Commands

```bash
# Check current PyPI package info
pip show nutaan-erp

# Uninstall
pip uninstall nutaan-erp

# Install specific version
pip install nutaan-erp==1.0.0

# Install latest
pip install --upgrade nutaan-erp

# View package on PyPI
# https://pypi.org/project/nutaan-erp/
```

## GitHub Release (Optional)

Create a GitHub release to match your PyPI version:

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

Then create release on GitHub with release notes.
