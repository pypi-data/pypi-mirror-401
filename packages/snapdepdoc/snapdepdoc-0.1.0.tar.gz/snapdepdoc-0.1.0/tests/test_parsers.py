import pytest
from pathlib import Path
from docs_mcp.parsers import ProjectFileParser

def test_parse_pyproject_toml(tmp_path):
    # Create a temporary pyproject.toml file
    pyproject_content = """
    [project]
    dependencies = [
        "requests>=2.25.1",
        "flask==2.0.1"
    ]

    [project.optional-dependencies]
    dev = [
        "pytest>=6.0",
        "black==21.9b0"
    ]
    """
    pyproject_file = tmp_path / "pyproject.toml"
    pyproject_file.write_text(pyproject_content)

    # Initialize the parser
    parser = ProjectFileParser()

    # Parse the file
    result = parser._parse_pyproject_toml(pyproject_file)

    # Assertions
    assert result["file_type"] == "python"
    assert result["dependencies"] == {
        "requests": ">=2.25.1",
        "flask": "==2.0.1"
    }
    print(result)
    assert result["dev_dependencies"] == {
        "pytest (dev)": ">=6.0",
        "black (dev)": "==21.9b0"
    }