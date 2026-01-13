"""Instance management schemas for SonarQube MCP."""

from __future__ import annotations

from pydantic import BaseModel, Field

from sonar_mcp.schemas.base import BaseResponse


class InstanceInfo(BaseModel):
    """Information about a SonarQube instance."""

    name: str = Field(..., description="Instance name (unique identifier)")
    url: str = Field(..., description="SonarQube server URL")
    organization: str | None = Field(default=None, description="Organization key for SonarCloud")
    default: bool = Field(default=False, description="Whether this is the default instance")
    verify_ssl: bool = Field(default=True, description="Whether SSL certificates are verified")
    timeout: float = Field(default=30.0, description="Request timeout in seconds")

    model_config = {"extra": "forbid"}


class InstanceListResponse(BaseResponse):
    """Response for sonar_list_instances tool."""

    instances: list[InstanceInfo] = Field(
        default_factory=list, description="List of configured instances"
    )
    total: int = Field(default=0, description="Total number of instances")
    active_instance: str | None = Field(
        default=None, description="Name of the currently active instance"
    )


class InstanceManageResponse(BaseResponse):
    """Response for sonar_manage_instance tool."""

    operation: str | None = Field(default=None, description="Operation performed (add or remove)")
    instance: InstanceInfo | None = Field(
        default=None, description="Instance details (for add operation)"
    )
    name: str | None = Field(default=None, description="Instance name (for remove operation)")


class SelectInstanceResponse(BaseResponse):
    """Response for sonar_select_instance tool."""

    selected_instance: str | None = Field(
        default=None, description="Name of the newly selected instance"
    )
    previous_instance: str | None = Field(
        default=None, description="Name of the previously active instance"
    )


class TestConnectionResponse(BaseResponse):
    """Response for sonar_test_connection tool."""

    connected: bool = Field(default=False, description="Whether connection was successful")
    version: str | None = Field(default=None, description="SonarQube server version (if connected)")
    instance: str | None = Field(default=None, description="Name of the tested instance")
