# Publishing to PyPI

This project uses GitHub Actions to automatically publish to PyPI.

## Setup

### Option 1: Trusted Publishing (Recommended)

1. Go to [PyPI Account Settings](https://pypi.org/manage/account/publishing/)
2. Click "Add a pending publisher"
3. Fill in:
   - **Owner**: Your GitHub username or organization (e.g., `your-username` or `your-org`)
   - **Repository name**: `noodler-python` (or your actual repo name)
   - **Workflow filename**: `publish.yml`
4. Click "Add"
5. Verify the publisher appears in your pending publishers list

### Option 2: API Token (Alternative)

1. Go to [PyPI Account Settings](https://pypi.org/manage/account/token/)
2. Create a new API token with "Upload packages" scope
3. Copy the token (it starts with `pypi-`)
4. In your GitHub repository, go to Settings > Secrets and variables > Actions
5. Add a new secret named `PYPI_API_TOKEN` with your token value
6. Update `.github/workflows/publish.yml` to uncomment the `env` section in the "Publish to PyPI" step

## Publishing

The workflow triggers automatically in three ways:

### 1. Create a GitHub Release

1. Go to your repository's Releases page
2. Click "Create a new release"
3. Create a new tag (e.g., `v0.1.0`)
4. Fill in release details and publish
5. The workflow will automatically run and publish to PyPI

### 2. Push a Tag

```bash
# Update version in pyproject.toml first
git tag v0.1.0
git push origin v0.1.0
```

The workflow will automatically detect the tag and publish.

### 3. Manual Workflow Dispatch

1. Go to Actions > Publish to PyPI
2. Click "Run workflow"
3. Enter the version number (e.g., `0.1.0`)
4. Click "Run workflow"

## Version Management

- Make sure to update the `version` field in `pyproject.toml` before publishing
- Use semantic versioning (e.g., `0.1.0`, `0.1.1`, `1.0.0`)
- Tag names should match the version (with or without `v` prefix)

## Testing Before Publishing

You can test the build locally:

```bash
pip install build twine
python -m build
twine check dist/*
```

To test upload to TestPyPI:

```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

