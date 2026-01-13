"""Project management schemas for SonarQube MCP."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from sonar_mcp.schemas.base import BaseResponse, PaginatedResponse


class ProjectInfo(BaseModel):
    """Basic project information."""

    key: str = Field(..., description="Project key")
    name: str = Field(..., description="Project name")
    qualifier: str = Field(default="TRK", description="Project qualifier")

    model_config = {"extra": "allow"}


class ProjectListResponse(PaginatedResponse):
    """Response for sonar_list_projects tool."""

    projects: list[ProjectInfo] = Field(default_factory=list, description="List of projects")


class ProjectDetailResponse(BaseResponse):
    """Response for sonar_get_project tool."""

    project: dict[str, Any] | None = Field(default=None, description="Project details")
    metrics: dict[str, Any] | None = Field(
        default=None, description="Project metrics (if requested)"
    )


class DetectProjectResponse(BaseResponse):
    """Response for sonar_detect_project tool."""

    project_key: str | None = Field(default=None, description="Detected project key")
    source: str | None = Field(
        default=None,
        description="Source file used for detection (sonar-project.properties, pom.xml, etc.)",
    )
