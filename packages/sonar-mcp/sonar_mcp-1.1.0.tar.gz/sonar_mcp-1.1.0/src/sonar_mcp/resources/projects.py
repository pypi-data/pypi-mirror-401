"""Project resources for SonarQube MCP server."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from sonar_mcp.client.sonar_client import SonarAPIError, SonarClient
from sonar_mcp.instance_manager import InstanceManager, NoActiveInstanceError
from sonar_mcp.tools.client_helper import create_sonar_client


if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP


# Module-level instance manager for resources
# This is initialized when resources are registered
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


async def get_projects_list() -> str:
    """Get list of all SonarQube projects.

    Returns:
        JSON string containing list of projects.
    """
    client = _get_client()
    if client is None:
        return json.dumps({"error": "No active SonarQube instance configured"})

    try:
        async with client:
            response = await client.get(
                "/api/components/search",
                params={"qualifiers": "TRK", "ps": 100},
            )

        projects = [
            {
                "key": comp.get("key"),
                "name": comp.get("name"),
            }
            for comp in response.get("components", [])
        ]

        return json.dumps({"projects": projects, "total": len(projects)}, indent=2)
    except SonarAPIError as e:
        return json.dumps({"error": str(e)})


async def get_project_detail(project_key: str) -> str:
    """Get details for a specific SonarQube project.

    Args:
        project_key: The project key to retrieve.

    Returns:
        JSON string containing project details and summary metrics.
    """
    client = _get_client()
    if client is None:
        return json.dumps({"error": "No active SonarQube instance configured"})

    try:
        async with client:
            # Get project details
            project_response = await client.get(
                "/api/components/show",
                params={"component": project_key},
            )

            # Get key metrics
            metrics_response = await client.get(
                "/api/measures/component",
                params={
                    "component": project_key,
                    "metricKeys": "bugs,vulnerabilities,code_smells,coverage,"
                    "duplicated_lines_density,ncloc,sqale_rating,"
                    "reliability_rating,security_rating",
                },
            )

            # Get quality gate status
            qg_response = await client.get(
                "/api/qualitygates/project_status",
                params={"projectKey": project_key},
            )

        project = project_response.get("component", {})
        measures = metrics_response.get("component", {}).get("measures", [])
        metrics = {m["metric"]: m.get("value") for m in measures}
        quality_gate = qg_response.get("projectStatus", {})

        result = {
            "project": {
                "key": project.get("key"),
                "name": project.get("name"),
                "description": project.get("description"),
                "visibility": project.get("visibility"),
            },
            "metrics": metrics,
            "quality_gate": {
                "status": quality_gate.get("status"),
            },
        }

        return json.dumps(result, indent=2)
    except SonarAPIError as e:
        return json.dumps({"error": str(e)})


def register_project_resources(mcp: FastMCP, instance_manager: InstanceManager) -> None:
    """Register project resources with the MCP server.

    Args:
        mcp: FastMCP server instance.
        instance_manager: Instance manager for SonarQube connections.
    """
    global _instance_manager  # noqa: PLW0603
    _instance_manager = instance_manager

    @mcp.resource(
        "sonarqube://projects",
        name="SonarQube Projects",
        description="List all accessible SonarQube projects",
        mime_type="application/json",
    )
    async def projects_resource() -> str:
        return await get_projects_list()

    @mcp.resource(
        "sonarqube://projects/{project_key}",
        name="SonarQube Project",
        description="Get details and summary for a specific project",
        mime_type="application/json",
    )
    async def project_detail_resource(project_key: str) -> str:
        return await get_project_detail(project_key)
