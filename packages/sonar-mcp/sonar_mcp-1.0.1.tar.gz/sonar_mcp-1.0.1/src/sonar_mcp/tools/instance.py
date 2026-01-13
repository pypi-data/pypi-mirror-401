"""Instance management tools for SonarQube MCP server."""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import Context, FastMCP
from mcp.types import ToolAnnotations
from pydantic import SecretStr

from sonar_mcp.client.sonar_client import SonarAPIError, SonarClient
from sonar_mcp.config.models import SonarInstance
from sonar_mcp.context import (
    ServerContext,  # noqa: TC001 - Required at runtime for MCP introspection
)
from sonar_mcp.instance_manager import InstanceNotFoundError, NoActiveInstanceError
from sonar_mcp.tools.client_helper import get_server_context


def sonar_list_instances(ctx: Context[Any, ServerContext]) -> dict[str, Any]:
    """List all configured SonarQube instances.

    Args:
        ctx: MCP context.

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - instances: list - Array of instance info (without tokens)
        - total: int - Total number of instances
        - active_instance: str | None - Name of active instance
    """
    server_ctx = get_server_context(ctx)
    instances = server_ctx.instance_manager.list_instances()
    active_name = server_ctx.instance_manager.active_instance_name

    instance_list = [
        {
            "name": inst.name,
            "url": inst.url,
            "organization": inst.organization,
            "default": inst.default,
            "verify_ssl": inst.verify_ssl,
            "timeout": inst.timeout,
        }
        for inst in instances
    ]

    return {
        "success": True,
        "instances": instance_list,
        "total": len(instance_list),
        "active_instance": active_name,
    }


def sonar_manage_instance(
    ctx: Context[Any, ServerContext],
    operation: str,
    name: str,
    url: str | None = None,
    token: str | None = None,
    organization: str | None = None,
    verify_ssl: bool = True,
    request_timeout: float = 30.0,
) -> dict[str, Any]:
    """Add or remove SonarQube instances.

    Args:
        ctx: MCP context.
        operation: Operation to perform ("add" or "remove").
        name: Instance name (unique identifier).
        url: SonarQube server URL (required for "add").
        token: API authentication token (required for "add").
        organization: Organization key for SonarCloud (optional).
        verify_ssl: Whether to verify SSL certificates (default: True).
        request_timeout: Request timeout in seconds (default: 30.0).

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - operation: str - Operation performed
        - instance: dict - Instance details (for "add")
        - name: str - Instance name (for "remove")
        - error: str - Error message (if success is False)
    """
    server_ctx = get_server_context(ctx)

    if operation not in ("add", "remove"):
        return {
            "success": False,
            "error": f"Invalid operation '{operation}'. Must be 'add' or 'remove'.",
        }

    if operation == "add":
        if url is None or token is None:
            return {
                "success": False,
                "error": "Both 'url' and 'token' are required for 'add' operation.",
            }

        try:
            instance = SonarInstance(
                name=name,
                url=url,
                token=SecretStr(token),
                organization=organization,
                verify_ssl=verify_ssl,
                timeout=request_timeout,
            )
            server_ctx.instance_manager.add_instance(instance)

            return {
                "success": True,
                "operation": "add",
                "instance": {
                    "name": instance.name,
                    "url": instance.url,
                    "organization": instance.organization,
                    "verify_ssl": instance.verify_ssl,
                    "timeout": instance.timeout,
                },
            }
        except ValueError as e:
            return {
                "success": False,
                "error": str(e),
            }

    server_ctx.instance_manager.remove_instance(name)
    return {
        "success": True,
        "operation": "remove",
        "name": name,
    }


def sonar_select_instance(
    ctx: Context[Any, ServerContext],
    name: str,
) -> dict[str, Any]:
    """Select the active SonarQube instance.

    Args:
        ctx: MCP context.
        name: Name of the instance to select.

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - selected_instance: str - Name of newly selected instance
        - previous_instance: str | None - Name of previously active instance
        - error: str - Error message (if success is False)
    """
    server_ctx = get_server_context(ctx)
    previous = server_ctx.instance_manager.active_instance_name

    try:
        server_ctx.instance_manager.select_instance(name)
        return {
            "success": True,
            "selected_instance": name,
            "previous_instance": previous,
        }
    except InstanceNotFoundError:
        return {
            "success": False,
            "error": f"Instance '{name}' not found.",
        }


async def sonar_test_connection(
    ctx: Context[Any, ServerContext],
    instance_name: str | None = None,
) -> dict[str, Any]:
    """Test connection to a SonarQube instance.

    Args:
        ctx: MCP context.
        instance_name: Name of instance to test (optional, uses active if not specified).

    Returns:
        Dictionary with:
        - success: bool - Tool execution success
        - connected: bool - Whether connection succeeded
        - version: str - SonarQube version (if connected)
        - instance: str - Instance name tested
        - error: str - Error message (if not connected)
    """
    server_ctx = get_server_context(ctx)

    try:
        if instance_name is not None:
            instance = server_ctx.instance_manager.get_instance(instance_name)
            if instance is None:
                return {
                    "success": False,
                    "error": f"Instance '{instance_name}' not found.",
                }
        else:
            instance = server_ctx.instance_manager.get_active_instance()
    except NoActiveInstanceError:
        return {
            "success": False,
            "error": "No active instance configured.",
        }

    client = SonarClient(
        base_url=instance.url,
        token=instance.token.get_secret_value(),
        organization=instance.organization,
        timeout=instance.timeout,
        verify_ssl=instance.verify_ssl,
    )

    try:
        async with client:
            response = await client.get("/api/system/status")
            version = response.get("version", "unknown")

            return {
                "success": True,
                "connected": True,
                "version": version,
                "instance": instance.name,
            }
    except SonarAPIError as e:
        return {
            "success": True,
            "connected": False,
            "error": str(e),
            "instance": instance.name,
        }


def register_instance_tools(mcp: FastMCP) -> None:
    """Register instance management tools with the MCP server."""
    # Read-only: just lists instances, no state changes
    mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))(
        sonar_list_instances
    )

    # Destructive: adds/removes instances from configuration
    mcp.tool(annotations=ToolAnnotations(destructiveHint=True))(sonar_manage_instance)

    # Not destructive but changes active instance state
    mcp.tool(annotations=ToolAnnotations(idempotentHint=True))(sonar_select_instance)

    # Read-only: tests connection, no state changes
    mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))(
        sonar_test_connection
    )
