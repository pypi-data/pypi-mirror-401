from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union

from ..metrics.store import MetricStore


class BaseLoader(ABC):
    """Abstract base class for log file loaders."""

    @abstractmethod
    def load(self, path: Union[str, Path], store: MetricStore) -> None:
        """Load metrics from a file or directory into the store.

        Args:
            path: Path to the log file or directory.
            store: MetricStore to populate with loaded data.
        """
        pass

    @abstractmethod
    def can_load(self, path: Union[str, Path]) -> bool:
        """Check if this loader can handle the given path.

        Args:
            path: Path to check.

        Returns:
            True if this loader can handle the path.
        """
        pass
