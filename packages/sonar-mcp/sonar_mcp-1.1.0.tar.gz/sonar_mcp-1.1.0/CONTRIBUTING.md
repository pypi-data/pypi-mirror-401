# Contributing to SonarQube MCP Server

Thank you for your interest in contributing to the SonarQube MCP server! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Testing](#testing)
- [Code Style](#code-style)
- [Submitting Changes](#submitting-changes)
- [Release Process](#release-process)

## Code of Conduct

Please be respectful and constructive in all interactions. We aim to maintain a welcoming environment for all contributors.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Git
- Access to a SonarQube instance for testing

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/sonar-mcp.git
   cd sonar-mcp
   ```

3. Add upstream remote:
   ```bash
   git remote add upstream https://github.com/wadew/sonar-mcp.git
   ```

## Development Setup

### Create Virtual Environment

```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate

# Install with dev dependencies
uv pip install -e ".[dev]"
```

### Configure Environment

Create a `.env` file for local testing (never commit this):

```bash
SONAR_TOKEN=your-test-token
SONAR_URL=https://your-sonarqube-instance.com
```

### Verify Setup

```bash
# Run tests
pytest tests/ -v

# Check linting
ruff check src/ tests/

# Type check
mypy src/
```

## Development Workflow

### Branch Strategy

We use a simplified Git flow:

- `main`: Production releases only
- `develop`: Integration branch for all development
- Feature branches: Created from `develop`

### Creating a Feature Branch

```bash
# Update develop
git checkout develop
git pull upstream develop

# Create feature branch
git checkout -b feature/your-feature-name
```

### Test-Driven Development (TDD)

**We strictly follow TDD**. For every change:

1. **RED**: Write a failing test first
2. **GREEN**: Write minimal code to pass the test
3. **REFACTOR**: Clean up while keeping tests green

Example workflow:

```bash
# 1. Write test
vim tests/unit/tools/test_new_feature.py

# 2. Run test (should fail)
pytest tests/unit/tools/test_new_feature.py -v

# 3. Implement feature
vim src/sonar_mcp/tools/new_feature.py

# 4. Run test (should pass)
pytest tests/unit/tools/test_new_feature.py -v

# 5. Refactor if needed, ensure tests still pass
pytest tests/ -v
```

## Testing

### Running Tests

```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=src/sonar_mcp --cov-report=term-missing

# Specific test file
pytest tests/unit/tools/test_issue.py -v

# Filter by test name
pytest tests/ -v -k "test_list_issues"

# Unit tests only
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v
```

### Coverage Requirements

- **Minimum 80% coverage per module** (not just overall)
- **100% test pass rate** before any commit

Check module-level coverage:

```bash
pytest tests/ -v --cov=src/sonar_mcp --cov-report=term-missing
```

### Writing Tests

Follow these patterns:

```python
"""Tests for your_module."""

from __future__ import annotations

import pytest
from unittest.mock import AsyncMock, patch


class TestYourFeature:
    """Tests for YourFeature class."""

    @pytest.fixture
    def mock_client(self) -> AsyncMock:
        """Create mock SonarQube client."""
        return AsyncMock()

    async def test_feature_does_something(
        self, mock_client: AsyncMock
    ) -> None:
        """Test that feature does what it should."""
        # Arrange
        mock_client.get.return_value = {"data": "value"}

        # Act
        result = await your_function(mock_client)

        # Assert
        assert result["success"] is True
        mock_client.get.assert_called_once()
```

## Code Style

### Python Style Guide

We use **ruff** for linting and formatting:

```bash
# Check linting
ruff check src/ tests/

# Auto-fix issues
ruff check src/ tests/ --fix

# Format code
ruff format src/ tests/

# Check formatting without changes
ruff format --check src/ tests/
```

### Type Hints

All code must have type hints. We use **mypy** for checking:

```bash
mypy src/
```

Example:

```python
from __future__ import annotations

async def get_issues(
    project_key: str,
    severities: list[str] | None = None,
    limit: int = 100,
) -> dict[str, Any]:
    """Get issues from SonarQube.

    Args:
        project_key: The project key to query.
        severities: Optional severity filter.
        limit: Maximum number of issues.

    Returns:
        Dictionary with issues and metadata.
    """
    ...
```

### Docstrings

Use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """Short description of function.

    Longer description if needed, explaining the purpose
    and behavior of the function.

    Args:
        param1: Description of param1.
        param2: Description of param2.

    Returns:
        Description of return value.

    Raises:
        ValueError: When param1 is empty.
    """
```

### Imports

Organize imports in this order (ruff handles this automatically):

1. Standard library
2. Third-party packages
3. Local imports

```python
from __future__ import annotations

import json
from typing import TYPE_CHECKING

import httpx
from pydantic import BaseModel

from sonar_mcp.client import SonarClient
from sonar_mcp.models import Issue
```

## Submitting Changes

### Before Committing

Run all quality checks:

```bash
# All checks in one command
ruff check src/ tests/ && \
ruff format --check src/ tests/ && \
mypy src/ && \
pytest tests/ -v --cov=src/sonar_mcp --cov-fail-under=80
```

### Commit Messages

Use conventional commit format:

```
type(scope): short description

Longer description if needed.

- Bullet points for details
- Coverage: XX%
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `test`: Tests
- `refactor`: Code refactoring
- `chore`: Maintenance tasks

Examples:

```bash
git commit -m "feat(tools): add bulk issue transition

- Support transitioning multiple issues at once
- Add progress tracking
- Coverage: 92%"
```

### Creating a Pull Request

1. Push your branch:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Create PR on GitHub targeting `develop`

3. Fill in the PR template:
   - Description of changes
   - Testing performed
   - Related issues

4. Wait for CI checks to pass

5. Request review

### PR Checklist

- [ ] All tests pass
- [ ] Coverage >= 80% per module
- [ ] Ruff linting clean
- [ ] Ruff formatting clean
- [ ] MyPy type checking clean
- [ ] No hardcoded credentials
- [ ] Documentation updated (if needed)
- [ ] CHANGELOG.md updated (for features/fixes)

## Release Process

Releases are managed by maintainers:

1. MR from `develop` to `main`
2. Version bump in `pyproject.toml`
3. Update `CHANGELOG.md`
4. Tag release: `git tag v0.x.0`
5. Push tag: `git push origin v0.x.0`
6. CI publishes to package registry

## Getting Help

- Create an issue for bugs or feature requests
- Check existing issues before creating new ones
- Join discussions on merge requests

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
