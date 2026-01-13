"""MCP Resources for exposing SonarQube data via URIs.

These resources provide browseable access to SonarQube data including
projects, issues, metrics, and quality gate status.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sonar_mcp.resources.issues import register_issue_resources
from sonar_mcp.resources.metrics import register_metrics_resources
from sonar_mcp.resources.projects import register_project_resources


if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP

    from sonar_mcp.instance_manager import InstanceManager

__all__ = [
    "register_all_resources",
    "register_issue_resources",
    "register_metrics_resources",
    "register_project_resources",
]


def register_all_resources(mcp: FastMCP, instance_manager: InstanceManager) -> None:
    """Register all SonarQube resources with the MCP server.

    Args:
        mcp: FastMCP server instance.
        instance_manager: Instance manager for SonarQube connections.
    """
    register_project_resources(mcp, instance_manager)
    register_issue_resources(mcp, instance_manager)
    register_metrics_resources(mcp, instance_manager)
