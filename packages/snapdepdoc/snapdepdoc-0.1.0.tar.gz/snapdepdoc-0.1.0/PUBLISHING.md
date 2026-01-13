# Publishing to PyPI

This guide explains how to publish SnapDepDoc to PyPI (Python Package Index).

## Prerequisites

1. **PyPI Account**
   - Create an account at https://pypi.org/account/register/
   - Verify your email address

2. **TestPyPI Account** (optional but recommended)
   - Create an account at https://test.pypi.org/account/register/
   - Used for testing releases before publishing to production PyPI

3. **API Tokens**
   - Create a PyPI API token at https://pypi.org/manage/account/token/
   - Create a TestPyPI token at https://test.pypi.org/manage/account/token/
   - Store these securely - you'll only see them once!

## Setup

### Install Build Tools

```bash
pip install build twine
```

### Configure PyPI Credentials

Create or edit `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR_PYPI_TOKEN_HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR_TESTPYPI_TOKEN_HERE
```

**Security Note**: Keep your `.pypirc` file private! Add it to `.gitignore`.

## Manual Publishing (First Release)

### 1. Prepare the Release

```bash
# Ensure you're on the main branch
git checkout main
git pull

# Verify version in pyproject.toml is correct
grep version pyproject.toml

# Verify version in __init__.py matches
grep __version__ src/docs_mcp/__init__.py
```

### 2. Build the Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build source distribution and wheel
python -m build
```

This creates two files in `dist/`:
- `snapdepdoc-VERSION.tar.gz` (source distribution)
- `snapdepdoc-VERSION-py3-none-any.whl` (wheel)

### 3. Verify the Build

```bash
# Check package with twine
twine check dist/*

# Inspect the contents
tar -tzf dist/snapdepdoc-*.tar.gz | head -20
unzip -l dist/snapdepdoc-*.whl | head -20
```

### 4. Test on TestPyPI (Recommended)

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ snapdepdoc

# Verify it works
snapdepdoc --version
python -c "from docs_mcp import server; print('Success!')"
```

Note: `--extra-index-url` allows pip to install dependencies from the main PyPI.

### 5. Upload to PyPI

```bash
# Upload to production PyPI
twine upload dist/*
```

### 6. Verify Publication

```bash
# Check on PyPI
open https://pypi.org/project/snapdepdoc/

# Test installation
pip install --upgrade snapdepdoc

# Verify version
pip show snapdepdoc
```

## Automated Publishing with GitHub Actions

The repository includes a GitHub Actions workflow (`.github/workflows/release.yml`) that automatically publishes to PyPI when you create a git tag.

### Setup GitHub Secrets

1. Go to your repository settings
2. Navigate to Secrets and variables → Actions
3. Add a new repository secret:
   - Name: `PYPI_API_TOKEN`
   - Value: Your PyPI API token (including `pypi-` prefix)

### Create a Release

```bash
# Ensure main branch is up to date
git checkout main
git pull

# Create and push a tag
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin v0.1.0
```

The workflow will automatically:
1. Build the package
2. Run checks
3. Create a GitHub Release
4. Upload to PyPI

### Monitor the Workflow

1. Go to https://github.com/YOUR_USERNAME/docs_mcp/actions
2. Find the "Release" workflow run
3. Check for any errors
4. Verify the package appears on PyPI

## Post-Release Checklist

After publishing:

- [ ] Verify package on PyPI: https://pypi.org/project/snapdepdoc/
- [ ] Test installation: `pip install snapdepdoc`
- [ ] Check that README renders correctly on PyPI
- [ ] Update CHANGELOG.md with release date
- [ ] Create GitHub Release with release notes
- [ ] Announce release (if applicable)
- [ ] Monitor for issues

## Version Bumping

For the next release:

1. Update version in `pyproject.toml`:
```toml
version = "0.2.0"
```

2. Update version in `src/docs_mcp/__init__.py`:
```python
__version__ = "0.2.0"
```

3. Update CHANGELOG.md:
```markdown
## [Unreleased]

## [0.2.0] - 2026-XX-XX
### Added
- New features...
```

4. Commit and tag:
```bash
git add pyproject.toml src/docs_mcp/__init__.py CHANGELOG.md
git commit -m "Bump version to 0.2.0"
git push
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin v0.2.0
```

## Troubleshooting

### "File already exists" Error

**Problem**: Trying to upload a version that already exists on PyPI

**Solution**: 
- You cannot overwrite existing versions on PyPI
- Bump the version number and rebuild
- Delete local dist/ folder before rebuilding

### Build Artifacts Missing

**Problem**: `dist/` folder is empty or missing files

**Solution**:
```bash
# Clean and rebuild
rm -rf dist/ build/ *.egg-info
python -m build
```

### Import Errors After Installation

**Problem**: Package installs but imports fail

**Solution**:
- Check `[tool.hatch.build.targets.wheel]` in pyproject.toml
- Verify package structure with: `unzip -l dist/*.whl`
- Ensure `src/docs_mcp/__init__.py` exists

### README Not Rendering on PyPI

**Problem**: README appears as plain text on PyPI

**Solution**:
- Ensure `readme = "README.md"` in pyproject.toml
- Verify README.md is in the project root
- Check for Markdown syntax errors

### Authentication Failed

**Problem**: "Invalid credentials" when uploading

**Solution**:
- Verify your API token is correct
- Ensure token starts with `pypi-`
- Check `.pypirc` format
- Token might have expired - generate a new one

## Best Practices

1. **Always test on TestPyPI first** for new releases
2. **Use version tags** that match the package version (v0.1.0)
3. **Keep CHANGELOG.md updated** before releasing
4. **Don't delete releases** - yank them if there are issues
5. **Use semantic versioning** (MAJOR.MINOR.PATCH)
6. **Test installation** in a fresh environment
7. **Update documentation** before releasing

## Additional Resources

- [Python Packaging User Guide](https://packaging.python.org/)
- [PyPI Help](https://pypi.org/help/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [Semantic Versioning](https://semver.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## Support

For issues with publishing:
- Check the [Python Packaging Guide](https://packaging.python.org/tutorials/packaging-projects/)
- Ask on [Python Discourse](https://discuss.python.org/c/packaging/)
- File an issue in the repository
