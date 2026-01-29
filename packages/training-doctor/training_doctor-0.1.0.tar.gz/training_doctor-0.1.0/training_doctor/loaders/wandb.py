import json
from pathlib import Path
from typing import Union, Optional, Dict, Any

from .base import BaseLoader
from ..metrics.store import MetricStore


class WandBLoader(BaseLoader):
    """Loader for Weights & Biases run directories."""

    def can_load(self, path: Union[str, Path]) -> bool:
        """Check if path is a W&B run directory."""
        path = Path(path)
        if not path.is_dir():
            return False
        # W&B runs have wandb-metadata.json or wandb-summary.json
        return (
            (path / "wandb-metadata.json").exists() or
            (path / "files" / "wandb-summary.json").exists() or
            any(path.glob("*.wandb"))
        )

    def load(self, path: Union[str, Path], store: MetricStore) -> None:
        """Load metrics from a W&B run directory."""
        path = Path(path)

        # Try to find and load the history file
        history_file = self._find_history_file(path)
        if history_file:
            self._load_history(history_file, store)
            return

        # Fall back to summary if no history
        summary_file = path / "files" / "wandb-summary.json"
        if not summary_file.exists():
            summary_file = path / "wandb-summary.json"

        if summary_file.exists():
            self._load_summary(summary_file, store)
        else:
            raise ValueError(f"No W&B history or summary found in: {path}")

    def _find_history_file(self, path: Path) -> Optional[Path]:
        """Find the history file in a W&B run directory."""
        # Check common locations
        candidates = [
            path / "wandb-history.jsonl",
            path / "files" / "wandb-history.jsonl",
        ]

        # Also check for .wandb files which contain history
        candidates.extend(path.glob("*.wandb"))
        candidates.extend((path / "files").glob("*.wandb") if (path / "files").is_dir() else [])

        for candidate in candidates:
            if candidate.exists() and candidate.is_file():
                return candidate

        return None

    def _load_history(self, path: Path, store: MetricStore) -> None:
        """Load metrics from a W&B history file (JSONL format)."""
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue

                step = self._extract_step(record)
                if step is None:
                    continue

                metrics = self._extract_metrics(record)
                if metrics:
                    store.log(step, **metrics)

    def _load_summary(self, path: Path, store: MetricStore) -> None:
        """Load metrics from a W&B summary file (single JSON object)."""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        step = self._extract_step(data) or 0
        metrics = self._extract_metrics(data)
        if metrics:
            store.log(step, **metrics)

    def _extract_step(self, record: Dict[str, Any]) -> Optional[int]:
        """Extract step number from a record."""
        for key in ["_step", "step", "global_step", "iteration", "trainer/global_step"]:
            if key in record:
                try:
                    return int(record[key])
                except (ValueError, TypeError):
                    continue
        return None

    def _extract_metrics(self, record: Dict[str, Any]) -> Dict[str, float]:
        """Extract numeric metrics from a record."""
        metrics = {}
        skip_prefixes = ("_", "system/", "system.")

        for key, value in record.items():
            # Skip internal W&B keys
            if any(key.startswith(p) for p in skip_prefixes):
                continue

            # Skip non-numeric values
            if not isinstance(value, (int, float)):
                continue

            # Clean up the key name
            clean_key = key.replace("/", "_").replace(".", "_")
            metrics[clean_key] = float(value)

        return metrics
