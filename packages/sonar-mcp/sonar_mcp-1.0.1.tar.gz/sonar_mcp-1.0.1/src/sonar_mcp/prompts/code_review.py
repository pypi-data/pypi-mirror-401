"""Code review prompts for SonarQube MCP server."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any


if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP


def register_code_review_prompts(mcp: FastMCP) -> None:
    """Register code review prompts with the MCP server."""

    @mcp.prompt(
        name="code_review",
        description="Review code issues from SonarQube and suggest fixes",
    )
    def code_review_prompt(
        project_key: str,
        severity_filter: str = "CRITICAL,BLOCKER",
    ) -> list[dict[str, Any]]:
        """Generate a code review prompt based on SonarQube issues.

        Args:
            project_key: The SonarQube project key to review.
            severity_filter: Comma-separated severity levels to include.

        Returns:
            List of messages for the prompt.
        """
        return [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"""Please review the code quality issues for project '{project_key}'.

Focus on issues with severity: {severity_filter}

For each issue found:
1. Explain what the issue is and why it matters
2. Show the affected code location
3. Provide a specific fix recommendation
4. Rate the priority (High/Medium/Low)

Use the sonar_list_issues tool to fetch issues with:
- project_key: {project_key}
- severities: [{severity_filter}]

Then analyze each issue and provide actionable remediation guidance.""",
                },
            }
        ]

    @mcp.prompt(
        name="fix_issues",
        description="Generate fix recommendations for specific SonarQube issue types",
    )
    def fix_issues_prompt(
        project_key: str,
        issue_type: str = "BUG",
    ) -> list[dict[str, Any]]:
        """Generate a prompt to fix specific types of issues.

        Args:
            project_key: The SonarQube project key.
            issue_type: Issue type to focus on (BUG, VULNERABILITY, CODE_SMELL).

        Returns:
            List of messages for the prompt.
        """
        type_descriptions = {
            "BUG": "bugs that may cause runtime errors or incorrect behavior",
            "VULNERABILITY": "security vulnerabilities that could be exploited",
            "CODE_SMELL": "code smells that affect maintainability",
        }
        description = type_descriptions.get(issue_type.upper(), "issues affecting code quality")

        return [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"""Help fix {description} in project '{project_key}'.

Use the sonar_list_issues tool to fetch issues:
- project_key: {project_key}
- types: [{issue_type}]

For each {issue_type} found:
1. Read the affected file using appropriate tools
2. Understand the context around the issue
3. Generate a specific code fix
4. Explain the fix and how it resolves the issue

Prioritize issues by severity (BLOCKER > CRITICAL > MAJOR > MINOR > INFO).""",
                },
            }
        ]
