"""Authentication manager for SonarQube MCP server."""

from __future__ import annotations

import os


class AuthenticationError(Exception):
    """Raised when authentication configuration is missing or invalid."""


class AuthManager:
    """Manages authentication for SonarQube API access.

    This manager retrieves authentication credentials from environment variables.
    It supports multiple environment variable names for flexibility with different
    CI/CD systems and deployment configurations.

    Environment Variables:
        Token (checked in order):
            - SONAR_TOKEN
            - SONARQUBE_TOKEN

        URL (checked in order):
            - SONAR_URL
            - SONARQUBE_URL
            - SONAR_HOST_URL (GitLab CI convention)

        Organization (optional):
            - SONAR_ORGANIZATION
            - SONARQUBE_ORGANIZATION
    """

    # Token environment variable names in priority order
    TOKEN_ENV_VARS = ("SONAR_TOKEN", "SONARQUBE_TOKEN")

    # URL environment variable names in priority order
    URL_ENV_VARS = ("SONAR_URL", "SONARQUBE_URL", "SONAR_HOST_URL")

    # Organization environment variable names in priority order
    ORG_ENV_VARS = ("SONAR_ORGANIZATION", "SONARQUBE_ORGANIZATION")

    def get_token(self) -> str:
        """Get the SonarQube API token from environment.

        Returns:
            The API token string.

        Raises:
            AuthenticationError: If no token is found in environment.
        """
        for env_var in self.TOKEN_ENV_VARS:
            token = os.environ.get(env_var)
            if token:
                return token

        msg = f"SonarQube token not found. Set one of: {', '.join(self.TOKEN_ENV_VARS)}"
        raise AuthenticationError(msg)

    def get_url(self) -> str:
        """Get the SonarQube server URL from environment.

        Returns:
            The server URL string (trailing slash removed).

        Raises:
            AuthenticationError: If no URL is found in environment.
        """
        for env_var in self.URL_ENV_VARS:
            url = os.environ.get(env_var)
            if url:
                return url.rstrip("/")

        msg = f"SonarQube URL not found. Set one of: {', '.join(self.URL_ENV_VARS)}"
        raise AuthenticationError(msg)

    def get_organization(self) -> str | None:
        """Get the SonarQube/SonarCloud organization from environment.

        Returns:
            The organization key or None if not set.
        """
        for env_var in self.ORG_ENV_VARS:
            org = os.environ.get(env_var)
            if org:
                return org
        return None

    def is_configured(self) -> bool:
        """Check if authentication is properly configured.

        Returns:
            True if both token and URL are available, False otherwise.
        """
        try:
            self.get_token()
            self.get_url()
            return True
        except AuthenticationError:
            return False

    def validate(self) -> None:
        """Validate that authentication is properly configured.

        Raises:
            AuthenticationError: If configuration is incomplete.
        """
        errors: list[str] = []

        try:
            self.get_token()
        except AuthenticationError as e:
            errors.append(str(e))

        try:
            self.get_url()
        except AuthenticationError as e:
            errors.append(str(e))

        if errors:
            msg = "Authentication configuration incomplete: " + "; ".join(errors)
            raise AuthenticationError(msg)

    def get_auth_headers(self) -> dict[str, str]:
        """Get HTTP headers for authenticated API requests.

        Returns:
            Dictionary of HTTP headers including Authorization.

        Raises:
            AuthenticationError: If token is not available.
        """
        token = self.get_token()
        return {"Authorization": f"Bearer {token}"}
