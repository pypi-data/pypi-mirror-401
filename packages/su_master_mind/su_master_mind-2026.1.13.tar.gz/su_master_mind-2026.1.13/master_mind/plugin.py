"""Plugin interface for master-mind course plugins.

This module defines the base classes that course plugins must implement
to be discovered and integrated into the master-mind CLI.
"""

from abc import ABC, abstractmethod
from typing import Optional
import click


class CoursePlugin(ABC):
    """Base class for course plugins.

    Each course plugin must implement this interface to be discovered
    and integrated into the master-mind CLI.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the course identifier (e.g., 'llm', 'rl', 'deepl').

        This must match the entry point name.
        """
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Return a human-readable description of the course."""
        pass

    @property
    def package_name(self) -> str:
        """Return the package name for installation.

        Default implementation returns 'su_master_mind' with course as extra.
        Plugin packages should override this to return their own package name.
        """
        return "su_master_mind"

    @property
    def package_extra(self) -> Optional[str]:
        """Return the extra name for pip install, if using extras.

        For built-in courses: returns course name (e.g., 'rl')
        For external plugins: returns None (they are standalone packages)
        """
        return self.name

    @property
    def is_builtin(self) -> bool:
        """Return True if this is a built-in course (uses extras on su_master_mind).

        Built-in courses require config file tracking since their entry points
        are always present. External courses are detected by package installation.
        """
        return self.package_extra is not None

    def get_cli_group(self) -> Optional[click.Group]:
        """Return a Click command group for course-specific commands.

        Returns None if no additional CLI commands are provided.
        Example: RL course provides 'master-mind rl stk-race'
        """
        return None

    def download_datasets(self) -> None:
        """Download datasets required for this course.

        Called when user runs 'master-mind download-datasets'.
        Default implementation does nothing.
        """
        pass

    def pre_install_check(self) -> bool:
        """Run pre-flight checks before installing course dependencies.

        Returns True if all checks pass, False otherwise.
        Should log appropriate error messages if checks fail.
        Default implementation returns True (no checks).
        """
        return True


class BuiltinCoursePlugin(CoursePlugin):
    """Base class for built-in courses that use extras on su_master_mind."""

    @property
    def package_name(self) -> str:
        return "su_master_mind"

    @property
    def package_extra(self) -> Optional[str]:
        return self.name


class ExternalCoursePlugin(CoursePlugin):
    """Base class for external course plugins that are separate packages."""

    @property
    def package_extra(self) -> Optional[str]:
        return None

    @property
    @abstractmethod
    def package_name(self) -> str:
        """External plugins must specify their package name."""
        pass
