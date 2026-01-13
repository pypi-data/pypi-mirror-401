# SonarQube MCP Server

[![PyPI version](https://badge.fury.io/py/sonar-mcp.svg)](https://badge.fury.io/py/sonar-mcp)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Coverage](https://img.shields.io/badge/coverage-93%25-brightgreen.svg)](https://github.com/wadew/sonar-mcp)

A Model Context Protocol (MCP) server for interacting with SonarQube code quality platform.

## Features

- **21 SonarQube tools** organized into 7 categories, accessible via dispatch pattern
- **6 MCP Prompts** for code review, security audits, and quality reports
- **7 MCP Resources** for browseable URI-based access to SonarQube data
- **Multi-instance support** for managing multiple SonarQube servers
- **HTTP transport modes** - stdio, SSE, and streamable-http

## Installation

```bash
# Using pip
pip install sonar-mcp

# Using uv (recommended)
uv pip install sonar-mcp
```

## Quick Start

### 1. Configure for Claude Code

Add to your Claude Code MCP settings:

```json
{
  "mcpServers": {
    "sonar-mcp": {
      "command": "sonar-mcp",
      "env": {
        "SONAR_TOKEN": "your-sonarqube-token",
        "SONAR_URL": "https://sonarqube.example.com"
      }
    }
  }
}
```

### 2. Use the Tools

The server uses a **dispatch pattern** (similar to GitLab MCP) with just 3 meta-tools:

```
# Discover available tools by category
sonar_list_categories()
sonar_list_categories(category="issue")  # Filter to specific category

# Get parameter schema for a tool
sonar_get_tool_schema(tool_name="sonar_list_issues")

# Execute any tool by name
sonar_execute_tool(tool_name="sonar_list_projects")
sonar_execute_tool(tool_name="sonar_list_issues", arguments={"project": "my-project"})
```

## Running the Server

### Stdio Mode (Default)

For Claude Code and other MCP clients that use stdio transport:

```bash
sonar-mcp
# or
python -m sonar_mcp
```

### Streamable HTTP Mode

For web-based clients or remote access:

```bash
# Start server on default port 8000
sonar-mcp --transport streamable-http

# Custom host and port
sonar-mcp --transport streamable-http --host 0.0.0.0 --port 3000

# Using environment variables
SONAR_MCP_TRANSPORT=streamable-http SONAR_MCP_PORT=3000 sonar-mcp
```

### SSE Mode (Server-Sent Events)

For clients that support SSE transport:

```bash
sonar-mcp --transport sse --port 8000
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--transport` | Transport protocol: `stdio`, `sse`, `streamable-http` | `stdio` |
| `--host` | Host address for HTTP transports | `127.0.0.1` |
| `--port` | Port for HTTP transports | `8000` |
| `--version` | Show version and exit | - |

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SONAR_TOKEN` | SonarQube API token | Yes |
| `SONAR_URL` | SonarQube server URL | Yes |
| `SONAR_MCP_TRANSPORT` | Default transport mode | No |
| `SONAR_MCP_HOST` | Default host for HTTP | No |
| `SONAR_MCP_PORT` | Default port for HTTP | No |

## Available Tools

### Dispatch Meta-Tools (3 tools, always available)

These 3 tools provide access to all SonarQube functionality:

| Tool | Description |
|------|-------------|
| `sonar_list_categories` | Discover available tools by category |
| `sonar_get_tool_schema` | Get parameter schema for a specific tool |
| `sonar_execute_tool` | Execute any tool by name with arguments |

### Category: instance (4 tools)

Instance management for SonarQube server connections:

- `sonar_list_instances` - List all configured instances
- `sonar_manage_instance` - Create, update, delete instances
- `sonar_select_instance` - Set the active instance
- `sonar_test_connection` - Test instance connectivity

### Category: project (3 tools)

Project operations:

- `sonar_list_projects` - List all accessible projects
- `sonar_get_project` - Get project details and metrics
- `sonar_detect_project` - Auto-detect project from current directory

### Category: issue (5 tools)

Issue management:

- `sonar_list_issues` - List issues with filtering (severity, type, status)
- `sonar_get_issue` - Get detailed issue information
- `sonar_transition_issue` - Change issue status (resolve, falsepositive, etc.)
- `sonar_add_comment` - Add a comment to an issue
- `sonar_bulk_transition` - Bulk transition multiple issues

### Category: quality (2 tools)

Quality gate operations:

- `sonar_get_quality_gate` - Get quality gate status (OK/ERROR)
- `sonar_check_goals` - Validate against quality goals

### Category: metrics (3 tools)

Metrics retrieval:

- `sonar_get_metrics` - Get project metrics
- `sonar_get_coverage` - Get coverage percentage
- `sonar_get_file_coverage` - Get file-level coverage details

### Category: rules (1 tool)

Rule information:

- `sonar_get_rule` - Get rule details and remediation guidance

### Category: task (3 tools)

Async task management:

- `sonar_get_task` - Get task status
- `sonar_list_tasks` - List background tasks
- `sonar_cancel_task` - Cancel a running task

## MCP Resources

Browseable URI-based access to SonarQube data:

| URI Pattern | Description |
|-------------|-------------|
| `sonarqube://projects` | List all projects |
| `sonarqube://projects/{key}` | Get project details |
| `sonarqube://projects/{key}/issues` | Get project issues |
| `sonarqube://projects/{key}/issues/{severity}` | Get issues by severity |
| `sonarqube://projects/{key}/metrics` | Get project metrics |
| `sonarqube://projects/{key}/quality-gate` | Get quality gate status |

## MCP Prompts

Reusable prompt templates for code quality workflows:

| Prompt | Description |
|--------|-------------|
| `code_review` | Review code issues and suggest fixes |
| `fix_issues` | Generate fix recommendations for issues |
| `quality_report` | Generate quality report for a project |
| `quality_goals` | Check project against quality goals |
| `security_audit` | Perform security vulnerability audit |
| `vulnerability_fix` | Generate fixes for security vulnerabilities |

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/wadew/sonar-mcp.git
cd sonar-mcp

# Create virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv pip install -e ".[dev]"
```

### Testing

```bash
# Run all tests with coverage
pytest tests/ -v --cov=src/sonar_mcp --cov-report=term-missing

# Run with coverage enforcement (80% minimum)
pytest tests/ -v --cov=src/sonar_mcp --cov-fail-under=80
```

### Linting

```bash
# Check linting
ruff check src/ tests/

# Format code
ruff format src/ tests/

# Type checking
mypy src/
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

1. Follow TDD (Test-Driven Development) - write tests first
2. Maintain 80% coverage on ALL modules
3. Ensure all linting and type checks pass
4. Use conventional commits

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.
