# Examples

This directory contains example configurations and usage scenarios for SnapDepDoc.

## Quick Start Examples

### 1. Claude Desktop Configuration

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "snapdepdoc": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/docs_mcp",
        "run",
        "snapdepdoc"
      ]
    }
  }
}
```

Or if installed via pip:

```json
{
  "mcpServers": {
    "snapdepdoc": {
      "command": "snapdepdoc"
    }
  }
}
```

### 2. VS Code MCP Configuration

Create `.vscode/mcp.json` in your project:

```json
{
  "servers": {
    "snapdepdoc": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "run",
        "snapdepdoc"
      ]
    }
  }
}
```

Or with pip installation:

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

## Usage Examples

### Example 1: Discovering Project Files

```
User: What project files are in my current directory?

Assistant (using list_project_files tool):
I found the following project files:
- pyproject.toml (Python)
- package.json (Node.js)
```

### Example 2: Parsing Dependencies

```
User: What are the dependencies in my pyproject.toml?

Assistant (using parse_dependencies tool):
Your Python project has the following dependencies:
Production:
- fastapi: >=0.104.0
- uvicorn: >=0.24.0
- pydantic: >=2.0.0

Development:
- pytest: >=7.0.0
- black: >=23.0.0
```

### Example 3: Getting Documentation

```
User: Where can I find documentation for FastAPI version 0.104.0?

Assistant (using get_documentation_url tool):
FastAPI 0.104.0 documentation:
- Main docs: https://pypi.org/project/fastapi/0.104.0/
- API Reference: https://fastapi.readthedocs.io/en/0.104.0/api.html
- Official site: https://fastapi.tiangolo.com/
```

### Example 4: Searching API Documentation

```
User: How do I use the APIRouter in FastAPI?

Assistant (using search_api_documentation tool):
Here are the relevant documentation links for APIRouter:
1. FastAPI Documentation - https://fastapi.readthedocs.io/en/latest/
2. API Reference - https://fastapi.readthedocs.io/en/latest/api.html
```

### Example 5: Using Resources

The MCP server exposes resources that can be accessed by AI assistants:

**Dependencies Resource:**
```
dependencies:///path/to/project
```
Returns a formatted list of all project dependencies with versions.

**Documentation Resource:**
```
docs://fastapi@0.104.0
docs://npm:react@18.2.0
docs://mvn:org.springframework:spring-core@6.0.0
```
Returns documentation links and descriptions for specific library versions.

## Project Type Examples

### Python Projects

**pyproject.toml:**
```toml
[project]
name = "my-project"
version = "1.0.0"
dependencies = [
    "requests>=2.31.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "black>=23.0.0",
]
```

### Node.js Projects

**package.json:**
```json
{
  "name": "my-app",
  "version": "1.0.0",
  "dependencies": {
    "react": "^18.2.0",
    "express": "^4.18.0"
  },
  "devDependencies": {
    "jest": "^29.0.0",
    "eslint": "^8.0.0"
  }
}
```

### Java/Maven Projects

**pom.xml:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>my-app</artifactId>
    <version>1.0.0</version>
    
    <dependencies>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-core</artifactId>
            <version>6.0.0</version>
        </dependency>
    </dependencies>
</project>
```

### Scala/SBT Projects

**build.sbt:**
```scala
name := "my-scala-app"
version := "1.0.0"
scalaVersion := "2.13.12"

libraryDependencies ++= Seq(
  "org.typelevel" %% "cats-core" % "2.10.0",
  "org.scalatest" %% "scalatest" % "3.2.17" % Test
)
```

### Rust Projects

**Cargo.toml:**
```toml
[package]
name = "my-rust-app"
version = "1.0.0"
edition = "2021"

[dependencies]
serde = { version = "1.0", features = ["derive"] }
tokio = { version = "1.35", features = ["full"] }

[dev-dependencies]
criterion = "0.5"
```

### Go Projects

**go.mod:**
```
module github.com/user/my-go-app

go 1.21

require (
    github.com/gin-gonic/gin v1.9.1
    github.com/stretchr/testify v1.8.4
)
```

### Ruby Projects

**Gemfile:**
```ruby
source 'https://rubygems.org'

gem 'rails', '~> 7.1.0'
gem 'pg', '~> 1.5'

group :development, :test do
  gem 'rspec-rails', '~> 6.0'
  gem 'rubocop', '~> 1.57'
end
```

## Advanced Use Cases

### Multi-Project Workspace

When working with a monorepo or multiple projects, the MCP server can help discover and analyze all project files in your workspace.
