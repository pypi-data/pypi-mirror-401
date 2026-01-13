"""Quality gate tools for SonarQube MCP server."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from mcp.server.fastmcp import Context, FastMCP
from mcp.types import ToolAnnotations

from sonar_mcp.client.sonar_client import SonarAPIError
from sonar_mcp.context import (
    ServerContext,  # noqa: TC001 - Required at runtime for MCP introspection
)
from sonar_mcp.instance_manager import NoActiveInstanceError
from sonar_mcp.tools.client_helper import create_sonar_client, get_server_context


# Rating mappings (SonarQube uses 1.0-5.0 internally for A-E)
RATING_VALUES = {"A": 1.0, "B": 2.0, "C": 3.0, "D": 4.0, "E": 5.0}


@dataclass
class GoalCheck:
    """Configuration for a goal check."""

    metric_key: str
    goal_value: float | int | str | None
    is_max: bool  # True for max thresholds, False for min thresholds
    is_rating: bool = False
    display_name: str | None = None


def _make_failure_entry(check: GoalCheck, goal_str: str, actual_str: str) -> dict[str, str]:
    """Create a failure entry for a goal check."""
    return {
        "metric": check.display_name or check.metric_key,
        "goal": goal_str,
        "actual": actual_str,
    }


def _check_max_int_goal(
    metric_str: str | None, check: GoalCheck, failed_goals: list[dict[str, str]]
) -> None:
    """Check a maximum integer goal (bugs, vulnerabilities, code_smells)."""
    actual = int(metric_str) if metric_str else 0
    if actual > int(check.goal_value):  # type: ignore[arg-type]
        failed_goals.append(_make_failure_entry(check, f"<= {check.goal_value}", str(actual)))


def _check_max_float_goal(
    metric_str: str | None, check: GoalCheck, failed_goals: list[dict[str, str]]
) -> None:
    """Check a maximum float goal (duplicated_lines_density)."""
    actual = float(metric_str) if metric_str else 0.0
    if actual > float(check.goal_value):  # type: ignore[arg-type]
        failed_goals.append(_make_failure_entry(check, f"<= {check.goal_value}%", f"{actual}%"))


def _check_min_float_goal(
    metric_str: str | None, check: GoalCheck, failed_goals: list[dict[str, str]]
) -> None:
    """Check a minimum float goal (coverage)."""
    actual = float(metric_str) if metric_str else 0.0
    if actual < float(check.goal_value):  # type: ignore[arg-type]
        failed_goals.append(_make_failure_entry(check, f">= {check.goal_value}%", f"{actual}%"))


def _check_numeric_goal(
    metrics: dict[str, str | None],
    check: GoalCheck,
    failed_goals: list[dict[str, str]],
) -> None:
    """Check a numeric goal (coverage, bugs, etc.)."""
    if check.goal_value is None:
        return

    metric_str = metrics.get(check.metric_key)

    if check.is_max and isinstance(check.goal_value, int):
        _check_max_int_goal(metric_str, check, failed_goals)
    elif check.is_max and isinstance(check.goal_value, float):
        _check_max_float_goal(metric_str, check, failed_goals)
    elif isinstance(check.goal_value, float):
        _check_min_float_goal(metric_str, check, failed_goals)


def _rating_to_letter(rating: float) -> str:
    """Convert numeric rating to letter grade."""
    if rating <= 1.0:
        return "A"
    if rating <= 2.0:
        return "B"
    if rating <= 3.0:
        return "C"
    if rating <= 4.0:
        return "D"
    return "E"


def _check_rating_goal(
    metrics: dict[str, str | None],
    check: GoalCheck,
    failed_goals: list[dict[str, str]],
) -> None:
    """Check a rating goal (A-E scale)."""
    if check.goal_value is None:
        return

    rating_str = metrics.get(check.metric_key)
    rating = float(rating_str) if rating_str else 5.0
    target = RATING_VALUES.get(str(check.goal_value).upper(), 5.0)

    if rating > target:
        actual_letter = _rating_to_letter(rating)
        failed_goals.append(
            {
                "metric": check.display_name or check.metric_key,
                "goal": f">= {check.goal_value}",
                "actual": actual_letter,
            }
        )


async def sonar_get_quality_gate(
    ctx: Context[Any, ServerContext],
    project_key: str,
) -> dict[str, Any]:
    """Get quality gate status for a SonarQube project.

    Args:
        ctx: MCP context.
        project_key: Project key to get quality gate for.

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - status: str - Quality gate status (OK, WARN, ERROR)
        - conditions: list - Individual condition results
        - error: str - Error message (if success is False)
    """
    server_ctx = get_server_context(ctx)

    try:
        instance = server_ctx.instance_manager.get_active_instance()
    except NoActiveInstanceError:
        return {
            "success": False,
            "error": "No active instance configured.",
        }

    client = create_sonar_client(instance)

    try:
        async with client:
            response = await client.get(
                "/api/qualitygates/project_status",
                params={"projectKey": project_key},
            )

        project_status = response.get("projectStatus", {})

        return {
            "success": True,
            "status": project_status.get("status", "UNKNOWN"),
            "conditions": project_status.get("conditions", []),
        }
    except SonarAPIError as e:
        return {
            "success": False,
            "error": str(e),
        }


async def sonar_check_goals(
    ctx: Context[Any, ServerContext],
    project_key: str,
    min_coverage: float | None = None,
    max_bugs: int | None = None,
    max_vulnerabilities: int | None = None,
    max_code_smells: int | None = None,
    max_duplicated_lines_density: float | None = None,
    min_maintainability_rating: str | None = None,
    min_reliability_rating: str | None = None,
    min_security_rating: str | None = None,
    task_mode: bool = False,
) -> dict[str, Any]:
    """Check if a project meets custom quality goals.

    This tool allows checking custom quality goals that may differ from
    the configured quality gate. Ratings should be specified as A, B, C, D, or E.

    Args:
        ctx: MCP context.
        project_key: Project key to check.
        min_coverage: Minimum code coverage percentage (0-100).
        max_bugs: Maximum allowed bugs.
        max_vulnerabilities: Maximum allowed vulnerabilities.
        max_code_smells: Maximum allowed code smells.
        max_duplicated_lines_density: Maximum duplication percentage (0-100).
        min_maintainability_rating: Minimum maintainability rating (A-E).
        min_reliability_rating: Minimum reliability rating (A-E).
        min_security_rating: Minimum security rating (A-E).
        task_mode: If True, run in background and return task_id immediately.
                   Use sonar_get_task to check progress. Default: False.

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - passed: bool - Whether all goals are met (sync mode)
        - failed_goals: list - Goals that failed (sync mode)
        - metrics: dict - Current metric values (sync mode)
        - task_id: str - Task ID for tracking (task_mode only)
        - state: str - Initial task state (task_mode only)
        - message: str - Status message (task_mode only)
        - error: str - Error message (if success is False)
    """
    server_ctx = get_server_context(ctx)

    # Define all goal checks
    numeric_checks = [
        GoalCheck("coverage", min_coverage, is_max=False),
        GoalCheck("bugs", max_bugs, is_max=True),
        GoalCheck("vulnerabilities", max_vulnerabilities, is_max=True),
        GoalCheck("code_smells", max_code_smells, is_max=True),
        GoalCheck("duplicated_lines_density", max_duplicated_lines_density, is_max=True),
    ]

    rating_checks = [
        GoalCheck(
            "sqale_rating",
            min_maintainability_rating,
            is_max=False,
            is_rating=True,
            display_name="maintainability_rating",
        ),
        GoalCheck("reliability_rating", min_reliability_rating, is_max=False, is_rating=True),
        GoalCheck("security_rating", min_security_rating, is_max=False, is_rating=True),
    ]

    # Check if any goals are specified
    all_checks = numeric_checks + rating_checks
    if all(check.goal_value is None for check in all_checks):
        return {
            "success": False,
            "error": "No goals specified. Provide at least one goal to check.",
        }

    try:
        instance = server_ctx.instance_manager.get_active_instance()
    except NoActiveInstanceError:
        return {
            "success": False,
            "error": "No active instance configured.",
        }

    metric_keys = [
        "coverage",
        "bugs",
        "vulnerabilities",
        "code_smells",
        "duplicated_lines_density",
        "sqale_rating",
        "reliability_rating",
        "security_rating",
    ]

    # Task mode: run in background and return immediately
    if task_mode:
        task_manager = server_ctx.task_manager
        if not task_manager:
            return {
                "success": False,
                "error": "Task manager not available.",
            }

        async def _check_goals_operation() -> dict[str, Any]:
            """Execute goals check in background."""
            client = create_sonar_client(instance)

            async with client:
                response = await client.get(
                    "/api/measures/component",
                    params={
                        "component": project_key,
                        "metricKeys": ",".join(metric_keys),
                    },
                )

            measures = response.get("component", {}).get("measures", [])
            metrics = {m["metric"]: m.get("value") for m in measures}

            failed_goals: list[dict[str, str]] = []

            # Check all numeric goals
            for check in numeric_checks:
                _check_numeric_goal(metrics, check, failed_goals)

            # Check all rating goals
            for check in rating_checks:
                _check_rating_goal(metrics, check, failed_goals)

            return {
                "success": True,
                "passed": len(failed_goals) == 0,
                "failed_goals": failed_goals,
                "metrics": metrics,
            }

        task_info = await task_manager.create_task("check_goals", _check_goals_operation)
        return {
            "success": True,
            "task_id": task_info.task_id,
            "state": task_info.state.value,
            "message": f"Goals check started for {project_key}",
        }

    # Synchronous mode: execute and wait for result
    client = create_sonar_client(instance)

    try:
        async with client:
            response = await client.get(
                "/api/measures/component",
                params={
                    "component": project_key,
                    "metricKeys": ",".join(metric_keys),
                },
            )

        measures = response.get("component", {}).get("measures", [])
        metrics = {m["metric"]: m.get("value") for m in measures}

        failed_goals: list[dict[str, str]] = []

        # Check all numeric goals
        for check in numeric_checks:
            _check_numeric_goal(metrics, check, failed_goals)

        # Check all rating goals
        for check in rating_checks:
            _check_rating_goal(metrics, check, failed_goals)

        return {
            "success": True,
            "passed": len(failed_goals) == 0,
            "failed_goals": failed_goals,
            "metrics": metrics,
        }
    except SonarAPIError as e:
        return {
            "success": False,
            "error": str(e),
        }


def register_quality_gate_tools(mcp: FastMCP) -> None:
    """Register quality gate tools with the MCP server."""
    # Both quality gate tools are read-only and idempotent
    mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))(
        sonar_get_quality_gate
    )

    mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))(sonar_check_goals)
