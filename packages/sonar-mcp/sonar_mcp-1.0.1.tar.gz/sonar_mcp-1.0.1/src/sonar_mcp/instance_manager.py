"""Instance manager for SonarQube MCP server."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from pydantic import SecretStr

from sonar_mcp.auth.manager import AuthManager
from sonar_mcp.client.sonar_client import SonarClient
from sonar_mcp.config.models import SonarConfig, SonarInstance


if TYPE_CHECKING:
    from collections.abc import AsyncIterator


class InstanceNotFoundError(Exception):
    """Raised when a requested instance is not found."""

    def __init__(self, name: str) -> None:
        """Initialize error with instance name.

        Args:
            name: Name of the instance that was not found.
        """
        super().__init__(f"Instance '{name}' not found")
        self.name = name


class NoActiveInstanceError(Exception):
    """Raised when no active instance is configured."""

    def __init__(self) -> None:
        """Initialize error."""
        super().__init__("No active instance configured")


class InstanceManager:
    """Manages multiple SonarQube instance configurations.

    This manager handles:
    - Loading default instance from environment variables
    - Adding/removing instances dynamically
    - Selecting the active instance
    - Creating clients for API access

    Example:
        >>> manager = InstanceManager()
        >>> async with manager.get_client() as client:
        ...     result = await client.get("/api/server/version")
    """

    def __init__(self) -> None:
        """Initialize the instance manager.

        Attempts to load a default instance from environment variables.
        """
        self._config = SonarConfig()
        self._active_instance: str | None = None
        self._auth_manager = AuthManager()

        # Try to load default instance from environment
        self._load_env_instance()

    def _load_env_instance(self) -> None:
        """Load default instance from environment variables."""
        if not self._auth_manager.is_configured():
            return

        try:
            instance = SonarInstance(
                name="default",
                url=self._auth_manager.get_url(),
                token=SecretStr(self._auth_manager.get_token()),
                organization=self._auth_manager.get_organization(),
                default=True,
            )
            self._config = self._config.add_instance(instance)
            self._active_instance = "default"
        except (ValueError, OSError):
            # If we can't create the instance (validation error or env issue),
            # continue without it - the user can add instances manually
            pass

    def add_instance(self, instance: SonarInstance) -> None:
        """Add a new instance.

        Args:
            instance: The instance to add.

        Raises:
            ValueError: If instance name already exists.
        """
        if self.has_instance(instance.name):
            msg = f"Instance '{instance.name}' already exists"
            raise ValueError(msg)

        self._config = self._config.add_instance(instance)

        # If this is the first instance, make it active
        if self._active_instance is None:
            self._active_instance = instance.name

    def remove_instance(self, name: str) -> None:
        """Remove an instance.

        Args:
            name: Name of the instance to remove.
        """
        self._config = self._config.remove_instance(name)

        # If we removed the active instance, select a new one
        if self._active_instance == name:
            instances = self.list_instances()
            self._active_instance = instances[0].name if instances else None

    def select_instance(self, name: str) -> None:
        """Select an instance as active.

        Args:
            name: Name of the instance to select.

        Raises:
            InstanceNotFoundError: If instance does not exist.
        """
        if not self.has_instance(name):
            raise InstanceNotFoundError(name)

        self._active_instance = name

    def get_instance(self, name: str) -> SonarInstance | None:
        """Get an instance by name.

        Args:
            name: Name of the instance.

        Returns:
            The instance or None if not found.
        """
        return self._config.get_instance(name)

    def has_instance(self, name: str) -> bool:
        """Check if an instance exists.

        Args:
            name: Name of the instance.

        Returns:
            True if instance exists, False otherwise.
        """
        return self._config.get_instance(name) is not None

    def list_instances(self) -> list[SonarInstance]:
        """List all configured instances.

        Returns:
            List of all instances.
        """
        return list(self._config.instances)

    def get_active_instance(self) -> SonarInstance:
        """Get the currently active instance.

        Returns:
            The active instance.

        Raises:
            NoActiveInstanceError: If no active instance is configured.
        """
        if self._active_instance is None:
            raise NoActiveInstanceError()

        instance = self._config.get_instance(self._active_instance)
        if instance is None:
            raise NoActiveInstanceError()

        return instance

    @property
    def active_instance_name(self) -> str | None:
        """Get the name of the active instance.

        Returns:
            The active instance name or None.
        """
        return self._active_instance

    @asynccontextmanager
    async def get_client(self, instance_name: str | None = None) -> AsyncIterator[SonarClient]:
        """Get a client for an instance.

        Args:
            instance_name: Name of the instance to use, or None for active.

        Yields:
            A SonarClient for the instance.

        Raises:
            InstanceNotFoundError: If specified instance does not exist.
            NoActiveInstanceError: If no instance is specified and no active instance.
        """
        if instance_name is not None:
            instance = self.get_instance(instance_name)
            if instance is None:
                raise InstanceNotFoundError(instance_name)
        else:
            instance = self.get_active_instance()

        client = SonarClient(
            base_url=instance.url,
            token=instance.token.get_secret_value(),
            organization=instance.organization,
            timeout=instance.timeout,
            verify_ssl=instance.verify_ssl,
        )

        async with client:
            yield client
