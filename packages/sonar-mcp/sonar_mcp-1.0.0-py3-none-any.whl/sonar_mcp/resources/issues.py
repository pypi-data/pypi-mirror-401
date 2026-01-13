"""Issue resources for SonarQube MCP server."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from sonar_mcp.client.sonar_client import SonarAPIError, SonarClient
from sonar_mcp.instance_manager import InstanceManager, NoActiveInstanceError
from sonar_mcp.tools.client_helper import create_sonar_client
from sonar_mcp.tools.issue import compact_issue


if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP


# Module-level instance manager for resources
_instance_manager: InstanceManager | None = None


def _get_client() -> SonarClient | None:
    """Get a SonarClient from the instance manager, or None if not configured."""
    if _instance_manager is None:
        return None

    try:
        instance = _instance_manager.get_active_instance()
    except NoActiveInstanceError:
        return None

    return create_sonar_client(instance)


async def get_project_issues(project_key: str, severity: str | None = None) -> str:
    """Get issues for a SonarQube project.

    Args:
        project_key: The project key to get issues for.
        severity: Optional severity filter (BLOCKER, CRITICAL, MAJOR, MINOR, INFO).

    Returns:
        JSON string containing list of issues.
    """
    client = _get_client()
    if client is None:
        return json.dumps({"error": "No active SonarQube instance configured"})

    params: dict[str, Any] = {
        "componentKeys": project_key,
        "ps": 100,
    }

    if severity:
        params["severities"] = severity

    try:
        async with client:
            response = await client.get("/api/issues/search", params=params)

        issues = response.get("issues", [])
        # Use compact format for LLM consumption
        compact_issues = [compact_issue(issue) for issue in issues]

        result = {
            "project_key": project_key,
            "issues": compact_issues,
            "total": response.get("paging", {}).get("total", len(compact_issues)),
        }

        if severity:
            result["severity_filter"] = severity

        return json.dumps(result, indent=2)
    except SonarAPIError as e:
        return json.dumps({"error": str(e)})


def register_issue_resources(mcp: FastMCP, instance_manager: InstanceManager) -> None:
    """Register issue resources with the MCP server.

    Args:
        mcp: FastMCP server instance.
        instance_manager: Instance manager for SonarQube connections.
    """
    global _instance_manager  # noqa: PLW0603
    _instance_manager = instance_manager

    @mcp.resource(
        "sonarqube://projects/{project_key}/issues",
        name="Project Issues",
        description="Get all issues for a project",
        mime_type="application/json",
    )
    async def project_issues_resource(project_key: str) -> str:
        return await get_project_issues(project_key)

    @mcp.resource(
        "sonarqube://projects/{project_key}/issues/{severity}",
        name="Project Issues by Severity",
        description="Get issues filtered by severity (BLOCKER, CRITICAL, MAJOR, MINOR, INFO)",
        mime_type="application/json",
    )
    async def project_issues_by_severity_resource(project_key: str, severity: str) -> str:
        return await get_project_issues(project_key, severity.upper())
