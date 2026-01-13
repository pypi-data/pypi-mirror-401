"""Metrics schemas for SonarQube MCP."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from sonar_mcp.schemas.base import BaseResponse


class CoverageDetails(BaseModel):
    """Detailed coverage metrics."""

    overall: float | None = Field(default=None, description="Overall coverage percentage")
    line_coverage: float | None = Field(default=None, description="Line coverage percentage")
    branch_coverage: float | None = Field(default=None, description="Branch coverage percentage")
    lines_to_cover: int | None = Field(default=None, description="Total lines to cover")
    uncovered_lines: int | None = Field(default=None, description="Number of uncovered lines")
    conditions_to_cover: int | None = Field(default=None, description="Total conditions to cover")
    uncovered_conditions: int | None = Field(
        default=None, description="Number of uncovered conditions"
    )

    model_config = {"extra": "forbid"}


class MetricsResponse(BaseResponse):
    """Response for sonar_get_metrics tool."""

    project_key: str | None = Field(default=None, description="Project key")
    metrics: dict[str, Any] = Field(default_factory=dict, description="Metric key-value pairs")


class CoverageResponse(BaseResponse):
    """Response for sonar_get_coverage tool."""

    project_key: str | None = Field(default=None, description="Project key")
    coverage: CoverageDetails | None = Field(default=None, description="Coverage metrics")


class FileCoverageResponse(BaseResponse):
    """Response for sonar_get_file_coverage tool."""

    file_path: str | None = Field(default=None, description="File path")
    coverage: CoverageDetails | None = Field(default=None, description="File coverage metrics")
