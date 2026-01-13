"""Tool category definitions and dispatch pattern for SonarQube MCP server.

This module provides a dispatch pattern (similar to GitLab MCP) for tool invocation:
- sonar_list_categories: Discover available tools by category
- sonar_get_tool_schema: Get parameter schema for a specific tool
- sonar_execute_tool: Execute any tool by name

This pattern avoids MCP protocol limitations around dynamic tool registration.
"""

from __future__ import annotations

import contextlib
import inspect
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, get_type_hints

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

# Tool registry mapping tool names to their implementations
TOOL_REGISTRY: dict[str, Callable[..., Any]] = {}


@dataclass
class CategoryDefinition:
    """Definition of a tool category."""

    name: str
    description: str
    tool_names: list[str]


# Category definitions with their tools
CATEGORY_DEFINITIONS: dict[str, CategoryDefinition] = {}


def _define_categories() -> None:
    """Define all tool categories.

    This is called lazily to avoid circular imports.
    """
    if CATEGORY_DEFINITIONS:
        return  # Already defined

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
            ),
            "project": CategoryDefinition(
                name="project",
                description="Project operations: list, get details, and auto-detect projects",
                tool_names=[
                    "sonar_list_projects",
                    "sonar_get_project",
                    "sonar_detect_project",
                ],
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
            ),
            "quality": CategoryDefinition(
                name="quality",
                description="Quality gates: check project quality status and validate goals",
                tool_names=[
                    "sonar_get_quality_gate",
                    "sonar_check_goals",
                ],
            ),
            "metrics": CategoryDefinition(
                name="metrics",
                description="Metrics retrieval: coverage, bugs, vulnerabilities, code smells",
                tool_names=[
                    "sonar_get_metrics",
                    "sonar_get_coverage",
                    "sonar_get_file_coverage",
                ],
            ),
            "rules": CategoryDefinition(
                name="rules",
                description="Rule details: get information about SonarQube analysis rules",
                tool_names=[
                    "sonar_get_rule",
                ],
            ),
            "task": CategoryDefinition(
                name="task",
                description="Async task management: track long-running background operations",
                tool_names=[
                    "sonar_get_task",
                    "sonar_list_tasks",
                    "sonar_cancel_task",
                ],
            ),
        }
    )


def _build_tool_registry() -> None:
    """Build the tool registry mapping tool names to their implementations.

    This is called lazily to avoid circular imports.
    """
    if TOOL_REGISTRY:
        return  # Already built

    # Import all tool functions
    from sonar_mcp.tools.instance import (
        sonar_list_instances,
        sonar_manage_instance,
        sonar_select_instance,
        sonar_test_connection,
    )
    from sonar_mcp.tools.issue import (
        sonar_add_comment,
        sonar_bulk_transition,
        sonar_get_issue,
        sonar_list_issues,
        sonar_transition_issue,
    )
    from sonar_mcp.tools.metrics import (
        sonar_get_coverage,
        sonar_get_file_coverage,
        sonar_get_metrics,
    )
    from sonar_mcp.tools.project import (
        sonar_detect_project,
        sonar_get_project,
        sonar_list_projects,
    )
    from sonar_mcp.tools.quality_gate import (
        sonar_check_goals,
        sonar_get_quality_gate,
    )
    from sonar_mcp.tools.rules import sonar_get_rule
    from sonar_mcp.tools.task import (
        sonar_cancel_task,
        sonar_get_task,
        sonar_list_tasks,
    )

    TOOL_REGISTRY.update(
        {
            # Instance tools
            "sonar_list_instances": sonar_list_instances,
            "sonar_manage_instance": sonar_manage_instance,
            "sonar_select_instance": sonar_select_instance,
            "sonar_test_connection": sonar_test_connection,
            # Project tools
            "sonar_list_projects": sonar_list_projects,
            "sonar_get_project": sonar_get_project,
            "sonar_detect_project": sonar_detect_project,
            # Issue tools
            "sonar_list_issues": sonar_list_issues,
            "sonar_get_issue": sonar_get_issue,
            "sonar_transition_issue": sonar_transition_issue,
            "sonar_add_comment": sonar_add_comment,
            "sonar_bulk_transition": sonar_bulk_transition,
            # Quality gate tools
            "sonar_get_quality_gate": sonar_get_quality_gate,
            "sonar_check_goals": sonar_check_goals,
            # Metrics tools
            "sonar_get_metrics": sonar_get_metrics,
            "sonar_get_coverage": sonar_get_coverage,
            "sonar_get_file_coverage": sonar_get_file_coverage,
            # Rules tools
            "sonar_get_rule": sonar_get_rule,
            # Task tools
            "sonar_get_task": sonar_get_task,
            "sonar_list_tasks": sonar_list_tasks,
            "sonar_cancel_task": sonar_cancel_task,
        }
    )

    logger.info("tool_registry_built", tool_count=len(TOOL_REGISTRY))


def _extract_schema(func: Callable[..., Any]) -> dict[str, Any]:
    """Extract JSON schema from a function's signature and type hints.

    Args:
        func: The function to extract schema from.

    Returns:
        JSON schema dictionary with properties and descriptions.
    """
    sig = inspect.signature(func)
    type_hints: dict[str, Any] = {}
    with contextlib.suppress(Exception):
        type_hints = get_type_hints(func)

    properties: dict[str, Any] = {}
    required: list[str] = []

    for name, param in sig.parameters.items():
        # Skip 'ctx' parameter (MCP context)
        if name == "ctx":
            continue

        prop: dict[str, Any] = {}

        # Get type from type hints
        if name in type_hints:
            hint = type_hints[name]
            prop["type"] = _python_type_to_json_type(hint)

        # Check if parameter has a default
        if param.default is inspect.Parameter.empty:
            required.append(name)
        else:
            prop["default"] = param.default

        properties[name] = prop

    return {
        "type": "object",
        "properties": properties,
        "required": required,
    }


def _python_type_to_json_type(hint: Any) -> str:
    """Convert Python type hint to JSON schema type.

    Args:
        hint: Python type hint.

    Returns:
        JSON schema type string.
    """
    # Handle None type
    if hint is type(None):
        return "null"

    # Handle basic types
    type_mapping = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
    }

    # Check if it's a basic type
    if hint in type_mapping:
        return type_mapping[hint]

    # Handle Optional, Union, etc. - just return string as fallback
    origin = getattr(hint, "__origin__", None)
    if origin is list:
        return "array"
    if origin is dict:
        return "object"

    # Default to string for complex types
    return "string"


class CategoryManager:
    """Manages tool categories for the dispatch pattern."""

    def __init__(self, server: FastMCP[Any]) -> None:
        """Initialize the category manager.

        Args:
            server: The FastMCP server instance.
        """
        self._server = server
        _define_categories()
        _build_tool_registry()

    def list_categories(
        self, category_filter: str | None = None
    ) -> list[dict[str, Any]] | dict[str, Any] | None:
        """List available categories or get a specific category.

        Args:
            category_filter: Optional category name to filter by.

        Returns:
            List of all categories, single category dict, or None if not found.
        """
        if category_filter:
            if category_filter not in CATEGORY_DEFINITIONS:
                return None
            cat = CATEGORY_DEFINITIONS[category_filter]
            return {
                "name": cat.name,
                "description": cat.description,
                "tool_count": len(cat.tool_names),
                "tools": cat.tool_names,
            }

        return [
            {
                "name": cat.name,
                "description": cat.description,
                "tool_count": len(cat.tool_names),
                "tools": cat.tool_names,
            }
            for cat in CATEGORY_DEFINITIONS.values()
        ]

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


# Meta-tools for dispatch pattern


def sonar_list_categories(
    ctx: Context[Any, ServerContext],  # noqa: ARG001
    category: str | None = None,
) -> dict[str, Any]:
    """Discover available SonarQube tools by category.

    Returns tool names and descriptions. Categories: instance, project,
    issue, quality, metrics, rules, task

    Args:
        category: Optional category name to filter (e.g., "project", "issue").
            If provided, returns only that category's tools.

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - categories: list - Available categories (when no filter)
        - category: dict - Single category details (when filtered)
        - total_tools: int - Total number of tools
        - error: str - Error message (if success is False)
    """
    manager = get_category_manager()
    if manager is None:
        return {
            "success": False,
            "error": _MANAGER_NOT_INITIALIZED_ERROR,
        }

    if category:
        result = manager.list_categories(category_filter=category)
        if result is None:
            return {
                "success": False,
                "error": f"Category '{category}' not found. "
                "Valid categories: instance, project, issue, quality, metrics, rules, task",
            }
        return {
            "success": True,
            "category": result,
            "total_tools": manager.total_tool_count,
        }

    categories = manager.list_categories()
    return {
        "success": True,
        "categories": categories,
        "total_tools": manager.total_tool_count,
    }


def sonar_get_tool_schema(
    ctx: Context[Any, ServerContext],  # noqa: ARG001
    tool_name: str,
) -> dict[str, Any]:
    """Get the full JSON schema for a specific SonarQube tool.

    Use after list_categories to get parameter details before calling execute_tool.

    Args:
        tool_name: Name of the tool (e.g., 'sonar_list_issues', 'sonar_get_project')

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - tool_name: str - The tool name
        - schema: dict - JSON schema for tool parameters
        - description: str - Tool description from docstring
        - error: str - Error message (if success is False)
    """
    _build_tool_registry()

    if tool_name not in TOOL_REGISTRY:
        return {
            "success": False,
            "error": f"Unknown tool: {tool_name}. "
            "Use sonar_list_categories to see available tools.",
        }

    func = TOOL_REGISTRY[tool_name]
    schema = _extract_schema(func)

    # Get description from docstring
    description = ""
    if func.__doc__:
        # Take first paragraph of docstring
        description = func.__doc__.split("\n\n")[0].strip()

    return {
        "success": True,
        "tool_name": tool_name,
        "schema": schema,
        "description": description,
    }


async def sonar_execute_tool(
    ctx: Context[Any, ServerContext],
    tool_name: str,
    arguments: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Execute any SonarQube tool by name with the provided arguments.

    Use after getting the schema to understand required parameters.

    Args:
        tool_name: Name of the tool to execute (e.g., 'sonar_list_issues')
        arguments: Tool-specific arguments (optional). See sonar_get_tool_schema for details.

    Returns:
        The tool's return value, or error dict if tool not found or execution fails.
    """
    _build_tool_registry()

    if tool_name not in TOOL_REGISTRY:
        return {
            "success": False,
            "error": f"Unknown tool: {tool_name}. "
            "Use sonar_list_categories to see available tools.",
        }

    func = TOOL_REGISTRY[tool_name]
    args = arguments or {}

    try:
        # Handle both sync and async tools
        if inspect.iscoroutinefunction(func):
            result: dict[str, Any] = await func(ctx, **args)
        else:
            result = func(ctx, **args)
        return result
    except TypeError as e:
        # Likely missing required arguments
        return {
            "success": False,
            "error": f"Invalid arguments for {tool_name}: {e!s}. "
            "Use sonar_get_tool_schema to see required parameters.",
        }
    except Exception as e:
        logger.exception("tool_execution_error", tool=tool_name, error=str(e))
        return {
            "success": False,
            "error": f"Tool execution failed: {e!s}",
        }


def register_category_tools(mcp: FastMCP[Any]) -> None:
    """Register the dispatch meta-tools with the MCP server.

    These 3 tools are always available and provide access to all SonarQube functionality:
    - sonar_list_categories: Discover available tools
    - sonar_get_tool_schema: Get parameter schema for a tool
    - sonar_execute_tool: Execute any tool by name
    """
    from mcp.types import ToolAnnotations

    mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))(
        sonar_list_categories
    )
    mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))(
        sonar_get_tool_schema
    )
    mcp.tool()(sonar_execute_tool)
