"""Issue management tools for SonarQube MCP server."""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import Context, FastMCP
from mcp.types import ToolAnnotations

from sonar_mcp.client.sonar_client import SonarAPIError
from sonar_mcp.context import (
    ServerContext,  # noqa: TC001 - Required at runtime for MCP introspection
)
from sonar_mcp.instance_manager import NoActiveInstanceError
from sonar_mcp.tools.client_helper import create_sonar_client, get_server_context


# Error message constants
ERR_NO_ACTIVE_INSTANCE = "No active instance configured."

# API endpoint constants
API_ISSUES_SEARCH = "/api/issues/search"

# Essential fields to keep in compact mode
# These are the fields most useful for LLM consumption
ESSENTIAL_ISSUE_FIELDS = frozenset(
    {
        "key",  # Required for any operations on the issue
        "rule",  # Important to understand what rule was violated
        "severity",  # Critical for prioritization
        "component",  # File path, essential for locating the issue
        "project",  # Project key for context
        "line",  # Line number, essential for locating the issue
        "status",  # Critical to know state
        "message",  # The actual issue description
        "type",  # BUG, VULNERABILITY, CODE_SMELL
        "issueStatus",  # Useful (may differ from status)
        "resolution",  # Important when status is CLOSED
        "tags",  # Useful for categorization
    }
)

# Essential fields for compact component representation
ESSENTIAL_COMPONENT_FIELDS = frozenset(
    {
        "key",  # Component key
        "name",  # Short name
        "path",  # File path (if applicable)
        "qualifier",  # TRK, FIL, etc.
    }
)

# Essential fields for compact rule representation
ESSENTIAL_RULE_FIELDS = frozenset(
    {
        "key",  # Rule key
        "name",  # Rule name
        "lang",  # Language key
        "status",  # READY, DEPRECATED, etc.
    }
)


def compact_issue(issue: dict[str, Any]) -> dict[str, Any]:
    """Compact an issue by keeping only essential fields.

    This reduces response size for LLM consumption by removing verbose
    and redundant fields like hash, textRange, flows, effort, debt,
    author, scope, and various internal flags.

    Args:
        issue: Full issue dictionary from SonarQube API.

    Returns:
        Compact issue dictionary with only essential fields.
    """
    return {k: v for k, v in issue.items() if k in ESSENTIAL_ISSUE_FIELDS}


def compact_component(component: dict[str, Any]) -> dict[str, Any]:
    """Compact a component by keeping only essential fields.

    Args:
        component: Full component dictionary from SonarQube API.

    Returns:
        Compact component dictionary with only essential fields.
    """
    return {k: v for k, v in component.items() if k in ESSENTIAL_COMPONENT_FIELDS}


def compact_rule_summary(rule: dict[str, Any]) -> dict[str, Any]:
    """Compact a rule summary by keeping only essential fields.

    This is for rule summaries returned with issues, not the full rule
    details from sonar_get_rule.

    Args:
        rule: Rule summary dictionary from SonarQube API.

    Returns:
        Compact rule dictionary with only essential fields.
    """
    return {k: v for k, v in rule.items() if k in ESSENTIAL_RULE_FIELDS}


async def sonar_list_issues(
    ctx: Context[Any, ServerContext],
    project_key: str,
    severities: list[str] | None = None,
    types: list[str] | None = None,
    statuses: list[str] | None = None,
    page: int = 1,
    page_size: int = 100,
    compact: bool = True,
    task_mode: bool = False,
) -> dict[str, Any]:
    """List issues for a SonarQube project with optional filtering.

    Args:
        ctx: MCP context.
        project_key: Project key to list issues for.
        severities: Filter by severities (BLOCKER, CRITICAL, MAJOR, MINOR, INFO).
        types: Filter by types (BUG, VULNERABILITY, CODE_SMELL).
        statuses: Filter by statuses (OPEN, CONFIRMED, REOPENED, RESOLVED, CLOSED).
        page: Page number for pagination (default: 1).
        page_size: Number of results per page (default: 100).
        compact: Return compact issues with only essential fields (default: True).
                 Set to False to return the full API response.
        task_mode: If True, run in background and return task_id immediately.
                   Use sonar_get_task to check progress. Default: False.

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - issues: list - Array of issue objects (compact by default, sync mode)
        - total: int - Total number of issues (sync mode)
        - task_id: str - Task ID for tracking (task_mode only)
        - state: str - Initial task state (task_mode only)
        - message: str - Status message (task_mode only)
        - error: str - Error message (if success is False)
    """
    server_ctx = get_server_context(ctx)

    try:
        instance = server_ctx.instance_manager.get_active_instance()
    except NoActiveInstanceError:
        return {
            "success": False,
            "error": ERR_NO_ACTIVE_INSTANCE,
        }

    params: dict[str, Any] = {
        "componentKeys": project_key,
        "p": page,
        "ps": page_size,
    }

    if severities:
        params["severities"] = ",".join(severities)
    if types:
        params["types"] = ",".join(types)
    if statuses:
        params["statuses"] = ",".join(statuses)

    # Task mode: run in background and return immediately
    if task_mode:
        task_manager = server_ctx.task_manager
        if not task_manager:
            return {
                "success": False,
                "error": "Task manager not available.",
            }

        async def _list_issues_operation() -> dict[str, Any]:
            """Execute issue listing in background."""
            client = create_sonar_client(instance)

            async with client:
                response = await client.get(API_ISSUES_SEARCH, params=params)

            issues = response.get("issues", [])
            paging = response.get("paging", {})

            # Apply compaction by default to reduce response size
            if compact:
                issues = [compact_issue(issue) for issue in issues]

            return {
                "success": True,
                "issues": issues,
                "total": paging.get("total", len(issues)),
                "page": paging.get("pageIndex", page),
                "page_size": paging.get("pageSize", page_size),
            }

        task_info = await task_manager.create_task("list_issues", _list_issues_operation)
        return {
            "success": True,
            "task_id": task_info.task_id,
            "state": task_info.state.value,
            "message": f"Issue listing started for {project_key}",
        }

    # Synchronous mode: execute and wait for result
    client = create_sonar_client(instance)

    try:
        async with client:
            response = await client.get(API_ISSUES_SEARCH, params=params)

        issues = response.get("issues", [])
        paging = response.get("paging", {})

        # Apply compaction by default to reduce response size for LLM consumption
        if compact:
            issues = [compact_issue(issue) for issue in issues]

        return {
            "success": True,
            "issues": issues,
            "total": paging.get("total", len(issues)),
            "page": paging.get("pageIndex", page),
            "page_size": paging.get("pageSize", page_size),
        }
    except SonarAPIError as e:
        return {
            "success": False,
            "error": str(e),
        }


async def sonar_get_issue(
    ctx: Context[Any, ServerContext],
    issue_key: str,
    compact: bool = True,
) -> dict[str, Any]:
    """Get details of a specific SonarQube issue.

    Args:
        ctx: MCP context.
        issue_key: The issue key to retrieve.
        compact: Return compact response with only essential fields (default: True).
                 Set to False to return the full API response.

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - issue: dict - Issue details (compact by default)
        - components: list - Related components (compact by default)
        - rules: list - Related rules (compact by default)
        - error: str - Error message (if success is False)
    """
    server_ctx = get_server_context(ctx)

    try:
        instance = server_ctx.instance_manager.get_active_instance()
    except NoActiveInstanceError:
        return {
            "success": False,
            "error": ERR_NO_ACTIVE_INSTANCE,
        }

    client = create_sonar_client(instance)

    try:
        async with client:
            response = await client.get(
                API_ISSUES_SEARCH,
                params={"issues": issue_key, "additionalFields": "comments,rules"},
            )

        issues = response.get("issues", [])
        if not issues:
            return {
                "success": False,
                "error": f"Issue '{issue_key}' not found.",
            }

        issue = issues[0]
        components = response.get("components", [])
        rules = response.get("rules", [])

        # Apply compaction by default to reduce response size for LLM consumption
        if compact:
            issue = compact_issue(issue)
            components = [compact_component(c) for c in components]
            rules = [compact_rule_summary(r) for r in rules]

        return {
            "success": True,
            "issue": issue,
            "components": components,
            "rules": rules,
        }
    except SonarAPIError as e:
        return {
            "success": False,
            "error": str(e),
        }


async def sonar_transition_issue(
    ctx: Context[Any, ServerContext],
    issue_key: str,
    transition: str,
) -> dict[str, Any]:
    """Transition a SonarQube issue to a new status.

    Valid transitions:
    - confirm: Confirm issue (OPEN -> CONFIRMED)
    - unconfirm: Unconfirm issue (CONFIRMED -> REOPENED)
    - resolve: Resolve issue as fixed (OPEN/CONFIRMED -> RESOLVED)
    - reopen: Reopen issue (RESOLVED/CLOSED -> REOPENED)
    - wontfix: Mark as won't fix
    - falsepositive: Mark as false positive

    Args:
        ctx: MCP context.
        issue_key: The issue key to transition.
        transition: The transition to apply.

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - issue: dict - Updated issue details
        - error: str - Error message (if success is False)
    """
    server_ctx = get_server_context(ctx)

    try:
        instance = server_ctx.instance_manager.get_active_instance()
    except NoActiveInstanceError:
        return {
            "success": False,
            "error": ERR_NO_ACTIVE_INSTANCE,
        }

    client = create_sonar_client(instance)

    try:
        async with client:
            response = await client.post(
                "/api/issues/do_transition",
                data={"issue": issue_key, "transition": transition},
            )

        return {
            "success": True,
            "issue": response.get("issue", {}),
        }
    except SonarAPIError as e:
        return {
            "success": False,
            "error": str(e),
        }


async def sonar_add_comment(
    ctx: Context[Any, ServerContext],
    issue_key: str,
    text: str,
) -> dict[str, Any]:
    """Add a comment to a SonarQube issue.

    Args:
        ctx: MCP context.
        issue_key: The issue key to comment on.
        text: The comment text (supports markdown).

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - comment: dict - The added comment
        - error: str - Error message (if success is False)
    """
    server_ctx = get_server_context(ctx)

    try:
        instance = server_ctx.instance_manager.get_active_instance()
    except NoActiveInstanceError:
        return {
            "success": False,
            "error": ERR_NO_ACTIVE_INSTANCE,
        }

    client = create_sonar_client(instance)

    try:
        async with client:
            response = await client.post(
                "/api/issues/add_comment",
                data={"issue": issue_key, "text": text},
            )

        issue = response.get("issue", {})
        comments = issue.get("comments", [])
        latest_comment = comments[-1] if comments else {}

        return {
            "success": True,
            "comment": latest_comment,
        }
    except SonarAPIError as e:
        return {
            "success": False,
            "error": str(e),
        }


async def sonar_bulk_transition(
    ctx: Context[Any, ServerContext],
    issue_keys: list[str],
    transition: str,
    task_mode: bool = False,
) -> dict[str, Any]:
    """Bulk transition multiple SonarQube issues.

    Args:
        ctx: MCP context.
        issue_keys: List of issue keys to transition.
        transition: The transition to apply to all issues.
        task_mode: If True, run in background and return task_id immediately.
                   Use sonar_get_task to check progress. Default: False.

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - total: int - Total issues processed (sync mode)
        - failures: int - Number of failed transitions (sync mode)
        - task_id: str - Task ID for tracking (task_mode only)
        - state: str - Initial task state (task_mode only)
        - message: str - Status message (task_mode only)
        - error: str - Error message (if success is False)
    """
    if not issue_keys:
        return {
            "success": False,
            "error": "No issues provided for bulk transition.",
        }

    server_ctx = get_server_context(ctx)

    try:
        instance = server_ctx.instance_manager.get_active_instance()
    except NoActiveInstanceError:
        return {
            "success": False,
            "error": ERR_NO_ACTIVE_INSTANCE,
        }

    # Task mode: run in background and return immediately
    if task_mode:
        task_manager = server_ctx.task_manager
        if not task_manager:
            return {
                "success": False,
                "error": "Task manager not available.",
            }

        async def _bulk_transition_operation() -> dict[str, Any]:
            """Execute bulk transition in background."""
            client = create_sonar_client(instance)

            async with client:
                response = await client.post(
                    "/api/issues/bulk_change",
                    data={
                        "issues": ",".join(issue_keys),
                        "do_transition": transition,
                    },
                )

            return {
                "success": True,
                "total": response.get("total", len(issue_keys)),
                "failures": response.get("failures", 0),
            }

        task_info = await task_manager.create_task("bulk_transition", _bulk_transition_operation)
        return {
            "success": True,
            "task_id": task_info.task_id,
            "state": task_info.state.value,
            "message": f"Bulk transition started for {len(issue_keys)} issues",
        }

    # Synchronous mode: execute and wait for result
    client = create_sonar_client(instance)

    try:
        async with client:
            response = await client.post(
                "/api/issues/bulk_change",
                data={
                    "issues": ",".join(issue_keys),
                    "do_transition": transition,
                },
            )

        return {
            "success": True,
            "total": response.get("total", len(issue_keys)),
            "failures": response.get("failures", 0),
        }
    except SonarAPIError as e:
        return {
            "success": False,
            "error": str(e),
        }


def register_issue_tools(mcp: FastMCP) -> None:
    """Register issue management tools with the MCP server."""
    # Read-only: lists issues, no state changes
    mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True))(sonar_list_issues)

    # Read-only: gets issue details, no state changes
    mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True))(sonar_get_issue)

    # Modifies issue state (transitions status)
    mcp.tool(annotations=ToolAnnotations(destructiveHint=True))(sonar_transition_issue)

    # Adds data (comments) to issues
    mcp.tool(annotations=ToolAnnotations(destructiveHint=True))(sonar_add_comment)

    # Bulk modifies issue states - potentially destructive
    mcp.tool(annotations=ToolAnnotations(destructiveHint=True))(sonar_bulk_transition)
