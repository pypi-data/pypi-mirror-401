# Contributing to SnapDepDoc

Thank you for your interest in contributing to SnapDepDoc! This document provides guidelines and instructions for contributing.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- `uv` package manager (recommended) or `pip`
- Git

### Development Setup

1. Fork and clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/docs_mcp.git
cd docs_mcp
```

2. Create a virtual environment and install dependencies:
```bash
# Using uv (recommended)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"

# Or using pip
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

3. Verify the installation:
```bash
snapdepdoc --help
```

## Development Workflow

### Code Style

We use:
- **Black** for code formatting (line length: 100)
- **Ruff** for linting
- **Type hints** for all function signatures

Format your code before committing:
```bash
black .
ruff check --fix .
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=docs_mcp --cov-report=html

# Run specific test file
pytest tests/test_parsers.py
```

### Testing Your Changes

1. Test the MCP server locally:
```bash
# Run the server
uv run snapdepdoc

# Test with MCP inspector (if available)
npx @modelcontextprotocol/inspector uv run snapdepdoc
```

2. Test with a real MCP client (Claude Desktop or VS Code)

## Making Changes

### Adding Support for a New Ecosystem

To add support for a new package manager or build system:

1. Add the file pattern to `SUPPORTED_FILES` in `src/docs_mcp/parsers.py`
2. Implement a parser method (e.g., `_parse_new_format`)
3. Add the parser to the `parse_file` method's dispatch logic
4. Add documentation sources to `DOCUMENTATION_SOURCES` in `src/docs_mcp/documentation.py`
5. Update the README.md with the new supported format
6. Add tests for the new parser

Example:
```python
# In parsers.py
SUPPORTED_FILES = {
    ...
    "new_format.ext": "new_ecosystem",
}

def _parse_new_format(self, file_path: Path) -> dict[str, Any]:
    """Parse new_format.ext file."""
    # Your parsing logic here
    return {
        "file_type": "new_ecosystem",
        "dependencies": {...},
        "dev_dependencies": {...},
    }
```

### Adding Documentation Sources

To add documentation sources for an ecosystem:

```python
# In documentation.py
DOCUMENTATION_SOURCES = {
    ...
    "new_ecosystem": {
        "registry": "https://registry.example.com/{library}",
        "docs_pattern": "https://docs.example.com/{library}/{version}/",
    }
}
```

## Submitting Changes

### Pull Request Process

1. Create a new branch for your feature or bugfix:
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

2. Make your changes and commit them with clear, descriptive messages:
```bash
git add .
git commit -m "Add support for new ecosystem XYZ"
```

3. Push to your fork:
```bash
git push origin feature/your-feature-name
```

4. Open a Pull Request on GitHub with:
   - Clear title describing the change
   - Description of what changed and why
   - Any related issue numbers (e.g., "Fixes #123")
   - Screenshots/examples if applicable

### PR Guidelines

- Keep PRs focused on a single feature or fix
- Update tests for your changes
- Update documentation (README, docstrings) as needed
- Ensure all tests pass
- Follow the existing code style
- Add an entry to CHANGELOG.md under [Unreleased]

## Reporting Issues

When reporting issues, please include:

1. **Description**: Clear description of the issue
2. **Steps to Reproduce**: Minimal steps to reproduce the problem
3. **Expected Behavior**: What you expected to happen
4. **Actual Behavior**: What actually happened
5. **Environment**:
   - Python version
   - Operating system
   - Package version
6. **Sample Files**: Example project files that trigger the issue (if applicable)

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Assume good intentions

### Unacceptable Behavior

- Harassment, discrimination, or exclusionary behavior
- Trolling or insulting comments
- Publishing others' private information

## Questions?

- Open an issue for bugs or feature requests
- Start a discussion for questions or ideas
- Check existing issues before creating new ones

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
