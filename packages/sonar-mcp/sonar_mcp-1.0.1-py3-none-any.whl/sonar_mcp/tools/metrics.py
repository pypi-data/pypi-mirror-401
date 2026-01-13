"""Metrics tools for SonarQube MCP server."""

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
API_MEASURES_COMPONENT = "/api/measures/component"

# Default metrics to retrieve if no specific keys provided
DEFAULT_METRIC_KEYS = [
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

# Coverage-specific metrics
COVERAGE_METRIC_KEYS = [
    "coverage",
    "line_coverage",
    "branch_coverage",
    "lines_to_cover",
    "uncovered_lines",
    "conditions_to_cover",
    "uncovered_conditions",
]


async def sonar_get_metrics(
    ctx: Context[Any, ServerContext],
    project_key: str,
    metric_keys: list[str] | None = None,
) -> dict[str, Any]:
    """Get metrics for a SonarQube project.

    Args:
        ctx: MCP context.
        project_key: Project key to get metrics for.
        metric_keys: Specific metric keys to retrieve. If None, retrieves
            common metrics including coverage, bugs, vulnerabilities, etc.

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - project_key: str - The project key
        - metrics: dict - Metric key-value pairs
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

    keys_to_fetch = metric_keys if metric_keys else DEFAULT_METRIC_KEYS

    try:
        async with client:
            response = await client.get(
                API_MEASURES_COMPONENT,
                params={
                    "component": project_key,
                    "metricKeys": ",".join(keys_to_fetch),
                },
            )

        measures = response.get("component", {}).get("measures", [])
        metrics = {m["metric"]: m.get("value") for m in measures}

        return {
            "success": True,
            "project_key": project_key,
            "metrics": metrics,
        }
    except SonarAPIError as e:
        return {
            "success": False,
            "error": str(e),
        }


async def sonar_get_coverage(
    ctx: Context[Any, ServerContext],
    project_key: str,
) -> dict[str, Any]:
    """Get detailed coverage information for a SonarQube project.

    Args:
        ctx: MCP context.
        project_key: Project key to get coverage for.

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - project_key: str - The project key
        - coverage: dict - Coverage metrics including:
            - overall: Overall coverage percentage
            - line_coverage: Line coverage percentage
            - branch_coverage: Branch coverage percentage
            - lines_to_cover: Total lines to cover
            - uncovered_lines: Number of uncovered lines
            - conditions_to_cover: Total conditions to cover
            - uncovered_conditions: Number of uncovered conditions
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
                API_MEASURES_COMPONENT,
                params={
                    "component": project_key,
                    "metricKeys": ",".join(COVERAGE_METRIC_KEYS),
                },
            )

        measures = response.get("component", {}).get("measures", [])
        metrics = {m["metric"]: m.get("value") for m in measures}

        coverage = {
            "overall": metrics.get("coverage"),
            "line_coverage": metrics.get("line_coverage"),
            "branch_coverage": metrics.get("branch_coverage"),
            "lines_to_cover": metrics.get("lines_to_cover"),
            "uncovered_lines": metrics.get("uncovered_lines"),
            "conditions_to_cover": metrics.get("conditions_to_cover"),
            "uncovered_conditions": metrics.get("uncovered_conditions"),
        }

        return {
            "success": True,
            "project_key": project_key,
            "coverage": coverage,
        }
    except SonarAPIError as e:
        return {
            "success": False,
            "error": str(e),
        }


async def sonar_get_file_coverage(
    ctx: Context[Any, ServerContext],
    project_key: str,
    file_path: str,
) -> dict[str, Any]:
    """Get coverage information for a specific file.

    Args:
        ctx: MCP context.
        project_key: Project key containing the file.
        file_path: Path to the file within the project.

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - file_path: str - The file path
        - coverage: dict - Coverage metrics for the file
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

    # Construct the component key for the file
    component_key = f"{project_key}:{file_path}"

    try:
        async with client:
            response = await client.get(
                API_MEASURES_COMPONENT,
                params={
                    "component": component_key,
                    "metricKeys": ",".join(COVERAGE_METRIC_KEYS),
                },
            )

        measures = response.get("component", {}).get("measures", [])
        metrics = {m["metric"]: m.get("value") for m in measures}

        coverage = {
            "overall": metrics.get("coverage"),
            "line_coverage": metrics.get("line_coverage"),
            "branch_coverage": metrics.get("branch_coverage"),
            "lines_to_cover": metrics.get("lines_to_cover"),
            "uncovered_lines": metrics.get("uncovered_lines"),
            "conditions_to_cover": metrics.get("conditions_to_cover"),
            "uncovered_conditions": metrics.get("uncovered_conditions"),
        }

        return {
            "success": True,
            "file_path": file_path,
            "coverage": coverage,
        }
    except SonarAPIError as e:
        return {
            "success": False,
            "error": str(e),
        }


def register_metrics_tools(mcp: FastMCP) -> None:
    """Register metrics tools with the MCP server."""
    # All metrics tools are read-only and idempotent
    mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))(sonar_get_metrics)

    mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))(
        sonar_get_coverage
    )

    mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))(
        sonar_get_file_coverage
    )
