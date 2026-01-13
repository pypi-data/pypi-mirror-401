"""Task manager for async operations in SonarQube MCP server."""

from __future__ import annotations

import asyncio
import contextlib
import time
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

import structlog


if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

from sonar_mcp.tasks.models import TaskInfo, TaskResult, TaskState


logger = structlog.get_logger()


class TaskManager:
    """Manages async tasks for long-running operations.

    The TaskManager tracks task lifecycle, handles cancellation,
    and provides task status queries following MCP SEP-1686 spec.
    """

    def __init__(self, max_concurrent: int = 10, cleanup_interval: int = 300) -> None:
        """Initialize the task manager.

        Args:
            max_concurrent: Maximum concurrent tasks allowed.
            cleanup_interval: Interval in seconds for expired task cleanup.
        """
        self._tasks: dict[str, TaskInfo] = {}
        self._async_tasks: dict[str, asyncio.Task[Any]] = {}
        self._max_concurrent = max_concurrent
        self._cleanup_interval = cleanup_interval
        self._lock = asyncio.Lock()
        self._cleanup_task: asyncio.Task[None] | None = None

    async def start(self) -> None:
        """Start the task manager cleanup loop."""
        if self._cleanup_task is None:
            self._cleanup_task = asyncio.create_task(self._cleanup_loop())
            logger.info("task_manager_started")

    async def stop(self) -> None:
        """Stop the task manager and cancel all tasks."""
        if self._cleanup_task:
            self._cleanup_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._cleanup_task
            self._cleanup_task = None

        # Cancel all running tasks
        for task_id, async_task in list(self._async_tasks.items()):
            if not async_task.done():
                async_task.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await async_task
                await self._update_state(task_id, TaskState.CANCELLED)

        logger.info("task_manager_stopped", tasks_cancelled=len(self._async_tasks))

    async def _cleanup_loop(self) -> None:
        """Periodically clean up expired tasks."""
        while True:
            try:
                await asyncio.sleep(self._cleanup_interval)
                await self._cleanup_expired()
            except asyncio.CancelledError:
                # Re-raise CancelledError after cleanup (required by asyncio best practices)
                raise

    async def _cleanup_expired(self) -> None:
        """Remove tasks that have exceeded their TTL."""
        now = datetime.now()
        expired = []

        async with self._lock:
            for task_id, task_info in self._tasks.items():
                age = (now - task_info.created_at).total_seconds()
                if age > task_info.ttl_seconds:
                    expired.append(task_id)

            for task_id in expired:
                del self._tasks[task_id]
                self._async_tasks.pop(task_id, None)

        if expired:
            logger.debug("expired_tasks_cleaned", count=len(expired))

    async def create_task(
        self,
        operation: str,
        func: Callable[..., Awaitable[dict[str, Any]]],
        *args: Any,
        ttl_seconds: int = 3600,
        **kwargs: Any,
    ) -> TaskInfo:
        """Create and start a new async task.

        Args:
            operation: Name of the operation being performed.
            func: Async function to execute.
            *args: Positional arguments for the function.
            ttl_seconds: Time-to-live for task data.
            **kwargs: Keyword arguments for the function.

        Returns:
            TaskInfo for the created task.

        Raises:
            RuntimeError: If max concurrent tasks reached.
        """
        async with self._lock:
            active_count = sum(
                1
                for t in self._tasks.values()
                if t.state in (TaskState.WORKING, TaskState.INPUT_REQUIRED)
            )
            if active_count >= self._max_concurrent:
                raise RuntimeError(f"Maximum concurrent tasks ({self._max_concurrent}) reached")

            task_id = str(uuid.uuid4())
            task_info = TaskInfo(
                task_id=task_id,
                state=TaskState.WORKING,
                operation=operation,
                ttl_seconds=ttl_seconds,
            )
            self._tasks[task_id] = task_info

        # Start the async task
        async_task = asyncio.create_task(self._run_task(task_id, func, *args, **kwargs))
        self._async_tasks[task_id] = async_task

        logger.info("task_created", task_id=task_id, operation=operation)
        return task_info

    async def _run_task(
        self,
        task_id: str,
        func: Callable[..., Awaitable[dict[str, Any]]],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Execute a task and handle its lifecycle."""
        start_time = time.monotonic()
        try:
            result = await func(*args, **kwargs)
            duration_ms = int((time.monotonic() - start_time) * 1000)

            async with self._lock:
                if task_id in self._tasks:
                    task_info = self._tasks[task_id]
                    task_info.state = TaskState.COMPLETED
                    task_info.result = result
                    task_info.updated_at = datetime.now()
                    task_info.message = f"Completed in {duration_ms}ms"

            logger.info("task_completed", task_id=task_id, duration_ms=duration_ms)

        except asyncio.CancelledError:
            await self._update_state(task_id, TaskState.CANCELLED, "Task cancelled")
            raise

        except Exception as e:
            duration_ms = int((time.monotonic() - start_time) * 1000)
            async with self._lock:
                if task_id in self._tasks:
                    task_info = self._tasks[task_id]
                    task_info.state = TaskState.FAILED
                    task_info.error = str(e)
                    task_info.updated_at = datetime.now()

            logger.error(
                "task_failed",
                task_id=task_id,
                error=str(e),
                duration_ms=duration_ms,
            )

    async def _update_state(
        self, task_id: str, state: TaskState, message: str | None = None
    ) -> None:
        """Update task state."""
        async with self._lock:
            if task_id in self._tasks:
                task_info = self._tasks[task_id]
                task_info.state = state
                task_info.updated_at = datetime.now()
                if message:
                    task_info.message = message

    async def update_progress(
        self, task_id: str, progress: float, message: str | None = None
    ) -> None:
        """Update task progress.

        Args:
            task_id: Task identifier.
            progress: Progress value 0.0-1.0.
            message: Optional status message.
        """
        async with self._lock:
            if task_id in self._tasks:
                task_info = self._tasks[task_id]
                task_info.progress = max(0.0, min(1.0, progress))
                task_info.updated_at = datetime.now()
                if message:
                    task_info.message = message

    async def get_task(self, task_id: str) -> TaskInfo | None:
        """Get task information by ID.

        Args:
            task_id: Task identifier.

        Returns:
            TaskInfo if found, None otherwise.
        """
        async with self._lock:
            return self._tasks.get(task_id)

    async def get_result(self, task_id: str) -> TaskResult | None:
        """Get the result of a completed task.

        Args:
            task_id: Task identifier.

        Returns:
            TaskResult if task is completed, None otherwise.
        """
        async with self._lock:
            task_info = self._tasks.get(task_id)
            if not task_info:
                return None

            if task_info.state == TaskState.COMPLETED:
                return TaskResult(
                    task_id=task_id,
                    success=True,
                    result=task_info.result,
                )
            elif task_info.state == TaskState.FAILED:
                return TaskResult(
                    task_id=task_id,
                    success=False,
                    error=task_info.error,
                )
            return None

    async def cancel_task(self, task_id: str) -> bool:
        """Cancel a running task.

        Args:
            task_id: Task identifier.

        Returns:
            True if task was cancelled, False if not found or not cancellable.
        """
        async_task = self._async_tasks.get(task_id)
        if async_task and not async_task.done():
            async_task.cancel()
            # Update state immediately to ensure it's set before returning
            await self._update_state(task_id, TaskState.CANCELLED, "Task cancelled")
            logger.info("task_cancelled", task_id=task_id)
            return True
        return False

    async def list_tasks(
        self,
        state: TaskState | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[TaskInfo], int]:
        """List tasks with optional filtering.

        Args:
            state: Optional state filter.
            page: Page number (1-based).
            page_size: Number of tasks per page.

        Returns:
            Tuple of (list of TaskInfo, total count).
        """
        async with self._lock:
            tasks = list(self._tasks.values())

            if state:
                tasks = [t for t in tasks if t.state == state]

            total = len(tasks)

            # Sort by created_at descending (most recent first)
            tasks.sort(key=lambda t: t.created_at, reverse=True)

            # Paginate
            start = (page - 1) * page_size
            end = start + page_size
            return tasks[start:end], total
