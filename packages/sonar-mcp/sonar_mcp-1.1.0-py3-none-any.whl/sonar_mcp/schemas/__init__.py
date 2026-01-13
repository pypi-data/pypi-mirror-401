"""Pydantic output schemas for SonarQube MCP tools.

These schemas provide structured output definitions for MCP tools,
enabling better type safety and client validation.
"""

from __future__ import annotations

from sonar_mcp.schemas.instance import (
    InstanceInfo,
    InstanceListResponse,
    InstanceManageResponse,
    SelectInstanceResponse,
    TestConnectionResponse,
)
from sonar_mcp.schemas.issue import (
    AddCommentResponse,
    BulkTransitionResponse,
    CompactIssue,
    IssueDetailResponse,
    IssueListResponse,
    TransitionIssueResponse,
)
from sonar_mcp.schemas.metrics import (
    CoverageDetails,
    CoverageResponse,
    FileCoverageResponse,
    MetricsResponse,
)
from sonar_mcp.schemas.project import (
    DetectProjectResponse,
    ProjectDetailResponse,
    ProjectInfo,
    ProjectListResponse,
)
from sonar_mcp.schemas.quality_gate import (
    GoalFailure,
    GoalsCheckResponse,
    QualityGateCondition,
    QualityGateResponse,
)
from sonar_mcp.schemas.rule import (
    CompactRule,
    RuleDetailResponse,
)


__all__ = [
    "AddCommentResponse",
    "BulkTransitionResponse",
    "CompactIssue",
    "CompactRule",
    "CoverageDetails",
    "CoverageResponse",
    "DetectProjectResponse",
    "FileCoverageResponse",
    "GoalFailure",
    "GoalsCheckResponse",
    "InstanceInfo",
    "InstanceListResponse",
    "InstanceManageResponse",
    "IssueDetailResponse",
    "IssueListResponse",
    "MetricsResponse",
    "ProjectDetailResponse",
    "ProjectInfo",
    "ProjectListResponse",
    "QualityGateCondition",
    "QualityGateResponse",
    "RuleDetailResponse",
    "SelectInstanceResponse",
    "TestConnectionResponse",
    "TransitionIssueResponse",
]
