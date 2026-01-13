"""Server context for SonarQube MCP server."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from sonar_mcp.instance_manager import InstanceManager


if TYPE_CHECKING:
    from sonar_mcp.tasks import TaskManager
    from sonar_mcp.tools.categories import CategoryManager


@dataclass
class ServerContext:
    """Server context containing shared state.

    This context is created during server lifespan and provides access
    to the instance manager, task manager, and other shared resources.

    Attributes:
        instance_manager: Manager for SonarQube instances.
        task_manager: Manager for async tasks (optional).
        category_manager: Manager for tool categories (optional).
    """

    instance_manager: InstanceManager = field(default_factory=InstanceManager)
    task_manager: TaskManager | None = None
    category_manager: CategoryManager | None = None
