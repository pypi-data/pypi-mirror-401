"""Base schemas used across all SonarQube MCP responses."""

from __future__ import annotations

from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    """Base response schema for all MCP tool responses."""

    success: bool = Field(..., description="Whether the operation succeeded")
    error: str | None = Field(default=None, description="Error message if success is False")

    model_config = {"extra": "forbid"}


class PaginatedResponse(BaseResponse):
    """Base response schema for paginated results."""

    total: int = Field(..., description="Total number of items")
    page: int = Field(default=1, description="Current page number")
    page_size: int = Field(default=100, description="Number of items per page")
