# PyPI Publishing Guide

## Prerequisites

1. Create an account at https://pypi.org/account/register/
2. Enable two-factor authentication (2FA)
3. Generate an API Token at https://pypi.org/manage/account/token/

## Create API Token

1. Go to https://pypi.org/manage/account/token/
2. Click "Add API token"
3. Token name: e.g., "git-pluse-upload"
4. Scope: "Entire account" (for first-time publishers)
5. Click "Add token"
6. **Important**: Copy the token immediately (you won't see it again)

## Setup .pypirc

Create or edit `~/.pypirc` file:

```ini
[pypi]
  username = __token__
  password = pypi-<your-token-here>

[testpypi]
  username = __token__
  password = pypi-<your-token-here>
```

**Important**: The username must be exactly `__token__` (with two underscores)
The password is the full token string starting with `pypi-`

## Build the Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Build the package
python -m build
```

This creates:
- `dist/git-pluse-1.0.0.tar.gz` (sdist)
- `dist/git_pluse-1.0.0-py3-none-any.whl` (wheel)

## Test with TestPyPI

```bash
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ git-pluse
```

## Publish to PyPI (Production)

```bash
# Upload to PyPI
python -m twine upload dist/*
```

## Verify

After successful upload, verify at:
- Production: https://pypi.org/project/git-pluse/
- Test: https://test.pypi.org/project/git-pluse/

## Troubleshooting

### Error: 403 Forbidden

If you see "Username/Password authentication is no longer supported":

1. Ensure your `.pypirc` has:
   - `username = __token__` (exact)
   - `password = pypi-<your-token>` (full token)

2. Or use command-line:
   ```bash
   python -m twine upload --username __token__ --password pypi-<token> dist/*
   ```

### Package name already exists

Choose a different unique name in `setup.py` and `pyproject.toml`.

### Upload failed

- Run twine check: `twine check dist/*`
- Check file permissions on dist/
- Ensure version number is incremented
