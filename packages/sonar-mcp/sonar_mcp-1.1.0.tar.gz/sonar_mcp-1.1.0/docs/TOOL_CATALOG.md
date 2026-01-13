# SonarQube MCP Server - Tool Catalog

> Complete reference for all 21 SonarQube tools provided via the dispatch pattern.

## How It Works

The server exposes **3 meta-tools** that provide access to all 21 SonarQube tools:

| Meta-Tool | Description |
|-----------|-------------|
| `sonar_list_categories` | Discover available tools by category |
| `sonar_get_tool_schema` | Get parameter schema for a specific tool |
| `sonar_execute_tool` | Execute any tool by name with arguments |

### Usage Example

```python
# 1. List available categories
sonar_list_categories()

# 2. Get schema for a specific tool
sonar_get_tool_schema(tool_name="sonar_list_issues")

# 3. Execute the tool
sonar_execute_tool(
    tool_name="sonar_list_issues",
    arguments={"project": "my-project", "severities": ["CRITICAL", "BLOCKER"]}
)
```

## Table of Contents

- [Instance Management](#instance-management)
- [Project Operations](#project-operations)
- [Issue Management](#issue-management)
- [Quality Gates](#quality-gates)
- [Metrics](#metrics)
- [Rules](#rules)
- [Task Management](#task-management)

---

## Instance Management

Tools for managing SonarQube server connections.

### sonar_list_instances

List all configured SonarQube instances.

**Parameters:** None

**Returns:**
| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Operation success status |
| `instances` | list | Array of instance info (without tokens) |
| `total` | int | Total number of instances |
| `active_instance` | string | Name of active instance |

**Example:**
```json
{
  "success": true,
  "instances": [
    {
      "name": "production",
      "url": "https://sonarqube.example.com",
      "organization": null,
      "default": true
    }
  ],
  "total": 1,
  "active_instance": "production"
}
```

---

### sonar_manage_instance

Add or remove SonarQube instances.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `operation` | string | Yes | Operation: "add" or "remove" |
| `name` | string | Yes | Instance name (unique identifier) |
| `url` | string | For add | SonarQube server URL |
| `token` | string | For add | API authentication token |
| `organization` | string | No | Organization key (SonarCloud) |
| `verify_ssl` | bool | No | Verify SSL certificates (default: true) |
| `request_timeout` | float | No | Request timeout seconds (default: 30.0) |

**Returns:**
| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Operation success status |
| `operation` | string | Operation performed |
| `instance` | dict | Instance details (for "add") |
| `name` | string | Instance name (for "remove") |
| `error` | string | Error message (if failed) |

---

### sonar_select_instance

Select the active SonarQube instance for subsequent operations.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Name of instance to select |

**Returns:**
| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Operation success status |
| `selected_instance` | string | Newly selected instance name |
| `previous_instance` | string | Previously active instance |
| `error` | string | Error message (if failed) |

---

### sonar_test_connection

Test connection to a SonarQube instance.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `instance_name` | string | No | Instance to test (default: active) |

**Returns:**
| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Tool execution success |
| `connected` | bool | Whether connection succeeded |
| `version` | string | SonarQube version (if connected) |
| `instance` | string | Instance name tested |
| `error` | string | Error message (if not connected) |

---

## Project Operations

Tools for working with SonarQube projects.

### sonar_list_projects

List all accessible SonarQube projects.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `search` | string | No | Search query to filter projects |
| `page` | int | No | Page number (default: 1) |
| `page_size` | int | No | Results per page (default: 100) |

**Returns:**
| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Operation success status |
| `projects` | list | Array of project info |
| `total` | int | Total number of projects |
| `page` | int | Current page number |
| `page_size` | int | Results per page |
| `error` | string | Error message (if failed) |

**Example:**
```json
{
  "success": true,
  "projects": [
    {
      "key": "my-project",
      "name": "My Project",
      "qualifier": "TRK"
    }
  ],
  "total": 1
}
```

---

### sonar_get_project

Get details of a specific SonarQube project.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `project_key` | string | Yes | Project key to retrieve |
| `include_metrics` | bool | No | Include project metrics (default: false) |

**Returns:**
| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Operation success status |
| `project` | dict | Project details |
| `metrics` | dict | Metrics (if include_metrics=true) |
| `error` | string | Error message (if failed) |

---

### sonar_detect_project

Auto-detect SonarQube project from local files.

Searches for project configuration in order:
1. `sonar-project.properties` (sonar.projectKey)
2. `pom.xml` (groupId:artifactId)
3. `package.json` (name)
4. `pyproject.toml` (project.name)

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `directory` | string | No | Directory to search (default: cwd) |

**Returns:**
| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Detection success status |
| `project_key` | string | Detected project key |
| `source` | string | Source file used |
| `error` | string | Error message (if failed) |

---

## Issue Management

Tools for managing SonarQube issues.

### sonar_list_issues

List issues for a SonarQube project with optional filtering.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `project_key` | string | Yes | Project key |
| `severities` | list | No | Filter: BLOCKER, CRITICAL, MAJOR, MINOR, INFO |
| `types` | list | No | Filter: BUG, VULNERABILITY, CODE_SMELL |
| `statuses` | list | No | Filter: OPEN, CONFIRMED, REOPENED, RESOLVED, CLOSED |
| `page` | int | No | Page number (default: 1) |
| `page_size` | int | No | Results per page (default: 100) |

**Returns:**
| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Operation success status |
| `issues` | list | Array of issue objects |
| `total` | int | Total number of issues |
| `page` | int | Current page |
| `page_size` | int | Results per page |
| `error` | string | Error message (if failed) |

---

### sonar_get_issue

Get details of a specific SonarQube issue.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `issue_key` | string | Yes | Issue key to retrieve |

**Returns:**
| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Operation success status |
| `issue` | dict | Issue details |
| `components` | list | Related components |
| `rules` | list | Related rules |
| `error` | string | Error message (if failed) |

---

### sonar_transition_issue

Transition a SonarQube issue to a new status.

**Valid Transitions:**
- `confirm`: OPEN -> CONFIRMED
- `unconfirm`: CONFIRMED -> REOPENED
- `resolve`: OPEN/CONFIRMED -> RESOLVED
- `reopen`: RESOLVED/CLOSED -> REOPENED
- `wontfix`: Mark as won't fix
- `falsepositive`: Mark as false positive

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `issue_key` | string | Yes | Issue key to transition |
| `transition` | string | Yes | Transition to apply |

**Returns:**
| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Operation success status |
| `issue` | dict | Updated issue details |
| `error` | string | Error message (if failed) |

---

### sonar_add_comment

Add a comment to a SonarQube issue.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `issue_key` | string | Yes | Issue key to comment on |
| `text` | string | Yes | Comment text (supports markdown) |

**Returns:**
| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Operation success status |
| `comment` | dict | The added comment |
| `error` | string | Error message (if failed) |

---

### sonar_bulk_transition

Bulk transition multiple SonarQube issues.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `issue_keys` | list | Yes | List of issue keys |
| `transition` | string | Yes | Transition to apply |

**Returns:**
| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Operation success status |
| `total` | int | Total issues processed |
| `failures` | int | Number of failed transitions |
| `error` | string | Error message (if failed) |

---

## Quality Gates

Tools for quality gate monitoring.

### sonar_get_quality_gate

Get quality gate status for a SonarQube project.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `project_key` | string | Yes | Project key |

**Returns:**
| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Operation success status |
| `status` | string | Quality gate status: OK, WARN, ERROR |
| `conditions` | list | Individual condition results |
| `error` | string | Error message (if failed) |

**Example:**
```json
{
  "success": true,
  "status": "OK",
  "conditions": [
    {
      "status": "OK",
      "metricKey": "new_coverage",
      "comparator": "LT",
      "errorThreshold": "80",
      "actualValue": "85.5"
    }
  ]
}
```

---

### sonar_check_goals

Check if a project meets custom quality goals.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `project_key` | string | Yes | Project key |
| `min_coverage` | float | No | Minimum coverage % (0-100) |
| `max_bugs` | int | No | Maximum bugs allowed |
| `max_vulnerabilities` | int | No | Maximum vulnerabilities |
| `max_code_smells` | int | No | Maximum code smells |
| `max_duplicated_lines_density` | float | No | Maximum duplication % |
| `min_maintainability_rating` | string | No | Minimum rating (A-E) |
| `min_reliability_rating` | string | No | Minimum rating (A-E) |
| `min_security_rating` | string | No | Minimum rating (A-E) |

**Returns:**
| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Operation success status |
| `passed` | bool | Whether all goals are met |
| `failed_goals` | list | Goals that failed |
| `metrics` | dict | Current metric values |
| `error` | string | Error message (if failed) |

**Example:**
```json
{
  "success": true,
  "passed": false,
  "failed_goals": [
    {
      "metric": "coverage",
      "goal": ">= 80%",
      "actual": "75.5%"
    }
  ],
  "metrics": {
    "coverage": "75.5",
    "bugs": "0",
    "vulnerabilities": "0"
  }
}
```

---

## Metrics

Tools for retrieving project metrics.

### sonar_get_metrics

Get metrics for a SonarQube project.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `project_key` | string | Yes | Project key |
| `metric_keys` | list | No | Specific metrics to retrieve |

**Default Metrics (if none specified):**
- `coverage`, `line_coverage`, `branch_coverage`
- `bugs`, `vulnerabilities`, `code_smells`
- `ncloc`, `duplicated_lines_density`
- `sqale_rating`, `reliability_rating`, `security_rating`

**Returns:**
| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Operation success status |
| `project_key` | string | Project key |
| `metrics` | dict | Metric key-value pairs |
| `error` | string | Error message (if failed) |

---

### sonar_get_coverage

Get detailed coverage information for a project.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `project_key` | string | Yes | Project key |

**Returns:**
| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Operation success status |
| `project_key` | string | Project key |
| `coverage` | dict | Coverage metrics |
| `error` | string | Error message (if failed) |

**Coverage fields:**
- `overall`: Overall coverage percentage
- `line_coverage`: Line coverage percentage
- `branch_coverage`: Branch coverage percentage
- `lines_to_cover`: Total lines to cover
- `uncovered_lines`: Number of uncovered lines
- `conditions_to_cover`: Total conditions to cover
- `uncovered_conditions`: Number of uncovered conditions

---

### sonar_get_file_coverage

Get coverage information for a specific file.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `project_key` | string | Yes | Project key |
| `file_path` | string | Yes | Path to file within project |

**Returns:**
| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Operation success status |
| `file_path` | string | File path |
| `coverage` | dict | Coverage metrics for file |
| `error` | string | Error message (if failed) |

---

## Rules

Tools for rule information.

### sonar_get_rule

Get details of a SonarQube rule.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `rule_key` | string | Yes | Rule key (e.g., 'python:S1234') |
| `actives` | bool | No | Include quality profiles (default: false) |

**Returns:**
| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Operation success status |
| `rule` | dict | Rule details |
| `actives` | list | Quality profiles (if actives=true) |
| `error` | string | Error message (if failed) |

**Rule fields:**
- `key`: Rule key
- `name`: Rule name
- `severity`: BLOCKER, CRITICAL, MAJOR, MINOR, INFO
- `type`: BUG, VULNERABILITY, CODE_SMELL
- `lang`: Language key
- `langName`: Language name
- `htmlDesc`: HTML description
- `status`: READY, DEPRECATED, BETA
- `tags`: List of tags

---

## Error Handling

All tools return a consistent error format:

```json
{
  "success": false,
  "error": "Error message describing what went wrong"
}
```

Common errors:
- `"No active instance configured."` - No SonarQube instance selected
- `"Instance 'name' not found."` - Referenced instance doesn't exist
- `"Unauthorized"` - Invalid or expired token
- `"Component key 'key' not found"` - Project/component doesn't exist

---

## Configuration

Configure the MCP server via environment variables:

```json
{
  "mcpServers": {
    "sonar-mcp": {
      "command": "python",
      "args": ["-m", "sonar_mcp"],
      "env": {
        "SONAR_TOKEN": "your-api-token",
        "SONAR_URL": "https://sonarqube.example.com"
      }
    }
  }
}
```

Environment variables:
- `SONAR_TOKEN` or `SONARQUBE_TOKEN`: API authentication token
- `SONAR_URL` or `SONARQUBE_URL` or `SONAR_HOST_URL`: Server URL
- `SONAR_ORGANIZATION`: Organization key (optional, for SonarCloud)
