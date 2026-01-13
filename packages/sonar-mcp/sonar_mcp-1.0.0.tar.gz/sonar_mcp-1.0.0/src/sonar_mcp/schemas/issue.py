"""Issue management schemas for SonarQube MCP."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from sonar_mcp.schemas.base import BaseResponse, PaginatedResponse


class CompactIssue(BaseModel):
    """Compact representation of a SonarQube issue.

    Contains only essential fields for LLM consumption.
    """

    key: str = Field(..., description="Issue unique key")
    rule: str = Field(..., description="Rule key that triggered this issue")
    severity: str = Field(..., description="Issue severity (BLOCKER, CRITICAL, MAJOR, MINOR, INFO)")
    component: str = Field(..., description="File path containing the issue")
    project: str = Field(..., description="Project key")
    line: int | None = Field(default=None, description="Line number in the file")
    status: str = Field(
        ..., description="Issue status (OPEN, CONFIRMED, REOPENED, RESOLVED, CLOSED)"
    )
    message: str = Field(..., description="Issue description/message")
    type: str = Field(..., description="Issue type (BUG, VULNERABILITY, CODE_SMELL)")
    issueStatus: str | None = Field(default=None, description="Additional issue status information")
    resolution: str | None = Field(default=None, description="Resolution (when status is CLOSED)")
    tags: list[str] = Field(default_factory=list, description="Issue tags")

    model_config = {"extra": "allow"}


class CompactComponent(BaseModel):
    """Compact representation of a component."""

    key: str = Field(..., description="Component key")
    name: str = Field(..., description="Component name")
    path: str | None = Field(default=None, description="File path (if applicable)")
    qualifier: str = Field(..., description="Component qualifier (TRK, FIL, etc.)")

    model_config = {"extra": "allow"}


class CompactRuleSummary(BaseModel):
    """Compact representation of a rule summary."""

    key: str = Field(..., description="Rule key")
    name: str = Field(..., description="Rule name")
    lang: str = Field(..., description="Language key")
    status: str = Field(..., description="Rule status (READY, DEPRECATED, etc.)")

    model_config = {"extra": "allow"}


class IssueListResponse(PaginatedResponse):
    """Response for sonar_list_issues tool."""

    issues: list[dict[str, Any]] = Field(
        default_factory=list,
        description="List of issues (compact by default)",
    )


class IssueDetailResponse(BaseResponse):
    """Response for sonar_get_issue tool."""

    issue: dict[str, Any] | None = Field(
        default=None, description="Issue details (compact by default)"
    )
    components: list[dict[str, Any]] = Field(default_factory=list, description="Related components")
    rules: list[dict[str, Any]] = Field(default_factory=list, description="Related rules")


class TransitionIssueResponse(BaseResponse):
    """Response for sonar_transition_issue tool."""

    issue: dict[str, Any] | None = Field(default=None, description="Updated issue details")


class AddCommentResponse(BaseResponse):
    """Response for sonar_add_comment tool."""

    comment: dict[str, Any] | None = Field(default=None, description="The added comment")


class BulkTransitionResponse(BaseResponse):
    """Response for sonar_bulk_transition tool."""

    total: int = Field(default=0, description="Total issues processed")
    failures: int = Field(default=0, description="Number of failed transitions")
