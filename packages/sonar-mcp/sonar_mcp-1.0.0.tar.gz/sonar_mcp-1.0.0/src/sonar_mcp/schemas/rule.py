"""Rule schemas for SonarQube MCP."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from sonar_mcp.schemas.base import BaseResponse


class CompactRule(BaseModel):
    """Compact representation of a SonarQube rule.

    Contains only essential fields for LLM consumption.
    """

    key: str = Field(..., description="Rule key (e.g., 'python:S1234')")
    name: str = Field(..., description="Rule name")
    severity: str = Field(..., description="Rule severity (BLOCKER, CRITICAL, MAJOR, MINOR, INFO)")
    status: str = Field(..., description="Rule status (READY, DEPRECATED, BETA)")
    type: str = Field(..., description="Rule type (BUG, VULNERABILITY, CODE_SMELL)")
    lang: str = Field(..., description="Language key")
    langName: str = Field(..., description="Language name")
    tags: list[str] = Field(default_factory=list, description="User-defined tags")
    sysTags: list[str] = Field(default_factory=list, description="System tags")

    model_config = {"extra": "allow"}


class RuleDetailResponse(BaseResponse):
    """Response for sonar_get_rule tool."""

    rule: dict[str, Any] | None = Field(
        default=None, description="Rule details (compact by default)"
    )
    actives: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Quality profiles with this rule active (if requested)",
    )
