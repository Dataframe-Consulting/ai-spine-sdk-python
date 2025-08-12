# Deploy to PyPI Guide

This guide explains how to deploy the AI Spine SDK to PyPI (Python Package Index).

## Prerequisites

1. **PyPI Account**: Create an account at [https://pypi.org/account/register/](https://pypi.org/account/register/)
2. **TestPyPI Account**: Create an account at [https://test.pypi.org/account/register/](https://test.pypi.org/account/register/)
3. **Enable 2FA**: Two-factor authentication is required for both accounts
4. **Install Tools**:
   ```bash
   pip install build twine
   ```

## Setup Authentication

### 1. Create API Tokens

#### For TestPyPI:
1. Go to [https://test.pypi.org/manage/account/token/](https://test.pypi.org/manage/account/token/)
2. Create a token with scope "Entire account"
3. Save as `TEST_PIP_TOKEN` in `.env.local`

#### For PyPI:
1. Go to [https://pypi.org/manage/account/token/](https://pypi.org/manage/account/token/)
2. Create a token with scope "Entire account" (or project-specific after first upload)
3. Save as `PIP_TOKEN` in `.env.local`

### 2. Configure Environment

Create or update `.env.local`:
```bash
# PyPI tokens
PIP_TOKEN=pypi-AgEIcHlwaS5vcmc...
TEST_PIP_TOKEN=pypi-AgENdGVzdC5weXBpLm9yZw...
```

## Deployment Process

### Step 1: Update Version

Edit `ai_spine/__version__.py`:
```python
__version__ = "0.1.1"  # Increment version number
```

### Step 2: Build Package

```bash
# Load environment variables
source .env.local

# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build the package
python -m build
```

This creates:
- `dist/ai_spine_sdk-0.1.X.tar.gz` (source distribution)
- `dist/ai_spine_sdk-0.1.X-py3-none-any.whl` (wheel distribution)

### Step 3: Deploy to TestPyPI (Recommended First)

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/* -u __token__ -p $TEST_PIP_TOKEN

# You'll see output like:
# Uploading ai_spine_sdk-0.1.X-py3-none-any.whl
# 100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# View at: https://test.pypi.org/project/ai-spine-sdk/0.1.X/
```

### Step 4: Test Installation from TestPyPI

```bash
# Create a clean virtual environment for testing
python -m venv test-env
source test-env/bin/activate  # Windows: test-env\Scripts\activate

# Install from TestPyPI
pip install -i https://test.pypi.org/simple/ ai-spine-sdk --no-deps

# Install dependencies separately (TestPyPI doesn't have all packages)
pip install requests python-dateutil

# Test the package
python -c "from ai_spine import AISpine; print('Import successful!')"

# Cleanup
deactivate
rm -rf test-env
```

### Step 5: Deploy to Production PyPI

```bash
# If TestPyPI deployment worked, deploy to real PyPI
twine upload dist/* -u __token__ -p $PIP_TOKEN

# You'll see output like:
# Uploading ai_spine_sdk-0.1.X-py3-none-any.whl
# 100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# View at: https://pypi.org/project/ai-spine-sdk/0.1.X/
```

### Step 6: Verify Production Installation

```bash
# Wait 1-2 minutes for PyPI to update, then test
pip install ai-spine-sdk

# Verify
python -c "from ai_spine import AISpine; client = AISpine(); print('Success!')"
```

## Post-Deployment

### Update GitHub

After successful deployment:

```bash
# Create a git tag for the release
git tag -a v0.1.X -m "Release version 0.1.X"
git push origin v0.1.X

# Create GitHub release (optional)
gh release create v0.1.X --title "Release v0.1.X" --notes "See CHANGELOG.md"
```

### Update Token Scope (Optional)

After first successful upload, you can create project-specific tokens:
1. Go to [https://pypi.org/manage/project/ai-spine-sdk/settings/](https://pypi.org/manage/project/ai-spine-sdk/settings/)
2. Create a token with scope "Project: ai-spine-sdk"
3. Replace the general token with this project-specific one

## Troubleshooting

### Common Issues

1. **403 Forbidden**: Token doesn't have permission or wrong token for the repository
   - Ensure you're using `TEST_PIP_TOKEN` for TestPyPI
   - Ensure you're using `PIP_TOKEN` for PyPI

2. **Version already exists**: Can't overwrite existing versions
   - Increment version in `__version__.py`
   - Delete and rebuild (`rm -rf dist/ build/`)

3. **Package name taken**: Someone else owns the name
   - Check availability at pypi.org
   - Choose a different name in `setup.py`

4. **Authentication failed**: Token format issue
   - Username must be `__token__` (literal string)
   - Password is your actual token

### Useful Commands

```bash
# Check what will be included in the package
python setup.py sdist --formats=gztar --dry-run

# Validate package before upload
twine check dist/*

# Upload with verbose output for debugging
twine upload --verbose dist/*
```

## Version Management

Follow [Semantic Versioning](https://semver.org/):
- **MAJOR.MINOR.PATCH** (e.g., 1.2.3)
- **MAJOR**: Breaking API changes
- **MINOR**: New features, backwards compatible
- **PATCH**: Bug fixes, backwards compatible

For pre-releases:
- Alpha: `0.1.0a1`
- Beta: `0.1.0b1`
- Release Candidate: `0.1.0rc1`

## Security Notes

1. **Never commit tokens** to git
2. Keep `.env.local` in `.gitignore`
3. Use project-specific tokens when possible
4. Rotate tokens periodically
5. Use 2FA on PyPI accounts

## Automation (Future)

Consider setting up GitHub Actions for automated deployment:
- On tag push: Auto-deploy to PyPI
- On PR: Run tests and validation
- See `.github/workflows/` for examples

---

**Important**: Always test on TestPyPI first, especially for major changes!