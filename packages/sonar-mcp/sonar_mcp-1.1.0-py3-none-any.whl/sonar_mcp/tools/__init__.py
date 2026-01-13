"""MCP tools for SonarQube operations.

This module provides the dispatch pattern for tool invocation:
- sonar_list_categories: Discover available tools by category
- sonar_get_tool_schema: Get parameter schema for a specific tool
- sonar_execute_tool: Execute any tool by name

All SonarQube tools are accessed through these 3 meta-tools.
"""

from __future__ import annotations

from sonar_mcp.tools.categories import (
    CATEGORY_DEFINITIONS,
    TOOL_REGISTRY,
    CategoryManager,
    _build_tool_registry,
    _define_categories,
    register_category_tools,
    sonar_execute_tool,
    sonar_get_tool_schema,
    sonar_list_categories,
)


__all__ = [
    "CATEGORY_DEFINITIONS",
    "TOOL_REGISTRY",
    "CategoryManager",
    "_build_tool_registry",
    "_define_categories",
    "register_category_tools",
    "sonar_execute_tool",
    "sonar_get_tool_schema",
    "sonar_list_categories",
]
