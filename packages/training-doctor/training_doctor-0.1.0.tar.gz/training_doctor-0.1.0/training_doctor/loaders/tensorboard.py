from pathlib import Path
from typing import Union, List, Optional

from .base import BaseLoader
from ..metrics.store import MetricStore


class TensorBoardLoader(BaseLoader):
    """Loader for TensorBoard event files."""

    def can_load(self, path: Union[str, Path]) -> bool:
        """Check if path contains TensorBoard event files."""
        path = Path(path)
        if path.is_file() and "events.out.tfevents" in path.name:
            return True
        if path.is_dir():
            return any(path.glob("**/events.out.tfevents.*"))
        return False

    def load(self, path: Union[str, Path], store: MetricStore) -> None:
        """Load metrics from TensorBoard event files."""
        path = Path(path)

        # Try importing tensorboard
        try:
            from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
        except ImportError:
            raise ImportError(
                "TensorBoard is required to load TensorBoard logs. "
                "Install it with: pip install tensorboard"
            )

        event_files = self._find_event_files(path)
        if not event_files:
            raise ValueError(f"No TensorBoard event files found in: {path}")

        for event_file in event_files:
            self._load_event_file(event_file, store)

    def _find_event_files(self, path: Path) -> List[Path]:
        """Find all event files in a path."""
        if path.is_file():
            return [path]

        # Recursively find all event files
        return list(path.glob("**/events.out.tfevents.*"))

    def _load_event_file(self, path: Path, store: MetricStore) -> None:
        """Load metrics from a single event file."""
        from tensorboard.backend.event_processing.event_accumulator import EventAccumulator

        # Load the event file
        ea = EventAccumulator(str(path))
        ea.Reload()

        # Get all scalar tags
        scalar_tags = ea.Tags().get("scalars", [])

        for tag in scalar_tags:
            events = ea.Scalars(tag)
            for event in events:
                # Clean up tag name
                clean_tag = tag.replace("/", "_").replace(".", "_")
                store.log(event.step, **{clean_tag: event.value})


class TensorBoardLoaderNoTB(BaseLoader):
    """Fallback TensorBoard loader that parses event files without tensorboard package."""

    def can_load(self, path: Union[str, Path]) -> bool:
        """Check if path contains TensorBoard event files."""
        path = Path(path)
        if path.is_file() and "events.out.tfevents" in path.name:
            return True
        if path.is_dir():
            return any(path.glob("**/events.out.tfevents.*"))
        return False

    def load(self, path: Union[str, Path], store: MetricStore) -> None:
        """Load metrics from TensorBoard event files without tensorboard package.

        This is a basic implementation that reads the protobuf format directly.
        For full support, install tensorboard.
        """
        path = Path(path)

        # Try the full tensorboard loader first
        try:
            from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
            full_loader = TensorBoardLoader()
            full_loader.load(path, store)
            return
        except ImportError:
            pass

        # Fallback: try to parse with just tensorflow or basic protobuf
        try:
            self._load_with_tf(path, store)
        except ImportError:
            raise ImportError(
                "Could not load TensorBoard logs. Install tensorboard with:\n"
                "  pip install tensorboard\n"
                "Or tensorflow with:\n"
                "  pip install tensorflow"
            )

    def _load_with_tf(self, path: Path, store: MetricStore) -> None:
        """Load using TensorFlow's event reader."""
        import tensorflow as tf

        event_files = self._find_event_files(path)
        if not event_files:
            raise ValueError(f"No TensorBoard event files found in: {path}")

        for event_file in event_files:
            for event in tf.compat.v1.train.summary_iterator(str(event_file)):
                step = event.step
                for value in event.summary.value:
                    if value.HasField("simple_value"):
                        clean_tag = value.tag.replace("/", "_").replace(".", "_")
                        store.log(step, **{clean_tag: value.simple_value})

    def _find_event_files(self, path: Path) -> List[Path]:
        """Find all event files in a path."""
        if path.is_file():
            return [path]
        return list(path.glob("**/events.out.tfevents.*"))
