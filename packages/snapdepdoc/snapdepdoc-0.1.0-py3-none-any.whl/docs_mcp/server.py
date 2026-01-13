"""Main server implementation using FastMCP."""

import logging
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

from .parsers import ProjectFileParser
from .documentation import DocumentationFetcher

logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("snapdepdoc")


@mcp.tool()
async def list_project_files(directory: str) -> dict[str, Any]:
    """
    Discover project definition files in a directory.

    Args:
        directory: Path to the directory to scan

    Returns:
        Dictionary with found project files and their types
    """
    parser = ProjectFileParser()
    project_files = parser.discover_project_files(Path(directory))

    return {
        "directory": directory,
        "files": [
            {
                "path": str(file_path),
                "type": file_type,
                "exists": file_path.exists(),
            }
            for file_path, file_type in project_files
        ],
    }


@mcp.tool()
async def parse_dependencies(file_path: str) -> dict[str, Any]:
    """
    Parse dependencies from a project definition file.

    Args:
        file_path: Path to the project file (pyproject.toml, package.json, etc.)

    Returns:
        Dictionary containing dependencies with versions
    """
    parser = ProjectFileParser()
    dependencies = parser.parse_file(Path(file_path))

    return {
        "file_path": file_path,
        "file_type": dependencies.get("file_type", "unknown"),
        "dependencies": dependencies.get("dependencies", {}),
        "dev_dependencies": dependencies.get("dev_dependencies", {}),
    }


@mcp.tool()
async def get_documentation_url(
    library: str, version: str | None = None, ecosystem: str = "python"
) -> dict[str, Any]:
    """
    Get documentation URL for a specific library and version.

    Args:
        library: Name of the library
        version: Version of the library (optional, uses latest if not specified)
        ecosystem: Ecosystem (python, npm, maven, etc.)

    Returns:
        Dictionary with documentation URLs and metadata
    """
    fetcher = DocumentationFetcher()
    doc_info = await fetcher.get_documentation(library, version, ecosystem)

    return {
        "library": library,
        "version": version or "latest",
        "ecosystem": ecosystem,
        "documentation_url": doc_info.get("url"),
        "api_reference": doc_info.get("api_reference"),
        "changelog": doc_info.get("changelog"),
    }


@mcp.tool()
async def search_api_documentation(
    library: str, query: str, version: str | None = None, ecosystem: str = "python"
) -> dict[str, Any]:
    """
    Search for specific API documentation within a library.

    Args:
        library: Name of the library
        query: Search query (e.g., function name, class name)
        version: Version of the library
        ecosystem: Ecosystem (python, npm, maven, etc.)

    Returns:
        Search results with relevant documentation links
    """
    fetcher = DocumentationFetcher()
    results = await fetcher.search_documentation(library, query, version, ecosystem)

    return {
        "library": library,
        "query": query,
        "version": version or "latest",
        "ecosystem": ecosystem,
        "results": results,
    }


@mcp.resource("dependencies://{project_path}")
async def get_project_dependencies(project_path: str) -> str:
    """
    Get all dependencies for a project as a formatted resource.

    Args:
        project_path: Path to the project directory or file

    Returns:
        Formatted string with all project dependencies
    """
    parser = ProjectFileParser()
    path = Path(project_path)

    # If directory, find project files first
    if path.is_dir():
        project_files = parser.discover_project_files(path)
        if not project_files:
            return f"No project files found in {project_path}"
        file_path, _ = project_files[0]  # Use first found file
    else:
        file_path = path

    dependencies = parser.parse_file(file_path)

    # Format output
    output = [f"# Dependencies for {file_path.name}\n"]

    if dependencies.get("dependencies"):
        output.append("## Production Dependencies\n")
        for name, version in dependencies["dependencies"].items():
            output.append(f"- {name}: {version}")
        output.append("")

    if dependencies.get("dev_dependencies"):
        output.append("## Development Dependencies\n")
        for name, version in dependencies["dev_dependencies"].items():
            output.append(f"- {name}: {version}")

    return "\n".join(output)


@mcp.resource("docs://{library}@{version}")
async def get_library_documentation(library: str, version: str = "latest") -> str:
    """
    Get documentation for a specific library version.

    Args:
        library: Name of the library
        version: Version string (default: "latest")

    Returns:
        Documentation content or links
    """
    # Parse ecosystem from library name if contains prefix
    ecosystem = "python"  # default
    if library.startswith("npm:"):
        ecosystem = "npm"
        library = library[4:]
    elif library.startswith("mvn:"):
        ecosystem = "maven"
        library = library[4:]

    fetcher = DocumentationFetcher()
    doc_info = await fetcher.get_documentation(
        library, version if version != "latest" else None, ecosystem
    )

    output = [
        f"# Documentation for {library} @ {version}\n",
        f"**Ecosystem**: {ecosystem}\n",
    ]

    if doc_info.get("url"):
        output.append(f"**Documentation**: {doc_info['url']}")

    if doc_info.get("api_reference"):
        output.append(f"**API Reference**: {doc_info['api_reference']}")

    if doc_info.get("changelog"):
        output.append(f"**Changelog**: {doc_info['changelog']}")

    if doc_info.get("description"):
        output.append(f"\n## Description\n{doc_info['description']}")

    return "\n".join(output)


def main():
    """Run the MCP server."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
