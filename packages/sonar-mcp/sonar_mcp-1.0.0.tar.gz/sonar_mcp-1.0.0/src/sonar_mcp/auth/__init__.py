"""Authentication module for SonarQube MCP server."""

from __future__ import annotations

from sonar_mcp.auth.manager import AuthenticationError, AuthManager


__all__: list[str] = ["AuthManager", "AuthenticationError"]
