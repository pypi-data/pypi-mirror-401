"""Configuration models for SonarQube MCP server."""

from __future__ import annotations

import re
from typing import Self

from pydantic import (
    BaseModel,
    Field,
    SecretStr,
    field_validator,
    model_validator,
)


class SonarInstance(BaseModel):
    """Configuration for a single SonarQube instance.

    Attributes:
        name: Unique identifier for this instance (alphanumeric and dashes only).
        url: Base URL of the SonarQube server.
        token: API token for authentication (stored securely).
        organization: Organization key for SonarCloud (optional).
        default: Whether this is the default instance.
        verify_ssl: Whether to verify SSL certificates.
        timeout: Request timeout in seconds.
    """

    name: str = Field(..., description="Unique instance identifier")
    url: str = Field(..., description="SonarQube server URL")
    token: SecretStr = Field(..., description="API authentication token")
    organization: str | None = Field(default=None, description="Organization key")
    default: bool = Field(default=False, description="Is default instance")
    verify_ssl: bool = Field(default=True, description="Verify SSL certificates")
    timeout: float = Field(default=30.0, gt=0, description="Request timeout seconds")

    model_config = {"frozen": True}

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate that name contains only alphanumeric characters and dashes."""
        if not re.match(r"^[a-zA-Z0-9-]+$", v):
            msg = "Name must contain only alphanumeric characters and dashes"
            raise ValueError(msg)
        return v

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        """Validate and normalize URL."""
        # Strip trailing slash
        v = v.rstrip("/")

        # Check for valid scheme
        if not v.startswith(("http://", "https://")):
            msg = "URL must start with http:// or https://"
            raise ValueError(msg)

        return v


class SonarConfig(BaseModel):
    """Configuration containing multiple SonarQube instances.

    Attributes:
        instances: List of configured SonarQube instances.
        default_instance: Name of the default instance to use.
    """

    instances: list[SonarInstance] = Field(default_factory=list, description="Configured instances")
    default_instance: str | None = Field(default=None, description="Default instance name")

    model_config = {"frozen": True}

    @model_validator(mode="after")
    def validate_config(self) -> Self:
        """Validate configuration consistency."""
        # Check for unique instance names
        names = [inst.name for inst in self.instances]
        if len(names) != len(set(names)):
            msg = "Instance names must be unique"
            raise ValueError(msg)

        # If default_instance is set, verify it exists
        if self.default_instance is not None and self.default_instance not in names:
            msg = f"default_instance '{self.default_instance}' not found in instances"
            raise ValueError(msg)

        # Auto-detect default from instances if not explicitly set
        if self.default_instance is None:
            for inst in self.instances:
                if inst.default:
                    # Use object.__setattr__ to bypass frozen model
                    object.__setattr__(self, "default_instance", inst.name)
                    break

        return self

    def get_instance(self, name: str) -> SonarInstance | None:
        """Get an instance by name.

        Args:
            name: Instance name to look up.

        Returns:
            The instance if found, None otherwise.
        """
        for instance in self.instances:
            if instance.name == name:
                return instance
        return None

    def get_default_instance(self) -> SonarInstance | None:
        """Get the default instance.

        Returns the instance marked as default, or the first instance if no
        default is set, or None if there are no instances.

        Returns:
            The default instance or None.
        """
        if not self.instances:
            return None

        if self.default_instance:
            return self.get_instance(self.default_instance)

        # Return first instance if no default set
        return self.instances[0]

    def add_instance(self, instance: SonarInstance) -> SonarConfig:
        """Add an instance to the configuration.

        Creates a new config with the added instance (immutable operation).

        Args:
            instance: The instance to add.

        Returns:
            New SonarConfig with the added instance.
        """
        new_instances = [*self.instances, instance]
        return SonarConfig(
            instances=new_instances,
            default_instance=self.default_instance,
        )

    def remove_instance(self, name: str) -> SonarConfig:
        """Remove an instance from the configuration.

        Creates a new config without the specified instance (immutable operation).

        Args:
            name: Name of the instance to remove.

        Returns:
            New SonarConfig without the specified instance.
        """
        new_instances = [inst for inst in self.instances if inst.name != name]
        new_default = self.default_instance if self.default_instance != name else None
        return SonarConfig(
            instances=new_instances,
            default_instance=new_default,
        )

    @property
    def instance_names(self) -> list[str]:
        """Get list of all instance names.

        Returns:
            List of instance names.
        """
        return [inst.name for inst in self.instances]
