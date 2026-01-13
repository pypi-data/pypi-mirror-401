"""Task models for async operations in SonarQube MCP server."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class TaskState(str, Enum):
    """Task execution state following MCP SEP-1686 specification."""

    WORKING = "working"
    INPUT_REQUIRED = "input_required"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskInfo(BaseModel):
    """Information about an async task."""

    task_id: str = Field(..., description="Unique task identifier")
    state: TaskState = Field(..., description="Current task state")
    created_at: datetime = Field(
        default_factory=datetime.now, description="Task creation timestamp"
    )
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    operation: str = Field(..., description="Operation being performed")
    progress: float | None = Field(default=None, ge=0.0, le=1.0, description="Progress 0.0-1.0")
    message: str | None = Field(default=None, description="Status message")
    result: dict[str, Any] | None = Field(default=None, description="Task result when completed")
    error: str | None = Field(default=None, description="Error message if failed")
    ttl_seconds: int = Field(default=3600, description="Time-to-live in seconds for task data")

    model_config = {"frozen": False}

    def to_mcp_status(self) -> dict[str, Any]:
        """Convert to MCP task status format."""
        return {
            "taskId": self.task_id,
            "state": self.state.value,
            "progress": self.progress,
            "message": self.message,
        }


class TaskRequest(BaseModel):
    """Request to create an async task."""

    operation: str = Field(..., description="Operation to perform")
    parameters: dict[str, Any] = Field(default_factory=dict, description="Operation parameters")
    ttl_seconds: int = Field(
        default=3600, ge=60, le=86400, description="TTL in seconds (1min to 24h)"
    )

    model_config = {"frozen": True}


class TaskResult(BaseModel):
    """Result of a completed task."""

    task_id: str = Field(..., description="Task identifier")
    success: bool = Field(..., description="Whether task completed successfully")
    result: dict[str, Any] | None = Field(default=None, description="Task result data")
    error: str | None = Field(default=None, description="Error message if failed")
    duration_ms: int | None = Field(default=None, description="Task duration in milliseconds")

    model_config = {"frozen": True}
