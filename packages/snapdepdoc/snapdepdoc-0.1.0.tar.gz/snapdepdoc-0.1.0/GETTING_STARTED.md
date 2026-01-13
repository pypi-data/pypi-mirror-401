# Getting Started with SnapDepDoc

This guide will help you get started with SnapDepDoc after installation.

## Installation

### From PyPI (Recommended)

Once released, you can install SnapDepDoc from PyPI:

```bash
pip install snapdepdoc
```

Or using uv (recommended for MCP development):

```bash
uv pip install snapdepdoc
```

### From Source

For the latest development version:

```bash
git clone https://github.com/thec0dewriter/docs_mcp.git
cd docs_mcp
pip install -e .
```

## Configuration

### Claude Desktop

1. Locate your Claude Desktop configuration file:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

2. Add the SnapDepDoc server configuration:

```json
{
  "mcpServers": {
    "snapdepdoc": {
      "command": "snapdepdoc"
    }
  }
}
```

3. Restart Claude Desktop

### VS Code

1. Create or edit `.vscode/mcp.json` in your project root:

```json
{
  "servers": {
    "snapdepdoc": {
      "type": "stdio",
      "command": "snapdepdoc"
    }
  }
}
```

2. Reload VS Code window

### Other MCP Clients

For other MCP clients, use the stdio transport with the command:

```bash
snapdepdoc
```

## Usage Examples

### Example 1: Discovering Project Dependencies

Ask your AI assistant:

```
What dependencies does my project have?
```

The assistant will use the `list_project_files` and `parse_dependencies` tools to:
1. Find all project definition files in your directory
2. Parse the dependencies from each file
3. Present them in a readable format

### Example 2: Getting Documentation for a Library

Ask your AI assistant:

```
Where can I find documentation for FastAPI version 0.104.0?
```

The assistant will use the `get_documentation_url` tool to fetch:
- PyPI package page
- Official documentation
- API reference
- Changelog (if available)

### Example 3: Exploring a New Library

Ask your AI assistant:

```
I'm using the requests library version 2.31.0. Can you show me how to make a POST request?
```

The assistant will:
1. Use `get_documentation_url` to find the documentation
2. Use `search_api_documentation` to find specific API docs
3. Provide you with links and potentially examples

### Example 4: Multi-Language Projects

For projects with multiple language ecosystems:

```
This is a full-stack project. What are all the dependencies?
```

The server will discover and parse:
- Python dependencies from `pyproject.toml`
- Node.js dependencies from `package.json`
- Any other supported project files

## Supported Project Types

### Python

**Files**: `pyproject.toml`, `requirements.txt`, `setup.py`

**Example pyproject.toml**:
```toml
[project]
dependencies = [
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
]
```

### Node.js

**Files**: `package.json`, `package-lock.json`

**Example package.json**:
```json
{
  "dependencies": {
    "express": "^4.18.0",
    "react": "^18.2.0"
  }
}
```

### Java/Maven

**Files**: `pom.xml`

**Example pom.xml**:
```xml
<dependencies>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
    <version>3.1.0</version>
  </dependency>
</dependencies>
```

### Scala/SBT

**Files**: `build.sbt`

**Example build.sbt**:
```scala
libraryDependencies ++= Seq(
  "com.typesafe.akka" %% "akka-actor" % "2.8.0",
  "org.scalatest" %% "scalatest" % "3.2.15" % Test
)
```

### Other Ecosystems

- **Gradle**: `build.gradle`, `build.gradle.kts`
- **Rust**: `Cargo.toml`
- **Go**: `go.mod`
- **Ruby**: `Gemfile`

## Advanced Features

### Using Resources

MCP resources provide direct access to dependency information:

**Dependencies Resource**:
```
dependencies:///path/to/your/project
```

Returns a formatted list of all dependencies.

**Documentation Resource**:
```
docs://library@version
```

For specific ecosystems:
- Python: `docs://fastapi@0.104.0`
- npm: `docs://npm:react@18.2.0`
- Maven: `docs://mvn:org.springframework:spring-core@6.0.0`

### Tips for Best Results

1. **Be Specific**: Include version numbers when asking about libraries
2. **Provide Context**: Mention the programming language or ecosystem
3. **Ask Follow-up Questions**: The assistant can search specific API documentation
4. **Use in Development**: Keep the server running while coding for instant documentation access

## Troubleshooting

### Server Not Starting

**Problem**: The server command is not found

**Solution**:
```bash
# Verify installation
pip show snapdepdoc

# Check if command is in PATH
which snapdepdoc  # Unix/macOS
where snapdepdoc  # Windows

# Reinstall if needed
pip install --force-reinstall snapdepdoc
```

### No Project Files Found

**Problem**: The server can't find your project files

**Solution**:
- Ensure you're in the correct directory
- Check that your project file names match supported formats exactly
- Use `list_project_files` explicitly to see what the server finds

### Documentation URLs Not Working

**Problem**: Some libraries don't return documentation URLs

**Solution**:
- Not all packages have standardized documentation
- Check if the package name and version are correct
- Try searching on the package registry directly (PyPI, npm, etc.)

### MCP Client Connection Issues

**Problem**: Claude Desktop or VS Code can't connect to the server

**Solution**:
1. Check the configuration file syntax (must be valid JSON)
2. Verify the command path is correct
3. Check MCP client logs for specific error messages
4. Restart the MCP client after configuration changes

## Getting Help

- **Documentation**: [GitHub Repository](https://github.com/thec0dewriter/docs_mcp)
- **Issues**: [Report bugs or request features](https://github.com/thec0dewriter/docs_mcp/issues)
- **Contributing**: [See CONTRIBUTING.md](https://github.com/thec0dewriter/docs_mcp/blob/main/CONTRIBUTING.md)

## What's Next?

- Explore the [examples](https://github.com/thec0dewriter/docs_mcp/tree/main/examples) directory
- Check out the [CHANGELOG](https://github.com/thec0dewriter/docs_mcp/blob/main/CHANGELOG.md) for updates
- Star the repository on GitHub to stay updated

## Feedback

We'd love to hear about your experience! Please:
- ⭐ Star the repository if you find it useful
- 🐛 Report bugs via GitHub Issues
- 💡 Suggest features or improvements
- 🤝 Contribute code or documentation

Happy coding! 🚀
