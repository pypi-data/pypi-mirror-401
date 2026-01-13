"""MCP Prompts for SonarQube code quality workflows.

These prompts provide reusable templates for common code quality
tasks like code review, quality reports, security audits, and issue fixing.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sonar_mcp.prompts.code_review import register_code_review_prompts
from sonar_mcp.prompts.quality_report import register_quality_report_prompts
from sonar_mcp.prompts.security_audit import register_security_audit_prompts


if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP

__all__ = [
    "register_code_review_prompts",
    "register_quality_report_prompts",
    "register_security_audit_prompts",
]


def register_all_prompts(mcp: FastMCP) -> None:
    """Register all SonarQube prompts with the MCP server.

    Args:
        mcp: FastMCP server instance.
    """
    register_code_review_prompts(mcp)
    register_quality_report_prompts(mcp)
    register_security_audit_prompts(mcp)
