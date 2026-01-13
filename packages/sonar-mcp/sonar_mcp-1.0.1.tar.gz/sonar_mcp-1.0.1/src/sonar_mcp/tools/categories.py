"""Tool category definitions and meta-tools for hierarchical tool management.

This module provides category-based lazy loading of tools to reduce context
window consumption. Instead of loading all 18 tools at startup, only 3
meta-tools are exposed initially. Users can enable specific categories
on-demand.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import structlog
from mcp.server.fastmcp import Context, FastMCP

from sonar_mcp.context import (
    ServerContext,  # noqa: TC001 - Required at runtime for MCP introspection
)


if TYPE_CHECKING:
    from collections.abc import Callable

logger = structlog.get_logger()

# Error message constant to avoid duplication (S1192)
_MANAGER_NOT_INITIALIZED_ERROR = "Category manager not initialized"


@dataclass
class CategoryDefinition:
    """Definition of a tool category."""

    name: str
    description: str
    tool_names: list[str]
    register_func: Callable[[FastMCP[Any]], None]


# Category definitions with their tools
CATEGORY_DEFINITIONS: dict[str, CategoryDefinition] = {}


def _define_categories() -> None:
    """Define all tool categories.

    This is called lazily to avoid circular imports.
    """
    if CATEGORY_DEFINITIONS:
        return  # Already defined

    from sonar_mcp.tools.instance import register_instance_tools
    from sonar_mcp.tools.issue import register_issue_tools
    from sonar_mcp.tools.metrics import register_metrics_tools
    from sonar_mcp.tools.project import register_project_tools
    from sonar_mcp.tools.quality_gate import register_quality_gate_tools
    from sonar_mcp.tools.rules import register_rules_tools
    from sonar_mcp.tools.task import register_task_tools

    CATEGORY_DEFINITIONS.update(
        {
            "instance": CategoryDefinition(
                name="instance",
                description="Instance management: configure SonarQube server connections",
                tool_names=[
                    "sonar_list_instances",
                    "sonar_manage_instance",
                    "sonar_select_instance",
                    "sonar_test_connection",
                ],
                register_func=register_instance_tools,
            ),
            "project": CategoryDefinition(
                name="project",
                description="Project operations: list, get details, and auto-detect projects",
                tool_names=[
                    "sonar_list_projects",
                    "sonar_get_project",
                    "sonar_detect_project",
                ],
                register_func=register_project_tools,
            ),
            "issue": CategoryDefinition(
                name="issue",
                description="Issue management: list, view, transition, comment on code issues",
                tool_names=[
                    "sonar_list_issues",
                    "sonar_get_issue",
                    "sonar_transition_issue",
                    "sonar_add_comment",
                    "sonar_bulk_transition",
                ],
                register_func=register_issue_tools,
            ),
            "quality": CategoryDefinition(
                name="quality",
                description="Quality gates: check project quality status and validate goals",
                tool_names=[
                    "sonar_get_quality_gate",
                    "sonar_check_goals",
                ],
                register_func=register_quality_gate_tools,
            ),
            "metrics": CategoryDefinition(
                name="metrics",
                description="Metrics retrieval: coverage, bugs, vulnerabilities, code smells",
                tool_names=[
                    "sonar_get_metrics",
                    "sonar_get_coverage",
                    "sonar_get_file_coverage",
                ],
                register_func=register_metrics_tools,
            ),
            "rules": CategoryDefinition(
                name="rules",
                description="Rule details: get information about SonarQube analysis rules",
                tool_names=[
                    "sonar_get_rule",
                ],
                register_func=register_rules_tools,
            ),
            "task": CategoryDefinition(
                name="task",
                description="Async task management: track long-running background operations",
                tool_names=[
                    "sonar_get_task",
                    "sonar_list_tasks",
                    "sonar_cancel_task",
                ],
                register_func=register_task_tools,
            ),
        }
    )


class CategoryManager:
    """Manages tool categories with lazy loading support."""

    def __init__(self, server: FastMCP[Any]) -> None:
        """Initialize the category manager.

        Args:
            server: The FastMCP server instance.
        """
        self._server = server
        self._enabled_categories: set[str] = set()
        _define_categories()

    def list_categories(self) -> list[dict[str, Any]]:
        """List all available categories.

        Returns:
            List of category information dictionaries.
        """
        return [
            {
                "name": cat.name,
                "description": cat.description,
                "tool_count": len(cat.tool_names),
                "tools": cat.tool_names,
                "enabled": cat.name in self._enabled_categories,
            }
            for cat in CATEGORY_DEFINITIONS.values()
        ]

    def enable_category(self, name: str) -> dict[str, Any]:
        """Enable a category and register its tools.

        Args:
            name: Category name to enable.

        Returns:
            Result dictionary with enabled tools.

        Raises:
            ValueError: If category doesn't exist.
        """
        if name not in CATEGORY_DEFINITIONS:
            raise ValueError(f"Category '{name}' not found")

        category = CATEGORY_DEFINITIONS[name]

        if name in self._enabled_categories:
            return {
                "success": True,
                "category": name,
                "already_enabled": True,
                "tools": category.tool_names,
            }

        # Register the tools
        category.register_func(self._server)
        self._enabled_categories.add(name)

        logger.info(
            "category_enabled",
            category=name,
            tools=category.tool_names,
        )

        return {
            "success": True,
            "category": name,
            "already_enabled": False,
            "tools": category.tool_names,
            "message": f"Enabled {len(category.tool_names)} tools from '{name}' category",
        }

    def disable_category(self, name: str) -> dict[str, Any]:
        """Mark a category as disabled.

        Note: FastMCP doesn't support unregistering tools at runtime.
        This marks the category as disabled but tools remain available
        until server restart.

        Args:
            name: Category name to disable.

        Returns:
            Result dictionary.

        Raises:
            ValueError: If category doesn't exist.
        """
        if name not in CATEGORY_DEFINITIONS:
            raise ValueError(f"Category '{name}' not found")

        if name not in self._enabled_categories:
            return {
                "success": True,
                "category": name,
                "was_enabled": False,
                "message": f"Category '{name}' was not enabled",
            }

        self._enabled_categories.discard(name)

        logger.info("category_disabled", category=name)

        return {
            "success": True,
            "category": name,
            "was_enabled": True,
            "message": (
                f"Category '{name}' marked as disabled. "
                "Note: Tools remain registered until server restart."
            ),
        }

    def enable_all(self) -> dict[str, Any]:
        """Enable all categories.

        Returns:
            Result dictionary with all enabled tools.
        """
        all_tools: list[str] = []
        for name in CATEGORY_DEFINITIONS:
            if name not in self._enabled_categories:
                result = self.enable_category(name)
                all_tools.extend(result.get("tools", []))

        return {
            "success": True,
            "enabled_categories": list(CATEGORY_DEFINITIONS.keys()),
            "total_tools": len(all_tools),
        }

    def get_enabled_categories(self) -> list[str]:
        """Get list of enabled category names."""
        return list(self._enabled_categories)

    @property
    def total_tool_count(self) -> int:
        """Get total number of tools across all categories."""
        return sum(len(cat.tool_names) for cat in CATEGORY_DEFINITIONS.values())


# Global category manager instance (set by server initialization)
_category_manager: CategoryManager | None = None


def get_category_manager() -> CategoryManager | None:
    """Get the global category manager instance."""
    return _category_manager


def set_category_manager(manager: CategoryManager | None) -> None:
    """Set the global category manager instance."""
    global _category_manager  # noqa: PLW0603
    _category_manager = manager


# Meta-tools for category management


def sonar_list_categories(
    ctx: Context[Any, ServerContext],  # noqa: ARG001
) -> dict[str, Any]:
    """List available tool categories with descriptions.

    Use this to discover what SonarQube capabilities are available.
    Enable specific categories with sonar_enable_category to access their tools.

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - categories: list - Available categories with descriptions and tool counts
        - total_tools: int - Total number of tools across all categories
        - enabled_count: int - Number of currently enabled categories
    """
    manager = get_category_manager()
    if manager is None:
        return {
            "success": False,
            "error": _MANAGER_NOT_INITIALIZED_ERROR,
        }

    categories = manager.list_categories()
    enabled = [c for c in categories if c["enabled"]]

    return {
        "success": True,
        "categories": categories,
        "total_tools": manager.total_tool_count,
        "enabled_count": len(enabled),
    }


def sonar_enable_category(
    ctx: Context[Any, ServerContext],  # noqa: ARG001
    category: str,
) -> dict[str, Any]:
    """Enable tools in a category, making them available for use.

    After enabling, the category's tools will appear in the available tools list.

    Args:
        category: Category name (instance, project, issue, quality, metrics, rules, task)

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - category: str - Category that was enabled
        - tools: list - List of newly available tool names
        - message: str - Status message
        - error: str - Error message (if success is False)
    """
    manager = get_category_manager()
    if manager is None:
        return {
            "success": False,
            "error": _MANAGER_NOT_INITIALIZED_ERROR,
        }

    try:
        return manager.enable_category(category)
    except ValueError as e:
        return {
            "success": False,
            "error": str(e),
        }


def sonar_disable_category(
    ctx: Context[Any, ServerContext],  # noqa: ARG001
    category: str,
) -> dict[str, Any]:
    """Disable tools in a category to reduce context usage.

    Note: Due to MCP protocol limitations, tools remain registered until
    server restart. This primarily serves as a signal for future sessions.

    Args:
        category: Category name to disable.

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - category: str - Category that was disabled
        - message: str - Status message
        - error: str - Error message (if success is False)
    """
    manager = get_category_manager()
    if manager is None:
        return {
            "success": False,
            "error": _MANAGER_NOT_INITIALIZED_ERROR,
        }

    try:
        return manager.disable_category(category)
    except ValueError as e:
        return {
            "success": False,
            "error": str(e),
        }


def register_category_tools(mcp: FastMCP[Any]) -> None:
    """Register the category meta-tools with the MCP server.

    These tools are always available regardless of --all-tools flag.
    """
    from mcp.types import ToolAnnotations

    mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))(
        sonar_list_categories
    )
    mcp.tool(annotations=ToolAnnotations(idempotentHint=True))(sonar_enable_category)
    mcp.tool(annotations=ToolAnnotations(idempotentHint=True))(sonar_disable_category)
