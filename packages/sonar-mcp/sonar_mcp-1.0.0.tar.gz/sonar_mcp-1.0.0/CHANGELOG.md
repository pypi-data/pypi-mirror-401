# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-01-10

### Changed

- **First public release** on PyPI and GitHub
- Version bump from 0.2.0 to 1.0.0 to signal production readiness
- Updated development status to "Production/Stable"
- Updated all repository URLs to GitHub (github.com/wadew/sonar-mcp)

### Documentation

- Added LICENSE file (MIT)
- Added SECURITY.md with vulnerability reporting policy
- Added CODE_OF_CONDUCT.md (Contributor Covenant v2.1)
- Added GitHub issue templates and PR template
- Updated README with PyPI badges
- Updated CONTRIBUTING.md for GitHub workflow

### Infrastructure

- Added PyPI publishing to GitLab CI/CD pipeline
- Added GitHub mirror support for public releases
- Added MANIFEST.in for PyPI packaging

## [0.2.0] - 2025-12-29

### Added

#### MCP Resources (7)
New browseable URI-based access to SonarQube data:
- `sonarqube://projects` - List all accessible projects
- `sonarqube://projects/{project_key}` - Get project details with metrics summary
- `sonarqube://projects/{project_key}/issues` - Get all project issues
- `sonarqube://projects/{project_key}/issues/{severity}` - Get issues filtered by severity
- `sonarqube://projects/{project_key}/metrics` - Get project metrics
- `sonarqube://projects/{project_key}/quality-gate` - Get quality gate status

#### MCP Prompts (6)
Reusable prompt templates for common code quality workflows:
- `code_review` - Review code issues from SonarQube and suggest fixes
- `fix_issues` - Generate fix recommendations for specific issue types
- `quality_report` - Generate comprehensive quality report for a project
- `quality_goals` - Check project against custom quality goals
- `security_audit` - Perform security-focused audit of a project
- `vulnerability_fix` - Get detailed fix guidance for vulnerabilities

#### MCP Tasks Infrastructure
Async task support for long-running operations (SEP-1686):
- `TaskManager` - Manages async task lifecycle and status
- `TaskInfo` - Task state tracking (working, completed, failed, cancelled)
- `TaskResult` - Completed task results with duration tracking
- Background cleanup for expired tasks
- Concurrent task limiting

#### Tool Annotations
All 18 tools now include MCP behavior annotations:
- Read-only tools marked with `readOnlyHint: true`
- State-changing tools marked with `destructiveHint: true`
- Open world hint for dynamic responses

#### Pydantic Output Schemas
Structured output models for consistent API responses:
- `BaseResponse` and `PaginatedResponse` base classes
- Issue schemas: `CompactIssue`, `IssueListResponse`, `IssueDetailResponse`
- Project schemas: `ProjectListResponse`, `ProjectDetailResponse`
- Metrics schemas: `MetricsResponse`, `CoverageDetails`, `FileCoverageResponse`
- Quality gate schemas: `QualityGateResponse`, `GoalsCheckResponse`
- Instance schemas: `InstanceListResponse`, `InstanceManageResponse`
- Rule schemas: `RuleSummary`, `RuleDetailResponse`

### Changed

- Upgraded MCP SDK from 1.23.3 to 1.25.0
- Updated pytest to 9.0.2
- Updated ruff to 0.14.10
- Updated mypy to 1.19.1
- ServerContext now includes optional TaskManager
- Resources use shared InstanceManager for API access

### Technical Details

- Python 3.11+ required
- MCP SDK 1.25.0+
- Full MCP 2025-11-25 specification compliance
- Resources, Prompts, Tool Annotations enabled

## [0.1.0] - 2025-12-07

### Added

#### MCP Server
- Initial release of the SonarQube MCP server
- Full MCP protocol compliance with stdio transport
- Multi-instance support for managing multiple SonarQube servers
- Environment variable configuration (SONAR_TOKEN, SONAR_URL)

#### Instance Management Tools (4)
- `sonar_list_instances` - List all configured SonarQube instances
- `sonar_manage_instance` - Add or remove SonarQube instances
- `sonar_select_instance` - Select the active instance for operations
- `sonar_test_connection` - Test connectivity to a SonarQube instance

#### Project Operations Tools (3)
- `sonar_list_projects` - List all accessible projects with pagination
- `sonar_get_project` - Get detailed project information with optional metrics
- `sonar_detect_project` - Auto-detect project from local configuration files

#### Issue Management Tools (5)
- `sonar_list_issues` - List issues with filtering by severity, type, and status
- `sonar_get_issue` - Get detailed issue information including components and rules
- `sonar_transition_issue` - Transition issues between states (confirm, resolve, etc.)
- `sonar_add_comment` - Add comments to issues with markdown support
- `sonar_bulk_transition` - Bulk transition multiple issues at once

#### Quality Gate Tools (2)
- `sonar_get_quality_gate` - Get quality gate status with condition details
- `sonar_check_goals` - Check project against custom quality goals

#### Metrics Tools (3)
- `sonar_get_metrics` - Get comprehensive project metrics
- `sonar_get_coverage` - Get detailed coverage breakdown
- `sonar_get_file_coverage` - Get file-level coverage information

#### Rules Tools (1)
- `sonar_get_rule` - Get rule details including description and quality profiles

#### Infrastructure
- Pydantic v2 models for all data structures
- Async HTTP client with httpx
- Retry logic with tenacity
- Structured logging with structlog
- Comprehensive type hints throughout

#### Quality & Testing
- 93%+ test coverage
- Unit tests for all modules
- Integration test framework
- Ruff linting and formatting
- MyPy strict type checking
- Bandit security scanning

#### CI/CD
- GitLab CI/CD pipeline with 5 stages
- SonarQube quality gate integration
- Package registry publishing
- Renovate dependency automation

#### Documentation
- Complete tool catalog with examples
- API reference documentation
- Contributing guidelines
- Configuration examples

### Technical Details

- Python 3.11+ required
- MCP SDK 1.23.1+
- Pydantic 2.12.5+
- httpx 0.28.1+

[Unreleased]: https://github.com/wadew/sonar-mcp/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/wadew/sonar-mcp/compare/v0.2.0...v1.0.0
[0.2.0]: https://github.com/wadew/sonar-mcp/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/wadew/sonar-mcp/releases/tag/v0.1.0
