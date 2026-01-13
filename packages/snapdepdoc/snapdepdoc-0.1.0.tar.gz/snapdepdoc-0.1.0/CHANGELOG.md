# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-01-10

### Added
- Initial release of SnapDepDoc
- Support for parsing multiple project definition file formats:
  - Python: `pyproject.toml`, `requirements.txt`, `setup.py`
  - Node.js: `package.json`, `package-lock.json`
  - Java: `pom.xml` (Maven)
  - Gradle: `build.gradle`, `build.gradle.kts`
  - Scala: `build.sbt` (SBT)
  - Rust: `Cargo.toml`
  - Go: `go.mod`
  - Ruby: `Gemfile`
- MCP tools for project file discovery and dependency parsing
- Documentation fetcher for Python, npm, Maven, and SBT ecosystems
- MCP resources for accessing dependency lists and library documentation
- FastMCP-based server implementation with stdio transport

### Features
- `list_project_files` tool: Discover project definition files in a directory
- `parse_dependencies` tool: Extract dependencies from project files
- `get_documentation_url` tool: Get documentation URLs for specific library versions
- `search_api_documentation` tool: Search for API documentation
- `dependencies://{project_path}` resource: List all dependencies with versions
- `docs://{library}@{version}` resource: Access documentation for specific library version

[Unreleased]: https://github.com/thec0dewriter/docs_mcp/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/thec0dewriter/docs_mcp/releases/tag/v0.1.0
