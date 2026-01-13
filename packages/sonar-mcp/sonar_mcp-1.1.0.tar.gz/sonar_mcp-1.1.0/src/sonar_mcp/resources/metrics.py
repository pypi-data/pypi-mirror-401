"""Metrics resources for SonarQube MCP server."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from sonar_mcp.client.sonar_client import SonarAPIError, SonarClient
from sonar_mcp.instance_manager import InstanceManager, NoActiveInstanceError
from sonar_mcp.tools.client_helper import create_sonar_client


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


async def get_project_metrics(project_key: str) -> str:
    """Get metrics for a SonarQube project.

    Args:
        project_key: The project key to get metrics for.

    Returns:
        JSON string containing project metrics.
    """
    client = _get_client()
    if client is None:
        return json.dumps({"error": "No active SonarQube instance configured"})

    metric_keys = [
        "coverage",
        "line_coverage",
        "branch_coverage",
        "bugs",
        "vulnerabilities",
        "code_smells",
        "ncloc",
        "duplicated_lines_density",
        "sqale_rating",
        "reliability_rating",
        "security_rating",
    ]

    try:
        async with client:
            response = await client.get(
                "/api/measures/component",
                params={
                    "component": project_key,
                    "metricKeys": ",".join(metric_keys),
                },
            )

        measures = response.get("component", {}).get("measures", [])
        metrics = {m["metric"]: m.get("value") for m in measures}

        result = {
            "project_key": project_key,
            "metrics": metrics,
        }

        return json.dumps(result, indent=2)
    except SonarAPIError as e:
        return json.dumps({"error": str(e)})


async def get_project_quality_gate(project_key: str) -> str:
    """Get quality gate status for a SonarQube project.

    Args:
        project_key: The project key to get quality gate for.

    Returns:
        JSON string containing quality gate status.
    """
    client = _get_client()
    if client is None:
        return json.dumps({"error": "No active SonarQube instance configured"})

    try:
        async with client:
            response = await client.get(
                "/api/qualitygates/project_status",
                params={"projectKey": project_key},
            )

        project_status = response.get("projectStatus", {})

        result = {
            "project_key": project_key,
            "status": project_status.get("status", "UNKNOWN"),
            "conditions": project_status.get("conditions", []),
        }

        return json.dumps(result, indent=2)
    except SonarAPIError as e:
        return json.dumps({"error": str(e)})


def register_metrics_resources(mcp: FastMCP, instance_manager: InstanceManager) -> None:
    """Register metrics resources with the MCP server.

    Args:
        mcp: FastMCP server instance.
        instance_manager: Instance manager for SonarQube connections.
    """
    global _instance_manager  # noqa: PLW0603
    _instance_manager = instance_manager

    @mcp.resource(
        "sonarqube://projects/{project_key}/metrics",
        name="Project Metrics",
        description="Get metrics including coverage, bugs, vulnerabilities, and ratings",
        mime_type="application/json",
    )
    async def project_metrics_resource(project_key: str) -> str:
        return await get_project_metrics(project_key)

    @mcp.resource(
        "sonarqube://projects/{project_key}/quality-gate",
        name="Project Quality Gate",
        description="Get quality gate status and conditions for a project",
        mime_type="application/json",
    )
    async def project_quality_gate_resource(project_key: str) -> str:
        return await get_project_quality_gate(project_key)
