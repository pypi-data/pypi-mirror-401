"""Project management tools for SonarQube MCP server."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import Context, FastMCP
from mcp.types import ToolAnnotations

from sonar_mcp.client.sonar_client import SonarAPIError
from sonar_mcp.context import (
    ServerContext,  # noqa: TC001 - Required at runtime for MCP introspection
)
from sonar_mcp.instance_manager import NoActiveInstanceError
from sonar_mcp.tools.client_helper import create_sonar_client, get_server_context


def _detect_from_sonar_properties(search_dir: Path) -> dict[str, Any] | None:
    """Detect project key from sonar-project.properties."""
    sonar_props = search_dir / "sonar-project.properties"
    if not sonar_props.exists():
        return None
    content = sonar_props.read_text()
    match = re.search(r"sonar\.projectKey\s*=\s*(.+)", content)
    if not match:
        return None
    return {
        "success": True,
        "project_key": match.group(1).strip(),
        "source": "sonar-project.properties",
    }


def _detect_from_pom_xml(search_dir: Path) -> dict[str, Any] | None:
    """Detect project key from pom.xml."""
    pom_xml = search_dir / "pom.xml"
    if not pom_xml.exists():
        return None
    content = pom_xml.read_text()
    group_match = re.search(r"<groupId>([^<]+)</groupId>", content)
    artifact_match = re.search(r"<artifactId>([^<]+)</artifactId>", content)
    if not (group_match and artifact_match):
        return None
    return {
        "success": True,
        "project_key": f"{group_match.group(1)}:{artifact_match.group(1)}",
        "source": "pom.xml",
    }


def _detect_from_package_json(search_dir: Path) -> dict[str, Any] | None:
    """Detect project key from package.json."""
    package_json = search_dir / "package.json"
    if not package_json.exists():
        return None
    try:
        content = json.loads(package_json.read_text())
        if "name" not in content:
            return None
        return {
            "success": True,
            "project_key": content["name"],
            "source": "package.json",
        }
    except json.JSONDecodeError:
        return None


def _detect_from_pyproject_toml(search_dir: Path) -> dict[str, Any] | None:
    """Detect project key from pyproject.toml."""
    pyproject_toml = search_dir / "pyproject.toml"
    if not pyproject_toml.exists():
        return None
    content = pyproject_toml.read_text()
    # Use line-by-line parsing instead of DOTALL to avoid ReDoS vulnerability
    in_project_section = False
    for line in content.splitlines():
        if line.strip() == "[project]":
            in_project_section = True
            continue
        if in_project_section and line.strip().startswith("["):
            break  # Entered a new section
        if in_project_section:
            match = re.match(r'name\s*=\s*["\']([^"\']+)["\']', line.strip())
            if match:
                return {
                    "success": True,
                    "project_key": match.group(1),
                    "source": "pyproject.toml",
                }
    return None


async def sonar_list_projects(
    ctx: Context[Any, ServerContext],
    search: str | None = None,
    page: int = 1,
    page_size: int = 100,
) -> dict[str, Any]:
    """List all accessible SonarQube projects.

    Args:
        ctx: MCP context.
        search: Search query to filter projects (optional).
        page: Page number for pagination (default: 1).
        page_size: Number of results per page (default: 100).

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - projects: list - Array of project info
        - total: int - Total number of projects
        - error: str - Error message (if success is False)
    """
    server_ctx = get_server_context(ctx)

    try:
        instance = server_ctx.instance_manager.get_active_instance()
    except NoActiveInstanceError:
        return {
            "success": False,
            "error": "No active instance configured.",
        }

    client = create_sonar_client(instance)

    params: dict[str, Any] = {
        "p": page,
        "ps": page_size,
        "qualifiers": "TRK",
    }

    if search:
        params["q"] = search

    try:
        async with client:
            response = await client.get("/api/components/search", params=params)

        components = response.get("components", [])
        paging = response.get("paging", {})

        projects = [
            {
                "key": comp.get("key"),
                "name": comp.get("name"),
                "qualifier": comp.get("qualifier"),
            }
            for comp in components
        ]

        return {
            "success": True,
            "projects": projects,
            "total": paging.get("total", len(projects)),
            "page": paging.get("pageIndex", page),
            "page_size": paging.get("pageSize", page_size),
        }
    except SonarAPIError as e:
        return {
            "success": False,
            "error": str(e),
        }


async def sonar_get_project(
    ctx: Context[Any, ServerContext],
    project_key: str,
    include_metrics: bool = False,
) -> dict[str, Any]:
    """Get details of a specific SonarQube project.

    Args:
        ctx: MCP context.
        project_key: The project key to retrieve.
        include_metrics: Whether to include project metrics (default: False).

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - project: dict - Project details
        - metrics: dict - Metrics (if include_metrics is True)
        - error: str - Error message (if success is False)
    """
    server_ctx = get_server_context(ctx)

    try:
        instance = server_ctx.instance_manager.get_active_instance()
    except NoActiveInstanceError:
        return {
            "success": False,
            "error": "No active instance configured.",
        }

    client = create_sonar_client(instance)

    try:
        async with client:
            response = await client.get(
                "/api/components/show",
                params={"component": project_key},
            )

            project = response.get("component", {})

            result: dict[str, Any] = {
                "success": True,
                "project": project,
            }

            if include_metrics:
                metrics_response = await client.get(
                    "/api/measures/component",
                    params={
                        "component": project_key,
                        "metricKeys": "bugs,vulnerabilities,code_smells,coverage,"
                        "duplicated_lines_density,ncloc,sqale_rating,"
                        "reliability_rating,security_rating",
                    },
                )
                measures = metrics_response.get("component", {}).get("measures", [])
                result["metrics"] = {m["metric"]: m.get("value") for m in measures}

            return result
    except SonarAPIError as e:
        return {
            "success": False,
            "error": str(e),
        }


def sonar_detect_project(
    ctx: Context[Any, ServerContext],
    directory: str | None = None,
) -> dict[str, Any]:
    """Auto-detect SonarQube project from local files.

    Searches for project configuration in the following order:
    1. sonar-project.properties (sonar.projectKey)
    2. pom.xml (groupId:artifactId)
    3. package.json (name)
    4. pyproject.toml (project.name)

    Args:
        ctx: MCP context.
        directory: Directory to search in (default: current working directory).

    Returns:
        Dictionary with:
        - success: bool - Detection success status
        - project_key: str - Detected project key
        - source: str - Source file used for detection
        - error: str - Error message (if success is False)
    """
    # ctx is required for MCP but not used in this tool
    _ = ctx

    search_dir = Path(directory) if directory else Path.cwd()

    # Try each detection method in priority order
    detectors = [
        _detect_from_sonar_properties,
        _detect_from_pom_xml,
        _detect_from_package_json,
        _detect_from_pyproject_toml,
    ]

    for detector in detectors:
        result = detector(search_dir)
        if result is not None:
            return result

    return {
        "success": False,
        "error": f"Could not detect project key in {search_dir}. "
        "No sonar-project.properties, pom.xml, package.json, or pyproject.toml found.",
    }


def register_project_tools(mcp: FastMCP) -> None:
    """Register project management tools with the MCP server."""
    # All project tools are read-only and idempotent
    mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True))(
        sonar_list_projects
    )

    mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True))(sonar_get_project)

    mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))(
        sonar_detect_project
    )
