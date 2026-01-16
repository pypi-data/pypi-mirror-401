"""Plugin interface for master-mind course plugins.

This module defines the base classes that course plugins must implement
to be discovered and integrated into the master-mind CLI.
"""

from abc import ABC, abstractmethod
from typing import Callable, Dict, List, Optional
import click


class DownloadableResource(ABC):
    """A downloadable resource for a course.

    Each resource represents a dataset, model, or other downloadable artifact
    that can be individually downloaded or listed.
    """

    @property
    @abstractmethod
    def key(self) -> str:
        """Return a unique identifier for this resource within the course."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Return a short description of this resource."""
        pass

    @property
    def optional(self) -> bool:
        """Return True if this resource is optional (not downloaded by default)."""
        return False

    @abstractmethod
    def download(self) -> str:
        """Download the resource.

        Returns:
            A short description of what was downloaded.
        """
        pass


class FunctionalResource(DownloadableResource):
    """A downloadable resource defined by a function.

    Convenience class for creating resources from simple functions.
    """

    def __init__(
        self,
        key: str,
        description: str,
        download_fn: Callable[[], str],
        optional: bool = False,
    ) -> None:
        self._key = key
        self._description = description
        self._download_fn = download_fn
        self._optional = optional

    @property
    def key(self) -> str:
        return self._key

    @property
    def description(self) -> str:
        return self._description

    @property
    def optional(self) -> bool:
        return self._optional

    def download(self) -> str:
        return self._download_fn()


def make_hf_model_resource(
    hf_id: str, description: str, *class_names: str, optional: bool = False
) -> DownloadableResource:
    """Create a downloadable resource for a HuggingFace model.

    Args:
        hf_id: The HuggingFace model identifier (e.g., "bert-base-uncased")
        description: A short description of the model
        *class_names: Names of transformers classes to load (e.g., "AutoTokenizer",
            "AutoModelForCausalLM")
        optional: If True, this resource is optional (not downloaded by default)

    Returns:
        A DownloadableResource that downloads the model when called.
    """

    def download() -> str:
        import transformers

        for class_name in class_names:
            model_class = getattr(transformers, class_name)
            model_class.from_pretrained(hf_id)

        return f"Downloaded {hf_id}"

    return FunctionalResource(
        key=hf_id,
        description=description,
        download_fn=download,
        optional=optional,
    )


def make_hf_dataset_resource(
    dataset_id: str, description: str, split: str = "train", optional: bool = False
) -> DownloadableResource:
    """Create a downloadable resource for a HuggingFace dataset.

    Args:
        dataset_id: The HuggingFace dataset identifier (e.g., "imdb")
        description: A short description of the dataset
        split: The dataset split to download (default: "train")
        optional: If True, this resource is optional (not downloaded by default)

    Returns:
        A DownloadableResource that downloads the dataset when called.
    """

    def download() -> str:
        import datasets

        datasets.load_dataset(dataset_id, split=split)
        return f"Downloaded {dataset_id}"

    return FunctionalResource(
        key=dataset_id,
        description=description,
        download_fn=download,
        optional=optional,
    )


def make_pyterrier_dataset_resource(
    dataset_id: str, description: str, optional: bool = False
) -> DownloadableResource:
    """Create a downloadable resource for a PyTerrier/ir-datasets dataset.

    Args:
        dataset_id: The PyTerrier dataset identifier (e.g., "irds:lotte/technology/dev")
        description: A short description of the dataset
        optional: If True, this resource is optional (not downloaded by default)

    Returns:
        A DownloadableResource that downloads the dataset when called.
    """

    def download() -> str:
        import pyterrier as pt

        pt.get_dataset(dataset_id)
        return f"Downloaded {dataset_id}"

    return FunctionalResource(
        key=dataset_id,
        description=description,
        download_fn=download,
        optional=optional,
    )


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

        Note: New plugins should implement get_downloadable_resources() instead.
        This method is kept for backward compatibility.
        """
        pass

    def get_downloadable_resources(self) -> Dict[str, List[DownloadableResource]]:
        """Return downloadable resources organized by lecture/section.

        Returns:
            A dict mapping lecture/section names to lists of DownloadableResource.
            Return an empty dict to fall back to download_datasets() behavior.

        Example:
            {
                "lecture1": [resource1, resource2],
                "lecture2": [resource3],
            }
        """
        return {}

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
