"""
Common utilities for runtime dependency management.
"""

import platform
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class RuntimeDependency:
    """
    Represents a runtime dependency (e.g., language server binary, .NET runtime).
    """
    id: str
    description: str
    platform_id: str
    archive_type: str
    binary_name: str
    package_name: Optional[str] = None
    package_version: Optional[str] = None
    url: Optional[str] = None
    extract_path: Optional[str] = None


class RuntimeDependencyCollection:
    """
    Manages a collection of runtime dependencies with platform-specific resolution
    and override support.
    """

    def __init__(self, dependencies: list[RuntimeDependency], overrides: list[dict[str, Any]] | None = None):
        """
        Initialize the collection with base dependencies and optional overrides.

        Args:
            dependencies: List of RuntimeDependency objects
            overrides: Optional list of dicts containing override values. Each dict must
                      contain at least 'id' and optionally 'platform_id' to identify which
                      dependency to override.
        """
        self.dependencies = list(dependencies)
        self.overrides = overrides or []

        # Apply overrides
        for override in self.overrides:
            self._apply_override(override)

    def _apply_override(self, override: dict[str, Any]) -> None:
        """Apply an override to matching dependencies."""
        override_id = override.get("id")
        override_platform = override.get("platform_id")

        if not override_id:
            return

        for dep in self.dependencies:
            # Match by id and optionally platform_id
            if dep.id == override_id:
                if override_platform is None or dep.platform_id == override_platform:
                    # Apply all override fields
                    for key, value in override.items():
                        if hasattr(dep, key) and key not in ["id"]:  # Don't override id
                            setattr(dep, key, value)

    @property
    def get_dependencies_for_current_platform(self) -> list[RuntimeDependency]:
        """Get all dependencies for the current platform."""
        current_platform = self._get_current_platform_id()
        return [dep for dep in self.dependencies if dep.platform_id == current_platform]

    def get_single_dep_for_current_platform(self, dep_id: str) -> RuntimeDependency:
        """
        Get a single dependency by ID for the current platform.

        Args:
            dep_id: The ID of the dependency to retrieve

        Returns:
            The matching RuntimeDependency

        Raises:
            ValueError: If no matching dependency is found or multiple matches exist
        """
        current_platform = self._get_current_platform_id()
        matches = [
            dep for dep in self.dependencies
            if dep.id == dep_id and dep.platform_id == current_platform
        ]

        if not matches:
            raise ValueError(
                f"No dependency found with id='{dep_id}' for platform '{current_platform}'"
            )
        if len(matches) > 1:
            raise ValueError(
                f"Multiple dependencies found with id='{dep_id}' for platform '{current_platform}'"
            )

        return matches[0]

    @staticmethod
    def _get_current_platform_id() -> str:
        """
        Determine the current platform ID in .NET RID format.

        Returns:
            Platform ID string (e.g., 'linux-x64', 'win-x64', 'osx-arm64')

        Raises:
            RuntimeError: If platform is not supported
        """
        system = platform.system().lower()
        machine = platform.machine().lower()

        if system == "linux":
            if machine in ["x86_64", "amd64"]:
                return "linux-x64"
            elif machine in ["aarch64", "arm64"]:
                return "linux-arm64"
        elif system == "darwin":
            if machine == "x86_64":
                return "osx-x64"
            elif machine in ["arm64", "aarch64"]:
                return "osx-arm64"
        elif system == "windows":
            if machine in ["amd64", "x86_64"]:
                return "win-x64"
            elif machine in ["arm64", "aarch64"]:
                return "win-arm64"

        raise RuntimeError(f"Unsupported platform: {system}/{machine}")
