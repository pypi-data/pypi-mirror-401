# Release Guide

This document describes the process for releasing new versions of docs-mcp-server.

## Prerequisites

Before releasing:

1. Ensure all tests pass: `pytest`
2. Ensure code is formatted: `black .` and `ruff check --fix .`
3. Review and update CHANGELOG.md
4. Verify documentation is up to date
5. Test the package locally: `pip install -e .` and `docs-mcp-server`

## Release Process

### 1. Update Version Number

Update the version in `pyproject.toml`:

```toml
[project]
name = "docs-mcp-server"
version = "0.2.0"  # Update this
```

Update the version in `src/docs_mcp/__init__.py`:

```python
__version__ = "0.2.0"  # Update this
```

### 2. Update CHANGELOG.md

Move items from `[Unreleased]` to a new version section:

```markdown
## [Unreleased]

## [0.2.0] - 2026-01-XX

### Added
- New feature X
- Support for Y

### Changed
- Updated Z behavior

### Fixed
- Bug fix for issue #N

[Unreleased]: https://github.com/thec0dewriter/docs_mcp/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/thec0dewriter/docs_mcp/releases/tag/v0.2.0
[0.1.0]: https://github.com/thec0dewriter/docs_mcp/releases/tag/v0.1.0
```

### 3. Commit Changes

```bash
git add pyproject.toml src/docs_mcp/__init__.py CHANGELOG.md
git commit -m "Bump version to 0.2.0"
git push origin main
```

### 4. Create and Push Tag

```bash
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin v0.2.0
```

This will automatically trigger the GitHub Actions release workflow.

### 5. Verify GitHub Release

1. Go to https://github.com/thec0dewriter/docs_mcp/releases
2. Verify the release was created with:
   - Correct version number
   - Release notes from CHANGELOG.md
   - Built distribution files (`.tar.gz` and `.whl`)

### 6. Verify PyPI Publication

1. Go to https://pypi.org/project/docs-mcp-server/
2. Verify the new version is listed
3. Check that the package metadata is correct

### 7. Test Installation

Test that users can install the new version:

```bash
# In a fresh virtual environment
pip install --upgrade docs-mcp-server

# Verify version
python -c "import docs_mcp; print(docs_mcp.__version__)"

# Test the CLI
docs-mcp-server --help
```

## PyPI Setup (One-time)

To enable automatic PyPI publishing, you need to set up a PyPI API token:

1. Create a PyPI account at https://pypi.org/
2. Generate an API token:
   - Go to https://pypi.org/manage/account/token/
   - Create a new token with scope "Entire account" (or specific to this project)
3. Add the token to GitHub Secrets:
   - Go to https://github.com/thec0dewriter/docs_mcp/settings/secrets/actions
   - Add a new secret named `PYPI_API_TOKEN`
   - Paste the API token (including the `pypi-` prefix)

## Manual Release (Fallback)

If the automatic release fails, you can release manually:

### 1. Build the Package

```bash
# Install build tools
pip install build twine

# Build distributions
python -m build

# Verify the build
twine check dist/*
```

### 2. Upload to TestPyPI (optional)

```bash
# Upload to TestPyPI first to verify
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ docs-mcp-server
```

### 3. Upload to PyPI

```bash
twine upload dist/*
```

## Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR** version (1.0.0): Incompatible API changes
- **MINOR** version (0.2.0): New functionality, backwards compatible
- **PATCH** version (0.1.1): Backwards compatible bug fixes

Pre-release versions:
- **Alpha**: 0.2.0-alpha.1 (early testing)
- **Beta**: 0.2.0-beta.1 (feature complete, testing)
- **RC**: 0.2.0-rc.1 (release candidate)

## Post-Release

After releasing:

1. Announce the release:
   - GitHub Discussions
   - Social media (if applicable)
   - Update documentation sites

2. Monitor for issues:
   - Check GitHub Issues
   - Monitor PyPI download stats
   - Watch for user feedback

3. Plan next release:
   - Create milestone for next version
   - Triage issues and feature requests

## Hotfix Process

For urgent bug fixes:

1. Create a hotfix branch from the release tag:
   ```bash
   git checkout -b hotfix/0.1.1 v0.1.0
   ```

2. Fix the bug and update version to patch release (0.1.1)

3. Commit, tag, and release:
   ```bash
   git commit -m "Fix critical bug XYZ"
   git tag -a v0.1.1 -m "Hotfix release 0.1.1"
   git push origin v0.1.1
   ```

4. Merge back to main:
   ```bash
   git checkout main
   git merge hotfix/0.1.1
   git push origin main
   ```

## Rollback

If a release has critical issues:

1. Mark the release as pre-release on GitHub
2. Yank the release from PyPI (if critical security issue):
   ```bash
   # Login to PyPI and use the web interface to "yank" the release
   # This prevents new installations but doesn't break existing ones
   ```
3. Release a fixed version immediately

## Checklist Template

Use this checklist for each release:

- [ ] All tests passing
- [ ] Code formatted and linted
- [ ] CHANGELOG.md updated
- [ ] Version bumped in pyproject.toml
- [ ] Version bumped in __init__.py
- [ ] Changes committed to main
- [ ] Tag created and pushed
- [ ] GitHub release created successfully
- [ ] PyPI package published
- [ ] Installation tested
- [ ] Documentation updated
- [ ] Release announced
