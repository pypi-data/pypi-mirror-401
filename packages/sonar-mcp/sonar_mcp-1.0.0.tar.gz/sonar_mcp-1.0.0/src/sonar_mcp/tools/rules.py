"""Rules tools for SonarQube MCP server."""

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


# Essential fields to keep in compact mode for rules
# Removes verbose fields like descriptionSections, params, debt info
ESSENTIAL_RULE_FIELDS = frozenset(
    {
        "key",  # Rule key (e.g., 'python:S1234')
        "name",  # Rule name
        "severity",  # BLOCKER, CRITICAL, MAJOR, MINOR, INFO
        "status",  # READY, DEPRECATED, BETA
        "type",  # BUG, VULNERABILITY, CODE_SMELL
        "lang",  # Language key
        "langName",  # Language name
        "tags",  # User-defined tags
        "sysTags",  # System tags
    }
)


def compact_rule(rule: dict[str, Any]) -> dict[str, Any]:
    """Compact a rule by keeping only essential fields.

    This reduces response size for LLM consumption by removing verbose
    fields like descriptionSections (large HTML), params, debt info,
    and various metadata fields.

    Args:
        rule: Full rule dictionary from SonarQube API.

    Returns:
        Compact rule dictionary with only essential fields.
    """
    return {k: v for k, v in rule.items() if k in ESSENTIAL_RULE_FIELDS}


async def sonar_get_rule(
    ctx: Context[Any, ServerContext],
    rule_key: str,
    actives: bool = False,
    compact: bool = True,
) -> dict[str, Any]:
    """Get details of a SonarQube rule.

    This tool retrieves detailed information about a specific rule, including
    its description, severity, type, and optionally which quality profiles
    have it activated.

    Args:
        ctx: MCP context.
        rule_key: The rule key (e.g., 'python:S1234').
        actives: If True, also return quality profiles where this rule is active.
        compact: Return compact response with only essential fields (default: True).
                 Set to False to return the full API response including
                 descriptionSections (large HTML), params, and other verbose fields.

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - rule: dict - Rule details (compact by default, includes key, name,
                severity, type, lang, langName, status, tags, sysTags)
        - actives: list - Quality profiles with this rule (if actives=True)
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

    params: dict[str, str] = {"key": rule_key}
    if actives:
        params["actives"] = "true"

    try:
        async with client:
            response = await client.get("/api/rules/show", params=params)

        rule = response.get("rule", {})

        # Apply compaction by default to reduce response size for LLM consumption
        if compact:
            rule = compact_rule(rule)

        result: dict[str, Any] = {
            "success": True,
            "rule": rule,
        }

        if actives and "actives" in response:
            result["actives"] = response["actives"]

        return result
    except SonarAPIError as e:
        return {
            "success": False,
            "error": str(e),
        }


def register_rules_tools(mcp: FastMCP) -> None:
    """Register rules tools with the MCP server."""
    # Read-only: fetches rule details, no state changes
    mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True))(sonar_get_rule)
