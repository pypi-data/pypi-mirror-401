# SonarQube MCP Server

[![PyPI version](https://badge.fury.io/py/sonar-mcp.svg)](https://badge.fury.io/py/sonar-mcp)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Coverage](https://img.shields.io/badge/coverage-93%25-brightgreen.svg)](https://github.com/wadew/sonar-mcp)

A Model Context Protocol (MCP) server for interacting with SonarQube code quality platform.

## Features

- **18 MCP Tools** for comprehensive SonarQube management
- **Multi-instance support** for managing multiple SonarQube servers
- **Issue management** - list, transition, comment, bulk operations
- **Quality gates** - check status, validate against goals
- **Metrics** - coverage, ratings, file-level analysis
- **Project detection** - auto-detect from git remote

## Installation

```bash
# Using uv (recommended)
uv pip install sonar-mcp

# Using pip
pip install sonar-mcp
```

## Configuration

Configure the MCP server in your Claude Code settings:

```json
{
  "mcpServers": {
    "sonar-mcp": {
      "command": "python",
      "args": ["-m", "sonar_mcp"],
      "env": {
        "SONAR_TOKEN": "your-sonarqube-token",
        "SONAR_URL": "https://sonarqube.example.com"
      }
    }
  }
}
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SONAR_TOKEN` | SonarQube API token | Yes |
| `SONAR_URL` | SonarQube server URL | Yes |

## Available Tools

### Instance Management
- `sonar_manage_instance` - Create, update, delete, or test instances
- `sonar_list_instances` - List all configured instances
- `sonar_select_instance` - Set the active instance

### Project Operations
- `sonar_list_projects` - List all accessible projects
- `sonar_get_project` - Get project details and metrics
- `sonar_detect_project` - Auto-detect project from current directory

### Issue Management
- `sonar_list_issues` - List issues with filtering (severity, type, status)
- `sonar_get_issue` - Get detailed issue information
- `sonar_transition_issue` - Change issue status (resolve, falsepositive, etc.)
- `sonar_add_comment` - Add a comment to an issue
- `sonar_bulk_transition` - Bulk transition multiple issues

### Quality Gates
- `sonar_get_quality_gate` - Get quality gate status (OK/ERROR)
- `sonar_check_goals` - Validate against quality goals

### Metrics
- `sonar_get_metrics` - Get project metrics
- `sonar_get_coverage` - Get coverage percentage
- `sonar_get_file_coverage` - Get file-level coverage details

### Rules
- `sonar_get_rule` - Get rule details and remediation guidance

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

# Run specific test file
pytest tests/unit/test_client.py -v

# Run with coverage enforcement (80% minimum)
pytest tests/ -v --cov=src/sonar_mcp --cov-fail-under=80
```

### Linting

```bash
# Check linting
ruff check src/ tests/

# Auto-fix issues
ruff check src/ tests/ --fix

# Format code
ruff format src/ tests/

# Type checking
mypy src/
```

### Quality Gates

Before committing, ensure all quality gates pass:

```bash
# All-in-one check
ruff check src/ tests/ && \
ruff format --check src/ tests/ && \
mypy src/ && \
pytest tests/ -v --cov=src/sonar_mcp --cov-fail-under=80
```

## Architecture

```
src/sonar_mcp/
├── __init__.py          # Package initialization
├── __main__.py          # Entry point
├── server.py            # MCP server core
├── instance_manager.py  # Multi-instance management
├── types.py             # Type definitions
├── auth/                # Token management
├── client/              # SonarQube API client
├── config/              # Configuration models
├── models/              # Data models (Issue, Metric, Project)
├── tools/               # MCP tools (18 total)
└── utils/               # Utilities (logging)
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

1. Follow TDD (Test-Driven Development) - write tests first
2. Maintain 80% coverage on ALL modules
3. Ensure all linting and type checks pass
4. Use conventional commits

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.
