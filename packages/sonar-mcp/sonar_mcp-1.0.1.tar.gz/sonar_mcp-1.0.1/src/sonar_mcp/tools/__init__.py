"""MCP tools for SonarQube operations."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from sonar_mcp.tools.instance import register_instance_tools
from sonar_mcp.tools.issue import register_issue_tools
from sonar_mcp.tools.metrics import register_metrics_tools
from sonar_mcp.tools.project import register_project_tools
from sonar_mcp.tools.quality_gate import register_quality_gate_tools
from sonar_mcp.tools.rules import register_rules_tools
from sonar_mcp.tools.task import register_task_tools


def register_all_tools(mcp: FastMCP) -> None:
    """Register all SonarQube tools with the MCP server.

    Args:
        mcp: The FastMCP server instance to register tools with.
    """
    register_instance_tools(mcp)
    register_issue_tools(mcp)
    register_metrics_tools(mcp)
    register_project_tools(mcp)
    register_quality_gate_tools(mcp)
    register_rules_tools(mcp)
    register_task_tools(mcp)


__all__ = [
    "register_all_tools",
    "register_instance_tools",
    "register_issue_tools",
    "register_metrics_tools",
    "register_project_tools",
    "register_quality_gate_tools",
    "register_rules_tools",
    "register_task_tools",
]
