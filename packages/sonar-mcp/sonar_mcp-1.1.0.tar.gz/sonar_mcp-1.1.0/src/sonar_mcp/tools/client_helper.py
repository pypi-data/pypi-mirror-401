"""Client helper for SonarQube MCP tools."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from sonar_mcp.client.sonar_client import SonarClient
from sonar_mcp.context import ServerContext


if TYPE_CHECKING:
    from mcp.server.fastmcp import Context

    from sonar_mcp.config.models import SonarInstance


def get_server_context(ctx: Context[Any, ServerContext] | ServerContext) -> ServerContext:
    """Extract ServerContext from MCP Context or return if already ServerContext.

    This helper handles both runtime (MCP Context) and test (ServerContext) cases.

    Args:
        ctx: Either an MCP Context wrapping ServerContext, or a ServerContext directly.

    Returns:
        The ServerContext instance.
    """
    if isinstance(ctx, ServerContext):
        return ctx
    return ctx.request_context.lifespan_context


def create_sonar_client(instance: SonarInstance) -> SonarClient:
    """Create a SonarClient from an instance configuration.

    This centralizes client creation to reduce code duplication
    across tool modules.

    Args:
        instance: The SonarQube instance configuration.

    Returns:
        Configured SonarClient ready for use.
    """
    return SonarClient(
        base_url=instance.url,
        token=instance.token.get_secret_value(),
        organization=instance.organization,
        timeout=instance.timeout,
        verify_ssl=instance.verify_ssl,
    )
