# Publishing emotion-framework to PyPI

This guide explains how to publish the `emotion-framework` package to PyPI.

## Prerequisites

1. **PyPI Account**: Create accounts on:
   - [PyPI](https://pypi.org/account/register/) (production)
   - [TestPyPI](https://test.pypi.org/account/register/) (testing)

2. **Install build tools**:
```bash
pip install --upgrade build twine
```

## Directory Structure

The package should have this structure:

```
emotion_framework/
├── pyproject.toml      # Modern Python project configuration
├── setup.py            # Legacy setup file (optional, for compatibility)
├── README.md           # Package description (shows on PyPI)
├── LICENSE             # MIT License
├── MANIFEST.in         # Include non-Python files
├── __init__.py         # Package entry point
├── core/               # Core modules
├── processors/         # Processing modules
├── analyzers/          # Analysis modules
└── models/             # Model definitions
```

## Step-by-Step Publishing

### 1. Clean Previous Builds

```bash
cd /Users/dogukangundogan/Desktop/Dev/random-feature-representation-boosting/app/emotion_framework

# Remove old build artifacts
rm -rf build/ dist/ *.egg-info/
```

### 2. Build the Package

```bash
# Build source distribution and wheel
python -m build
```

This creates:
- `dist/emotion-framework-1.0.0.tar.gz` (source distribution)
- `dist/emotion_framework-1.0.0-py3-none-any.whl` (wheel)

### 3. Test on TestPyPI (Recommended)

First, test your package on TestPyPI:

```bash
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# You'll be prompted for:
# Username: __token__
# Password: <your TestPyPI API token>
```

#### Get API Tokens:
- **TestPyPI**: https://test.pypi.org/manage/account/token/
- **PyPI**: https://pypi.org/manage/account/token/

#### Test Installation:

```bash
# Create a test environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ emotion-framework

# Test it
python -c "from emotion_framework import EmotionAnalysisPipeline; print('Success!')"

# Deactivate and remove test env
deactivate
rm -rf test_env
```

**Note**: `--extra-index-url https://pypi.org/simple/` is needed because your package dependencies (like torch, opencv-python, etc.) are on PyPI, not TestPyPI.

### 4. Publish to PyPI (Production)

Once you've tested on TestPyPI:

```bash
# Upload to PyPI
python -m twine upload dist/*

# You'll be prompted for:
# Username: __token__
# Password: <your PyPI API token>
```

### 5. Verify Publication

```bash
# Check the package page
open https://pypi.org/project/emotion-framework/

# Install in a fresh environment
pip install emotion-framework

# Test
python -c "from emotion_framework import EmotionAnalysisPipeline; print('✅ Published successfully!')"
```

## Using API Tokens

Instead of entering username/password every time, use API tokens:

### Create ~/.pypirc

```bash
# Create the file
cat > ~/.pypirc << 'EOF'
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-AgEIcH...your_token_here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-AgENdGVzdC...your_test_token_here
EOF

# Secure the file
chmod 600 ~/.pypirc
```

Now you can upload without entering credentials:

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

## Updating the Package

When you make changes:

### 1. Update Version

Edit `pyproject.toml`:

```toml
[project]
version = "1.0.1"  # Increment version
```

Also update `setup.py` if present:

```python
setup(
    version="1.0.1",  # Keep in sync with pyproject.toml
    ...
)
```

And `__init__.py`:

```python
__version__ = "1.0.1"
```

### 2. Update CHANGELOG.md (Optional but recommended)

Create a `CHANGELOG.md`:

```markdown
# Changelog

## [1.0.1] - 2026-01-14
### Added
- New feature X
### Fixed
- Bug in Y
### Changed
- Improved Z

## [1.0.0] - 2026-01-14
### Added
- Initial release
```

### 3. Rebuild and Upload

```bash
# Clean old builds
rm -rf build/ dist/ *.egg-info/

# Build new version
python -m build

# Upload (test first!)
twine upload --repository testpypi dist/*

# Then production
twine upload dist/*
```

## Common Issues & Solutions

### Issue: "File already exists"

**Problem**: You're trying to upload a version that already exists.

**Solution**: You cannot replace existing versions on PyPI. Increment the version number.

### Issue: Package structure not found

**Problem**: `package_dir` or `packages` configuration is wrong.

**Solution**: Use `pyproject.toml` with explicit package listing:

```toml
[tool.setuptools]
packages = ["emotion_framework", "emotion_framework.core", ...]

[tool.setuptools.package-dir]
emotion_framework = "."
```

### Issue: Dependencies not installing

**Problem**: `install_requires` or `dependencies` list is incorrect.

**Solution**: Ensure all dependencies are listed in `pyproject.toml`:

```toml
[project]
dependencies = [
    "torch>=2.2.0",
    # ... all your dependencies
]
```

### Issue: README not showing on PyPI

**Problem**: README path or format issue.

**Solution**: Ensure `pyproject.toml` has:

```toml
[project]
readme = "README.md"
```

And `README.md` is in the same directory as `pyproject.toml`.

### Issue: Missing files in distribution

**Problem**: Non-Python files not included.

**Solution**: Update `MANIFEST.in`:

```
include README.md LICENSE
include *.yaml *.json
recursive-include emotion_framework *.yaml *.json
```

## Best Practices

1. **Semantic Versioning**: Use [SemVer](https://semver.org/)
   - `1.0.0` → Major.Minor.Patch
   - Major: Breaking changes
   - Minor: New features (backward compatible)
   - Patch: Bug fixes

2. **Always Test on TestPyPI First**

3. **Git Tag Releases**:
```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

4. **Keep Dependencies Up to Date**: But pin major versions to avoid breaking changes.

5. **Maintain a CHANGELOG**: Users appreciate knowing what changed.

6. **CI/CD**: Automate publishing with GitHub Actions (see below).

## Automating with GitHub Actions (Optional)

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install build twine
      
      - name: Build package
        run: python -m build
      
      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: twine upload dist/*
```

Then create a GitHub secret `PYPI_API_TOKEN` with your PyPI token.

## Quick Reference

```bash
# Build
python -m build

# Test upload
twine upload --repository testpypi dist/*

# Production upload
twine upload dist/*

# Check distribution
twine check dist/*

# List files in distribution
tar -tzf dist/emotion-framework-1.0.0.tar.gz
```

## Resources

- [Python Packaging User Guide](https://packaging.python.org/)
- [PyPI Help](https://pypi.org/help/)
- [TestPyPI](https://test.pypi.org/)
- [Semantic Versioning](https://semver.org/)
- [PEP 517](https://peps.python.org/pep-0517/) - Modern build system
- [PEP 621](https://peps.python.org/pep-0621/) - Project metadata in pyproject.toml

---

**Ready to publish?** Follow the steps above and your package will be live on PyPI! 🚀

