"""Task management tools for SonarQube MCP server."""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import Context, FastMCP
from mcp.types import ToolAnnotations

from sonar_mcp.context import (
    ServerContext,  # noqa: TC001 - Required at runtime for MCP introspection
)
from sonar_mcp.tasks import TaskState
from sonar_mcp.tools.client_helper import get_server_context


# Error message constants
ERR_TASK_MANAGER_NOT_AVAILABLE = "Task manager not available."


async def sonar_get_task(
    ctx: Context[Any, ServerContext],
    task_id: str,
) -> dict[str, Any]:
    """Get status of an async task by ID.

    Use this tool to check the progress and status of a background task
    that was started with task_mode=True.

    Args:
        ctx: MCP context.
        task_id: The task ID returned when the task was created.

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - task: dict - Task details including state, progress, message
        - error: str - Error message (if success is False)
    """
    server_ctx = get_server_context(ctx)
    task_manager = server_ctx.task_manager

    if not task_manager:
        return {
            "success": False,
            "error": ERR_TASK_MANAGER_NOT_AVAILABLE,
        }

    task_info = await task_manager.get_task(task_id)

    if not task_info:
        return {
            "success": False,
            "error": f"Task '{task_id}' not found.",
        }

    return {
        "success": True,
        "task": {
            "task_id": task_info.task_id,
            "state": task_info.state.value,
            "operation": task_info.operation,
            "progress": task_info.progress,
            "message": task_info.message,
            "created_at": task_info.created_at.isoformat(),
            "updated_at": task_info.updated_at.isoformat(),
            "result": task_info.result,
            "error": task_info.error,
        },
    }


async def sonar_list_tasks(
    ctx: Context[Any, ServerContext],
    state: str | None = None,
    page: int = 1,
    page_size: int = 20,
) -> dict[str, Any]:
    """List all tasks with optional state filtering.

    Use this tool to see all background tasks and their current status.

    Args:
        ctx: MCP context.
        state: Optional filter by state (working, completed, failed, cancelled).
        page: Page number for pagination (default: 1).
        page_size: Number of results per page (default: 20).

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - tasks: list - Array of task objects
        - total: int - Total number of tasks matching filter
        - page: int - Current page number
        - page_size: int - Results per page
        - error: str - Error message (if success is False)
    """
    server_ctx = get_server_context(ctx)
    task_manager = server_ctx.task_manager

    if not task_manager:
        return {
            "success": False,
            "error": ERR_TASK_MANAGER_NOT_AVAILABLE,
        }

    # Convert state string to TaskState enum if provided
    task_state = None
    if state:
        try:
            task_state = TaskState(state.lower())
        except ValueError:
            valid_states = "working, completed, failed, cancelled, input_required"
            return {
                "success": False,
                "error": f"Invalid state '{state}'. Valid states: {valid_states}.",
            }

    tasks, total = await task_manager.list_tasks(
        state=task_state,
        page=page,
        page_size=page_size,
    )

    return {
        "success": True,
        "tasks": [
            {
                "task_id": t.task_id,
                "state": t.state.value,
                "operation": t.operation,
                "progress": t.progress,
                "message": t.message,
                "created_at": t.created_at.isoformat(),
            }
            for t in tasks
        ],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


async def sonar_cancel_task(
    ctx: Context[Any, ServerContext],
    task_id: str,
) -> dict[str, Any]:
    """Cancel a running task by ID.

    Use this tool to stop a background task that is currently running.
    Only tasks in 'working' state can be cancelled.

    Args:
        ctx: MCP context.
        task_id: The task ID to cancel.

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - cancelled: bool - Whether the task was cancelled
        - message: str - Status message
        - error: str - Error message (if success is False)
    """
    server_ctx = get_server_context(ctx)
    task_manager = server_ctx.task_manager

    if not task_manager:
        return {
            "success": False,
            "error": ERR_TASK_MANAGER_NOT_AVAILABLE,
        }

    cancelled = await task_manager.cancel_task(task_id)

    if cancelled:
        return {
            "success": True,
            "cancelled": True,
            "message": f"Task '{task_id}' has been cancelled.",
        }

    # Check if task exists to provide better error message
    task_info = await task_manager.get_task(task_id)
    if not task_info:
        return {
            "success": False,
            "cancelled": False,
            "error": f"Task '{task_id}' not found.",
        }

    return {
        "success": False,
        "cancelled": False,
        "error": f"Task '{task_id}' cannot be cancelled (state: {task_info.state.value}).",
    }


def register_task_tools(mcp: FastMCP) -> None:
    """Register task management tools with the MCP server."""
    # Read-only: gets task status, no state changes
    mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(sonar_get_task)

    # Read-only: lists tasks, no state changes
    mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(sonar_list_tasks)

    # Modifies task state (cancels running tasks)
    mcp.tool(annotations=ToolAnnotations(destructiveHint=True))(sonar_cancel_task)
