"""Security audit prompts for SonarQube MCP server."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any


if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP


def register_security_audit_prompts(mcp: FastMCP) -> None:
    """Register security audit prompts with the MCP server."""

    @mcp.prompt(
        name="security_audit",
        description="Perform a security-focused audit of a project",
    )
    def security_audit_prompt(project_key: str) -> list[dict[str, Any]]:
        """Generate a security audit prompt for a project.

        Args:
            project_key: The SonarQube project key to audit.

        Returns:
            List of messages for the prompt.
        """
        return [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"""Perform a security audit for project '{project_key}'.

## Data Collection
Use these tools to gather security-related data:
1. sonar_list_issues with types=["VULNERABILITY"]
2. sonar_get_metrics for security_rating
3. sonar_get_quality_gate for security conditions

## Audit Report Structure

### Security Rating
- Current rating (A-E)
- Trend (improving/stable/declining)

### Vulnerability Analysis
For each vulnerability:
- CWE/OWASP category
- Severity and impact
- Affected code location
- Exploitation potential

### Risk Assessment
Categorize findings:
- **Critical**: Immediate action required
- **High**: Address within sprint
- **Medium**: Plan for upcoming release
- **Low**: Track and monitor

### Remediation Plan
For each vulnerability provide:
1. Detailed fix recommendation
2. Code example if applicable
3. Testing requirements
4. Verification steps

### Security Hardening Suggestions
- Best practices not currently implemented
- Configuration improvements
- Dependency updates needed""",
                },
            }
        ]

    @mcp.prompt(
        name="vulnerability_fix",
        description="Get detailed fix guidance for specific vulnerabilities",
    )
    def vulnerability_fix_prompt(
        project_key: str,
        severity: str = "CRITICAL,BLOCKER",
    ) -> list[dict[str, Any]]:
        """Generate a prompt to fix vulnerabilities.

        Args:
            project_key: The SonarQube project key.
            severity: Severity filter for vulnerabilities.

        Returns:
            List of messages for the prompt.
        """
        return [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"""Fix security vulnerabilities in '{project_key}'.

Use sonar_list_issues to get vulnerabilities:
- project_key: {project_key}
- types: [VULNERABILITY]
- severities: [{severity}]

For each vulnerability:

1. **Understanding the Issue**
   - Use sonar_get_rule to understand the vulnerability type
   - Identify the CWE/OWASP category
   - Explain the attack vector

2. **Impact Assessment**
   - What could an attacker do?
   - What data is at risk?
   - What is the blast radius?

3. **Fix Implementation**
   - Provide specific code fix
   - Show before/after code
   - Explain why the fix works

4. **Verification**
   - How to test the fix
   - Automated test suggestions
   - Security testing approach

Prioritize by severity and potential impact.""",
                },
            }
        ]
