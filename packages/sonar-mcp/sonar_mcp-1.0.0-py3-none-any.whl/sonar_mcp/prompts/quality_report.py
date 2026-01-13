"""Quality report prompts for SonarQube MCP server."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any


if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP


def register_quality_report_prompts(mcp: FastMCP) -> None:
    """Register quality report prompts with the MCP server."""

    @mcp.prompt(
        name="quality_report",
        description="Generate a comprehensive quality report for a project",
    )
    def quality_report_prompt(project_key: str) -> list[dict[str, Any]]:
        """Generate a quality report prompt for a project.

        Args:
            project_key: The SonarQube project key to report on.

        Returns:
            List of messages for the prompt.
        """
        return [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"""Generate a comprehensive code quality report for '{project_key}'.

Use these SonarQube tools to gather data:
1. sonar_get_quality_gate - Get quality gate status
2. sonar_get_metrics - Get all project metrics
3. sonar_get_coverage - Get detailed coverage information
4. sonar_list_issues - Get issue breakdown by type/severity

Create a report with these sections:

## Executive Summary
- Overall health rating (Green/Yellow/Red)
- Quality gate status and key conditions
- Top 3 areas needing attention

## Metrics Overview
| Metric | Value | Rating |
|--------|-------|--------|
| Coverage | X% | A-E |
| Bugs | N | A-E |
| Vulnerabilities | N | A-E |
| Code Smells | N | A-E |
| Duplications | X% | A-E |

## Issue Breakdown
- Critical/Blocker issues count and summary
- Top 5 most common issues
- Trend analysis if available

## Recommendations
- Prioritized action items
- Quick wins vs long-term improvements
- Suggested sprint goals""",
                },
            }
        ]

    @mcp.prompt(
        name="quality_goals",
        description="Check project against custom quality goals",
    )
    def quality_goals_prompt(
        project_key: str,
        min_coverage: str = "80",
        max_bugs: str = "0",
        max_vulnerabilities: str = "0",
    ) -> list[dict[str, Any]]:
        """Generate a prompt to check quality goals.

        Args:
            project_key: The SonarQube project key.
            min_coverage: Minimum required coverage percentage.
            max_bugs: Maximum allowed bugs.
            max_vulnerabilities: Maximum allowed vulnerabilities.

        Returns:
            List of messages for the prompt.
        """
        return [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"""Check if project '{project_key}' meets these quality goals:

- Minimum Coverage: {min_coverage}%
- Maximum Bugs: {max_bugs}
- Maximum Vulnerabilities: {max_vulnerabilities}
- Minimum Maintainability Rating: A
- Minimum Reliability Rating: A
- Minimum Security Rating: A

Use sonar_check_goals with these parameters and report:
1. Which goals are met vs. not met
2. Current values for each metric
3. Gap analysis for failed goals
4. Specific recommendations to meet each failed goal""",
                },
            }
        ]
