"""MCP server core for SonarQube."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from mcp.server.fastmcp import FastMCP

from sonar_mcp import __version__
from sonar_mcp.context import ServerContext
from sonar_mcp.instance_manager import InstanceManager
from sonar_mcp.prompts import register_all_prompts
from sonar_mcp.resources import register_all_resources
from sonar_mcp.tasks import TaskManager
from sonar_mcp.tools.categories import (
    CategoryManager,
    register_category_tools,
    set_category_manager,
)


if TYPE_CHECKING:
    from collections.abc import AsyncIterator

# Re-export ServerContext for backward compatibility
__all__ = [
    "ServerContext",
    "create_server",
    "get_server_version",
    "mcp",
]

# Shared instance manager for both server context and resources
_shared_instance_manager = InstanceManager()


def get_server_version() -> str:
    """Get the server version.

    Returns:
        Version string from package metadata.
    """
    return __version__


@asynccontextmanager
async def lifespan(server: FastMCP[ServerContext]) -> AsyncIterator[ServerContext]:
    """Manage server lifespan.

    Creates and provides the server context during the server's lifetime.
    Initializes the task manager and category manager, cleans up on shutdown.

    Args:
        server: The FastMCP server instance.

    Yields:
        ServerContext with initialized resources.
    """
    task_manager = TaskManager()
    await task_manager.start()

    # Initialize category manager (builds tool registry)
    category_manager = CategoryManager(server)
    set_category_manager(category_manager)

    # Use the shared instance manager
    context = ServerContext(
        instance_manager=_shared_instance_manager,
        task_manager=task_manager,
        category_manager=category_manager,
    )
    try:
        yield context
    finally:
        await task_manager.stop()
        set_category_manager(None)


def create_server(
    host: str = "127.0.0.1",
    port: int = 8000,
) -> FastMCP[ServerContext]:
    """Create and configure the MCP server.

    The server exposes 3 dispatch meta-tools that provide access to all
    SonarQube functionality via the dispatch pattern (similar to GitLab MCP):
    - sonar_list_categories: Discover available tools by category
    - sonar_get_tool_schema: Get parameter schema for a specific tool
    - sonar_execute_tool: Execute any tool by name

    Args:
        host: Host address for HTTP transports (default: 127.0.0.1).
        port: Port for HTTP transports (default: 8000).

    Returns:
        Configured FastMCP server instance.
    """
    server: FastMCP[ServerContext] = FastMCP(
        name="sonar-mcp",
        instructions="SonarQube MCP Server - Interact with SonarQube code quality platform",
        lifespan=lifespan,
        host=host,
        port=port,
    )

    # Register the 3 dispatch meta-tools
    register_category_tools(server)

    # Register resources and prompts (always available)
    register_all_resources(server, _shared_instance_manager)
    register_all_prompts(server)

    return server


# Create the default server instance (stdio transport, default host/port for HTTP if needed)
mcp = create_server()
