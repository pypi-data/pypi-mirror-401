"""Quality gate schemas for SonarQube MCP."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from sonar_mcp.schemas.base import BaseResponse


class QualityGateCondition(BaseModel):
    """Quality gate condition result."""

    status: str = Field(..., description="Condition status (OK, WARN, ERROR)")
    metricKey: str = Field(..., description="Metric key")
    comparator: str = Field(..., description="Comparator used (GT, LT, EQ)")
    errorThreshold: str | None = Field(default=None, description="Error threshold value")
    actualValue: str | None = Field(default=None, description="Actual metric value")

    model_config = {"extra": "allow"}


class QualityGateResponse(BaseResponse):
    """Response for sonar_get_quality_gate tool."""

    status: str | None = Field(default=None, description="Quality gate status (OK, WARN, ERROR)")
    conditions: list[QualityGateCondition] = Field(
        default_factory=list, description="Individual condition results"
    )


class GoalFailure(BaseModel):
    """A failed quality goal."""

    metric: str = Field(..., description="Metric name")
    goal: str = Field(..., description="Expected goal value")
    actual: str = Field(..., description="Actual value")

    model_config = {"extra": "forbid"}


class GoalsCheckResponse(BaseResponse):
    """Response for sonar_check_goals tool."""

    passed: bool = Field(default=False, description="Whether all goals are met")
    failed_goals: list[GoalFailure] = Field(default_factory=list, description="Goals that failed")
    metrics: dict[str, Any] = Field(default_factory=dict, description="Current metric values")
