# ✅ PyPI Publishing Checklist

## Before Publishing

- [ ] **Version Updated**
  - [ ] `sdk/nutaan_erp/__init__.py` → `__version__ = "1.0.0"`
  - [ ] `sdk/setup.py` → `version="1.0.0"`

- [ ] **README Updated**
  - [ ] Installation instructions show PyPI install
  - [ ] Examples are correct
  - [ ] Links work

- [ ] **Dependencies Correct**
  - [ ] `requirements.txt` lists all dependencies
  - [ ] Version constraints are appropriate

- [ ] **License File Present**
  - [ ] `sdk/LICENSE` exists with MIT license

- [ ] **Package Structure Correct**
  - [ ] All `__init__.py` files present
  - [ ] No sensitive data in code
  - [ ] No hardcoded paths

## Publishing Steps

1. **Install Build Tools**
   ```bash
   pip install --upgrade pip setuptools wheel twine build
   ```

2. **Build Package**
   ```bash
   cd /home/tecosys/ERP-agent/sdk
   ./publish.sh
   ```

3. **Test on Test PyPI** (Optional)
   ```bash
   python -m twine upload --repository testpypi dist/*
   pip install --index-url https://test.pypi.org/simple/ nutaan-erp
   python -c "from nutaan_erp import AgentManager; print('Works!')"
   ```

4. **Upload to PyPI**
   ```bash
   python -m twine upload dist/*
   ```
   - Username: `__token__`
   - Password: Your PyPI API token

5. **Verify Installation**
   ```bash
   # In fresh environment
   pip install nutaan-erp
   python -c "from nutaan_erp import AgentManager, AgentConfig; print('Success!')"
   ```

## After Publishing

- [ ] **Test Installation in ERPNext**
  ```bash
  cd ~/frappe-bench
  ./env/bin/pip install nutaan-erp
  bench restart
  # Test widget in browser
  ```

- [ ] **Update Documentation**
  - [ ] Main README shows PyPI install
  - [ ] Frappe integration README updated
  - [ ] DOCUMENTATION.md updated

- [ ] **Announce Release**
  - [ ] GitHub release created
  - [ ] Tag version: `git tag -a v1.0.0 -m "Release 1.0.0"`
  - [ ] Push tags: `git push origin v1.0.0`

- [ ] **Monitor PyPI**
  - [ ] Check package page: https://pypi.org/project/nutaan-erp/
  - [ ] Verify statistics
  - [ ] Check for issues

## Quick Commands

```bash
# Build
cd /home/tecosys/ERP-agent/sdk && ./publish.sh

# Upload to Test PyPI
python -m twine upload --repository testpypi dist/*

# Upload to Production PyPI
python -m twine upload dist/*

# Install from PyPI
pip install nutaan-erp

# Test import
python -c "from nutaan_erp import AgentManager; print('OK')"
```

## Version Numbering

- **Major.Minor.Patch** (e.g., 1.0.0)
- **Major**: Breaking changes
- **Minor**: New features, backward compatible
- **Patch**: Bug fixes

Next versions:
- 1.0.3 - Bug fixes
- 1.1.0 - New features
- 2.0.0 - Breaking changes

## Common Issues

**Problem**: "File already exists"
- **Solution**: Increment version number, rebuild, re-upload

**Problem**: Import fails after install
- **Solution**: Check package name
  - Install: `pip install nutaan-erp`
  - Import: `from nutaan_erp import AgentManager`

**Problem**: Dependencies not installing
- **Solution**: Check `requirements.txt` is included in MANIFEST.in

## Support

- PyPI Package: https://pypi.org/project/nutaan-erp/
- Issues: https://github.com/tecosys/nutaan-erp/issues
- Documentation: See PUBLISHING.md for detailed guide
